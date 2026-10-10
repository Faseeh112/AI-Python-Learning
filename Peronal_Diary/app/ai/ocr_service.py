"""
OCR Service — Optical Character Recognition for scanned documents.
Provider: Tesseract / Azure Form Recognizer
"""


def extract_pdf_text(pdf_path):
    # Try direct text extraction first (PyMuPDF/pdfplumber)
    # If scanned (no text layer) → run OCR via Tesseract
    # Return { text, page_count, word_count }
    pass


def extract_image_text(image_path):
    # Run OCR on image file
    # Return extracted text string
    pass
