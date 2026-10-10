# intent_predict.py
def get_intent(text):
    """
    Dummy intent detection based on keywords.
    Returns one of: reminder, event, query_audio, item_location, attachment, ai_query
    """
    text = text.lower()

    if any(word in text for word in ["remind", "reminder", "remember"]):
        return "reminder"
    elif any(word in text for word in ["meeting", "event", "schedule"]):
        return "event"
    elif any(word in text for word in ["play", "music", "song", "audio"]):
        return "query_audio"
    elif any(word in text for word in ["where", "location", "find"]):
        return "item_location"
    elif any(word in text for word in ["attach", "attachment", "file"]):
        return "attachment"
    elif any(word in text for word in ["ask", "question", "ai", "query"]):
        return "ai_query"
    else:
        return "unknown"
