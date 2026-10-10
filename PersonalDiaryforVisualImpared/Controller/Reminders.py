import pyttsx3
from datetime import datetime
from flask import request, jsonify
from dateutil import parser
from PersonalDiaryforVisualImpared.db import (db)
from PersonalDiaryforVisualImpared.Model.Reminders import Reminders

class ReminderController:

    @staticmethod
    def add_reminder():
        data = request.get_json()

        # Get all inputs including content
        user_id = data.get("user_id")
        remind_time_str = data.get("reminder_time")
        remind_date_str = data.get("reminder_date")
        repeat_type = data.get("repeat_type")
        remind_content = data.get("remind_content")  # "Take medicine", etc.

        if not all([user_id, remind_time_str, remind_date_str, repeat_type, remind_content]):
            return jsonify({"error": "Missing fields. Please provide user_id, time, date, type, and content."}), 400

        try:
            remind_date = parser.parse(remind_date_str).date()
            remind_time = datetime.strptime(remind_time_str, '%H:%M').time()

            new_reminder = Reminders(
                User_id=int(user_id),
                Remind_date=remind_date,
                Remind_time=remind_time,
                Repeat_type=repeat_type,
                remind_content=remind_content,  # Saving the text
                created_at=datetime.now()
            )

            db.session.add(new_reminder)
            db.session.commit()

            # Voice Feedback
            try:
                engine = pyttsx3.init()
                engine.say(f"Reminder saved for: {remind_content}")
                engine.runAndWait()
            except:
                pass

            return jsonify({"message": "Reminder set successfully", "id": new_reminder.Reminder_id}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def update_reminder(reminder_id):
        data = request.get_json()
        reminder = Reminders.query.get(reminder_id)

        if not reminder:
            return jsonify({"error": "Reminder not found"}), 404

        try:
            # Update content if provided
            if "remind_content" in data:
                reminder.remind_content = data.get("remind_content")

            # Update date if provided
            if "reminder_date" in data:
                reminder.Remind_date = parser.parse(data.get("reminder_date")).date()

            # Update time if provided
            if "reminder_time" in data:
                reminder.Remind_time = datetime.strptime(data.get("reminder_time"), '%H:%M').time()

            db.session.commit()

            # Voice Feedback for the change
            try:
                engine = pyttsx3.init()
                engine.say(f"Updated. New content is: {reminder.remind_content}")
                engine.runAndWait()
            except:
                pass

            return jsonify({"message": "Update successful", "content": reminder.remind_content}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)})

    @staticmethod
    def get_reminders_sorted(user_id):
        # try:
        #     # Query the database, filter by user, and sort by Date then Time
        #     reminders = Reminders.query.filter_by(User_id=user_id) \
        #         .order_by(Reminders.Remind_date.asc(), Reminders.Remind_time.asc()) \
        #         .all()
        #
        #     if not reminders:
        #         return jsonify({"message": "No reminders found for this user"}), 404
        #
        #     # Convert the database objects into a list of dictionaries for JSON
        #     results = []
        #     for r in reminders:
        #         results.append({
        #             "id": r.Reminder_id,
        #             "content": r.remind_content,
        #             "date": r.Remind_date.strftime('%Y-%m-%d'),
        #             "time": r.Remind_time.strftime('%H:%M'),
        #             "type": r.Repeat_type
        #         })
        #
        #     return jsonify(results), 200
        # except Exception as e:
        #     return jsonify({"error": str(e)}), 500
        try:
            # 1. Get current moment
            now = datetime.now()
            current_date = now.date()
            current_time = now.time()

            # 2. Query all reminders for the user
            all_reminders = Reminders.query.filter_by(User_id=user_id).all()

            upcoming = []

            for r in all_reminders:
                # Normalize type to lowercase to handle "Daily" vs "daily"
                r_type = r.Repeat_type.lower() if r.Repeat_type else ""

                # LOGIC FOR 'DAILY'
                if r_type == 'daily':
                    # Even if the date is 2025-01-01, it repeats every day.
                    # We only show it if the TIME for TODAY hasn't passed yet.
                    if r.Remind_time > current_time:
                        upcoming.append(r)

                # LOGIC FOR 'ONCE'
                elif r_type == 'once':
                    # Condition A: The date is in the future
                    if r.Remind_date > current_date:
                        upcoming.append(r)
                    # Condition B: The date is today, but the time is still coming up
                    elif r.Remind_date == current_date and r.Remind_time > current_time:
                        upcoming.append(r)

            # 3. Sort the list so the nearest reminder is at the top
            # We sort by Time only for Daily, and Date/Time for Once
            upcoming.sort(
                key=lambda x: (x.Remind_date if x.Repeat_type.lower() == 'once' else current_date, x.Remind_time))

            # 4. Format for JSON
            results = []
            for r in upcoming:
                results.append({
                    "id": r.Reminder_id,
                    "content": r.remind_content if r.remind_content else "No Title",
                    "date": r.Remind_date.strftime('%Y-%m-%d'),
                    "time": r.Remind_time.strftime('%H:%M'),
                    "type": r.Repeat_type
                })

            return jsonify(results), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def delete_reminder(reminder_id):
        try:
            # 1. Find the reminder by its ID
            reminder = Reminders.query.get(reminder_id)

            if not reminder:
                return jsonify({"error": f"Reminder with ID {reminder_id} not found"}), 404

            # 2. Capture content for voice feedback before deleting
            content_name = reminder.remind_content if reminder.remind_content else "Unnamed reminder"

            # 3. Delete from database
            db.session.delete(reminder)
            db.session.commit()

            # Voice Feedback (Optional)
            # try:
            #     engine = pyttsx3.init()
            #     engine.say(f"Deleted reminder for {content_name}")
            #     engine.runAndWait()
            # except:
            #     pass

            return jsonify({
                "message": f"Reminder '{content_name}' deleted successfully",
                "id": reminder_id,
                "status": "Success"
            }), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500