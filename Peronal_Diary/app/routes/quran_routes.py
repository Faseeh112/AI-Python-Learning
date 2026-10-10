"""
Quran Routes — /api/quran
Surah listing, audio streaming, and listening progress.
"""
from flask import Blueprint, request
from app.utils.response_helpers import success_response, error_response

quran_bp = Blueprint('quran', __name__, url_prefix='/api/quran')


@quran_bp.route('/surahs', methods=['GET'])
def list_surahs():
    # Purpose: List all surahs with metadata
    # Auth:    JWT required
    # Calls:   quran_service.get_surahs()
    # Returns: 200 with surah list
    pass


@quran_bp.route('/surahs/<int:surah_id>/stream', methods=['GET'])
def stream_audio(surah_id):
    # Purpose: Stream surah audio file
    # Auth:    JWT required
    # Calls:   quran_service.get_audio_path()
    # Returns: audio file stream
    pass


@quran_bp.route('/listen', methods=['POST'])
def log_listen():
    # Purpose: Log listening session (progress, completion)
    # Auth:    JWT required
    # Input:   { surah_id, progress_sec, is_completed, device, session_id }
    # Calls:   quran_service.log_listen()
    # Returns: 201
    pass


@quran_bp.route('/history', methods=['GET'])
def get_history():
    # Purpose: User's listening history and progress
    # Auth:    JWT required
    # Query:   ?page=&per_page=
    # Calls:   quran_service.get_listen_history()
    # Returns: 200 paginated
    pass
