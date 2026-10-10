# # # # # # %% full NER training + live input script
# # # # # import os
# # # # # from datasets import Dataset, Features, Sequence, Value, ClassLabel
# # # # # from transformers import AutoTokenizer, AutoModelForTokenClassification
# # # # # from transformers import TrainingArguments, Trainer, DataCollatorForTokenClassification, pipeline
# # # # #
# # # # # # ====== CONFIG ======
# # # # # BIO_FILE = "bio_dataset.txt"   # Your dataset file
# # # # # MODEL_NAME = "dslim/bert-base-NER"
# # # # # OUTPUT_DIR = "./personal_ner_model"
# # # # # NUM_EPOCHS = 3
# # # # # BATCH_SIZE = 8
# # # # # LEARNING_RATE = 5e-5
# # # # #
# # # # # # ====== LOAD BIO DATA ======
# # # # # def load_bio_file(file_path):
# # # # #     sentences = []
# # # # #     words = []
# # # # #     labels = []
# # # # #     with open(file_path, 'r', encoding='utf-8') as f:
# # # # #         for line in f:
# # # # #             line = line.strip()
# # # # #             if not line:
# # # # #                 if words:
# # # # #                     sentences.append({'words': words, 'ner_tags': labels})
# # # # #                     words = []
# # # # #                     labels = []
# # # # #                 continue
# # # # #             splits = line.split('\t')
# # # # #             if len(splits) != 2:
# # # # #                 continue
# # # # #             word, label = splits
# # # # #             words.append(word)
# # # # #             labels.append(label)
# # # # #         if words:
# # # # #             sentences.append({'words': words, 'ner_tags': labels})
# # # # #     return sentences
# # # # #
# # # # # # ====== LABELS ======
# # # # # label_list = [
# # # # #     "O",
# # # # #     "B-PERSON","I-PERSON",
# # # # #     "B-RELATIVE","I-RELATIVE",
# # # # #     "B-EVENT","I-EVENT",
# # # # #     "B-MONEY","I-MONEY",
# # # # #     "B-DATE","I-DATE",
# # # # #     "B-TIME","I-TIME",
# # # # #     "B-ASSET","I-ASSET",
# # # # #     "B-LOC","I-LOC",
# # # # #     "B-CARDINAL","I-CARDINAL"
# # # # # ]
# # # # #
# # # # # # ====== CONVERT TO DATASET ======
# # # # # bio_data = load_bio_file(BIO_FILE)
# # # # # features = Features({
# # # # #     'words': Sequence(Value('string')),
# # # # #     'ner_tags': Sequence(ClassLabel(names=label_list))
# # # # # })
# # # # # dataset = Dataset.from_list(bio_data, features=features)
# # # # # dataset = dataset.train_test_split(test_size=0.1)
# # # # # train_dataset = dataset['train']
# # # # # test_dataset = dataset['test']
# # # # #
# # # # # # ====== TOKENIZER ======
# # # # # tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
# # # # #
# # # # # def tokenize_and_align_labels(examples):
# # # # #     tokenized_inputs = tokenizer(
# # # # #         examples["words"],
# # # # #         truncation=True,
# # # # #         is_split_into_words=True
# # # # #     )
# # # # #     labels = []
# # # # #     for i, label in enumerate(examples["ner_tags"]):
# # # # #         word_ids = tokenized_inputs.word_ids(batch_index=i)
# # # # #         previous_word_idx = None
# # # # #         label_ids = []
# # # # #         for word_idx in word_ids:
# # # # #             if word_idx is None:
# # # # #                 label_ids.append(-100)
# # # # #             elif word_idx != previous_word_idx:
# # # # #                 label_ids.append(label_list.index(label[word_idx]))
# # # # #             else:
# # # # #                 label_ids.append(-100)
# # # # #             previous_word_idx = word_idx
# # # # #         labels.append(label_ids)
# # # # #     tokenized_inputs["labels"] = labels
# # # # #     return tokenized_inputs
# # # # #
# # # # # train_dataset = train_dataset.map(tokenize_and_align_labels, batched=True)
# # # # # test_dataset = test_dataset.map(tokenize_and_align_labels, batched=True)
# # # # #
# # # # # # ====== MODEL ======
# # # # # model = AutoModelForTokenClassification.from_pretrained(
# # # # #     MODEL_NAME, num_labels=len(label_list)
# # # # # )
# # # # #
# # # # # data_collator = DataCollatorForTokenClassification(tokenizer)
# # # # # training_args = TrainingArguments(
# # # # #     output_dir=OUTPUT_DIR,
# # # # #     evaluation_strategy="epoch",
# # # # #     save_strategy="epoch",
# # # # #     learning_rate=LEARNING_RATE,
# # # # #     per_device_train_batch_size=BATCH_SIZE,
# # # # #     per_device_eval_batch_size=BATCH_SIZE,
# # # # #     num_train_epochs=NUM_EPOCHS,
# # # # #     weight_decay=0.01,
# # # # #     logging_dir="./logs",
# # # # #     load_best_model_at_end=True,
# # # # # )
# # # # #
# # # # # trainer = Trainer(
# # # # #     model=model,
# # # # #     args=training_args,
# # # # #     train_dataset=train_dataset,
# # # # #     eval_dataset=test_dataset,
# # # # #     tokenizer=tokenizer,
# # # # #     data_collator=data_collator
# # # # # )
# # # # #
# # # # # # ====== TRAIN ======
# # # # # trainer.train()
# # # # #
# # # # # # ====== SAVE ======
# # # # # model.save_pretrained(OUTPUT_DIR)
# # # # # tokenizer.save_pretrained(OUTPUT_DIR)
# # # # #
# # # # # # ====== LIVE NER PIPELINE ======
# # # # # nlp = pipeline(
# # # # #     "ner",
# # # # #     model=OUTPUT_DIR,
# # # # #     tokenizer=OUTPUT_DIR,
# # # # #     aggregation_strategy="simple"
# # # # # )
# # # # #
# # # # # print("✅ NER Model Ready. Type 'exit' to stop.")
# # # # # while True:
# # # # #     text = input("Enter sentence: ")
# # # # #     if text.lower() in ["exit", "quit"]:
# # # # #         break
# # # # #     entities = nlp(text)
# # # # #     result = {}
# # # # #     for ent in entities:
# # # # #         result.setdefault(ent['entity_group'], []).append(ent['word'])
# # # # #     print("🔹 Extracted Entities (JSON):")
# # # # #     print(result)
# # # #
# # # #
# # # # # %% full NER training + live input script
# # # # import os
# # # # import torch
# # # # from datasets import Dataset, Features, Sequence, Value, ClassLabel
# # # # from transformers import AutoTokenizer, AutoModelForTokenClassification
# # # # from transformers import TrainingArguments, Trainer, DataCollatorForTokenClassification, pipeline
# # # #
# # # # # ====== CONFIG ======
# # # # # FIX 1: Ensure the path matches your Colab sidebar (check for typos like 'datset')
# # # # BIO_FILE = "bio_dataset.txt"
# # # # MODEL_NAME = "dslim/bert-base-NER"
# # # # OUTPUT_DIR = "./personal_ner_model"
# # # # NUM_EPOCHS = 3
# # # # BATCH_SIZE = 8
# # # # LEARNING_RATE = 5e-5
# # # #
# # # #
# # # # # ====== LOAD BIO DATA ======
# # # # def load_bio_file(file_path):
# # # # 	sentences = []
# # # # 	words = []
# # # # 	labels = []
# # # # 	if not os.path.exists(file_path):
# # # # 		raise FileNotFoundError(f"File not found at {file_path}. Please upload it to the Colab folder icon.")
# # # #
# # # # 	with open(file_path, 'r', encoding='utf-8') as f:
# # # # 		for line in f:
# # # # 			line = line.strip()
# # # # 			if not line:
# # # # 				if words:
# # # # 					sentences.append({'words': words, 'ner_tags': labels})
# # # # 					words = []
# # # # 					labels = []
# # # # 				continue
# # # # 			splits = line.split('\t')
# # # # 			if len(splits) != 2:
# # # # 				continue
# # # # 			word, label = splits
# # # # 			words.append(word)
# # # # 			labels.append(label)
# # # # 		if words:
# # # # 			sentences.append({'words': words, 'ner_tags': labels})
# # # # 	return sentences
# # # #
# # # #
# # # # # ====== LABELS ======
# # # # label_list = [
# # # # 	"O",
# # # # 	"B-PERSON", "I-PERSON",
# # # # 	"B-RELATIVE", "I-RELATIVE",
# # # # 	"B-EVENT", "I-EVENT",
# # # # 	"B-MONEY", "I-MONEY",
# # # # 	"B-DATE", "I-DATE",
# # # # 	"B-TIME", "I-TIME",
# # # # 	"B-ASSET", "I-ASSET",
# # # # 	"B-LOC", "I-LOC",
# # # # 	"B-CARDINAL", "I-CARDINAL"
# # # # ]
# # # #
# # # # # ====== CONVERT TO DATASET ======
# # # # bio_data = load_bio_file(BIO_FILE)
# # # # features = Features({
# # # # 	'words': Sequence(Value('string')),
# # # # 	'ner_tags': Sequence(ClassLabel(names=label_list))
# # # # })
# # # # dataset = Dataset.from_list(bio_data, features=features)
# # # # dataset = dataset.train_test_split(test_size=0.1)
# # # # train_dataset = dataset['train']
# # # # test_dataset = dataset['test']
# # # #
# # # # # ====== TOKENIZER ======
# # # # tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
# # # #
# # # #
# # # # def tokenize_and_align_labels(examples):
# # # # 	tokenized_inputs = tokenizer(
# # # # 		examples["words"],
# # # # 		truncation=True,
# # # # 		is_split_into_words=True
# # # # 	)
# # # # 	labels = []
# # # # 	for i, label in enumerate(examples["ner_tags"]):
# # # # 		word_ids = tokenized_inputs.word_ids(batch_index=i)
# # # # 		previous_word_idx = None
# # # # 		label_ids = []
# # # # 		for word_idx in word_ids:
# # # # 			if word_idx is None:
# # # # 				label_ids.append(-100)
# # # # 			elif word_idx != previous_word_idx:
# # # # 				# FIX 2: Removed .index() because labels are already integers here
# # # # 				label_ids.append(label[word_idx])
# # # # 			else:
# # # # 				label_ids.append(-100)
# # # # 			previous_word_idx = word_idx
# # # # 		labels.append(label_ids)
# # # # 	tokenized_inputs["labels"] = labels
# # # # 	return tokenized_inputs
# # # #
# # # #
# # # # train_dataset = train_dataset.map(tokenize_and_align_labels, batched=True)
# # # # test_dataset = test_dataset.map(tokenize_and_align_labels, batched=True)
# # # #
# # # # # ====== MODEL ======
# # # # # FIX 3: Added ignore_mismatched_sizes=True to allow 19 labels instead of the original 9
# # # # model = AutoModelForTokenClassification.from_pretrained(
# # # # 	MODEL_NAME,
# # # # 	num_labels=len(label_list),
# # # # 	ignore_mismatched_sizes=True
# # # # )
# # # #
# # # # data_collator = DataCollatorForTokenClassification(tokenizer)
# # # # training_args = TrainingArguments(
# # # # 	output_dir=OUTPUT_DIR,
# # # # 	eval_strategy="epoch",  # Updated from deprecated 'evaluation_strategy'
# # # # 	save_strategy="epoch",
# # # # 	learning_rate=LEARNING_RATE,
# # # # 	per_device_train_batch_size=BATCH_SIZE,
# # # # 	per_device_eval_batch_size=BATCH_SIZE,
# # # # 	num_train_epochs=NUM_EPOCHS,
# # # # 	weight_decay=0.01,
# # # # 	logging_dir="./logs",
# # # # 	load_best_model_at_end=True,
# # # # 	report_to="none"  # Prevents prompts for WandB account
# # # # )
# # # #
# # # # # trainer = Trainer(
# # # # # 	model=model,
# # # # # 	args=training_args,
# # # # # 	train_dataset=train_dataset,
# # # # # 	eval_dataset=test_dataset,
# # # # # 	tokenizer=tokenizer,
# # # # # 	data_collator=data_collator
# # # # # )
# # # # # ====== UPDATED TRAINER ======
# # # # trainer = Trainer(
# # # #     model=model,
# # # #     args=training_args,
# # # #     train_dataset=train_dataset,
# # # #     eval_dataset=test_dataset,
# # # #     # CHANGE THIS LINE:
# # # #     processing_class=tokenizer,
# # # #     data_collator=data_collator
# # # # )
# # # #
# # # # # ====== TRAIN ======
# # # # trainer.train()
# # # #
# # # # # ====== SAVE ======
# # # # model.save_pretrained(OUTPUT_DIR)
# # # # tokenizer.save_pretrained(OUTPUT_DIR)
# # # #
# # # # # ====== LIVE NER PIPELINE ======
# # # # nlp = pipeline(
# # # # 	"ner",
# # # # 	model=OUTPUT_DIR,
# # # # 	tokenizer=OUTPUT_DIR,
# # # # 	aggregation_strategy="simple"
# # # # )
# # # #
# # # # print("\n✅ NER Model Ready. Type 'exit' to stop.")
# # # # while True:
# # # # 	text = input("Enter sentence: ")
# # # # 	if text.lower() in ["exit", "quit"]:
# # # # 		break
# # # # 	entities = nlp(text)
# # # # 	result = {}
# # # # 	for ent in entities:
# # # # 		result.setdefault(ent['entity_group'], []).append(ent['word'])
# # # # 	print("🔹 Extracted Entities:")
# # # # 	print(result)
# # # from transformers import pipeline
# # #
# # # # Load your fine-tuned model
# # # MODEL_PATH = "./personal_ner_model"
# # #
# # # # Initialize the pipeline with 'simple' aggregation to merge sub-tokens
# # # nlp = pipeline(
# # # 	"ner",
# # # 	model=MODEL_PATH,
# # # 	tokenizer=MODEL_PATH,
# # # 	aggregation_strategy="simple"
# # # )
# # #
# # #
# # # def get_clean_ner(text):
# # # 	# Get raw entities from the model
# # # 	entities = nlp(text)
# # #
# # # 	# Format into a dictionary: {'LABEL': ['word1', 'word2']}
# # # 	result = {}
# # # 	for ent in entities:
# # # 		label = ent['entity_group']
# # # 		word = ent['word'].strip()
# # #
# # # 		if label not in result:
# # # 			result[label] = []
# # # 		result[label].append(word)
# # #
# # # 	return result
# # #
# # #
# # # # --- Testing the output ---
# # # if __name__ == "__main__":
# # # 	text = input("Enter sentence: ")
# # #
# # # 	extracted = get_clean_ner(text)
# # #
# # # 	print("🔹 Extracted Entities:")
# # # 	print(extracted)
# #
# # # full_ner_windows_safe.py
# # # ====== LOAD TRAINED MODEL ONLY (NO TRAINING) ======
# #
# # from transformers import pipeline
# #
# # OUTPUT_DIR = "./personal_ner_model"
# #
# # # Load saved model
# # nlp = pipeline(
# #     "ner",
# #     model=OUTPUT_DIR,
# #     tokenizer=OUTPUT_DIR,
# #     aggregation_strategy="simple"
# # )
# #
# # print("\n✅ NER Model Ready. Type 'exit' to stop.")
# #
# # while True:
# #     text = input("Enter sentence: ")
# #     if text.lower() in ["exit", "quit"]:
# #         break
# #
# #     entities = nlp(text)
# #
# #     result = {}
# #     for ent in entities:
# #         result.setdefault(ent['entity_group'], []).append(ent['word'])
# #
# #     print("🔹 Extracted Entities:")
# #     print(result)
# from transformers import pipeline
#
# OUTPUT_DIR = "./personal_ner_model"
#
# # Load saved offline NER model
# nlp = pipeline(
#     "ner",
#     model=OUTPUT_DIR,
#     tokenizer=OUTPUT_DIR,
#     aggregation_strategy="simple"  # Aggregates tokens to entities
# )
#
# print("\n✅ NER Model Ready. Type 'exit' to stop.\n")
#
# def merge_subwords(words):
#     """
#     Merge subwords starting with '##' into full words.
#     Example: ['1000', '##0'] -> ['10000']
#     """
#     merged = []
#     buffer = ""
#     for w in words:
#         if w.startswith("##"):
#             buffer += w[2:]
#         else:
#             if buffer:
#                 merged.append(buffer)
#             buffer = w
#     if buffer:
#         merged.append(buffer)
#     return merged
#
# while True:
#     text = input("Enter sentence: ")
#     if text.lower() in ["exit", "quit"]:
#         break
#
#     entities = nlp(text)
#
#     # Prepare result dictionary
#     result = {}
#     for ent in entities:
#         entity_type = ent['entity_group']
#         word_list = ent['word'] if isinstance(ent['word'], list) else [ent['word']]
#         merged_words = merge_subwords(word_list)
#         result.setdefault(entity_type, []).extend(merged_words)
#
#     # Print clean output
#     print("\n🔹 Extracted Entities:")
#     for k, v in result.items():
#         print(f"{k}: {v}")
#
#     print("\n" + "-"*50 + "\n")
from transformers import pipeline

