import pyttsx3
from datetime import datetime
from flask import request, jsonify
from Visual_Impired_Diary.db import db
from Visual_Impired_Diary.Model.Reminders import Reminders
from datetime import date, time, datetime
from dateutil import parser


class ReminderController:

	@staticmethod
	def add_reminder():
		data = request.get_json()

		user_id = data.get("user_id")

		remind_time_str = data.get("reminder_time")
		remind_date_str = data.get("reminder_date")
		repeat_type = data.get("repeat_type")
		remind_content = data.get("remind_content")

		# -------- Validation --------
		if not all([user_id, remind_time_str, remind_date_str, repeat_type,remind_content]):
			return jsonify({"error": "Missing required fields (user_id, time, date, or repeat type)"}), 400

		try:
			remind_date = parser.parse(remind_date_str).date()

			remind_time = datetime.strptime(remind_time_str, '%H:%M').time()

			user_id = int(user_id)

		except ValueError as e:
			return jsonify({"error": f"Invalid date/time format: {e}"}), 400
		except Exception as e:
			return jsonify({"error": f"An unexpected error occurred during data processing: {e}"}), 500

		valid_repeat_types = ["On", "Off", "Daily", "Weekly", "Monthly"]
		if repeat_type not in valid_repeat_types:
			pass

		# -------- Create new reminder object --------
		try:
			new_reminder = Reminders(
				User_id=user_id,
				Remind_date=remind_date,
				Remind_time=remind_time,
				Repeat_type=repeat_type,
				Remind_content=remind_content,
				created_at=datetime.now()
			)

			db.session.add(new_reminder)
			db.session.commit()

			engine=pyttsx3.init()
			engine.say(f"Successfully Added Remainder of {remind_content} at Date {remind_date}")
			engine.runAndWait()

			return jsonify({
				"message": "Reminder set successfully",
				"reminder_id": new_reminder.Reminder_id
			}), 201

		except Exception as e:
			db.session.rollback()
			return jsonify({"error": f"Failed to save reminder: {e}"}), 500