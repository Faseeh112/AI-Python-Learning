# whisperoff.py  —  voice + text, full NLP, reminders, 100% offline
import os
import sys

# ── Offline locks — MUST be the very first thing before any imports ────────
os.environ["TRANSFORMERS_OFFLINE"]         = "1"
os.environ["HF_DATASETS_OFFLINE"]          = "1"
os.environ["HF_HUB_OFFLINE"]              = "1"
os.environ["HF_HUB_DISABLE_TELEMETRY"]    = "1"
os.environ["HF_HOME"]                      = os.path.expanduser("~/.cache/huggingface")
os.environ["SENTENCE_TRANSFORMERS_HOME"]   = os.path.expanduser("~/.cache/torch/sentence_transformers")
os.environ["TF_ENABLE_ONEDNN_OPTS"]        = "0"
os.environ["TOKENIZERS_PARALLELISM"]       = "false"

import re
import time
import threading
import json
import uuid
import tempfile
import winsound

import numpy as np
import sounddevice as sd
import scipy.io.wavfile as wav
import whisper
import pyttsx3
import stanza
import parsedatetime
import chromadb

from datetime import datetime, timedelta
from transformers import pipeline as hf_pipeline
from sentence_transformers import SentenceTransformer

# ════════════════════════════════════════════════════════════════════════════
# CONFIG
# ════════════════════════════════════════════════════════════════════════════
SAMPLE_RATE      = 16000
ENERGY_THRESHOLD = 80
SILENCE_TIMEOUT  = 4
CHUNK_DURATION   = 0.5
WAKE_WORD_BUFFER = 3.0

WAKE_PHRASES = ["hi diary", "hi, diary", "hi dairy", "hey diary", "high diary"]
TEXT_WAKE    = ["hi diary", "hey diary"]

INTENT_LABELS = [
    "set a reminder or alarm",
    "schedule an event or meeting",
    "play audio or music",
    "find where something is located",
    "attach or reference a file",
    "ask a general AI question",
    "store a personal memory or diary entry",
    "retrieve or search past information",
    "cancel or delete a reminder",
    "list or show pending reminders",
]

LABEL_MAP = {
    "set a reminder or alarm":                "reminder",
    "schedule an event or meeting":           "event",
    "play audio or music":                    "query_audio",
    "find where something is located":        "item_location",
    "attach or reference a file":             "attachment",
    "ask a general AI question":              "ai_query",
    "store a personal memory or diary entry": "memory",
    "retrieve or search past information":    "retrieval",
    "cancel or delete a reminder":            "cancel_reminder",
    "list or show pending reminders":         "list_reminders",
}

# ════════════════════════════════════════════════════════════════════════════
# LOAD ALL MODELS  (all from local cache — zero network)
# ════════════════════════════════════════════════════════════════════════════
print("🧠 Loading Whisper model...")
whisper_model = whisper.load_model("tiny")

print("📦 Loading Stanza NLP pipeline...")
stanza_nlp = stanza.Pipeline(
    "en",
    processors      = "tokenize,ner,pos,lemma,depparse",
    use_gpu         = False,
    verbose         = False,
    download_method = None,
)

print("📦 Loading zero-shot classifier...")
zero_shot = hf_pipeline(
    "zero-shot-classification",
    model            = "facebook/bart-large-mnli",
    device           = -1,
    local_files_only = True,
)

print("📦 Loading sentence embedder...")
embedder = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2",
    device           = "cpu",
    local_files_only = True,
)

print("📦 Connecting to ChromaDB (local persistent store)...")
chroma_client = chromadb.PersistentClient(path="./diary_db")
collection     = chroma_client.get_or_create_collection(
    name     = "diary_entries",
    metadata = {"hnsw:space": "cosine"},
)

print("🔊 Loading TTS engine...")
tts_engine = pyttsx3.init()

# parsedatetime calendar
cal = parsedatetime.Calendar()

# global reminder store + lock
pending_reminders = []
reminder_lock     = threading.Lock()

