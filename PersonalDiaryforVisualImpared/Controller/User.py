
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask import request, jsonify
from PersonalDiaryforVisualImpared.db import db
# Corrected import path using the project name and snake_case filename
from PersonalDiaryforVisualImpared.Model.User import User


class UserController:

    # USER SIGNUP
    @staticmethod
    def signup():
        data = request.get_json()

        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        confirm_password = data.get("confirm_password")
        agree = data.get("agree")  # checkbox value True/False

        # -------- Validation --------
        if not all([name, email, password, confirm_password]):
            return jsonify({"error": "All fields are required"})

        if password != confirm_password:
            return jsonify({"error": "Password and Confirm Password do not match"})

        if agree != True:
            return jsonify({"error": "You must agree to the terms"})

        # Note: Email is capitalized in your ERD
        existing = User.query.filter_by(Email=email).first()
        if existing:
            return jsonify({"error": "Email already registered"})

        hashed_password = generate_password_hash(password, method='scrypt')

        # -------- Create new user --------
        # Columns match your ERD: Name, Email, Password, created_at
        new_user = User(
            Name=name,
            Email=email,
            Password=hashed_password,
            created_at=datetime.now()
        )

        db.session.add(new_user)
        db.session.commit()

        # Text-to-speech logic
        # try:
        #     engine = pyttsx3.init()
        #     engine.say(f"Hi User {name}, successfully signed up to Personal diary for Visually Impaired")
        #     engine.runAndWait()
        # except Exception as e:
        #     print(f"Text-to-speech failed: {e}")

        return jsonify({"message": "User registered successfully"})

    @staticmethod
    def login():
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        if not all([email, password]):
            return jsonify({"error": "Email and Password are required"})

        user = User.query.filter_by(Email=email).first()

        if not user:
            return jsonify({"error": "Invalid email or password"})

        if not check_password_hash(user.Password, password):
            return jsonify({"error": "Invalid email or password"})

            # Login successful logic
        # try:
        #     engine = pyttsx3.init()
        #     engine.say(f"Hi {user.Name}, successfully logging into Personal diary for Visually Impaired")
        #     engine.runAndWait()
        # except Exception as e:
        #     print(f"Text-to-speech failed: {e}")

        return jsonify({
            "message": "Login successful",
            "user_id": user.User_id,  # Match ERD attribute
            "name": user.Name,
            "email": user.Email
        })

    @staticmethod
    def change_password(user_id):
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        old_password = data.get("old_password")
        new_password = data.get("new_password")
        confirm_password = data.get("confirm_password")

        # 1. Validation
        if not all([old_password, new_password, confirm_password]):
            return jsonify({"error": "Current password and new passwords are required"}), 400

        if new_password != confirm_password:
            return jsonify({"error": "New passwords do not match"}), 400

        # 2. Find the user
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        # 3. Verify Old Password
        if not check_password_hash(user.Password, old_password):
            return jsonify({"error": "Incorrect current password"}), 401

        try:
            # 4. Hash and Save new password
            user.Password = generate_password_hash(new_password, method='scrypt')
            db.session.commit()

            return jsonify({
                "message": "Password changed successfully",
                "status": "Success"
            }), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500