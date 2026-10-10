"""
Upload Routes — /api/uploads
File upload with extraction pipeline tracking.
"""
from flask import Blueprint, request
from app.utils.response_helpers import success_response, error_response

upload_bp = Blueprint('uploads', __name__, url_prefix='/api/uploads')


@upload_bp.route('', methods=['POST'])
def upload_file():
    # Purpose: Accept file → register in DB → queue for extraction
    # Auth:    JWT required
    # Input:   multipart/form-data with file + optional notes_id
    # Flow:    receive → hash SHA-256 → store → insert file_upload (pending)
    #          → insert raw_text_log → queue async extraction
    # Calls:   upload_service.register_upload()
    # Returns: 201 with { upload_id, status: 'pending' }
    pass


@upload_bp.route('', methods=['GET'])
def list_uploads():
    # Purpose: List uploads with processing status
    # Auth:    JWT required
    # Query:   ?page=&per_page=&file_type=&extraction_status=
    # Calls:   upload_service.get_uploads()
    # Returns: 200 paginated
    pass


@upload_bp.route('/<int:upload_id>', methods=['GET'])
def get_upload(upload_id):
    # Purpose: Get upload detail with extraction results
    # Auth:    JWT required + ownership check
    # Calls:   upload_service.get_upload_detail()
    # Returns: 200 or 404
    pass


@upload_bp.route('/<int:upload_id>/download', methods=['GET'])
def download_file(upload_id):
    # Purpose: Serve original uploaded file
    # Auth:    JWT required + ownership check
    # Calls:   upload_service.get_file_path()
    # Returns: file stream with correct MIME type
    pass


@upload_bp.route('/<int:upload_id>', methods=['DELETE'])
def delete_upload(upload_id):
    # Purpose: Soft-delete upload record
    # Auth:    JWT required + ownership check
    # Calls:   upload_service.soft_delete_upload()
    # Returns: 200
    pass


@upload_bp.route('/<int:upload_id>/reprocess', methods=['POST'])
def reprocess(upload_id):
    # Purpose: Re-queue failed upload for extraction
    # Auth:    JWT required + ownership check
    # Calls:   upload_service.requeue_upload()
    # Returns: 200 with { status: 'pending' }
    pass


@upload_bp.route('/queue', methods=['GET'])
def get_queue():
    # Purpose: Pending/failed uploads (mirrors vw_upload_queue)
    # Auth:    JWT required
    # Calls:   upload_service.get_pending_uploads()
    # Returns: 200
    pass


@upload_bp.route('/summary', methods=['GET'])
def get_summary():
    # Purpose: Upload stats per user (mirrors vw_upload_summary)
    # Auth:    JWT required
    # Calls:   upload_service.get_upload_summary()
    # Returns: 200 with { total_files, pdfs, excels, processed, pending, ... }
    pass
