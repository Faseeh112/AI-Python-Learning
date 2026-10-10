"""
Query Routes — /api/query
Natural-language question → NLP → dynamic SQL → LLM formatted answer.
"""
from flask import Blueprint, request
from app.utils.response_helpers import success_response, error_response

query_bp = Blueprint('query', __name__, url_prefix='/api/query')


@query_bp.route('', methods=['POST'])
def ask_question():
    # Purpose: Accept text question → NLP pipeline → answer
    # Auth:    JWT required
    # Input:   { question }
    # Flow:    text → nlp_service.classify_intent() → nlp_service.extract_entities()
    #          → similarity_service.resolve_entities() → build dynamic SQL
    #          → execute parameterized query → llm_service.format_answer()
    # Calls:   query_service.process_text_query()
    # Returns: 200 with { answer, sources, confidence }
    pass


@query_bp.route('/voice', methods=['POST'])
def voice_query():
    # Purpose: Accept audio question → STT → same pipeline → TTS response
    # Auth:    JWT required
    # Input:   multipart/form-data with audio file
    # Flow:    audio → stt_service.transcribe() → process_text_query()
    #          → tts_service.synthesize() → audio response
    # Calls:   query_service.process_voice_query()
    # Returns: 200 with { answer, audio_response_url }
    pass
