# # import sounddevice as sd
# # import numpy as np
# # import whisper
# # import scipy.io.wavfile as wav
# # import tempfile
# # from intent_predict import get_intent
# #
# # # ---------------- CONFIG ----------------
# # SAMPLE_RATE = 16000
# # ENERGY_THRESHOLD = 150        # lower to detect quieter speech
# # SILENCE_TIMEOUT = 1.5         # seconds of continuous silence to stop recording
# # CHUNK_DURATION = 0.3          # seconds per chunk while recording
# # WAKE_WORD_BUFFER = 2          # seconds buffer for wake word detection (shorter = faster response)
# #
# # # ---------------- LOAD WHISPER MODEL ----------------
# # print("🧠 Loading Whisper model (CPU-friendly)...")
# # whisper_model = whisper.load_model("tiny")  # tiny = fast on CPU, small = more accurate
# #
# # # ---------------- WAKE WORD DETECTION ----------------
# # def detect_wake_word():
# #     print("🎧 Listening for wake word 'Hi Diary'... speak naturally")
# #     while True:
# #         # Record a small buffer of WAKE_WORD_BUFFER seconds
# #         rec = sd.rec(int(WAKE_WORD_BUFFER * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='int16')
# #         sd.wait()
# #         rec = rec.flatten()
# #         energy = np.abs(rec).mean()
# #
# #         if energy < ENERGY_THRESHOLD:
# #             continue  # too quiet, keep listening
# #
# #         # Save to temporary WAV
# #         with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
# #             wav.write(f.name, SAMPLE_RATE, rec)
# #             result = whisper_model.transcribe(f.name, language="en", fp16=False)
# #             text = result["text"].lower()
# #             if "hi" in text:
# #                 print("💡 Wake word detected!")
# #                 return
# #
# # # ---------------- COMMAND RECORDING ----------------
# # def record_command():
# #     print("🎤 Listening for your command...")
# #     recording = []
# #     silence_counter = 0
# #     max_silence_chunks = int(SILENCE_TIMEOUT / CHUNK_DURATION)
# #
# #     while True:
# #         chunk = sd.rec(int(CHUNK_DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='int16')
# #         sd.wait()
# #         chunk = chunk.flatten()
# #         recording.append(chunk)
# #
# #         # Energy-based silence detection
# #         energy = np.abs(chunk).mean()
# #         if energy < ENERGY_THRESHOLD:
# #             silence_counter += 1
# #         else:
# #             silence_counter = 0
# #
# #         # Stop recording after continuous silence
# #         if silence_counter >= max_silence_chunks:
# #             break
# #
# #     print("✅ Command recording stopped")
# #     audio_bytes = np.concatenate(recording)
# #     with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
# #         wav.write(f.name, SAMPLE_RATE, audio_bytes)
# #         return f.name
# #
# # # ---------------- MAIN LOOP ----------------
# # print("🤖 Hi Diary Assistant is ready!\n")
# #
# # while True:
# #     detect_wake_word()             # Wait for wake word
# #     wav_file = record_command()    # Record full command
# #     print("📝 Transcribing your command...")
# #     result = whisper_model.transcribe(wav_file, language="en", fp16=False)
# #     text = result["text"].strip()
# #     print(f"You said: {text}")
# #
# #     # Detect intent using dummy intent predictor
# #     intent = get_intent(text)
# #     print(f"Detected intent: {intent}\n")
# #
# #     print("--- Waiting for next wake word ---\n")
#
#
# ##########################################################################################################################################3
# # import sounddevice as sd
# # import numpy as np
# # import whisper
# # import scipy.io.wavfile as wav
# # import tempfile
# # import pyttsx3
# # from intent_predict import get_intent
# #
# # # ---------------- CONFIG ----------------
# # SAMPLE_RATE = 16000
# # ENERGY_THRESHOLD = 120         # slightly lower so quieter speech is detected
# # SILENCE_TIMEOUT = 1.5          # seconds of silence to stop recording
# # CHUNK_DURATION = 0.3           # seconds per chunk while recording
# # WAKE_WORD_BUFFER = 3.0         # longer buffer so "Hi Diary" fits easily
# #
# # # ---------------- TTS ENGINE ----------------
# # engine = pyttsx3.init()
# #
# # def speak(text):
# #     """Print plus speak the text so you know it fired."""
# #     print(f"🔊 {text}")
# #     engine.say(text)
# #     engine.runAndWait()
# #
# # # ---------------- LOAD WHISPER MODEL ----------------
# # print("🧠 Loading Whisper model (CPU-friendly)...")
# # whisper_model = whisper.load_model("small")  # tiny = fast on CPU, small = more accurate
# # speak("Hi Diary Assistant is ready.")
# #
# # # ---------------- WAKE WORD DETECTION ----------------
# # def detect_wake_word():
# #     print("🎧 Listening for wake word 'Hi Diary'... speak naturally")
# #     wake_phrases = ["hi diary", "hi, diary", "hi dairy", "hey diary"]
# #     while True:
# #         rec = sd.rec(int(WAKE_WORD_BUFFER * SAMPLE_RATE),
# #                      samplerate=SAMPLE_RATE, channels=1, dtype='int16')
# #         sd.wait()
# #         rec = rec.flatten()
# #         energy = np.abs(rec).mean()
# #
# #         if energy < ENERGY_THRESHOLD:
# #             continue  # keep listening
# #
# #         with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
# #             wav.write(f.name, SAMPLE_RATE, rec)
# #             result = whisper_model.transcribe(f.name, language="en", fp16=False)
# #             text = result["text"].lower().strip()
# #             print(f"[wake buffer] {text}")  # debug so you see what Whisper heard
# #
# #             if any(phrase in text for phrase in wake_phrases):
# #                 speak("Yes, I'm listening.")
# #                 return
# #
# # # ---------------- COMMAND RECORDING ----------------
# # def record_command():
# #     print("🎤 Listening for your command...")
# #     recording = []
# #     silence_counter = 0
# #     max_silence_chunks = int(SILENCE_TIMEOUT / CHUNK_DURATION)
# #
# #     while True:
# #         chunk = sd.rec(int(CHUNK_DURATION * SAMPLE_RATE),
# #                        samplerate=SAMPLE_RATE, channels=1, dtype='int16')
# #         sd.wait()
# #         chunk = chunk.flatten()
# #         recording.append(chunk)
# #
# #         energy = np.abs(chunk).mean()
# #         if energy < ENERGY_THRESHOLD:
# #             silence_counter += 1
# #         else:
# #             silence_counter = 0
# #
# #         if silence_counter >= max_silence_chunks:
# #             break
# #
# #     print("✅ Command recording stopped")
# #     audio_bytes = np.concatenate(recording)
# #     with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
# #         wav.write(f.name, SAMPLE_RATE, audio_bytes)
# #         return f.name
# #
# # # ---------------- MAIN LOOP ----------------
# # print("🤖 Hi Diary Assistant is ready!\n")
# #
# # while True:
# #     detect_wake_word()
# #     wav_file = record_command()
# #
# #     print("📝 Transcribing your command...")
# #     result = whisper_model.transcribe(wav_file, language="en", fp16=False)
# #     text = result["text"].strip()
# #     print(f"You said: {text}")
# #     speak(f"You said: {text}")
# #
# #     intent = get_intent(text)
# #     print(f"Detected intent: {intent}\n")
# #     speak(f"I detected the intent {intent}")
# #
# #     print("--- Waiting for next wake word ---\n")
#
#
#
#
# ##########################################################################################################################################3
# import json
# import queue
# import re
# import time
# from collections import Counter
#
# import numpy as np
# import pyttsx3
# import sounddevice as sd
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.naive_bayes import MultinomialNB
# from sklearn.pipeline import Pipeline
# from vosk import Model, KaldiRecognizer, SetLogLevel
#
# SetLogLevel(-1)  # silence Vosk logs; remove if you want to see them
#
#
# # ---------- TEXT PREPROCESSING ---------- #
#
# def preprocess_text(text):
#     text = text.lower()
#     text = ' '.join(text.split())
#     text = re.sub(r'[^a-z0-9\s]', '', text)
#     return text.strip()
#
#
# def extract_keywords(text):
#     stopwords = {
#         'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'you', 'your', 'yours',
#         'he', 'him', 'his', 'she', 'her', 'hers', 'it', 'its', 'they', 'them',
#         'their', 'what', 'which', 'who', 'this', 'that', 'these', 'those',
#         'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has',
#         'had', 'do', 'does', 'did', 'a', 'an', 'the', 'and', 'but', 'if', 'or',
#         'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with',
#         'about', 'to', 'from', 'in', 'out', 'on', 'off', 'over', 'under'
#     }
#     words = text.lower().split()
#     return [w for w in words if w not in stopwords and len(w) > 2]
#
#
# # ---------- INTENT DETECTION ---------- #
#
# class IntentDetector:
#     def __init__(self):
#         self.model = None
#         self.trained = False
#         self.training_data = {
#             'task_reminder': [
#                 'I need to call the doctor tomorrow',
#                 "Don't forget to buy groceries",
#                 'I have a meeting at 3 PM',
#                 'Remember to take medicine',
#                 'I should finish the report by Friday',
#                 'Need to pick up the kids from school',
#                 'Have to pay the electricity bill',
#                 'Must submit the assignment',
#                 'I need to schedule a dentist appointment',
#                 "Don't forget to call mom",
#                 'I have to renew my passport',
#                 'Need to book flight tickets',
#                 'Remember to water the plants',
#                 'I should call back my friend',
#                 'Have to attend the conference'
#             ],
#             'emotional_expression': [
#                 'I feel so happy today',
#                 'I am feeling anxious about the exam',
#                 'Today was a really frustrating day',
#                 'I felt excited about the news',
#                 "I'm worried about my health",
#                 'Feeling grateful for my family',
#                 'I am so tired and stressed',
#                 'Today made me really sad',
#                 'I feel peaceful and calm',
#                 "I'm angry about what happened",
#                 'Feeling depressed lately',
#                 'I am so proud of myself',
#                 'Feeling lonely today',
#                 'I feel overwhelmed with work',
#                 'Really nervous about tomorrow'
#             ],
#             'daily_activity': [
#                 'I went to the park this morning',
#                 'Today I cooked pasta for dinner',
#                 'I watched a movie with friends',
#                 'Spent the day cleaning the house',
#                 'I worked on my project all day',
#                 'Went shopping at the mall',
#                 'I played basketball after work',
#                 'Read a book in the evening',
#                 'I walked my dog in the park',
#                 'Had breakfast at a cafe',
#                 'Visited the museum today',
#                 'Went for a run this morning',
#                 'Attended yoga class',
#                 'Played video games all evening',
#                 'Studied for my exam'
#             ],
#             'health_concern': [
#                 'My back has been hurting all day',
#                 'I have a terrible headache',
#                 'I think I caught a cold',
#                 'My knee pain is getting worse',
#                 'I need to see a doctor about this cough',
#                 'Feeling dizzy and nauseous',
#                 'I have a fever and sore throat',
#                 'My stomach has been upset',
#                 'I injured my ankle while running',
#                 'Having trouble sleeping lately',
#                 'My eyes are really sore',
#                 'I have chest pain',
#                 'Feeling really weak today',
#                 'My tooth is aching',
#                 "I'm experiencing allergies"
#             ],
#             'social_interaction': [
#                 'I met my friend Sarah for coffee',
#                 'Had a great conversation with my colleague',
#                 'Called my sister to catch up',
#                 'Went to a party last night',
#                 'Chatted with neighbors this morning',
#                 'Had lunch with my coworkers',
#                 'Texted my old friend from college',
#                 'Hung out with my cousins',
#                 'Had a video call with family',
#                 'Met new people at the event',
#                 'Went on a date tonight',
#                 'Had dinner with my parents',
#                 'Celebrated birthday with friends',
#                 'Visited my grandmother',
#                 'Reconnected with old classmates'
#             ],
#             'goal_planning': [
#                 'I want to learn Spanish next year',
#                 'My goal is to lose weight',
#                 'Planning to start a business',
#                 'I hope to travel to Europe',
#                 'Want to save money for a house',
#                 'Next week I will start exercising',
#                 'I plan to finish my degree',
#                 'My dream is to become a teacher',
#                 'Will start reading more books',
#                 'I want to improve my cooking skills',
#                 'Planning to run a marathon',
#                 'Want to learn guitar',
#                 'My goal is to get promoted',
#                 'I plan to move to a new city',
#                 'Want to start a YouTube channel'
#             ]
#         }
#         self.train_model()
#
#     def train_model(self):
#         texts, labels = [], []
#         for intent, examples in self.training_data.items():
#             texts.extend(examples)
#             labels.extend([intent] * len(examples))
#
#         self.model = Pipeline([
#             ('tfidf', TfidfVectorizer(max_features=150, ngram_range=(1, 3))),
#             ('clf', MultinomialNB(alpha=0.1))
#         ])
#
#         self.model.fit(texts, labels)
#         self.trained = True
#         print("✅ Intent detection model trained with 90 examples!")
#
#     def predict_intent(self, text):
#         if not self.trained:
#             return None
#         prediction = self.model.predict([text])[0]
#         probabilities = self.model.predict_proba([text])[0]
#         intent_scores = {
#             intent: float(probabilities[idx])
#             for idx, intent in enumerate(self.model.classes_)
#         }
#         sorted_intents = sorted(intent_scores.items(), key=lambda x: x[1], reverse=True)
#         return {
#             'primary_intent': prediction,
#             'confidence': float(max(probabilities)),
#             'all_intents': sorted_intents
#         }
#
#
# # ---------- SPEECH OUTPUT ---------- #
#
# def speak(text):
#     print(f"AI: {text}")
#     try:
#         engine = pyttsx3.init()
#         engine.setProperty('rate', 180)
#         engine.setProperty('volume', 1.0)
#         engine.say(text)
#         engine.runAndWait()
#         engine.stop()
#         del engine
#     except Exception as e:
#         print(f"Speech error: {e}")
#
#
# # ---------- OFFLINE SPEECH RECOGNIZER ---------- #
#
# class OfflineRecognizer:
#     def __init__(self, model_path, device_index=None):
#         self.model = Model(model_path)
#         self.device = device_index
#         self.q = queue.Queue()
#
#         info = sd.query_devices(device_index, 'input')
#         self.samplerate = int(info['default_samplerate'])
#
#     def _callback(self, indata, frames, time_info, status):
#         if status:
#             print(status)
#         self.q.put(bytes(indata))
#
#     def listen_and_transcribe(self, max_duration=20, silence_duration=1.5):
#         rec = KaldiRecognizer(self.model, self.samplerate)
#         rec.SetWords(True)
#
#         with sd.RawInputStream(samplerate=self.samplerate,
#                                blocksize=4000,
#                                device=self.device,
#                                dtype='int16',
#                                channels=1,
#                                callback=self._callback):
#             speak("I am listening. Please speak now.")
#             print("🎤 Recording... (Ctrl+C to stop)")
#
#             start_time = time.time()
#             last_voice_time = start_time
#             text_chunks = []
#
#             while True:
#                 data = self.q.get()
#                 if rec.AcceptWaveform(data):
#                     res = json.loads(rec.Result())
#                     if res.get("text"):
#                         text_chunks.append(res["text"])
#                         last_voice_time = time.time()
#                 else:
#                     partial = json.loads(rec.PartialResult()).get("partial", "")
#                     if partial.strip():
#                         last_voice_time = time.time()
#
#                 if (time.time() - last_voice_time) > silence_duration:
#                     break
#                 if (time.time() - start_time) > max_duration:
#                     break
#
#             final_res = json.loads(rec.FinalResult()).get("text", "")
#             if final_res:
#                 text_chunks.append(final_res)
#
#         result_text = " ".join(text_chunks).strip()
#         if result_text:
#             print(f"✅ Transcribed: '{result_text}'")
#             speak(f"You said: {result_text}")
#         else:
#             speak("I couldn't understand that.")
#         return result_text
#
#
# # ---------- LOCAL ANALYSIS ---------- #
#
# def simple_analysis(text, intent_info):
#     keywords = intent_info.get('keywords', [])
#     intent = intent_info['primary_intent']
#     confidence = intent_info['confidence']
#
#     summary = text if len(text.split()) <= 30 else " ".join(text.split()[:30]) + "..."
#
#     mood_words = {
#         'happy': ['happy', 'excited', 'glad', 'joy', 'proud'],
#         'sad': ['sad', 'down', 'depressed', 'lonely'],
#         'angry': ['angry', 'mad', 'upset', 'frustrated'],
#         'anxious': ['worried', 'nervous', 'anxious'],
#         'calm': ['calm', 'peaceful', 'relaxed']
#     }
#     mood = 'neutral'
#     lower_text = text.lower()
#     for mood_label, words in mood_words.items():
#         if any(word in lower_text for word in words):
#             mood = mood_label
#             break
#
#     action_items = []
#     if intent == 'task_reminder':
#         action_items.append("Consider setting a reminder.")
#     elif intent == 'health_concern':
#         action_items.append("Monitor symptoms or consult a professional.")
#     elif intent == 'goal_planning':
#         action_items.append("Break the goal into small steps.")
#     elif intent == 'daily_activity':
#         action_items.append("Log any important outcomes.")
#     elif intent == 'emotional_expression':
#         action_items.append("Reflect further or talk to someone you trust.")
#     elif intent == 'social_interaction':
#         action_items.append("Stay connected with supportive people.")
#
#     advice = {
#         'task_reminder': "Stay organized; a checklist might help.",
#         'health_concern': "Take care of yourself and seek medical advice if needed.",
#         'goal_planning': "Consistency and tracking progress can keep you motivated.",
#         'daily_activity': "Great job staying engaged with your day.",
#         'emotional_expression': "Your feelings are valid—consider journaling more about them.",
#         'social_interaction': "It’s wonderful to maintain relationships."
#     }.get(intent, "Keep listening to yourself and doing your best.")
#
#     result = (
#         f"Summary: {summary}\n"
#         f"Mood: {mood}\n"
#         f"Primary Intent: {intent.replace('_', ' ')} ({confidence:.0%} confidence)\n"
#         f"Keywords: {', '.join(keywords[:10])}\n"
#         f"Action Items: {', '.join(action_items) if action_items else 'None'}\n"
#         f"Advice: {advice}"
#     )
#     return result
#
#
# # ---------- MAIN PROGRAM ---------- #
#
# def main():
#     print("\n" + "=" * 70)
#     print("🎙️  SMART DIARY (FULLY OFFLINE)")
#     print("=" * 70 + "\n")
#
#     detector = IntentDetector()
#
#     # --- choose your Vosk model path and microphone index here ---
#     MODEL_PATH = "vosk-model-small-en-us-0.15"
#     MICROPHONE_INDEX = None  # set to integer index from sd.query_devices()
#
#     recognizer = OfflineRecognizer(MODEL_PATH, MICROPHONE_INDEX)
#
#     speak("Welcome! I'm ready to record offline. Say exit to stop.")
#     diary_entries = []
#
#     while True:
#         try:
#             text = recognizer.listen_and_transcribe()
#
#             if not text:
#                 continue
#
#             if any(word in text.lower() for word in ['exit', 'stop', 'quit', 'goodbye']):
#                 speak(f"Goodbye! Saved {len(diary_entries)} entries.")
#                 break
#
#             print("\n" + "=" * 70)
#             print("🔍 ANALYZING YOUR ENTRY...")
#             print("=" * 70)
#
#             cleaned_text = preprocess_text(text)
#             keywords = extract_keywords(text)
#
#             intent_result = detector.predict_intent(text)
#             intent_result['keywords'] = keywords[:10]
#             intent_result['cleaned_text'] = cleaned_text
#
#             print("\n📊 INTENT ANALYSIS:")
#             print(f"   Primary Intent: {intent_result['primary_intent']}")
#             print(f"   Confidence: {intent_result['confidence']:.2%}")
#             print("\n   All Detected Intents (top 3):")
#             for intent, score in intent_result['all_intents'][:3]:
#                 print(f"      • {intent.replace('_', ' ')}: {score:.2%}")
#
#             print("\n🔤 TEXT ANALYSIS:")
#             print(f"   Keywords: {', '.join(keywords[:10])}")
#             print(f"   Cleaned: {cleaned_text[:100]}...")
#
#             intent_name = intent_result['primary_intent'].replace('_', ' ')
#             speak(f"I detected this is about {intent_name} with {intent_result['confidence']:.0%} confidence")
#
#             print("\n🤖 OFFLINE ANALYSIS:")
#             speak("Let me provide you with a quick analysis.")
#             analysis = simple_analysis(text, intent_result)
#             print(analysis)
#             speak(analysis)
#
#             diary_entries.append({
#                 'text': text,
#                 'intent': intent_result['primary_intent'],
#                 'confidence': intent_result['confidence'],
#                 'keywords': keywords
#             })
#
#             print("\n" + "=" * 70)
#             speak("Continue sharing, or say exit.")
#
#         except KeyboardInterrupt:
#             break
#         except Exception as e:
#             print(f"❌ Error: {e}")
#             speak("Something went wrong. Let's try again.")
#
#     print("\n" + "=" * 70)
#     print(f"✅ SESSION COMPLETE - {len(diary_entries)} entries recorded")
#     print("=" * 70)
#
#     if diary_entries:
#         print("\n📈 SESSION STATISTICS:")
#         intent_counts = Counter(entry['intent'] for entry in diary_entries)
#         for intent, count in intent_counts.most_common():
#             print(f"   {intent.replace('_', ' ')}: {count} times")
#
#         avg_confidence = np.mean(entry['confidence'] for entry in diary_entries)
#         print(f"\n📊 Average Confidence: {avg_confidence:.2%}")
#
#         all_keywords = []
#         for entry in diary_entries:
#             all_keywords.extend(entry['keywords'])
#         keyword_counts = Counter(all_keywords)
#         print("\n🔑 Top Keywords:")
#         for keyword, count in keyword_counts.most_common(5):
#             print(f"   {keyword}: {count} times")
#
#
# if __name__ == "__main__":
#     main()
# ##########################################################################################################################################3
# #
# # """
# # Hi Diary — offline Siri-like voice assistant
# # Optimized for Pakistani / Indian / South Asian English accents
# # """
# #
# # import sounddevice as sd
# # import numpy as np
# # import whisper
# # import scipy.io.wavfile as wav
# # import tempfile
# # import pyttsx3
# # import os
# # import re
# # from intent_predict import get_intent
# #
# # # ──────────────────── CONFIG ────────────────────
# # SAMPLE_RATE = 16000
# # CHANNELS = 1
# # DTYPE = "int16"
# #
# # # --- Wake word ---
# # WAKE_BUFFER_SEC = 4.0            # longer buffer — South Asian speech can be slower paced
# # WAKE_STRIDE_SEC = 2.0            # overlap so wake word isn't split
# # WAKE_ENERGY_MIN = 60             # lower threshold — some speakers are softer
# #
# # # --- Command recording ---
# # CMD_CHUNK_SEC = 0.5
# # CMD_SILENCE_TIMEOUT = 2.5        # longer pause tolerance (Asian English has more pauses)
# # CMD_ENERGY_MIN = 60
# # CMD_MAX_DURATION = 20.0          # allow longer commands (code-switching takes more time)
# #
# # # --- Whisper ---
# # WHISPER_MODEL_SIZE = "small"     # "small" handles accents MUCH better than "tiny"
# #
# # # ──────────────────── WAKE PHRASES ────────────────────
# # # Whisper commonly mishears "Hi Diary" with South Asian accents as:
# # WAKE_PHRASES = [
# #     # --- Correct ---
# #     "hi diary", "hi, diary", "hey diary", "hey, diary",
# #     "hi diary.", "hey diary.",
# #
# #     # --- Common Whisper mishearings (Pakistani/Indian accent) ---
# #     "hi dairy", "hi dairy.", "hey dairy",
# #     "hi dary", "hi dari", "hey dari",
# #     "hi diaries", "hey diaries",
# #     "hi dayri", "hey dayri",
# #     "haideri", "hi deri", "hey deri",
# #     "hyderi", "hi diari",
# #     "hide iary", "hideiary",
# #     "high diary", "high dairy",
# #     "hi there e", "hi there i",
# #     "hi daari", "hey daari",
# #     "hi dee ari", "hi deari",
# #     "hi diary yaar",                # Urdu/Hindi filler
# #     "hi diary na",                  # filler
# #     "haan hi diary",               # "yes hi diary"
# #
# #     # --- Urdu/Hindi style ---
# #     "hello diary", "assalam diary",
# #     "hey diari", "hi diaary",
# # ]
# #
# #
# # # ──────────────────── FILLER / NOISE CLEANUP ────────────────────
# # # South Asian speakers often add these — strip them before intent detection
# # FILLER_WORDS = [
# #     r"\byaar\b", r"\bna\b", r"\bhaan\b", r"\baccha\b",
# #     r"\bbasically\b", r"\bactually\b", r"\blike\b",
# #     r"\bmeans\b",          # "means" used as filler in Pak/Indian English
# #     r"\bno\?\s*$",         # trailing "no?" (tag question)
# #     r"\bright\?\s*$",      # trailing "right?"
# #     r"\bhai\b",            # Urdu/Hindi "hai" (is)
# #     r"\bkaro\b",           # "karo" (do) — common in code-switching
# #     r"\bkr\b",             # short form
# #     r"\bkia\b",            # Urdu "kia" (did/what)
# #     r"\bmujhe\b",          # "mujhe" (me) — partial Urdu
# #     r"\baur\b",            # "aur" (and) — Urdu
# # ]
# #
# #
# # def clean_text(text: str) -> str:
# #     """Remove filler words and normalize South Asian English patterns."""
# #     cleaned = text.strip()
# #
# #     # Remove common fillers
# #     for pattern in FILLER_WORDS:
# #         cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE)
# #
# #     # Normalize common South Asian pronunciations that Whisper might transcribe literally
# #     replacements = {
# #         "vhat": "what",
# #         "vhen": "when",
# #         "vhere": "where",
# #         "vhy": "why",
# #         "very": "very",
# #         "tink": "think",
# #         "ting": "thing",
# #         "dat": "that",
# #         "dis": "this",
# #         "dey": "they",
# #         "vedder": "weather",
# #         "veather": "weather",
# #         "vork": "work",
# #         "vorry": "worry",
# #         "vait": "wait",
# #         "vant": "want",
# #         "vould": "would",
# #         "vill": "will",
# #         "vatch": "watch",
# #         "skedule": "schedule",
# #         "shedule": "schedule",
# #     }
# #
# #     for wrong, right in replacements.items():
# #         cleaned = re.sub(rf"\b{wrong}\b", right, cleaned, flags=re.IGNORECASE)
# #
# #     # Collapse extra spaces
# #     cleaned = re.sub(r"\s{2,}", " ", cleaned).strip()
# #     return cleaned
# #
# #
# # # ──────────────────── WHISPER PROMPTING ────────────────────
# # # This is the SECRET WEAPON for accent handling!
# # # Whisper accepts an `initial_prompt` that biases the model toward
# # # certain vocabulary and speaking styles.
# #
# # WHISPER_PROMPT = (
# #     "The speaker has a Pakistani or Indian English accent. "
# #     "They may mix Urdu or Hindi words like 'yaar', 'accha', 'haan', 'karo'. "
# #     "Common topics: diary, journal, mood, reminder, schedule, note, entry, "
# #     "feeling, happy, sad, stressed, weather, meeting, task, todo. "
# #     "The wake word is 'Hi Diary'."
# # )
# #
# #
# # # ──────────────────── TTS ENGINE ────────────────────
# # engine = pyttsx3.init()
# # engine.setProperty("rate", 160)   # slightly slower for clarity
# #
# #
# # def speak(text: str):
# #     print(f"🔊  {text}")
# #     try:
# #         engine.say(text)
# #         engine.runAndWait()
# #     except RuntimeError:
# #         pass
# #
# #
# # # ──────────────────── LOAD WHISPER ────────────────────
# # print(f"🧠  Loading Whisper '{WHISPER_MODEL_SIZE}' model …")
# # whisper_model = whisper.load_model(WHISPER_MODEL_SIZE)
# # speak("Hi Diary assistant is ready. Say Hi Diary to start.")
# #
# #
# # # ──────────────────── AUDIO HELPERS ────────────────────
# # def rms_energy(audio: np.ndarray) -> float:
# #     return float(np.sqrt(np.mean(audio.astype(np.float32) ** 2)))
# #
# #
# # def save_wav(audio: np.ndarray) -> str:
# #     tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
# #     wav.write(tmp.name, SAMPLE_RATE, audio)
# #     tmp.close()
# #     return tmp.name
# #
# #
# # def transcribe(path: str, prompt: str = "") -> str:
# #     """Transcribe with accent-aware prompting."""
# #     result = whisper_model.transcribe(
# #         path,
# #         language="en",
# #         fp16=False,
# #         initial_prompt=prompt,           # <-- accent bias!
# #         temperature=0.0,                 # deterministic = more stable
# #         no_speech_threshold=0.5,         # filter out silence hallucinations
# #         condition_on_previous_text=False, # each transcription is independent
# #     )
# #     return result["text"].strip()
# #
# #
# # # ──────────────────── WAKE WORD DETECTION ────────────────────
# # def detect_wake_word():
# #     print("\n🎧  Listening for 'Hi Diary' … speak naturally.")
# #
# #     buf_samples = int(WAKE_BUFFER_SEC * SAMPLE_RATE)
# #     stride_samples = int(WAKE_STRIDE_SEC * SAMPLE_RATE)
# #     rolling = np.zeros(buf_samples, dtype=np.int16)
# #
# #     while True:
# #         new_audio = sd.rec(stride_samples, samplerate=SAMPLE_RATE,
# #                            channels=CHANNELS, dtype=DTYPE)
# #         sd.wait()
# #         new_audio = new_audio.flatten()
# #         rolling = np.concatenate([rolling[stride_samples:], new_audio])
# #
# #         energy = rms_energy(rolling)
# #         if energy < WAKE_ENERGY_MIN:
# #             continue
# #
# #         path = save_wav(rolling)
# #         text = transcribe(path, prompt="Hi Diary.").lower()
# #         os.unlink(path)
# #
# #         print(f"   [wake] heard: \"{text}\"  (energy {energy:.0f})")
# #
# #         if any(wp in text for wp in WAKE_PHRASES):
# #             speak("Ji haan, I'm listening!")  # 🇵🇰🇮🇳 friendly response
# #             return
# #
# #
# # # ──────────────────── COMMAND RECORDING ────────────────────
# # def record_command() -> str:
# #     print("🎤  Recording your command …")
# #
# #     chunk_samples = int(CMD_CHUNK_SEC * SAMPLE_RATE)
# #     max_silent = int(CMD_SILENCE_TIMEOUT / CMD_CHUNK_SEC)
# #     max_chunks = int(CMD_MAX_DURATION / CMD_CHUNK_SEC)
# #
# #     chunks = []
# #     silent_count = 0
# #     heard_speech = False
# #
# #     for _ in range(max_chunks):
# #         chunk = sd.rec(chunk_samples, samplerate=SAMPLE_RATE,
# #                        channels=CHANNELS, dtype=DTYPE)
# #         sd.wait()
# #         chunk = chunk.flatten()
# #         chunks.append(chunk)
# #
# #         energy = rms_energy(chunk)
# #         if energy >= CMD_ENERGY_MIN:
# #             heard_speech = True
# #             silent_count = 0
# #         else:
# #             silent_count += 1
# #
# #         if heard_speech and silent_count >= max_silent:
# #             break
# #
# #     print("✅  Command recording finished.")
# #     return save_wav(np.concatenate(chunks))
# #
# #
# # # ──────────────────── MAIN LOOP ────────────────────
# # def main():
# #     print("\n🤖  Hi Diary Assistant (South Asian English Mode)")
# #     print("    Say \"Hi Diary\" to wake me up")
# #     print("    Urdu/Hindi mixing supported!")
# #     print("    Press Ctrl+C to quit\n")
# #
# #     try:
# #         while True:
# #             detect_wake_word()
# #
# #             wav_path = record_command()
# #
# #             print("📝  Transcribing …")
# #             raw_text = transcribe(wav_path, prompt=WHISPER_PROMPT)
# #             os.unlink(wav_path)
# #
# #             if not raw_text or len(raw_text) < 2:
# #                 speak("Sorry, zara dobara boliye.")  # "please say again"
# #                 continue
# #
# #             # Clean up filler words and accent artifacts
# #             cleaned_text = clean_text(raw_text)
# #
# #             print(f"    Raw:     \"{raw_text}\"")
# #             print(f"    Cleaned: \"{cleaned_text}\"")
# #             speak(f"You said: {cleaned_text}")
# #
# #             # Intent detection on cleaned text
# #             intent = get_intent(cleaned_text)
# #             print(f"    🧭 Intent: {intent}\n")
# #             speak(f"Intent detected: {intent}")
# #
# #             print("── waiting for next wake word ──\n")
# #
# #     except KeyboardInterrupt:
# #         print("\n👋  Allah Hafiz! Goodbye!")
# #
# #
# # if __name__ == "__main__":
# #     main()


