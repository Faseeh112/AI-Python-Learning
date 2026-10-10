"""
NLP Queue Worker — ASYNC JOB
Process pending raw_text_log entries through NLP pipeline.
"""


def run():
    # Query raw_text_log WHERE is_processed = 0
    # For each unprocessed entry:
    #   call nlp_service.classify_intent(raw_text)
    #   call nlp_service.extract_entities(raw_text)
    #   call nlp_service.extract_triples(raw_text)
    #   create structured records (notes, transactions, etc.)
    #   set is_processed = 1
    # On failure: set error_msg, leave is_processed = 0
    # Log processing summary
    pass
