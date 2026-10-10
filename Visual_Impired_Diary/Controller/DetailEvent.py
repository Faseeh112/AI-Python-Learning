from datetime import datetime
from flask import request, jsonify
from Visual_Impired_Diary.db import db
from Visual_Impired_Diary.Model.DetailEvent import DetailEvent  # Import the DetailEvent model
from Visual_Impired_Diary.Model.Event import Event  # Import Event model for lookup
from dateutil import parser


import pyttsx3 # Uncomment if text-to-speech is needed here

class DetailEventController:

	@staticmethod
	def add_event_note():
		"""
		Handles creation of a new detailed event note (DetailEvent model).
		Data must include the Event_id of the category this note belongs to.
		"""
		data = request.get_json()

		event_id_str = data.get("event_id")  # Must be provided to link the note (e.g., to 'Wedding')
		title = data.get("title")
		date_str = data.get("date")
		transaction = data.get("transaction")
		transaction_type = data.get("transaction_type")
		context = data.get("description")  # Note: UI uses 'Description', model uses 'Context'

		# -------- Validation --------
		if not all([event_id_str, title, date_str, transaction, transaction_type, context]):
			return jsonify(
				{"error": "Missing required fields (event_id, title, date, transaction, type, or description)"}), 400

		# 1. Type Conversion and Date/Time Parsing
		try:
			event_id = int(event_id_str)

			# Convert date string to Python date object
			# Note: Assumes date is in a format like 'MM-DD-YYYY' as seen in UI
			event_date = parser.parse(date_str).date()

		except ValueError as e:
			return jsonify({"error": f"Invalid format for Event ID or Date: {e}"}), 400
		except Exception as e:
			return jsonify({"error": f"An unexpected error occurred during data parsing: {e}"}), 500

		# 2. Check if the parent Event Category exists
		parent_event = Event.query.get(event_id)
		if not parent_event:
			return jsonify({"error": f"Event Category with ID {event_id} does not exist."}), 404

		# -------- Create new DetailEvent object --------
		try:
			new_detail_event = DetailEvent(
				Event_id=event_id,
				Title=title,
				Context=context,  # The 'Description' field in the UI maps to 'Context' in the model
				Date=event_date,
				_Transaction=transaction,
				Transaction_Type=transaction_type,
				created_at=datetime.now()
			)

			db.session.add(new_detail_event)

			# Optional: Update the Total_event count on the parent Event category
			# parent_event.Total_event = (parent_event.Total_event or 0) + 1

			db.session.commit()

			# Optional: Add text-to-speech confirmation here

			return jsonify({
				"message": f"Note added successfully to category '{parent_event.Name}'",
				"detail_id": new_detail_event.Detail_id
			}), 201

		except Exception as e:
			db.session.rollback()
			return jsonify({"error": f"Failed to save event note: {e}"}), 500