OUTPUT_DIR = "./personal_ner_model"

# Load saved offline NER model (NO aggregation → real NER)
nlp = pipeline(
    "ner",
    model=OUTPUT_DIR,
    tokenizer=OUTPUT_DIR
)

print("\n✅ NER Model Ready. Type 'exit' to stop.\n")

def merge_subwords(words):
    """
    Merge subwords starting with '##' into full words.
    Example: ['1000', '##0'] -> ['10000']
    """
    merged = []
    buffer = ""
    for w in words:
        if w.startswith("##"):
            buffer += w[2:]
        else:
            if buffer:
                merged.append(buffer)
            buffer = w
    if buffer:
        merged.append(buffer)
    return merged


# Simple fallback PERSON names (temporary solution)
COMMON_NAMES = {
    "ali", "ahmed", "usman", "hassan", "faisal", "zain", "bilal"
}

while True:
    text = input("Enter sentence: ")
    if text.lower() in ["exit", "quit"]:
        break

    entities = nlp(text)

    # Fixed schema output (always present)
    result = {
        "PERSON": [],
        "EVENT": [],
        "LOCATION": [],
        "DATE": []
    }

    # Token-level NER processing
    for ent in entities:
        tag = ent["entity"]

        # Only care about real entities
        if tag == "O":
            continue

        # BIO → entity type
        entity_type = tag.split("-")[-1]

        word = ent["word"]
        result.setdefault(entity_type, []).append(word)

    # Merge subwords per entity
    for k, v in result.items():
        result[k] = merge_subwords(v)

    # 🔹 Fallback PERSON detection (rule-based)
    detected_persons = set(name.lower() for name in result["PERSON"])
    for token in text.split():
        clean = token.lower().strip(".,!?")
        if clean in COMMON_NAMES and clean not in detected_persons:
            result["PERSON"].append(token)

    # 🔹 Print clean output
    print("\n🔹 Extracted Entities:")
    for k, v in result.items():
        print(f"{k}: {v}")

    print("\n" + "-" * 50 + "\n")