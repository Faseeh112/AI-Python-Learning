"""
Document Expiry Checker — DAILY JOB
Alert users about documents expiring within 90 days.
"""


def run():
    # Query vw_expiring_docs equivalent:
    #   documents with expiry_date within 90 days
    # Group by user_id
    # For each user:
    #   send notification with expiring document list
    #   create reminder if not exists
    # Log count of alerts sent
    pass
