# # from flask import request, jsonify
# # from Visual_Impired_Diary.db import db, app
# #
# # # IMPORT CONTROLLERS
# # from Visual_Impired_Diary.Controller.User import UserController
# # from Visual_Impired_Diary.Controller.Event import EventController
# # # --- ADD THIS IMPORT ---
# # from Visual_Impired_Diary.Controller.Reminders import ReminderController
# #
# # @app.route('/signup', methods=['POST'])
# # def signup():
# #     return UserController.signup()
# #
# # @app.route('/login', methods=['GET'])
# # def login_user():
# #     return UserController.login()
# #
# # @app.route('/addevent', methods=['POST'])
# # def add_event():
# #     return EventController.add_event()
# #
# #
# # # --- ADD THIS ROUTE FOR REMINDERS ---
# # @app.route('/reminder/add', methods=['POST'])
# # def add_reminder_route():
# #     # This calls the static method in your ReminderController
# #     return ReminderController.add_reminder()
# # # ------------------------------------
# #
# #
# # if __name__ == '__main__':
# #     with app.app_context():
# #         print("Note: Not creating tables (they already exist in database)")
# #         # db.create_all()  # COMMENT THIS OUT - tables already exist!
# #         print("Connected to existing database")
# #     app.run(debug=True)
#
# import urllib.parse
# import json
# from flask import Flask, jsonify, request
# from flask_sqlalchemy import SQLAlchemy
# from flask_cors import CORS
#
# app = Flask(__name__)
# CORS(app)  # Allows your Frontend (React) to talk to this Backend
#
# # --- DATABASE CONNECTION ---
# # UPDATE 'ADEEL\SQLEXPRESS' with your actual Server Name if different
# params = urllib.parse.quote_plus(
#     "DRIVER={ODBC Driver 17 for SQL Server};SERVER=ADEEL\SQLEXPRESS;DATABASE=Task;Trusted_Connection=yes;")
# app.config['SQLALCHEMY_DATABASE_URI'] = f"mssql+pyodbc:///?odbc_connect={params}"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
#
# # --- DATABASE MODEL (Creates the Table 'Name' for you) ---
# class Name(db.Model):
#     __tablename__ = 'Name'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(255), nullable=False)
#     gender = db.Column(db.String(50))
#     origin = db.Column(db.String(255))
#     meaning = db.Column(db.String(None))  # Maps to VARCHAR(MAX)
#
#
# # Create the table automatically
# with app.app_context():
#     db.create_all()
#
#
# # --- ROUTE 1: SAVE DATA (POST) ---
# @app.route('/add_name', methods=['POST'])
# def add_name():
#     data = request.json
#     try:
#         # Create a new object (row)
#         new_entry = Name(
#             name=data['name'],
#             gender=data['gender'],
#             origin=data['origin'],
#             meaning=data['meaning']
#         )
#         db.session.add(new_entry)
#         db.session.commit()
#         return jsonify({"message": "Data saved successfully to SQL!"})
#     except Exception as e:
#         return jsonify({"message": f"Error: {str(e)}"}), 500
#
#
# # --- ROUTE 2: GET DATA (GET) ---
# @app.route('/get_name', methods=['GET'])
# def get_name():
#     search_name = request.args.get('name')
#
#     # Search the database using SQLAlchemy syntax
#     user = Name.query.filter_by(name=search_name).first()
#
#     if user:
#         return jsonify({
#             "gender": user.gender,
#             "meaning": user.meaning
#         })
#     else:
#         return jsonify(None), 404
#
#
# if __name__ == '__main__':
#     app.run(debug=True, port=5000)
#
import json
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.engine import URL

app = Flask(__name__)
CORS(app) # Crucial for React to connect

# --- YOUR SPECIFIC DATABASE CONNECTION ---
connection_url = URL.create(
    drivername="mssql+pyodbc",
    username="sa",
    password="123",
    host="DESKTOP-58B8CB8\\VE_SERVER",
    database="Web_Api",
    query={
        "driver": "ODBC Driver 18 for SQL Server",
        "Encrypt": "no",
        "TrustServerCertificate": "yes"
    }
)

app.config['SQLALCHEMY_DATABASE_URI'] = connection_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- DATABASE MODEL ---
class Name(db.Model):
    __tablename__ = 'Name'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.String(50))
    origin = db.Column(db.String(255))
    meaning = db.Column(db.String(None)) # VARCHAR(MAX)

# Initialize table if it doesn't exist
with app.app_context():
    db.create_all()

# --- ROUTES ---

@app.route('/add_name', methods=['POST'])
def add_name():
    data = request.json
    try:
        new_entry = Name(
            name=data['name'],
            gender=data['gender'],
            origin=data['origin'],
            meaning=data['meaning']
        )
        db.session.add(new_entry)
        db.session.commit()
        return jsonify({"message": "Data saved successfully!"})
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"})

@app.route('/get_name', methods=['GET'])
def get_name():
    search_name = request.args.get('name')
    user = Name.query.filter_by(name=search_name).first()

    if user:
        return jsonify({
            "gender": user.gender,
            "meaning": user.meaning
        })
    else:
        return jsonify({"message": "Not found"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)