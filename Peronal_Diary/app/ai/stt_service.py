"""
STT Service — Speech-to-Text using OpenAI Whisper.
Input:  audio file path (wav/mp3/ogg/webm)
Output: { transcript, confidence, language, duration_sec }
Supports: Urdu + English multilingual
"""


def transcribe(audio_path, language_hint='auto'):
    # Load whisper model (cached singleton)
    # Transcribe audio file
    # Return { transcript, confidence, language, duration_sec }
    pass
