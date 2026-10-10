import json
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

# ==============================
# 🔹 YOUR LOCAL MODEL PATH
# ==============================
LOCAL_MODEL_PATH = r"C:/Users/Faseeh-Ur-Rehman/PycharmProjects/PythonProject/models/custom_ner_model"

# ==============================
# 🔹 Load Model (Offline)
# ==============================
tokenizer = AutoTokenizer.from_pretrained(LOCAL_MODEL_PATH)
model = AutoModelForTokenClassification.from_pretrained(LOCAL_MODEL_PATH)

ner_pipeline = pipeline(
    "ner",
    model=model,
    tokenizer=tokenizer,
    aggregation_strategy="simple"
)

# ==============================
# 🔹 Entity Extraction Function
# ==============================
def extract_entities(text):
    results = ner_pipeline(text)

    structured_output = {}

    for entity in results:
        label = entity["entity_group"]
        value = entity["word"]

        if label not in structured_output:
            structured_output[label] = []

        if value not in structured_output[label]:
            structured_output[label].append(value)

    return structured_output


# ==============================
# 🔹 Main Loop
# ==============================
if __name__ == "__main__":
    print("✅ Custom Offline NER System Ready")
    print("Type 'exit' to stop.\n")

    while True:
        text = input("Enter sentence: ")

        if text.lower() == "exit":
            break

        output = extract_entities(text)

        print("\n🔹 Extracted Entities:")
        print(json.dumps(output, indent=2))
        print("\n" + "="*50 + "\n")