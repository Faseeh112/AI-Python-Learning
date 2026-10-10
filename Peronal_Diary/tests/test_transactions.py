"""
Transaction Tests
"""


class TestTransactions:
    def test_create_transaction(self):
        # POST /api/transactions → 201
        pass

    def test_create_transaction_negative_amount(self):
        # POST /api/transactions with amount < 0 → 400
        pass

    def test_list_by_category(self):
        # GET /api/transactions?category_id=1 → 200 filtered
        pass

    def test_list_by_direction(self):
        # GET /api/transactions?direction=given → 200 filtered
        pass

    def test_summary_by_category(self):
        # GET /api/transactions/summary?group_by=category → 200
        pass
