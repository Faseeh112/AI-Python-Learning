"""
File Utilities — file handling, hashing, MIME detection.
"""


def compute_sha256(file_path):
    # Read file in chunks
    # Compute SHA-256 hash
    # Return hash as bytes (32 bytes for VARBINARY(32))
    pass


def detect_mime_type(file_path):
    # Use python-magic or mimetypes module
    # Return MIME type string (e.g., 'application/pdf')
    pass


def get_file_size_kb(file_path):
    # Return file size in KB (integer)
    pass


def generate_secure_filename(original_filename):
    # Sanitize filename (remove special chars, add UUID prefix)
    # Return safe filename for storage
    pass


def extract_docx_text(file_path):
    # Extract plain text from .docx file using python-docx
    # Return extracted text string
    pass


def extract_tabular_data(file_path, file_type):
    # Extract data from xlsx/csv/tsv using openpyxl or pandas
    # Return { headers: [], rows: [], sheet_count, row_count }
    pass