import whisper
import torch
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import datetime
import webbrowser
import os

# ==============================
# FORCE CPU + FP32 MODE
# ==============================
torch.set_num_threads(os.cpu_count())

DEVICE = "cpu"
MODEL_SIZE = "medium"

WAKE_WORDS = ["hi diary", "hey diary", "hi dairy", "hey dairy", "hi deary"]
EXIT_WORDS = ["stop program", "exit program", "close program"]

fs = 16000
seconds = 4

# ==============================
# LOAD WHISPER (CPU FP32)
# ==============================
print("🧠 Loading Whisper model on CPU (FP32)...")
model = whisper.load_model(MODEL_SIZE, device=DEVICE)
print("✅ Assistant Ready!")

# ==============================
# RECORD AUDIO
# ==============================
def record_audio(filename="temp.wav"):
    print("🎧 Listening...")
    audio = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype='float32')
    sd.wait()

    # Normalize volume (important for mic clarity)
    audio = audio / np.max(np.abs(audio))

    write(filename, fs, audio)

# ==============================
# SPEECH → TEXT (CPU SAFE)
# ==============================
def speech_to_text():
    record_audio()

    result = model.transcribe(
        "temp.wav",
        language="en",
        fp16=False,        # ⭐ FORCE FP32
        temperature=0.0,
        best_of=1,
        beam_size=1
    )

    text = result["text"].lower().strip()
    return text

