"""
Voice Routes — /api/voice
Audio input → STT → NLP → store/query pipeline.
"""
from flask import Blueprint, request
from app.utils.response_helpers import success_response, error_response

voice_bp = Blueprint('voice', __name__, url_prefix='/api/voice')


@voice_bp.route('', methods=['POST'])
def process_voice():
    # Purpose: Accept audio → Whisper STT → NLP intent/entity → route to store or query
    # Auth:    JWT required
    # Input:   multipart/form-data with audio file (wav/mp3/ogg/webm)
    # Flow:    audio → stt_service.transcribe() → nlp_service.classify_intent()
    #          → nlp_service.extract_entities() → decision engine → store/query
    # Calls:   voice_service.process_audio()
    # Returns: 200 with { transcript, intent, entities, result }
    pass


@voice_bp.route('/history', methods=['GET'])
def list_entries():
    # Purpose: List user voice entries (paginated)
    # Auth:    JWT required
    # Query:   ?page=&per_page=&date_from=&date_to=
    # Calls:   voice_service.get_entries()
    # Returns: 200 paginated
    pass


@voice_bp.route('/<int:voice_entry_id>', methods=['GET'])
def get_entry(voice_entry_id):
    # Purpose: Get voice entry with transcript, NER output, linked note, triples
    # Auth:    JWT required + ownership check
    # Calls:   voice_service.get_entry_detail()
    # Returns: 200 or 404
    pass


@voice_bp.route('/<int:voice_entry_id>', methods=['DELETE'])
def delete_entry(voice_entry_id):
    # Purpose: Soft-delete voice entry
    # Auth:    JWT required + ownership check
    # Calls:   voice_service.soft_delete_entry()
    # Returns: 200
    pass
