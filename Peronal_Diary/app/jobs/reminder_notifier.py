"""
Reminder Notifier — DAILY JOB
Send notifications for upcoming reminders.
"""


def run():
    # Query reminders where:
    #   is_done = False, is_active = True
    #   date_time - remind_before <= now
    # For each due reminder:
    #   send push notification via FCM
    #   send email if configured
    #   optionally generate TTS audio alert
    # Log delivery status
    pass