print("✅ All models loaded from local cache. Running fully offline.\n")

# ════════════════════════════════════════════════════════════════════════════
# INPUT MODE SELECTOR
# ════════════════════════════════════════════════════════════════════════════
def choose_input_mode():
    print("\n" + "═" * 55)
    print("  Hi Diary Assistant")
    print("═" * 55)
    print("  How would you like to interact?")
    print("  [1] Voice only")
    print("  [2] Text only")
    print("  [3] Both (voice OR type 'hi diary')")
    print("═" * 55)
    while True:
        choice = input("  Enter 1 / 2 / 3: ").strip()
        if choice == "1": return "voice"
        if choice == "2": return "text"
        if choice == "3": return "both"
        print("  Please enter 1, 2, or 3.")

# ════════════════════════════════════════════════════════════════════════════
# TTS
# ════════════════════════════════════════════════════════════════════════════
def speak(text):
    print(f"🔊 {text}")
    try:
        tts_engine.say(text)
        tts_engine.runAndWait()
    except Exception as e:
        print(f"[TTS error] {e}")

# ════════════════════════════════════════════════════════════════════════════
# ALARM  (winsound is built into Windows Python — zero install)
# ════════════════════════════════════════════════════════════════════════════
def play_alarm(times=3):
    try:
        for _ in range(times):
            winsound.Beep(1000, 800)
            time.sleep(0.3)
    except Exception:
        for _ in range(times):
            print("\a", end="", flush=True)
            time.sleep(0.5)

# ════════════════════════════════════════════════════════════════════════════
# INTENT  (keyword overrides first, zero-shot fallback)
# ════════════════════════════════════════════════════════════════════════════
def get_intent_data(text):
    tl = text.lower()

    if any(w in tl for w in ["cancel reminder", "delete reminder",
                               "remove reminder", "stop reminder"]):
        return {"intent": "cancel_reminder", "confidence": 1.0,
                "raw_label": "keyword_override"}

    if any(w in tl for w in ["list reminders", "show reminders",
                               "what reminders", "pending reminders",
                               "my reminders", "do i have any reminders"]):
        return {"intent": "list_reminders", "confidence": 1.0,
                "raw_label": "keyword_override"}

    if any(w in tl for w in ["wake me up", "set alarm", "set a reminder",
                               "remind me", "don't forget", "remember to"]):
        return {"intent": "reminder", "confidence": 1.0,
                "raw_label": "keyword_override"}

    result    = zero_shot(text, candidate_labels=INTENT_LABELS)
    top_label = result["labels"][0]
    top_score = result["scores"][0]
    return {
        "intent":     LABEL_MAP.get(top_label, "unknown"),
        "confidence": round(top_score, 4),
        "raw_label":  top_label,
    }

# ════════════════════════════════════════════════════════════════════════════
# NER
# ════════════════════════════════════════════════════════════════════════════
def extract_entities(doc):
    entities = []
    for ent in doc.entities:
        entities.append({
            "text":        ent.text,
            "label":       ent.type,
            "description": ent.type,
            "start":       ent.start_char,
            "end":         ent.end_char,
        })
    return entities

# ════════════════════════════════════════════════════════════════════════════
# TRIPLET EXTRACTION
# ════════════════════════════════════════════════════════════════════════════
def _expand_span(word, sent):
    deps  = {"compound", "amod", "det", "nummod", "nmod:poss", "advmod"}
    parts = [w.text for w in sent.words
             if w.head == word.id and w.deprel in deps and w.id < word.id]
    parts.append(word.text)
    return " ".join(parts)


