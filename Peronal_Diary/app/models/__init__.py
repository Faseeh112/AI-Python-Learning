"""
Import all models so Alembic can discover them for migrations.
"""
from app.models.currency import Currency
from app.models.user import User
from app.models.category import Category
from app.models.person import Person
from app.models.location import Location
from app.models.tag import Tag
from app.models.note_tag import note_tag
from app.models.note_person import NotePerson
from app.models.notes import Notes
from app.models.event import Event
from app.models.reminder import Reminder
from app.models.attachment import Attachment
from app.models.item import Item
from app.models.document import Document
from app.models.raw_text_log import RawTextLog
from app.models.voice_entry import VoiceEntry
from app.models.transaction_log import TransactionLog
from app.models.asset import Asset
from app.models.file_upload import FileUpload
from app.models.quran_audio import QuranAudio
from app.models.user_quran_listen import UserQuranListen
from app.models.knowledge_triple import KnowledgeTriple
