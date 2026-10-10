"""
LLM Service — Large Language Model for RAG queries and summarization.
Provider: OpenAI GPT-4 / Anthropic Claude API / local LLM
"""


def format_answer(question, context_data):
    # Build prompt with question + DB query results as context
    # Call LLM API for natural language response
    # Return formatted answer string
    pass


def summarize(text):
    # Summarize extracted document text
    # Return summary string (max 1000 chars)
    pass


def generate_sql(intent, entities):
    # Generate parameterized SQL from intent + entities
    # Validate SQL safety (no injection)
    # Return { sql, params }
    pass