def extract_triplets(doc):
    triplets = []
    seen     = set()

    def add(subj, rel, obj):
        key = (subj.lower(), rel.lower(), obj.lower())
        if key not in seen and subj and rel and obj:
            seen.add(key)
            triplets.append({"subject": subj, "relation": rel, "object": obj})

    for sent in doc.sentences:
        word_map = {w.id: w for w in sent.words}

        for word in sent.words:

            if word.upos == "VERB":
                subjects = [w for w in sent.words if w.head == word.id
                            and w.deprel in ("nsubj", "nsubjpass", "csubj")]
                objects  = [w for w in sent.words if w.head == word.id
                            and w.deprel in ("obj", "dobj", "iobj", "attr", "oprd")]
                obliques = [w for w in sent.words if w.head == word.id
                            and w.deprel in ("obl", "obl:tmod", "obl:npmod")]

                for subj in subjects:
                    s = _expand_span(subj, sent)
                    for obj in objects:
                        add(s, word.lemma, _expand_span(obj, sent))
                    for obl in obliques:
                        prep_word = next(
                            (w for w in sent.words
                             if w.head == obl.id and w.deprel == "case"), None)
                        prep = prep_word.text if prep_word else "at"
                        add(s, f"{word.lemma} {prep}", _expand_span(obl, sent))

            if word.deprel == "cop":
                head = word_map.get(word.head)
                if head:
                    subjs = [w for w in sent.words
                             if w.head == head.id and w.deprel == "nsubj"]
                    for subj in subjs:
                        add(_expand_span(subj, sent), word.lemma,
                            _expand_span(head, sent))

            if word.deprel in ("nmod", "nmod:poss") and word_map.get(word.head):
                head = word_map[word.head]
                if head.upos in ("NOUN", "PROPN"):
                    prep_word = next(
                        (w for w in sent.words
                         if w.head == word.id and w.deprel == "case"), None)
                    prep = prep_word.text if prep_word else "of"
                    add(_expand_span(head, sent), prep,
                        _expand_span(word, sent))

    return triplets

# ════════════════════════════════════════════════════════════════════════════
# FULL ANALYSIS
# ════════════════════════════════════════════════════════════════════════════
def analyze(text):
    doc      = stanza_nlp(text)
    intent   = get_intent_data(text)
    entities = extract_entities(doc)
    triplets = extract_triplets(doc)
    return {
        "raw_text": text,
        "intent":   intent,
        "entities": entities,
        "triplets": triplets,
    }

# ════════════════════════════════════════════════════════════════════════════
# RAG — STORE
# ════════════════════════════════════════════════════════════════════════════
def store_to_rag(text, analysis):
    try:
        embedding = embedder.encode(text, normalize_embeddings=True).tolist()
        flat_meta = {
            "intent":     analysis["intent"]["intent"],
            "confidence": analysis["intent"]["confidence"],
            "entities":   json.dumps(analysis["entities"]),
            "triplets":   json.dumps(analysis["triplets"]),
            "raw_text":   text,
        }
        collection.add(
            documents  = [text],
            embeddings = [embedding],
            metadatas  = [flat_meta],
            ids        = [str(uuid.uuid4())],
        )
    except Exception as e:
        print(f"[RAG store error] {e}")

# ════════════════════════════════════════════════════════════════════════════
# RAG — QUERY
# ════════════════════════════════════════════════════════════════════════════
def query_rag(query, n_results=3, intent_filter=None):
    try:
        embedding    = embedder.encode(query, normalize_embeddings=True).tolist()
        where_clause = {"intent": intent_filter} if intent_filter else None
        results      = collection.query(
            query_embeddings = [embedding],
            n_results        = n_results,
            where            = where_clause,
            include          = ["documents", "metadatas", "distances"],
        )
        hits = []
        for doc, meta, dist in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        ):
            hits.append({
                "text":       doc,
                "similarity": round(1 - dist, 4),
                "intent":     meta["intent"],
                "entities":   json.loads(meta["entities"]),
                "triplets":   json.loads(meta["triplets"]),
            })
        return hits
    except Exception as e:
        print(f"[RAG query error] {e}")
        return []

# ════════════════════════════════════════════════════════════════════════════
# REMINDER — PARSE TIME
# ════════════════════════════════════════════════════════════════════════════
def parse_time_from_text(text):
    now                       = datetime.now()
    time_struct, parse_status = cal.parse(text, now)
    if parse_status == 0:
        return None
    parsed = datetime(*time_struct[:6])
    if parsed <= now:
        parsed += timedelta(days=1)
    return parsed

