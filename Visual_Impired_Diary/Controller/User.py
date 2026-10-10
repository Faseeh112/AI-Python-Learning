import pyttsx3
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask import request, jsonify
# from sqlalchemy import func # Not needed for current methods
from Visual_Impired_Diary.db import db
from Visual_Impired_Diary.Model.User import User  # <-- make sure path is correct


class UserController:

	#   USER SIGNUP
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
			return jsonify({"error": "All fields are required"}), 400

		if password != confirm_password:
			return jsonify({"error": "Password and Confirm Password do not match"}), 400

		if agree != True:
			return jsonify({"error": "You must agree to the terms"}), 400

		existing = User.query.filter_by(Email=email).first()
		if existing:
			return jsonify({"error": "Email already registered"}), 400

		hashed_password = generate_password_hash(password, method='scrypt')

		# -------- Create new user --------
		new_user = User(
			Name=name,
			Email=email,
			Password=hashed_password,
			created_at=datetime.now()
		)

		db.session.add(new_user)
		db.session.commit()

		# Text-to-speech logic (Corrected for single string argument)
		try:
			engine = pyttsx3.init()
			engine.say(f"Hi User {name}, successfully signed up to Personal diary for Visually Impaired")
			engine.runAndWait()
		except Exception as e:
			print(f"Text-to-speech failed: {e}")
		# Do not fail the API call if TTS fails

		return jsonify({"message": "User registered successfully"}), 201

	@staticmethod
	def login():
		data = request.get_json()
		email = data.get("email")
		password = data.get("password")
		if not all([email, password]):
			return jsonify({"error": "Email and Password are required"}), 400

		user = User.query.filter_by(Email=email).first()

		if not user:
			return jsonify({"error": "Invalid email or password"}),

		if not check_password_hash(user.Password, password):
			return jsonify({"error": "Invalid email or password"}), 401  # 401 Unauthorized

		# Login successful

		# Text-to-speech logic (Corrected for single string argument and login message)
		try:
			engine = pyttsx3.init()
			engine.say(f"Hi {user.Name}, successfully loging to Personal diary for Visually Impaired")
			engine.runAndWait()
		except Exception as e:
			print(f"Text-to-speech failed: {e}")

		return jsonify({
			"message": "Login successful",
			"user_id": user.User_id,
			"name": user.Name,
			"email": user.Email
		}), 200