"""
Serializers — Model → JSON conversion helpers.
Uses marshmallow for consistent serialization across all endpoints.
"""


def serialize_user(user):
    # Convert User model to dict (exclude password_hash)
    # Include: user_id, name, email, language, timezone, is_active, created_at
    pass


def serialize_note(note, include_tags=False, include_persons=False):
    # Convert Notes model to dict
    # Optionally include nested tags[] and persons[]
    pass


def serialize_transaction(transaction, include_category=True, include_person=True):
    # Convert TransactionLog to dict
    # Optionally include nested category and person objects
    pass


def serialize_asset(asset, include_category=True):
    # Convert Asset to dict with category details
    pass


def serialize_voice_entry(entry, include_note=False):
    # Convert VoiceEntry to dict
    # Optionally include linked note
    pass


def serialize_upload(upload):
    # Convert FileUpload to dict with processing stats
    pass


def serialize_knowledge_triple(triple):
    # Convert KnowledgeTriple to dict
    # Include resolved entity names from subject_type/object_type
    pass


def serialize_paginated(query, page, per_page, serializer_fn):
    # Execute paginated SQLAlchemy query
    # Apply serializer_fn to each item
    # Return { items: [], meta: { page, per_page, total, total_pages } }
    pass