# ════════════════════════════════════════════════════════════════════════════
# REMINDER — EXTRACT LABEL
# ════════════════════════════════════════════════════════════════════════════
def extract_reminder_label(text, analysis):
    for t in analysis.get("triplets", []):
        obj = t.get("object", "").strip()
        if obj and len(obj) > 2:
            return obj

    strip_phrases = [
        "remind me to", "remind me about", "remind me",
        "set a reminder to", "set a reminder for", "set a reminder",
        "set an alarm for", "set an alarm at", "set an alarm",
        "set alarm for", "set alarm at", "set alarm",
        "wake me up at", "wake me up",
        "alarm for", "alarm at",
        "remember to", "remember that",
        "don't forget to", "don't forget",
        "please remind me to", "please remind me",
    ]
    label = text.lower()
    for phrase in sorted(strip_phrases, key=len, reverse=True):
        label = label.replace(phrase, " ")

    time_words = [
        "tomorrow", "tonight", "today", "morning", "evening",
        "afternoon", "midnight", "noon",
        "monday", "tuesday", "wednesday", "thursday",
        "friday", "saturday", "sunday",
        "next", "this", "at", "in", "after", "around", "by",
        "am", "pm", "o'clock",
        "hour", "hours", "minute", "minutes", "second", "seconds",
        "half", "quarter", "past",
    ]
    for w in time_words:
        label = re.sub(rf"\b{w}\b", " ", label)

    label = re.sub(r"\b\d+[:\d]*\b", "", label)
    label = " ".join(label.split())
    return label if label else "reminder"

# ════════════════════════════════════════════════════════════════════════════
# REMINDER — FIRE
# ════════════════════════════════════════════════════════════════════════════
def fire_reminder(label, reminder_id):
    global pending_reminders
    print(f"\n{'█' * 55}")
    print(f"  ⏰ REMINDER: {label}")
    print(f"{'█' * 55}\n")
    speak(f"Attention! Your reminder: {label}")
    play_alarm()
    with reminder_lock:
        pending_reminders = [r for r in pending_reminders
                             if r["id"] != reminder_id]

# ════════════════════════════════════════════════════════════════════════════
# REMINDER — SCHEDULE
# ════════════════════════════════════════════════════════════════════════════
def schedule_reminder(text, analysis):
    fire_at = parse_time_from_text(text)
    if fire_at is None:
        speak("Sorry, I couldn't figure out when to remind you. "
              "Try something like 'in 10 minutes' or 'at 5am tomorrow'.")
        return False

    label       = extract_reminder_label(text, analysis)
    delay_secs  = (fire_at - datetime.now()).total_seconds()
    reminder_id = str(uuid.uuid4())

    def _run():
        time.sleep(max(delay_secs, 0))
        fire_reminder(label, reminder_id)

    t = threading.Thread(target=_run, daemon=True,
                         name=f"reminder-{reminder_id[:8]}")
    t.start()

    with reminder_lock:
        pending_reminders.append({
            "id":      reminder_id,
            "label":   label,
            "fire_at": fire_at,
            "thread":  t,
        })

    total_s          = max(int(delay_secs), 0)
    hours, remainder = divmod(total_s, 3600)
    minutes, seconds = divmod(remainder, 60)

    if hours > 0 and minutes > 0:
        human = (f"{hours} hour{'s' if hours > 1 else ''} "
                 f"and {minutes} minute{'s' if minutes > 1 else ''}")
    elif hours > 0:
        human = f"{hours} hour{'s' if hours > 1 else ''}"
    elif minutes > 0:
        human = f"{minutes} minute{'s' if minutes > 1 else ''}"
    else:
        human = f"{seconds} second{'s' if seconds > 1 else ''}"

    time_str = fire_at.strftime("%I:%M %p")
    confirm  = (f"Got it! I'll remind you to {label} "
                f"at {time_str}. That's in {human}.")
    print(f"\n✅ Reminder set → '{label}'  at {time_str}  (in {human})")
    speak(confirm)
    store_to_rag(text, analysis)
    return True

