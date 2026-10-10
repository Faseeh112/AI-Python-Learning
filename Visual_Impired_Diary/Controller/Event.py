from datetime import datetime
from flask import request, jsonify
from Visual_Impired_Diary.db import db
from Visual_Impired_Diary.Model.Event import Event  #
# Import the Event model
import pyttsx3

class EventController:
	@staticmethod
	def add_event():
		data = request.get_json()

		event_name = data.get("name")

		if not event_name:
			return jsonify({"error": "Event name is required"}), 400

		if len(event_name) > 150:  # Matches Event.Name column size
			return jsonify({"error": "Event name cannot exceed 150 characters"}), 400

		# Optional: Check if the event category already exists to avoid duplicates
		existing_event = Event.query.filter_by(Name=event_name).first()
		if existing_event:
			return jsonify({"error": f"Event category '{event_name}' already exists."}), 400

		# -------- Create new event category object --------
		try:
			new_event = Event(
				Name=event_name,
			)

			db.session.add(new_event)
			db.session.commit()

			try:
				engine = pyttsx3.init()
				engine.say(f"Successfully added event {event_name}")
				engine.runAndWait()
			except Exception as e:
				print(f"Text-to-speech failed: {e}")

			return jsonify({
				"message": "Event category added successfully",
				"event_id": new_event.Event_id
			}), 201

		except Exception as e:
			db.session.rollback()
			return jsonify({"error": f"Failed to save event category: {e}"}), 500