# ==============================
# COMMANDS
# ==============================
def execute_command(command):
    print("🤖 Command:", command)

    if "time" in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        print("⏰ Time:", now)

    elif "date" in command:
        today = datetime.datetime.now().strftime("%d %B %Y")
        print("📅 Date:", today)

    elif "open youtube" in command:
        webbrowser.open("https://youtube.com")
        print("🌐 Opening YouTube")

    elif "open google" in command:
        webbrowser.open("https://google.com")
        print("🌐 Opening Google")

    elif "open whatsapp" in command:
        webbrowser.open("https://web.whatsapp.com")
        print("🌐 Opening WhatsApp")

    elif "hello" in command or "salam" in command:
        print("👋 Walaikum Salam!")

    else:
        print("❌ Command not recognized")

# ==============================
# HELPERS
# ==============================
def is_wake_word(text):
    return any(word in text for word in WAKE_WORDS)

def is_exit_word(text):
    return any(word in text for word in EXIT_WORDS)

# ==============================
# MAIN LOOP
# ==============================
print("\n🎤 Say 'Hi Diary'...")

while True:
    text = speech_to_text()
    print("🗣️ Heard:", text)

    if is_exit_word(text):
        print("👋 Assistant stopped.")
        break

    if is_wake_word(text):
        print("✨ Wake word detected! Speak command...")
        command = speech_to_text()
        execute_command(command)


