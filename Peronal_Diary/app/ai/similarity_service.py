"""
Similarity Service — Semantic search and fuzzy entity matching.
Provider: Sentence-Transformers (all-MiniLM-L6-v2)
"""


def match_category(text, categories_list):
    # Encode text and category names with sentence transformer
    # Cosine similarity ranking
    # Return best matching category_id
    pass


def match_person(name, user_persons_list):
    # Fuzzy match person name against user's contacts
    # Return best matching person_id or None
    pass


def semantic_search(query, documents_list, top_k=5):
    # Encode query and document texts
    # Return top_k most similar documents with scores
    pass
