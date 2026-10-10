import pyttsx3
from datetime import datetime
from flask import request, jsonify
from PersonalDiaryforVisualImpared.db import db
from PersonalDiaryforVisualImpared.Model.Detail_event import Detail_event
from PersonalDiaryforVisualImpared.Model.Attend import Attend
# Corrected import path using the project name and snake_case filename
from PersonalDiaryforVisualImpared.Model.Event import Event

class EventController:
    @staticmethod
    def add_event():
        data = request.get_json()

        # Match the ERD attribute name 'Name'
        event_name = data.get("name")

        if not event_name:
            return jsonify({"error": "Event name is required"})

        # Matches typical string size constraints for the Event.Name column
        if len(event_name) > 255:
            return jsonify({"error": "Event name cannot exceed 255 characters"})

        # Check if the event category already exists to avoid duplicates
        existing_event = Event.query.filter_by(Name=event_name).first()
        if existing_event:
            return jsonify({"error": f"Event category '{event_name}' already exists."})

        # -------- Create new event category object --------
        try:
            new_event = Event(
                Name=event_name,
                # Note: 'Total_event' is also in the ERD if you need to initialize it
                Total_event = "0"
            )

            db.session.add(new_event)
            db.session.commit()

            # Text-to-speech logic for accessibility
            # try:
            #     engine = pyttsx3.init()
            #     engine.say(f"Successfully added event {event_name}")
            #     engine.runAndWait()
            # except Exception as e:
            #     print(f"Text-to-speech failed: {e}")

            return jsonify({
                "message": "Event category added successfully",
                "event_id": new_event.Event_id # Match ERD attribute
            })

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": f"Failed to save event category: {str(e)}"})

    @staticmethod
    def update_event(event_id):
        # 1. Get the JSON data
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        new_name = data.get("name")
        if not new_name:
            return jsonify({"error": "New event name is required"}), 400

        # 2. Find the existing event by ID
        event_to_update = Event.query.get(event_id)
        if not event_to_update:
            return jsonify({"error": f"Event with ID {event_id} not found"}), 404

        try:
            # 3. Check for duplicates (Make sure the new name isn't taken by another ID)
            existing_event = Event.query.filter_by(Name=new_name).first()
            if existing_event and existing_event.Event_id != event_id:
                return jsonify({"error": f"Another event category named '{new_name}' already exists."}), 400

            # 4. Perform the update
            event_to_update.Name = new_name
            db.session.commit()

            # 5. Return a flat structure
            return jsonify({
                "message": "Event updated successfully",
                "event_id": event_to_update.Event_id,
                "name": event_to_update.Name,
                "status": "Success"
            }), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": f"Failed to update event: {str(e)}"}), 500

    @staticmethod
    def delete_event(event_id):
        try:
            # 1. Find the event
            target_event = Event.query.get(event_id)
            if not target_event:
                return jsonify({"error": f"Event category with ID {event_id} not found"}), 404

            # 2. Find all links in the 'Attend' table for this event
            attend_records = Attend.query.filter_by(Event_id=event_id).all()

            for record in attend_records:
                # 3. Find and delete the actual Detail_event record first
                detail = Detail_event.query.get(record.Detail_event_id)
                if detail:
                    db.session.delete(detail)

                # 4. Delete the link in the Attend table
                db.session.delete(record)

            # 5. Finally, delete the main Event category
            db.session.delete(target_event)

            # 6. Finalize all deletions
            db.session.commit()

            return jsonify({
                "message": f"Successfully deleted category '{target_event.Name}' and all its related records.",
                "status": "Success"
            }), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500