# ════════════════════════════════════════════════════════════════════════════
# REMINDER — LIST
# ════════════════════════════════════════════════════════════════════════════
def list_reminders():
    with reminder_lock:
        active = [r for r in pending_reminders if r["thread"].is_alive()]

    if not active:
        speak("You have no pending reminders.")
        return

    count = len(active)
    speak(f"You have {count} pending reminder{'s' if count > 1 else ''}.")
    print(f"\n{'─' * 55}")
    for i, r in enumerate(active, 1):
        diff     = r["fire_at"] - datetime.now()
        total_s  = max(int(diff.total_seconds()), 0)
        mins     = total_s // 60
        time_str = r["fire_at"].strftime("%I:%M %p")
        print(f"  [{i}] {r['label']:<30} → {time_str}  ({mins}m remaining)")
        speak(f"{i}. {r['label']} at {time_str}.")
    print(f"{'─' * 55}\n")

# ════════════════════════════════════════════════════════════════════════════
# REMINDER — CANCEL
# ════════════════════════════════════════════════════════════════════════════
def cancel_reminder(text):
    global pending_reminders
    with reminder_lock:
        active = [r for r in pending_reminders if r["thread"].is_alive()]

    if not active:
        speak("You have no pending reminders to cancel.")
        return

    text_words   = set(text.lower().split())
    match        = None
    best_overlap = 0

    for r in active:
        label_words = set(r["label"].lower().split())
        overlap     = len(label_words & text_words)
        if overlap > best_overlap:
            best_overlap = overlap
            match        = r

    if not match:
        match = active[-1]

    with reminder_lock:
        pending_reminders = [r for r in pending_reminders
                             if r["id"] != match["id"]]

    speak(f"Cancelled reminder: {match['label']}.")
    print(f"❌ Cancelled: {match['label']}")

# ════════════════════════════════════════════════════════════════════════════
# DISPLAY ANALYSIS
# ════════════════════════════════════════════════════════════════════════════
def display_analysis(analysis):
    i     = analysis["intent"]
    ents  = analysis["entities"]
    trips = analysis["triplets"]

    print(f"\n{'═' * 55}")
    print(f"🎯 Intent    : {i['intent'].upper():<22} ({i['confidence']:.0%})")
    print(f"   Raw label : {i['raw_label']}")

    if ents:
        print(f"\n🏷️  Entities  ({len(ents)} found):")
        for e in ents:
            print(f"   • {e['text']:<24} [{e['label']}]")
    else:
        print("\n🏷️  Entities  : none detected")

    if trips:
        print(f"\n🔗 Triplets  ({len(trips)} found):")
        for t in trips:
            print(f"   • ({t['subject']})  —[{t['relation']}]→  ({t['object']})")
    else:
        print("\n🔗 Triplets  : none detected")

    print(f"{'═' * 55}\n")

# ════════════════════════════════════════════════════════════════════════════
# WAKE WORD — VOICE ONLY
# ════════════════════════════════════════════════════════════════════════════
def detect_wake_word_voice():
    print("🎧 Listening for wake word 'Hi Diary'...")
    while True:
        rec = sd.rec(
            int(WAKE_WORD_BUFFER * SAMPLE_RATE),
            samplerate=SAMPLE_RATE, channels=1, dtype="int16",
        )
        sd.wait()
        rec    = rec.flatten()
        energy = np.abs(rec).mean()
        if energy < ENERGY_THRESHOLD:
            continue
        tmp_path = None
        try:
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
                tmp_path = f.name
                wav.write(f.name, SAMPLE_RATE, rec)
            result = whisper_model.transcribe(tmp_path, language="en", fp16=False)
            text   = result["text"].lower().strip()
            print(f"[wake] heard: {text}")
            if any(p in text for p in WAKE_PHRASES):
                return
        except Exception as e:
            print(f"[wake error] {e}")
        finally:
            if tmp_path and os.path.exists(tmp_path):
                os.unlink(tmp_path)