####################################################################################333########
# import os
# import sys
# import queue
# import sounddevice as sd
# from vosk import Model, KaldiRecognizer
# import json
#
# WAKE_WORDS = ["hi diary", "hey diary", "hi dairy"]
# EXIT_WORDS = ["stop program", "exit program"]
#
# # Load model (download once)
# if not os.path.exists("vosk-model-small-en-us-0.15"):
#     print("Download model from https://alphacephei.com/vosk/models and unzip as 'vosk-model-small-en-us-0.15'")
#     sys.exit()
#
# model = Model("vosk-model-small-en-us-0.15")
# q = queue.Queue()
#
# # Audio callback
# def callback(indata, frames, time, status):
#     q.put(bytes(indata))
#
# # Stream microphone
# with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
#                        channels=1, callback=callback):
#     rec = KaldiRecognizer(model, 16000)
#     print("🎤 Say 'Hi Diary'...")
#
#     while True:
#         data = q.get()
#         if rec.AcceptWaveform(data):
#             result = json.loads(rec.Result())
#             text = result.get("text", "").lower()
#             print("🗣️ Heard:", text)
#
#             if any(word in text for word in EXIT_WORDS):
#                 print("👋 Stopping assistant...")
#                 break
#
#             if any(word in text for word in WAKE_WORDS):
#                 print("✨ Wake word detected! Speak command...")
#                 # Simple command listening
#                 command = ""
#                 while command.strip() == "":
#                     data = q.get()
#                     if rec.AcceptWaveform(data):
#                         command = json.loads(rec.Result()).get("text", "").lower()
#                 print("📢 Command:", command)




