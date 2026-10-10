"""
Notes Tests
"""


class TestNotes:
    def test_create_note(self):
        # POST /api/notes → 201
        pass

    def test_list_notes_paginated(self):
        # GET /api/notes?page=1&per_page=10 → 200 with meta
        pass

    def test_add_tags_to_note(self):
        # POST /api/notes/<id>/tags → 200
        pass

    def test_link_person_to_note(self):
        # POST /api/notes/<id>/persons → 200
        pass

    def test_search_notes(self):
        # GET /api/notes/search?q=keyword → 200
        pass

    def test_delete_note_soft(self):
        # DELETE /api/notes/<id> → 200, is_active = False
        pass

    def test_ownership_check(self):
        # GET /api/notes/<other_user_id> → 403
        pass
