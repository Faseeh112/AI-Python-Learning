# import json
# from datasets import load_dataset
# from transformers import (
#     AutoTokenizer,
#     AutoModelForTokenClassification,
#     TrainingArguments,
#     Trainer
# )
#
# # -----------------------------
# # PATHS (CHANGE IF NEEDED)
# # -----------------------------
# DATA_DIR = "data/ontonotes"
# TRAIN_FILE = f"{DATA_DIR}/train.conll"
# VAL_FILE = f"{DATA_DIR}/validation.conll"
# TEST_FILE = f"{DATA_DIR}/test.conll"
# LABEL_FILE = f"{DATA_DIR}/labels_fixed.json"
#
# MODEL_NAME = "bert-base-cased"
#
# # -----------------------------
# # LOAD LABELS
# # -----------------------------
# with open(LABEL_FILE, "r") as f:
#     label2id = json.load(f)
#
# # id2label = {v: k for k, v in label2id.items()}
# id2label = {v[0]: k for k, v in label2id.items()}  # extract first element of list
#
# num_labels = len(label2id)
#
# # -----------------------------
# # LOAD CoNLL DATA
# # -----------------------------
# dataset = load_dataset(
#     "text",
#     data_files={
#         "train": TRAIN_FILE,
#         "validation": VAL_FILE,
#         "test": TEST_FILE
#     }
# )
#
# # -----------------------------
# # PARSE CoNLL FORMAT
# # -----------------------------
# def parse_conll(example):
#     tokens, tags = [], []
#     for line in example["text"].split("\n"):
#         if line.strip():
#             token, tag = line.split()
#             tokens.append(token)
#             tags.append(tag)
#     return {"tokens": tokens, "ner_tags": tags}
#
# dataset = dataset.map(parse_conll)
#
# # -----------------------------
# # TOKENIZER
# # -----------------------------
# tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
#
# # -----------------------------
# # TOKENIZE & ALIGN LABELS
# # -----------------------------
# def tokenize_and_align_labels(examples):
#     tokenized = tokenizer(
#         examples["tokens"],
#         truncation=True,
#         is_split_into_words=True,
#         padding=False
#     )
#
#     all_labels = []
#     for i in range(len(examples["tokens"])):
#         word_ids = tokenized.word_ids(batch_index=i)
#         label_ids = []
#         prev_word_idx = None
#         for word_idx in word_ids:
#             if word_idx is None:
#                 label_ids.append(-100)
#             elif word_idx != prev_word_idx:
#                 tag = examples["ner_tags"][i][word_idx]
#                 # safe mapping in case of unknown tag
#                 label_ids.append(label2id.get(tag, label2id["O"]))
#             else:
#                 label_ids.append(-100)
#             prev_word_idx = word_idx
#         all_labels.append(label_ids)
#
#     tokenized["labels"] = all_labels
#     return tokenized
#
#
#
# dataset = dataset.map(tokenize_and_align_labels, batched=True)
#
# # -----------------------------
# # LOAD MODEL
# # -----------------------------
# model = AutoModelForTokenClassification.from_pretrained(
#     MODEL_NAME,
#     num_labels=num_labels,
#     id2label=id2label,
#     label2id=label2id
# )
#
# # -----------------------------
# # TRAINING SETUP
# # -----------------------------
# training_args = TrainingArguments(
#     output_dir="./ontonotes_ner_model",
#     evaluation_strategy="epoch",
#     learning_rate=2e-5,
#     per_device_train_batch_size=16,
#     per_device_eval_batch_size=16,
#     num_train_epochs=3,
#     weight_decay=0.01,
#     logging_dir="./logs",
#     save_total_limit=2,
#     report_to="none"
# )
#
# trainer = Trainer(
#     model=model,
#     args=training_args,
#     train_dataset=dataset["train"],
#     eval_dataset=dataset["validation"],
#     tokenizer=tokenizer
# )
#
# # -----------------------------
# # TRAIN
# # -----------------------------
# trainer.train()
#
# # -----------------------------
# # SAVE MODEL
# # -----------------------------
# model.save_pretrained("./ontonotes_ner_model")
# tokenizer.save_pretrained("./ontonotes_ner_model")
#
# # -----------------------------
# # INFERENCE TEST
# # -----------------------------
# text = "I went to Ali daughter wedding and gave him a gold watch and 500 cash"
#
# inputs = tokenizer(text, return_tensors="pt")
# outputs = model(**inputs)
#
# predictions = outputs.logits.argmax(dim=-1).squeeze().tolist()
# tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"].squeeze())
#
# print("\n--- PREDICTIONS ---")
# for token, pred in zip(tokens, predictions):
#     print(f"{token:15} -> {id2label[pred]}")

import json
import tensorflow as tf
from transformers import (
	AutoTokenizer,
	# TFBertForTokenClassification,
	DataCollatorForTokenClassification
)
# from transformers import TFBertForTokenClassification
from transformers import TFAutoModelForTokenClassification, AutoTokenizer
from datasets import Dataset

