import pyttsx3
from datetime import datetime
from flask import request, jsonify
from PersonalDiaryforVisualImpared.db import db
from PersonalDiaryforVisualImpared.Model.Play import Play
from PersonalDiaryforVisualImpared.Model.Quran_Audio import Quran_Audio


class PlayController:

    @staticmethod
    def add_play_audio():
        data = request.get_json()

        user_id = data.get("user_id")
        audio_id = data.get("audio_id")
        repeat = data.get("repeat_type", "Once")

        # User's requested timing
        requested_date = data.get("play_date")  # Format: "2025-12-20"
        requested_time = data.get("play_time")  # Format: "14:00:00"

        if not all([user_id, audio_id, requested_date, requested_time]):
            return jsonify({"error": "user_id, audio_id, date, and time are required"})

        try:
            # 1. Fetch Audio details
            audio = Quran_Audio.query.get(audio_id)
            if not audio:
                return jsonify({"error": "Surah not found"}), 404

            # 2. Parse the strings into Python date/time objects
            p_date = datetime.strptime(requested_date, '%Y-%m-%d').date()
            p_time = datetime.strptime(requested_time, '%H:%M:%S').time()

            # 3. Create the Scheduled Record
            new_play = Play(
                User_id=user_id,
                Audio_id=audio_id,
                Play_date=p_date,
                Play_time=p_time,
                Repeat_type=repeat
                # created_at will show WHEN the request was made
            )

            db.session.add(new_play)
            db.session.commit()

            # 4. Voice Confirmation
            # try:
            #     engine = pyttsx3.init()
            #     # Converting 14:00 to 2:00 PM for natural speech
            #     friendly_time = p_time.strftime("%I:%M %p")
            #     engine.say(f"Scheduled Surah {audio.Surah_name} for {requested_date} at {friendly_time}.")
            #     engine.runAndWait()
            # except:
            #     pass

            return jsonify({
                "message": "Playback scheduled",
                "surah": audio.Surah_name,
                "scheduled_for": f"{requested_date} {requested_time}"
            })

        except ValueError:
            return jsonify({"error": "Invalid date or time format"}), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)})

    @staticmethod
    def update_play_audio(play_id):
        # 1. Get JSON data
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON payload received"}), 400

        # 2. Find the scheduled record
        play_record = Play.query.get(play_id)
        if not play_record:
            return jsonify({"error": f"Scheduled playback ID {play_id} not found"}), 404

        try:
            # 3. Update date if provided
            if "play_date" in data:
                play_record.Play_date = datetime.strptime(data.get("play_date"), '%Y-%m-%d').date()

            # 4. Update time if provided
            if "play_time" in data:
                play_record.Play_time = datetime.strptime(data.get("play_time"), '%H:%M:%S').time()

            # 5. Update repeat type if provided
            if "repeat_type" in data:
                play_record.Repeat_type = data.get("repeat_type")

            # 6. Update audio_id if the user wants to change the Surah
            if "audio_id" in data:
                play_record.Audio_id = data.get("audio_id")

            db.session.commit()

            # 7. Return flat structure response
            return jsonify({
                "message": "Playback schedule updated successfully",
                "play_id": play_record.Play_id,
                "play_date": play_record.Play_date.strftime('%Y-%m-%d'),
                "play_time": play_record.Play_time.strftime('%H:%M:%S'),
                "repeat_type": play_record.Repeat_type,
                "status": "Success"
            }), 200

        except ValueError:
            return jsonify({"error": "Invalid date or time format. Use YYYY-MM-DD and HH:MM:SS"}), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def delete_play_audio(play_id):
        try:
            # 1. Find the playback record by ID
            play_record = Play.query.get(play_id)

            if not play_record:
                return jsonify({"error": f"Scheduled playback with ID {play_id} not found"}), 404

            # 2. Delete the record
            db.session.delete(play_record)
            db.session.commit()

            # 3. Return a flat structure
            return jsonify({
                "message": "Scheduled playback canceled successfully",
                "play_id": play_id,
                "status": "Success"
            }), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500