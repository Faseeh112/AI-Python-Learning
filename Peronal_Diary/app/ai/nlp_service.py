"""
NLP Service — Intent classification + Entity extraction.
Provider: SpaCy (NER) + custom intent classifier
Models:  spacy en_core_web_lg, custom Urdu model
"""


def classify_intent(text):
    # Classify into: store, query, update, delete, unknown
    # Uses fine-tuned classifier or rule-based patterns
    # Return { intent, confidence }
    pass


def extract_entities(text):
    # Extract: person names, amounts, dates, locations, items, categories
    # Uses SpaCy NER pipeline + custom entity rules
    # Return { persons: [], amounts: [], dates: [], locations: [],
    #          items: [], categories: [] }
    pass


def extract_triples(text):
    # Extract subject-predicate-object triples from text
    # Uses dependency parsing + relation extraction
    # Return [{ subject, predicate, object, confidence }]
    pass
