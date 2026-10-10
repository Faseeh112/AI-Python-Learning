import pyttsx3
from datetime import datetime
from flask import request, jsonify
from PersonalDiaryforVisualImpared.db import db
from PersonalDiaryforVisualImpared.Model.Detail_event import Detail_event
from PersonalDiaryforVisualImpared.Model.Event import Event
from PersonalDiaryforVisualImpared.Model.Attend import Attend


class DetailEventController:

    @staticmethod
    def add_detail_event():
        data = request.get_json()

        user_id = data.get("user_id")
        event_id = data.get("event_id")  # This identifies WHICH event to increment
        title = data.get("title")
        context = data.get("context")
        trans_type = data.get("transaction_type")
        trans_val = data.get("transaction")
        date_str = data.get("date")

        if not all([user_id, event_id, title]):
            return jsonify({"error": "Missing user_id, event_id, or title"})

        try:
            # 1. Handle the Detail Event entry
            parsed_date = None
            if date_str:
                parsed_date = datetime.strptime(date_str, '%Y-%m-%d').date()

            new_detail = Detail_event(
                Title=title,
                Context=context,
                Transaction_Type=trans_type,
                Date=parsed_date,
                Transaction=trans_val,
                created_at=datetime.now()
            )
            db.session.add(new_detail)
            db.session.flush()  # Gets the ID for the next step

            # 2. Link in the Attend table
            new_attend = Attend(
                User_id=user_id,
                Event_id=event_id,
                Detail_event_id=new_detail.Detail_event_id
            )
            db.session.add(new_attend)

            # 3. SPECIFIC INCREMENT LOGIC
            # We find the specific event category the user chose
            target_event = Event.query.get(event_id)

            if target_event:
                # Convert current string count to int, default to 0 if empty/null
                current_count = 0
                if target_event.Total_event and target_event.Total_event.isdigit():
                    current_count = int(target_event.Total_event)

                # Increment and save back as a string
                target_event.Total_event = str(current_count + 1)
            else:
                db.session.rollback()
                return jsonify({"error": f"Event ID {event_id} not found"})

            # 4. Finalize the transaction
            db.session.commit()

            # Voice Feedback
            # try:
            #     engine = pyttsx3.init()
            #     engine.say(
            #         f"Added {title} to {target_event.Name}")
            #     engine.runAndWait()
            # except:
            #     pass

            return jsonify({
                "message": "Record saved and event counter incremented",
                "event_name": target_event.Name,
                "total_count": target_event.Total_event
            })

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)})

    @staticmethod
    def update_detail_event(detail_id):
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON payload received"}), 400

        # 1. Find the existing detail record
        detail = Detail_event.query.get(detail_id)
        if not detail:
            return jsonify({"error": f"Detail event with ID {detail_id} not found"}), 404

        try:
            # 2. Update fields if they are provided in the JSON body
            # .get(key, default) ensures we keep old data if the new field isn't sent
            detail.Title = data.get("title", detail.Title)
            detail.Context = data.get("context", detail.Context)
            detail.Transaction_Type = data.get("transaction_type", detail.Transaction_Type)
            detail.Transaction = data.get("transaction", detail.Transaction)

            if "date" in data:
                detail.Date = datetime.strptime(data.get("date"), '%Y-%m-%d').date()

            # 3. Save changes
            db.session.commit()

            # 4. Return flat structure
            return jsonify({
                "message": "Detail updated successfully",
                "Detail_event_id": detail.Detail_event_id,
                "title": detail.Title,
                "context": detail.Context,
                "transaction": detail.Transaction,
                "status": "Success"
            }), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def delete_detail_event(detail_id):
        try:
            # 1. Find the detail record
            detail = Detail_event.query.get(detail_id)
            if not detail:
                return jsonify({"error": f"Detail event with ID {detail_id} not found"}), 404

            # 2. Find the link in the Attend table to get the Event_id
            attend_record = Attend.query.filter_by(Detail_event_id=detail_id).first()

            if attend_record:
                # 3. Decrement the counter in the Event table
                target_event = Event.query.get(attend_record.Event_id)
                if target_event:
                    current_count = 0
                    if target_event.Total_event and target_event.Total_event.isdigit():
                        current_count = int(target_event.Total_event)

                    # Ensure the count doesn't go below zero
                    new_count = max(0, current_count - 1)
                    target_event.Total_event = str(new_count)

                # 4. Delete the link in the Attend table
                db.session.delete(attend_record)

            # 5. Delete the actual Detail Event
            db.session.delete(detail)

            # 6. Finalize the transaction
            db.session.commit()

            return jsonify({
                "message": f"Successfully deleted '{detail.Title}' and updated event counter",
                "status": "Success"
            }), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500