# ════════════════════════════════════════════════════════════════════════════
# WAKE WORD — BOTH (voice + text race)
# ════════════════════════════════════════════════════════════════════════════
def detect_wake_word_both():
    result     = [None]
    stop_event = threading.Event()

    def voice_listener():
        print("🎧 Say 'Hi Diary'  OR  type 'hi diary' + Enter")
        while not stop_event.is_set():
            rec = sd.rec(
                int(WAKE_WORD_BUFFER * SAMPLE_RATE),
                samplerate=SAMPLE_RATE, channels=1, dtype="int16",
            )
            sd.wait()
            if stop_event.is_set():
                break
            rec    = rec.flatten()
            energy = np.abs(rec).mean()
            if energy < ENERGY_THRESHOLD:
                continue
            tmp_path = None
            try:
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
                    tmp_path = f.name
                    wav.write(f.name, SAMPLE_RATE, rec)
                r    = whisper_model.transcribe(tmp_path, language="en", fp16=False)
                text = r["text"].lower().strip()
                print(f"[wake] heard: {text}")
                if any(p in text for p in WAKE_PHRASES) and not stop_event.is_set():
                    result[0] = "voice"
                    stop_event.set()
            except Exception as e:
                print(f"[wake voice error] {e}")
            finally:
                if tmp_path and os.path.exists(tmp_path):
                    os.unlink(tmp_path)

    def text_listener():
        while not stop_event.is_set():
            try:
                typed = input().strip().lower()
                if any(p in typed for p in TEXT_WAKE) and not stop_event.is_set():
                    result[0] = "text"
                    stop_event.set()
            except EOFError:
                break

    vt = threading.Thread(target=voice_listener, daemon=True)
    tt = threading.Thread(target=text_listener,  daemon=True)
    vt.start()
    tt.start()
    stop_event.wait()
    return result[0]

# ════════════════════════════════════════════════════════════════════════════
# RECORD VOICE COMMAND
# ════════════════════════════════════════════════════════════════════════════
def record_command():
    print("🎤 Listening for your command...")
    recording       = []
    silence_counter = 0
    max_silence     = int(SILENCE_TIMEOUT / CHUNK_DURATION)

    while True:
        chunk = sd.rec(
            int(CHUNK_DURATION * SAMPLE_RATE),
            samplerate=SAMPLE_RATE, channels=1, dtype="int16",
        )
        sd.wait()
        chunk  = chunk.flatten()
        energy = np.abs(chunk).mean()
        recording.append(chunk)

        if energy < ENERGY_THRESHOLD:
            silence_counter += 1
        else:
            silence_counter = 0

        if silence_counter >= max_silence:
            break

    print("✅ Recording stopped")
    audio = np.concatenate(recording)
    tmp   = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    wav.write(tmp.name, SAMPLE_RATE, audio)
    tmp.close()
    return tmp.name

