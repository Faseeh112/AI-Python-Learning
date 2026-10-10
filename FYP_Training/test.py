# from flask import Flask, request, jsonify
#
# app = Flask(__name__)
#
# @app.route('/register', methods=['POST'])
# def register():
#     data = request.get_json()
#     return jsonify({"msg": "Received", "data": data})
#
# if __name__ == "__main__":
#     print("Routes:", app.url_map)
#     app.run(debug=True)

from flask import Flask, request, jsonify
from FYP_Training.Controllers.Customer import CustomerController
from FYP_Training.db import app, db
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text

# --- Customer routes ---

@app.route('/register', methods=['POST'])
def register_customer():
    return CustomerController.register()

@app.route('/profile', methods=['GET'])
def view_profile():
    return CustomerController.get_profile()

@app.route('/profile', methods=['PUT'])
def update_profile():
    data = request.get_json()
    mail = data.get('email')
    pas = data.get('password')
    name = data.get('name')
    return CustomerController.update_profile(mail, pas, name)

@app.route('/profile/password', methods=['PUT'])
def change_password():
    data = request.get_json()
    mail = data.get('email')
    pas = data.get('password')
    newpas = data.get('new_password')
    return CustomerController.change_password(mail, pas, newpas)

@app.route('/account', methods=['DELETE'])
def delete_account():
    data = request.get_json()
    mail = data.get('email')
    pas = data.get('password')
    return CustomerController.delete_account(mail, pas)

# You can add other routes (products, cart, orders) similarly.

# --- App runner with DB check ---

if __name__ == '__main__':
    with app.app_context():
        try:
            db.session.execute(text('SELECT 1'))
            print("✅ Database connection established successfully.")
        except SQLAlchemyError as e:
            print("❌ Database connection failed:", e)

        db.create_all()
        print("✅ Tables created successfully (or already exist).")

    app.run(debug=True)
