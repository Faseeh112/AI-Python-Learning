"""
Upload Processor — ASYNC JOB
Process pending file uploads through extraction pipeline.
"""


def run():
    # Query file_upload WHERE extraction_status = 'pending'
    # For each pending upload:
    #   set status = 'processing'
    #   based on file_type:
    #     pdf  → ocr_service.extract_pdf_text()
    #     docx → file_utils.extract_docx_text()
    #     xlsx/csv → file_utils.extract_tabular_data()
    #     jpg/png → ocr_service.extract_image_text()
    #     txt → read directly
    #   call nlp_service.extract_entities(extracted_text)
    #   call llm_service.summarize(extracted_text)
    #   create notes, transactions, documents, assets as found
    #   extract knowledge triples
    #   call sp_complete_upload equivalent with all counts
    # On failure: set status='failed', store extraction_error
    # Log processing summary
    pass