# ════════════════════════════════════════════════════════════════════════════
# PROCESS TEXT  — single entry point for all input paths
# ════════════════════════════════════════════════════════════════════════════
def process_text(text):
    if not text:
        speak("I didn't catch that. Please try again.")
        return

    print(f"\nYou said: {text}")
    speak(f"You said: {text}")

    print("🔍 Analysing...")
    analysis = analyze(text)
    intent   = analysis["intent"]["intent"]
    conf     = analysis["intent"]["confidence"]

    display_analysis(analysis)
    speak(f"Detected intent: {intent.replace('_', ' ')}, "
          f"with {conf:.0%} confidence.")

    if analysis["entities"]:
        names = list({e["text"] for e in analysis["entities"]})
        speak(f"I noticed: {', '.join(names)}.")

    if analysis["triplets"]:
        t = analysis["triplets"][0]
        speak(f"Key relation: {t['subject']} {t['relation']} {t['object']}.")

    # ── intent dispatch ───────────────────────────────────────────────────
    if intent == "reminder":
        schedule_reminder(text, analysis)

    elif intent == "cancel_reminder":
        cancel_reminder(text)

    elif intent == "list_reminders":
        list_reminders()

    elif intent == "event":
        persons = [e["text"] for e in analysis["entities"]
                   if e["label"] == "PERSON"]
        dates   = [e["text"] for e in analysis["entities"]
                   if e["label"] in ("DATE", "TIME")]
        msg = "Event noted."
        if persons:
            msg += f" With {', '.join(persons)}."
        if dates:
            msg += f" On {', '.join(dates)}."
        speak(msg)
        store_to_rag(text, analysis)

    elif intent == "item_location":
        hits = query_rag(text, n_results=1, intent_filter="item_location")
        if hits:
            speak(f"Last time you mentioned: {hits[0]['text']}")
        else:
            speak("I don't have a record of that location yet.")
        store_to_rag(text, analysis)

    elif intent == "retrieval":
        hits = query_rag(text, n_results=3)
        if hits:
            print(f"\n📂 Top {len(hits)} memory hit(s):")
            for idx, hit in enumerate(hits, 1):
                print(f"  [{idx}] ({hit['similarity']:.2f}) {hit['text']}")
            speak(f"I found this in my memory: {hits[0]['text']}")
        else:
            speak("I couldn't find anything related in my memory.")
        store_to_rag(text, analysis)

    elif intent == "memory":
        speak("Got it. I've saved that to your diary.")
        store_to_rag(text, analysis)

    elif intent == "ai_query":
        speak("That sounds like a question. I've noted it for you.")
        store_to_rag(text, analysis)

    elif intent == "query_audio":
        speak("Audio playback isn't connected yet, but I've noted your request.")
        store_to_rag(text, analysis)

    else:
        speak("I've recorded what you said, but wasn't sure what to do with it.")
        store_to_rag(text, analysis)

# ════════════════════════════════════════════════════════════════════════════
# MAIN LOOP
# ════════════════════════════════════════════════════════════════════════════
INPUT_MODE = choose_input_mode()
speak("Hi Diary Assistant is ready.")
print(f"\n🤖 Running in [{INPUT_MODE.upper()}] mode.\n")

while True:
    try:
        if INPUT_MODE == "voice":
            detect_wake_word_voice()
            speak("Yes, I'm listening.")
            wav_file = record_command()
            try:
                result = whisper_model.transcribe(
                    wav_file, language="en", fp16=False)
                text = result["text"].strip()
            finally:
                if os.path.exists(wav_file):
                    os.unlink(wav_file)
            process_text(text)

        elif INPUT_MODE == "text":
            print("\n⌨️  Type 'hi diary' to begin  (or 'quit' to exit):")
            wake = input("  > ").strip().lower()
            if wake in ("quit", "exit", "q"):
                speak("Goodbye!")
                sys.exit(0)
            if not any(p in wake for p in TEXT_WAKE):
                print("  (Waiting for 'hi diary'...)")
                continue
            speak("Yes, I'm listening.")
            print("⌨️  Type your command:")
            text = input("  > ").strip()
            process_text(text)

        elif INPUT_MODE == "both":
            winner = detect_wake_word_both()
            speak("Yes, I'm listening.")
            if winner == "voice":
                wav_file = record_command()
                try:
                    result = whisper_model.transcribe(
                        wav_file, language="en", fp16=False)
                    text = result["text"].strip()
                finally:
                    if os.path.exists(wav_file):
                        os.unlink(wav_file)
            else:
                print("⌨️  Type your command:")
                text = input("  > ").strip()
            process_text(text)

    except KeyboardInterrupt:
        print("\n👋 Shutting down.")
        speak("Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"[main loop error] {e}")
        speak("Something went wrong. Please try again.")

    print("\n--- Waiting for next wake word ---\n")