# -----------------------------
# CONFIG
# -----------------------------
MODEL_NAME = "bert-base-cased"
MAX_LEN = 128
BATCH_SIZE = 16
EPOCHS = 3

# -----------------------------
# COCO-LIKE NER DATA FILES
# -----------------------------
TRAIN_FILE = "train.conll"  # your CoNLL-style file
VAL_FILE = "validation.conll"  # validation file
TEST_FILE = "test.conll"  # test file


# -----------------------------
# PARSE CONLL FILES
# -----------------------------
def parse_conll_file(filepath):
	sentences, labels = [], []
	sentence, label = [], []

	with open(filepath, "r", encoding="utf-8") as f:
		for line in f:
			line = line.strip()
			if not line:
				if sentence:
					sentences.append(sentence)
					labels.append(label)
					sentence, label = [], []
			else:
				parts = line.split()
				token, tag = parts[0], parts[1]
				sentence.append(token)
				label.append(tag)
		# last sentence
		if sentence:
			sentences.append(sentence)
			labels.append(label)
	return sentences, labels


train_sentences, train_labels = parse_conll_file(TRAIN_FILE)
val_sentences, val_labels = parse_conll_file(VAL_FILE)
test_sentences, test_labels = parse_conll_file(TEST_FILE)

# -----------------------------
# BUILD LABEL MAPPING
# -----------------------------
all_labels = set(tag for doc in train_labels for tag in doc)
label2id = {label: i for i, label in enumerate(sorted(all_labels))}
id2label = {i: label for label, i in label2id.items()}

print("Labels:", label2id)


# -----------------------------
# CREATE HUGGINGFACE DATASET
# -----------------------------
def build_dataset(sentences, labels):
	data = {"tokens": sentences, "ner_tags": labels}
	return Dataset.from_dict(data)


train_dataset = build_dataset(train_sentences, train_labels)
val_dataset = build_dataset(val_sentences, val_labels)
test_dataset = build_dataset(test_sentences, test_labels)

# -----------------------------
# TOKENIZER
# -----------------------------
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)


def tokenize_and_align_labels(examples):
	tokenized = tokenizer(
		examples["tokens"],
		truncation=True,
		is_split_into_words=True,
		padding="max_length",
		max_length=MAX_LEN
	)

	all_labels = []
	for i in range(len(examples["tokens"])):
		word_ids = tokenized.word_ids(batch_index=i)
		label_ids = []
		prev_word_idx = None
		for word_idx in word_ids:
			if word_idx is None:
				label_ids.append(-100)
			elif word_idx != prev_word_idx:
				tag = examples["ner_tags"][i][word_idx]
				label_ids.append(label2id.get(tag, label2id["O"]))
			else:
				label_ids.append(-100)
			prev_word_idx = word_idx
		all_labels.append(label_ids)

	tokenized["labels"] = all_labels
	return tokenized


train_dataset = train_dataset.map(tokenize_and_align_labels, batched=True)
val_dataset = val_dataset.map(tokenize_and_align_labels, batched=True)

# -----------------------------
# DATA COLLATOR
# -----------------------------
data_collator = DataCollatorForTokenClassification(tokenizer, return_tensors="tf")

tf_train_dataset = train_dataset.to_tf_dataset(
	columns=["input_ids", "attention_mask", "labels"],
	shuffle=True,
	batch_size=BATCH_SIZE,
	collate_fn=data_collator
)

tf_val_dataset = val_dataset.to_tf_dataset(
	columns=["input_ids", "attention_mask", "labels"],
	shuffle=False,
	batch_size=BATCH_SIZE,
	collate_fn=data_collator
)

# -----------------------------
# LOAD MODEL
# -----------------------------
model = TFBertForTokenClassification.from_pretrained(
	MODEL_NAME,
	num_labels=len(label2id),
	id2label=id2label,
	label2id=label2id
)

# -----------------------------
# COMPILE
# -----------------------------
optimizer = tf.keras.optimizers.Adam(learning_rate=3e-5)
loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
model.compile(optimizer=optimizer, loss=loss)

# -----------------------------
# TRAIN
# -----------------------------
model.fit(tf_train_dataset, validation_data=tf_val_dataset, epochs=EPOCHS)

# -----------------------------
# SAVE MODEL
# -----------------------------
model.save_pretrained("./ontonotes_ner_model_tf")
tokenizer.save_pretrained("./ontonotes_ner_model_tf")
print("TensorFlow model saved to ./ontonotes_ner_model_tf")

# -----------------------------
# TEST INFERENCE
# -----------------------------
test_sentence = "I went to Ali daughter wedding and gave him a gold watch and 500 cash"
inputs = tokenizer(test_sentence, return_tensors="tf")
outputs = model(inputs)
predictions = tf.argmax(outputs.logits, axis=-1).numpy()[0]
tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])

print("\n--- PREDICTIONS ---")
for token, pred in zip(tokens, predictions):
	print(f"{token:15} -> {id2label[pred]}")