####################################################################################################3
# import queue
# import sounddevice as sd
# import numpy as np
# from transformers import WhisperProcessor, WhisperForConditionalGeneration
# import torch
#
# # -------------------------------
# # CONFIG
# # -------------------------------
# WAKE_WORDS = ["hi diary", "hey diary", "hi dairy"]
# EXIT_WORDS = ["stop program", "exit program"]
#
# # Path to your offline Whisper model folder
# LOCAL_MODEL_PATH = "models/whisper-small"  # <-- update with your model path
#
# DEVICE = "cpu"  # Change to "cuda" if you have GPU
# DTYPE = torch.float32
#
# # -------------------------------
# # LOAD MODEL
# # -------------------------------
# print("🧠 Loading Whisper model (offline, multilingual)...")
# processor = WhisperProcessor.from_pretrained(LOCAL_MODEL_PATH)
# model = WhisperForConditionalGeneration.from_pretrained(LOCAL_MODEL_PATH)
# model.to(DEVICE)
# model.eval()
# print("✅ Whisper Ready")
#
# # -------------------------------
# # AUDIO QUEUE
# # -------------------------------
# q = queue.Queue()
#
# def audio_callback(indata, frames, time, status):
#     """Put microphone audio into queue"""
#     q.put(indata.copy())
#
# # -------------------------------
# # TRANSCRIPTION FUNCTION
# # -------------------------------
# def transcribe(audio_np: np.ndarray) -> str:
#     """Convert raw audio (float32) to text using Whisper"""
#     # audio_np must be float32 in [-1, 1], shape=(num_samples,)
#     input_features = processor(audio_np, sampling_rate=16000, return_tensors="pt").input_features
#     input_features = input_features.to(DEVICE, dtype=DTYPE)
#     with torch.no_grad():
#         predicted_ids = model.generate(input_features)
#     text = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
#     return text.lower()
#
# # -------------------------------
# # MAIN LISTEN LOOP
# # -------------------------------
# print("🎧 Listening for wake word 'Hi Diary'...")
#
# # Microphone stream: 16kHz, mono, int16
# with sd.InputStream(samplerate=16000, channels=1, dtype='int16',
#                     callback=audio_callback, blocksize=16000):
#     try:
#         while True:
#             data = q.get()
#             # Convert int16 to float32 in [-1, 1]
#             audio_np = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0
#             if len(audio_np) == 0:
#                 continue
#
#             # Transcribe chunk
#             text = transcribe(audio_np)
#             if not text.strip():
#                 continue
#
#             print("🗣️ Heard:", text)
#
#             # Check for exit words
#             if any(word in text for word in EXIT_WORDS):
#                 print("👋 Stopping assistant...")
#                 break
#
#             # Check for wake words
#             if any(word in text for word in WAKE_WORDS):
#                 print("✨ Wake word detected! Listening for command...")
#                 command = ""
#                 while command.strip() == "":
#                     data_cmd = q.get()
#                     audio_cmd = np.frombuffer(data_cmd, dtype=np.int16).astype(np.float32) / 32768.0
#                     command = transcribe(audio_cmd)
#                 print("📢 Command:", command)
#
#     except KeyboardInterrupt:
#         print("👋 Assistant stopped by user")
