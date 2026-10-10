# # from flask import Flask, request, jsonify
# # from flask_cors import CORS
# # import pyodbc
# # from datetime import datetime, timedelta
#
# # app = Flask(__name__)
# # CORS(app)
# # DB_CONFIG = (
# #     r"DRIVER={ODBC Driver 17 for SQL Server};"
# #     r"SERVER=FARQULEET\SQLEXPRESS;"
# #     r"DATABASE=Polling_SystemDB;"
# #     r"UID=sa;"
# #     r"PWD=123;"
# #     r"Encrypt=no;"
# #     r"TrustServerCertificate=yes;"
# # )
#
# # def get_db_connection():
# #     """Establish database connection"""
# #     conn_str = f"DRIVER={{{DB_CONFIG['driver']}}};SERVER={DB_CONFIG['server']};DATABASE={DB_CONFIG['database']};UID={DB_CONFIG['uid']};PWD={DB_CONFIG['pwd']}"
# #     return pyodbc.connect(conn_str)
#
#
# # def verify_admin(arid):
# #     """Verify if user is admin"""
# #     conn = None
# #     try:
# #         conn = get_db_connection()
# #         cursor = conn.cursor()
# #         cursor.execute("SELECT role FROM Users WHERE arid_no = ?", (arid,))
# #         result = cursor.fetchone()
# #         if result:
# #             role = str(result[0]).strip().lower()
# #             return role == 'admin'
# #         return False
# #     except Exception as e:
# #         print(f"Admin verification error: {str(e)}")
# #         return False
# #     finally:
# #         if conn:
# #             conn.close()
# # @app.route('/login', methods=['POST'])
# # def login():
# #     conn = None
# #     try:
# #         data = request.get_json()
# #         arid = data.get("arid")
# #         password = data.get("password")
#
# #         conn = get_db_connection()
# #         cursor = conn.cursor()
# #         cursor.execute("""
# #             SELECT role, name, arid_no
# #             FROM Users
# #             WHERE arid_no = ? AND password = ?
# #         """, (arid, password))
#
# #         user = cursor.fetchone()
#
# #         if user:
# #             role = str(user[0]).strip().lower()
# #             return jsonify({
# #                 "success": True,
# #                 "role": role,
# #                 "name": user[1],
# #                 'arid_no': user[2]
# #             })
# #         return jsonify({"success": False, "message": "Invalid credentials"}), 401
# #     except Exception as e:
# #         print(f"Login error: {str(e)}")
# #         return jsonify({"success": False, "error": str(e)}), 500
# #     finally:
# #         if conn:
# #             conn.close()
# # @app.route('/add_user', methods=['POST'])
# # def add_user():
# #     data = request.get_json()
# #     arid_no = data.get('arid_no')
# #     password = data.get('password')
# #     role = data.get('role', 'student')  # Default to student
# #     name = data.get('name')
# #     admin_arid = data.get('admin_arid')  # Provided when admin adds a user
#
# #     if not all([arid_no, password, name]):
# #         return jsonify({"error": "All fields (arid_no, password, name) are required"}), 400
#
# #     if role == 'admin' and not verify_admin(admin_arid):
# #         return jsonify({"error": "Admin privileges required to add an admin user"}), 403
#
# #     conn = get_db_connection()
# #     cursor = conn.cursor()
# #     try:
# #         cursor.execute(
# #             "INSERT INTO Users (arid_no, password, role, name) VALUES (?, ?, ?, ?)",
# #             (arid_no, password, role, name)
# #         )
# #         conn.commit()
# #         return jsonify({"success": True, "message": "User added successfully"})
# #     except pyodbc.IntegrityError as e:
# #         if "Violation of PRIMARY KEY constraint" in str(e):
# #             return jsonify({"error": "User already has an account"}), 400
# #         return jsonify({"error": f"Database error: {str(e)}"}), 500
# #     except Exception as e:
# #         return jsonify({"error": f"Error adding user: {str(e)}"}), 500
# #     finally:
# #         conn.close()
#
# # @app.route('/create_poll', methods=['POST'])
# # def create_poll():
# #     try:
# #         data = request.get_json()
# #         print(f"Received payload: {data}")
# #         title = data['title']
# #         description = data.get('description')
# #         created_by = data['created_by']
# #         is_public = data.get('is_public', True)
# #         start_time = data.get('start_time')
# #         end_time = data.get('end_time')
# #         options = data.get('options', [])
#
# #         # Validate inputs
# #         if not title or not created_by or len(options) < 2:
# #             return jsonify({"success": False, "message": "Title, created_by, and at least 2 options are required"}), 400
#
# #         conn = get_db_connection()
# #         cursor = conn.cursor()
#
# #         print(f"Inserting poll: title={title}, created_by={created_by}, start_time={start_time}, end_time={end_time}, is_public={is_public}, options={options}")
#
# #         # Use OUTPUT clause to get the inserted id
# #         cursor.execute("""
# #             INSERT INTO Polls (title, description, created_by, is_public, start_time, end_time)
# #             OUTPUT INSERTED.id
# #             VALUES (?, ?, ?, ?, ?, ?)
# #         """, (title, description, created_by, is_public, start_time, end_time))
# #         poll_id_row = cursor.fetchone()
# #         print(f"OUTPUT result: {poll_id_row}")
#
# #         if not poll_id_row or poll_id_row[0] is None:
# #             conn.rollback()
# #             conn.close()
# #             return jsonify({"success": False, "message": "Failed to retrieve poll ID"}), 500
#
# #         poll_id = int(poll_id_row[0])
# #         print(f"Retrieved poll_id: {poll_id}")
#
# #         for opt in options:
# #             cursor.execute("INSERT INTO PollOptions (poll_id, option_text) VALUES (?, ?)", (poll_id, opt))
# #             print(f"Inserted option: {opt}")
#
# #         conn.commit()
# #         conn.close()
# #         return jsonify({"success": True, "poll_id": poll_id})
#
# #     except Exception as e:
# #         print(f"Error creating poll: {str(e)}")
# #         return jsonify({"success": False, "message": str(e)}), 500
# # @app.route('/get_polls', methods=['GET'])
# # def get_polls():
# #     conn = get_db_connection()
# #     cursor = conn.cursor()
# #     cursor.execute("SELECT id, title, description, is_public, start_time, end_time FROM Polls")
# #     rows = cursor.fetchall()
# #     conn.close()
#
# #     polls = [{
# #         "id": row[0],
# #         "title": row[1],
# #         "description": row[2],
# #         "is_public": row[3],
# #         "start_time": str(row[4]) if row[4] else None,
# #         "end_time": str(row[5]) if row[5] else None,
# #     } for row in rows]
#
# #     return jsonify(polls)
# # @app.route('/get_poll/<int:poll_id>', methods=['GET'])
# # def get_poll(poll_id):
# #     conn = get_db_connection()
# #     cursor = conn.cursor()
#
# #     cursor.execute("SELECT id, title, description FROM Polls WHERE id = ?", (poll_id,))
# #     poll = cursor.fetchone()
# #     if not poll:
# #         return jsonify({"error": "Poll not found"}), 404
#
# #     cursor.execute("SELECT id, option_text FROM PollOptions WHERE poll_id = ?", (poll_id,))
# #     options = [{"id": row[0], "text": row[1]} for row in cursor.fetchall()]
#
# #     conn.close()
# #     return jsonify({
# #         "id": poll[0],
# #         "title": poll[1],
# #         "description": poll[2],
# #         "options": options
# #     })
#
# # @app.route('/vote', methods=['POST'])
# # def vote():
# #     data = request.get_json()
# #     arid_no = data['arid_no']
# #     option_id = data['option_id']
#
# #     conn = get_db_connection()
# #     cursor = conn.cursor()
# #     cursor.execute("""
# #         SELECT 1 FROM Votes WHERE user_arid_no = ? AND poll_option_id IN (
# #             SELECT id FROM PollOptions WHERE poll_id = (
# #                 SELECT poll_id FROM PollOptions WHERE id = ?
# #             )
# #         )
# #     """, (arid_no, option_id))
# #     if cursor.fetchone():
# #         conn.close()
# #         return jsonify({"success": False, "message": "You already voted"}), 400
#
# #     cursor.execute("INSERT INTO Votes (user_arid_no, poll_option_id) VALUES (?, ?)", (arid_no, option_id))
# #     conn.commit()
# #     conn.close()
# #     return jsonify({"success": True})
# # @app.route('/poll_results/<int:poll_id>', methods=['GET'])
# # def poll_results(poll_id):
# #     conn = get_db_connection()
# #     cursor = conn.cursor()
# #     cursor.execute("""
# #         SELECT PO.option_text, COUNT(V.id) as votes
# #         FROM PollOptions PO
# #         LEFT JOIN Votes V ON PO.id = V.poll_option_id
# #         WHERE PO.poll_id = ?
# #         GROUP BY PO.option_text
# #     """, (poll_id,))
#
# #     results = [{"option": row[0], "votes": row[1]} for row in cursor.fetchall()]
# #     conn.close()
# #     return jsonify(results)
#
# # @app.route('/update_poll/<int:poll_id>', methods=['PUT'])
# # def update_poll(poll_id):
# #     data = request.get_json()
# #     title = data.get('title')
# #     description = data.get('description')
# #     #is_public = data.get('is_public', True)
# #     is_public = data.get('is_public')
# #     start_time = data.get('start_time')
# #     end_time = data.get('end_time')
# #     options = data.get('options', [])  # list of option texts
#
# #     if not title or len(options) < 2:
# #         return jsonify({"success": False, "message": "Title and at least 2 options required"}), 400
#
# #     conn = get_db_connection()
# #     cursor = conn.cursor()
#
# #     # Update Poll main data
# #     cursor.execute("""
# #         UPDATE Polls
# #         SET title = ?, description = ?, is_public = ?, start_time = ?, end_time = ?
# #         WHERE id = ?
# #     """, (title, description, is_public, start_time, end_time, poll_id))
#
# #     # Delete existing options for the poll
# #     cursor.execute("DELETE FROM PollOptions WHERE poll_id = ?", (poll_id,))
#
# #     # Insert new options
# #     for option_text in options:
# #         cursor.execute("INSERT INTO PollOptions (poll_id, option_text) VALUES (?, ?)", (poll_id, option_text))
#
# #     conn.commit()
# #     conn.close()
#
# #     return jsonify({"success": True, "message": "Poll updated successfully"})
#
# # @app.route('/delete_poll/<int:poll_id>', methods=['DELETE'])
# # def delete_poll(poll_id):
# #     conn = get_db_connection()
# #     cursor = conn.cursor()
# #     cursor.execute("DELETE FROM Votes WHERE poll_option_id IN (SELECT id FROM PollOptions WHERE poll_id = ?)", (poll_id,))
# #     cursor.execute("DELETE FROM PollOptions WHERE poll_id = ?", (poll_id,))
# #     cursor.execute("DELETE FROM Polls WHERE id = ?", (poll_id,))
# #     conn.commit()
# #     conn.close()
# #     return jsonify({"success": True})
#
# # @app.route('/reset_password', methods=['POST'])
# # def reset_password():
# #     data = request.get_json()
# #     arid_no = data.get('arid_no')
# #     new_password = data.get('new_password')
#
# #     if not arid_no or not new_password:
# #         return jsonify({'success': False, 'error': 'Missing ARID or password'}), 400
#
# #     try:
# #         conn = get_db_connection()
# #         cursor = conn.cursor()
#
# #         # Update the password in the database
# #         cursor.execute(
# #             "UPDATE Users SET password = ? WHERE arid_no = ?",
# #             (new_password, arid_no)
# #         )
#
# #         conn.commit()
#
# #         if cursor.rowcount == 0:
# #             return jsonify({'success': False, 'error': 'Student not found'}), 404
#
# #         return jsonify({'success': True}), 200
#
# #     except Exception as e:
# #         return jsonify({'success': False, 'error': str(e)}), 500
#
# #     finally:
# #         cursor.close()
# #         conn.close()
#
# # if __name__ == '__main__':
# #     app.run(host='0.0.0.0', port=5000, debug=True)
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import pyodbc
# from datetime import datetime, timedelta
#
# app = Flask(__name__)
# CORS(app)
#
# # Database config as a dictionary
# DB_CONFIG = {
#     "driver": "ODBC Driver 17 for SQL Server",
#     "server": "FASEEH-UR-REHMA\VE_SERVER",
#     "database": "Polling_SystemDB",
#     "uid": "sa",
#     "pwd": "mr123"
# }
#
# def get_db_connection():
#     """Establish database connection"""
#     conn_str = (
#         f"DRIVER={{{DB_CONFIG['driver']}}};"
#         f"SERVER={DB_CONFIG['server']};"
#         f"DATABASE={DB_CONFIG['database']};"
#         f"UID={DB_CONFIG['uid']};"
#         f"PWD={DB_CONFIG['pwd']};"
#         f"Encrypt=no;"
#         f"TrustServerCertificate=yes;"
#     )
#     return pyodbc.connect(conn_str)
#
# def verify_admin(arid):
#     """Verify if user is admin"""
#     conn = None
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         cursor.execute("SELECT role FROM Users WHERE arid_no = ?", (arid,))
#         result = cursor.fetchone()
#         return str(result[0]).strip().lower() == 'admin' if result else False
#     except Exception as e:
#         print(f"Admin verification error: {str(e)}")
#         return False
#     finally:
#         if conn:
#             conn.close()
#
# @app.route('/login', methods=['POST'])
# def login():
#     conn = None
#     try:
#         data = request.get_json()
#         arid = data.get("arid")
#         password = data.get("password")
#
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         cursor.execute("""
#             SELECT role, name, arid_no
#             FROM Users
#             WHERE arid_no = ? AND password = ?
#         """, (arid, password))
#
#         user = cursor.fetchone()
#
#         if user:
#             role = str(user[0]).strip().lower()
#             return jsonify({
#                 "success": True,
#                 "role": role,
#                 "name": user[1],
#                 'arid_no': user[2]
#             })
#         return jsonify({"success": False, "message": "Invalid credentials"}), 401
#     except Exception as e:
#         print(f"Login error: {str(e)}")
#         return jsonify({"success": False, "error": str(e)}), 500
#     finally:
#         if conn:
#             conn.close()
#
# @app.route('/add_user', methods=['POST'])
# def add_user():
#     data = request.get_json()
#     arid_no = data.get('arid_no')
#     password = data.get('password')
#     role = data.get('role', 'student')
#     name = data.get('name')
#     admin_arid = data.get('admin_arid')
#
#     if not all([arid_no, password, name]):
#         return jsonify({"error": "All fields (arid_no, password, name) are required"}), 400
#
#     if role == 'admin' and not verify_admin(admin_arid):
#         return jsonify({"error": "Admin privileges required to add an admin user"}), 403
#
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     try:
#         cursor.execute(
#             "INSERT INTO Users (arid_no, password, role, name) VALUES (?, ?, ?, ?)",
#             (arid_no, password, role, name)
#         )
#         conn.commit()
#         return jsonify({"success": True, "message": "User added successfully"})
#     except pyodbc.IntegrityError as e:
#         if "Violation of PRIMARY KEY constraint" in str(e):
#             return jsonify({"error": "User already has an account"}), 400
#         return jsonify({"error": f"Database error: {str(e)}"}), 500
#     except Exception as e:
#         return jsonify({"error": f"Error adding user: {str(e)}"}), 500
#     finally:
#         conn.close()
#
# @app.route('/create_poll', methods=['POST'])
# def create_poll():
#     try:
#         data = request.get_json()
#         title = data['title']
#         description = data.get('description')
#         created_by = data['created_by']
#         is_public = data.get('is_public', True)
#         start_time = data.get('start_time')
#         end_time = data.get('end_time')
#         options = data.get('options', [])
#
#         if not title or not created_by or len(options) < 2:
#             return jsonify({"success": False, "message": "Title, created_by, and at least 2 options are required"}), 400
#
#         conn = get_db_connection()
#         cursor = conn.cursor()
#
#         cursor.execute("""
#             INSERT INTO Polls (title, description, created_by, is_public, start_time, end_time)
#             OUTPUT INSERTED.id
#             VALUES (?, ?, ?, ?, ?, ?)
#         """, (title, description, created_by, is_public, start_time, end_time))
#         poll_id_row = cursor.fetchone()
#
#         if not poll_id_row or poll_id_row[0] is None:
#             conn.rollback()
#             conn.close()
#             return jsonify({"success": False, "message": "Failed to retrieve poll ID"}), 500
#
#         poll_id = int(poll_id_row[0])
#
#         for opt in options:
#             cursor.execute("INSERT INTO PollOptions (poll_id, option_text) VALUES (?, ?)", (poll_id, opt))
#
#         conn.commit()
#         conn.close()
#         return jsonify({"success": True, "poll_id": poll_id})
#
#     except Exception as e:
#         print(f"Error creating poll: {str(e)}")
#         return jsonify({"success": False, "message": str(e)}), 500
#
# @app.route('/get_polls', methods=['GET'])
# def get_polls():
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute("SELECT id, title, description, is_public, start_time, end_time FROM Polls")
#     rows = cursor.fetchall()
#     conn.close()
#
#     polls = [{
#         "id": row[0],
#         "title": row[1],
#         "description": row[2],
#         "is_public": row[3],
#         "start_time": str(row[4]) if row[4] else None,
#         "end_time": str(row[5]) if row[5] else None,
#     } for row in rows]
#
#     return jsonify(polls)
#
# @app.route('/get_poll/<int:poll_id>', methods=['GET'])
# def get_poll(poll_id):
#     conn = get_db_connection()
#     cursor = conn.cursor()
#
#     cursor.execute("SELECT id, title, description FROM Polls WHERE id = ?", (poll_id,))
#     poll = cursor.fetchone()
#     if not poll:
#         return jsonify({"error": "Poll not found"}), 404
#
#     cursor.execute("SELECT id, option_text FROM PollOptions WHERE poll_id = ?", (poll_id,))
#     options = [{"id": row[0], "text": row[1]} for row in cursor.fetchall()]
#
#     conn.close()
#     return jsonify({
#         "id": poll[0],
#         "title": poll[1],
#         "description": poll[2],
#         "options": options
#     })
#
# @app.route('/vote', methods=['POST'])
# def vote():
#     data = request.get_json()
#     arid_no = data['arid_no']
#     option_id = data['option_id']
#
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute("""
#         SELECT 1 FROM Votes WHERE user_arid_no = ? AND poll_option_id IN (
#             SELECT id FROM PollOptions WHERE poll_id = (
#                 SELECT poll_id FROM PollOptions WHERE id = ?
#             )
#         )
#     """, (arid_no, option_id))
#     if cursor.fetchone():
#         conn.close()
#         return jsonify({"success": False, "message": "You already voted"}), 400
#
#     cursor.execute("INSERT INTO Votes (user_arid_no, poll_option_id) VALUES (?, ?)", (arid_no, option_id))
#     conn.commit()
#     conn.close()
#     return jsonify({"success": True})
#
# @app.route('/poll_results/<int:poll_id>', methods=['GET'])
# def poll_results(poll_id):
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute("""
#         SELECT PO.option_text, COUNT(V.id) as votes
#         FROM PollOptions PO
#         LEFT JOIN Votes V ON PO.id = V.poll_option_id
#         WHERE PO.poll_id = ?
#         GROUP BY PO.option_text
#     """, (poll_id,))
#
#     results = [{"option": row[0], "votes": row[1]} for row in cursor.fetchall()]
#     conn.close()
#     return jsonify(results)
#
# @app.route('/update_poll/<int:poll_id>', methods=['PUT'])
# def update_poll(poll_id):
#     data = request.get_json()
#     title = data.get('title')
#     description = data.get('description')
#     is_public = data.get('is_public')
#     start_time = data.get('start_time')
#     end_time = data.get('end_time')
#     options = data.get('options', [])
#
#     if not title or len(options) < 2:
#         return jsonify({"success": False, "message": "Title and at least 2 options required"}), 400
#
#     conn = get_db_connection()
#     cursor = conn.cursor()
#
#     cursor.execute("""
#         UPDATE Polls
#         SET title = ?, description = ?, is_public = ?, start_time = ?, end_time = ?
#         WHERE id = ?
#     """, (title, description, is_public, start_time, end_time, poll_id))
#
#     cursor.execute("DELETE FROM PollOptions WHERE poll_id = ?", (poll_id,))
#     for option_text in options:
#         cursor.execute("INSERT INTO PollOptions (poll_id, option_text) VALUES (?, ?)", (poll_id, option_text))
#
#     conn.commit()
#     conn.close()
#     return jsonify({"success": True, "message": "Poll updated successfully"})
#
# @app.route('/delete_poll/<int:poll_id>', methods=['DELETE'])
# def delete_poll(poll_id):
#     conn = get_db_connection()
#     cursor = conn.cursor()
#
#     # Delete all related votes
#     cursor.execute("DELETE FROM Votes WHERE poll_option_id IN (SELECT id FROM PollOptions WHERE poll_id = ?)", (poll_id,))
#
#     # Delete poll options
#     cursor.execute("DELETE FROM PollOptions WHERE poll_id = ?", (poll_id,))
#
#     # Delete the poll
#     cursor.execute("DELETE FROM Polls WHERE id = ?", (poll_id,))
#
#     conn.commit()
#     conn.close()
#
#     return jsonify({"success": True, "message": "Poll deleted successfully"})
# @app.route('/reset_password', methods=['POST'])
# def reset_password():
#     data = request.get_json()
#     arid_no = data.get('arid_no')
#     new_password = data.get('new_password')
#
#     if not arid_no or not new_password:
#         return jsonify({'success': False, 'error': 'Missing ARID or password'}), 400
#
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()
#
#         # Update the password in the database
#         cursor.execute(
#             "UPDATE Users SET password = ? WHERE arid_no = ?",
#             (new_password, arid_no)
#         )
#
#         conn.commit()
#
#         if cursor.rowcount == 0:
#             return jsonify({'success': False, 'error': 'Student not found'}), 404
#
#         return jsonify({'success': True}), 200
#
#     except Exception as e:
#         return jsonify({'success': False, 'error': str(e)}), 500
#
#     finally:
#         cursor.close()
#         conn.close()
#
#
#
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)


from flask import Flask, request, jsonify
from flask_cors import CORS
import pyodbc
from datetime import datetime
import base64  # Import base64 for encoding/decoding image data

app = Flask(__name__)  # FIXED: Changed __queue__ to __name__
CORS(app)  # Enable Cross-Origin Resource Sharing for the Flask app

# Database configuration dictionary
DB_CONFIG = {
	"driver": "ODBC Driver 17 for SQL Server",
	"server": r"FASEEH-UR-REHMA\VE_SERVER",  # Changed to raw string to fix SyntaxWarning
	"database": "Polling_SystemDB",
	"uid": "sa",
	"pwd": "mr123"
}


def get_db_connection():
	"""
	Establishes and returns a database connection using the DB_CONFIG.
	Includes encryption and trust settings for local SQL Server.
	"""
	conn_str = (
		f"DRIVER={{{DB_CONFIG['driver']}}};"
		f"SERVER={DB_CONFIG['server']};"
		f"DATABASE={DB_CONFIG['database']};"
		f"UID={DB_CONFIG['uid']};"
		f"PWD={DB_CONFIG['pwd']};"
		f"Encrypt=no;"  # Set to 'yes' for production with proper certificates
		f"TrustServerCertificate=yes;"  # Set to 'no' for production with proper certificates
	)
	return pyodbc.connect(conn_str)


# def verify_admin(arid):
# 	"""
# 	Verifies if a user with the given ARID number has 'admin' role.
# 	"""
# 	conn = None
# 	try:
# 		conn = get_db_connection()
# 		cursor = conn.cursor()
# 		cursor.execute("SELECT role FROM Users WHERE arid_no = ?", (arid,))
# 		result = cursor.fetchone()
# 		# Return true if user exists and role is 'admin', false otherwise
# 		return str(result[0]).strip().lower() == 'admin' if result else False
# 	except Exception as e:
# 		print(f"Admin verification error: {str(e)}")
# 		return False
# 	finally:
# 		if conn:
# 			conn.close()

def verify_admin(arid):
	conn = None
	try:
		conn = get_db_connection()
		cursor = conn.cursor()
		cursor.execute("SELECT role FROM Users WHERE arid_no = ?", (arid,))
		result = cursor.fetchone()
		return str(result[0]).strip().lower() == 'admin' if result else False
	except Exception as e:
		print(f"Admin verification error: {str(e)}")
		return False
	finally:
		if conn:
			conn.close()

@app.route('/biometric_login', methods=['POST'])
def biometric_login():
	"""
	Allows biometric login based only on ARID (used after fingerprint verification on Flutter).
	"""
	conn = None
	try:
		data = request.get_json()
		arid = data.get("arid")

		if not arid:
			return jsonify({"success": False, "message": "ARID is required"}), 400

		conn = get_db_connection()
		cursor = conn.cursor()
		cursor.execute("SELECT role, name, arid_no FROM Users WHERE arid_no = ?", (arid,))
		user = cursor.fetchone()

		if user:
			role = str(user[0]).strip().lower()
			return jsonify({
				"success": True,
				"message": "Biometric login successful!",
				"role": role,
				"name": user[1],
				"arid_no": user[2]
			})
		return jsonify({"success": False, "message": "Invalid ARID or user not found"}), 404
	except Exception as e:
		print(f"Biometric login error: {str(e)}")
		return jsonify({"success": False, "error": str(e)}), 500
	finally:
		if conn:
			conn.close()

@app.route('/login', methods=['POST'])
def login():
	"""
	Authenticates a user based on ARID and password.
	Returns user role, name, and ARID on successful login.
	"""
	conn = None
	try:
		data = request.get_json()
		arid = data.get("arid")
		password = data.get("password")

		if not arid or not password:
			return jsonify({"success": False, "message": "ARID and password are required"}), 400

		conn = get_db_connection()
		cursor = conn.cursor()
		cursor.execute("""
            SELECT role, name, arid_no
            FROM Users 
            WHERE arid_no = ? AND password = ?
        """, (arid, password))

		user = cursor.fetchone()

		if user:
			role = str(user[0]).strip().lower()  # Strip whitespace and lowercase role
			return jsonify({
				"success": True,
				"message": "Login successful!",
				"role": role,
				"name": user[1],
				'arid_no': user[2]
			})
		return jsonify({"success": False, "message": "Invalid ARID or password"}), 401
	except Exception as e:
		print(f"Login error: {str(e)}")
		return jsonify({"success": False, "error": str(e)}), 500
	finally:
		if conn:
			conn.close()


@app.route('/add_user', methods=['POST'])
def add_user():
	"""
	Adds a new user to the database.
	Requires arid_no, password, name. Role defaults to 'student'.
	Admin privileges are required to add an 'admin' role user.
	"""
	data = request.get_json()
	arid_no = data.get('arid_no')
	password = data.get('password')
	role = data.get('role', 'student')  # Default role is 'student'
	name = data.get('name')
	admin_arid = data.get('admin_arid')  # ARID of the admin trying to add a new user

	if not all([arid_no, password, name]):
		return jsonify({"error": "All fields (arid_no, password, name) are required"}), 400

	# If an admin user is being added, verify the caller's admin privileges
	if role.lower() == 'admin' and not verify_admin(admin_arid):
		return jsonify({"error": "Admin privileges required to add an admin user"}), 403

	conn = None
	try:
		conn = get_db_connection()
		cursor = conn.cursor()
		cursor.execute(
			"INSERT INTO Users (arid_no, password, role, name) VALUES (?, ?, ?, ?)",
			(arid_no, password, role, name)
		)
		conn.commit()
		return jsonify({"success": True, "message": "User added successfully"})
	except pyodbc.IntegrityError as e:
		# Catch specific error for duplicate primary key (user already exists)
		if "Violation of PRIMARY KEY constraint" in str(e):
			return jsonify({"error": "User with this ARID number already has an account"}), 409  # Conflict status
		return jsonify({"error": f"Database integrity error: {str(e)}"}), 500
	except Exception as e:
		return jsonify({"error": f"Error adding user: {str(e)}"}), 500
	finally:
		if conn:
			conn.close()


@app.route('/create_poll', methods=['POST'])
def create_poll():
	"""
	Creates a new poll with options, now accepting Base64 image data for each option.
	"""
	conn = None
	try:
		data = request.get_json()
		title = data.get('title')
		description = data.get('description')
		created_by = data.get('created_by')
		is_public = data.get('is_public', True)  # Default to public
		start_time_str = data.get('start_time')
		end_time_str = data.get('end_time')
		options = data.get('options', [])  # Expects a list of dictionaries with 'text' and 'imageData' (Base64 string)

		if not title or not created_by or len(options) < 2:
			return jsonify({"success": False, "message": "Title, created_by, and at least 2 options are required"}), 400

		conn = get_db_connection()
		cursor = conn.cursor()

		start_time = datetime.fromisoformat(start_time_str) if start_time_str else None
		end_time = datetime.fromisoformat(end_time_str) if end_time_str else None

		cursor.execute("""
            INSERT INTO Polls (title, description, created_by, is_public, start_time, end_time)
            OUTPUT INSERTED.id
            VALUES (?, ?, ?, ?, ?, ?)
        """, (title, description, created_by, is_public, start_time, end_time))
		poll_id_row = cursor.fetchone()

		if not poll_id_row or poll_id_row[0] is None:
			conn.rollback()
			return jsonify({"success": False, "message": "Failed to retrieve poll ID after creation"}), 500

		poll_id = int(poll_id_row[0])

		for opt in options:
			option_text = opt.get('text')
			image_data_b64 = opt.get('imageData')  # Get Base64 string

			binary_image_data = None
			if image_data_b64:
				try:
					# Decode Base64 string to bytes
					binary_image_data = base64.b64decode(image_data_b64)
				except Exception as b64_e:
					print(f"Error decoding base64 image data: {b64_e}")
					# Optionally return an error or skip image for this option
					binary_image_data = None  # Treat invalid base64 as no image

			if option_text and option_text.strip():
				cursor.execute("INSERT INTO PollOptions (poll_id, option_text, image_data) VALUES (?, ?, ?)",
							   (poll_id, option_text.strip(), binary_image_data))

		conn.commit()
		return jsonify({"success": True, "poll_id": poll_id, "message": "Poll created successfully"})

	except Exception as e:
		if conn:
			conn.rollback()
		print(f"Error creating poll: {str(e)}")
		return jsonify({"success": False, "message": f"Failed to create poll: {str(e)}"}), 500
	finally:
		if conn:
			conn.close()


@app.route('/get_polls', methods=['GET'])
def get_polls():
	"""
	Retrieves a list of all polls, including their basic details.
	"""
	conn = None
	try:
		conn = get_db_connection()
		cursor = conn.cursor()
		# Explicitly select all 8 columns as per your database schema screenshot
		cursor.execute(
			"SELECT id, title, description, created_by, is_public, start_time, end_time, created_at FROM Polls")
		rows = cursor.fetchall()

		# --- DEEPER DEBUGGING FOR COLUMN MISMATCH ---
		if cursor.description:
			print(f"DEBUG: get_polls - Cursor Description: {[col[0] for col in cursor.description]}")
			print(f"DEBUG: get_polls - Number of columns returned by query: {len(cursor.description)}")
		else:
			print("DEBUG: get_polls - Cursor Description is None (no columns returned or empty result set).")
		# --- END DEEPER DEBUGGING ---

		polls = []
		for row in rows:
			print(
				f"DEBUG: get_polls - Processing row with length: {len(row)}. Content (first 3): {row[:3]}")  # Show first few for brevity
			# Ensure row has enough elements before accessing required indices
			if len(row) < 7:  # Indices 5 and 6 (start_time, end_time) are crucial for current code
				print(f"ERROR: get_polls - Row is too short ({len(row)} columns). Expected at least 7. Row: {row}")
				continue  # Skip this malformed row to prevent further errors

			start_time_str = row[5].isoformat() if isinstance(row[5], datetime) else None
			end_time_str = row[6].isoformat() if isinstance(row[6], datetime) else None

			# Note: 'created_at' (index 7) is available but not currently used in Flutter's display of polls list.
			# If you want to use it, you'd add it to this dictionary: "created_at": row[7].isoformat() if isinstance(row[7], datetime) else None,
			polls.append({
				"id": row[0],
				"title": row[1],
				"description": row[2],
				"created_by": row[3],
				"is_public": row[4],
				"start_time": start_time_str,
				"end_time": end_time_str,
			})
		return jsonify(polls)
	except Exception as e:
		print(f"Error fetching polls: {str(e)}")
		return jsonify({"success": False, "message": f"Failed to fetch polls: {str(e)}"}), 500
	finally:
		if conn:
			conn.close()


@app.route('/get_poll/<int:poll_id>', methods=['GET'])
def get_poll(poll_id):
	"""
	Retrieves detailed information for a single poll, including its options and Base64 image data.
	"""
	conn = None
	try:
		conn = get_db_connection()
		cursor = conn.cursor()

		# Explicitly select all 8 columns as per your database schema screenshot
		cursor.execute(
			"SELECT id, title, description, created_by, is_public, start_time, end_time, created_at FROM Polls WHERE id = ?",
			(poll_id,))
		poll_row = cursor.fetchone()

		if not poll_row:
			return jsonify({"error": "Poll not found"}), 404

		# --- DEEPER DEBUGGING FOR COLUMN MISMATCH ---
		if cursor.description:
			print(f"DEBUG: get_poll - Cursor Description: {[col[0] for col in cursor.description]}")
			print(f"DEBUG: get_poll - Number of columns returned by query: {len(cursor.description)}")
		else:
			print("DEBUG: get_poll - Cursor Description is None (no columns returned or empty result set).")
		# --- END DEEPER DEBUGGING ---

		print(
			f"DEBUG: get_poll - Poll row has length: {len(poll_row)}. Content (first 3): {poll_row[:3]}")  # Show first few for brevity

		# Ensure poll_row has enough elements before accessing required indices
		if len(poll_row) < 7:  # Indices 5 and 6 (start_time, end_time) are crucial for current code
			print(
				f"ERROR: get_poll - Poll row is too short ({len(poll_row)} columns). Expected at least 7. Row: {poll_row}")
			return jsonify({"success": False, "message": "Malformed poll data in database. Missing time columns."}), 500

		# Fetch poll options including image_data
		cursor.execute("SELECT id, option_text, image_data FROM PollOptions WHERE poll_id = ?", (poll_id,))

		options = []
		for row in cursor.fetchall():
			image_data_b64 = None
			if row[2]:  # If image_data is not None (i.e., image exists)
				image_data_b64 = base64.b64encode(row[2]).decode('utf-8')  # Encode bytes to Base64 string
			options.append({"id": row[0], "text": row[1], "imageData": image_data_b64})

		start_time_str = poll_row[5].isoformat() if isinstance(poll_row[5], datetime) else None
		end_time_str = poll_row[6].isoformat() if isinstance(poll_row[6], datetime) else None

		return jsonify({
			"id": poll_row[0],
			"title": poll_row[1],
			"description": poll_row[2],
			"created_by": poll_row[3],
			"is_public": poll_row[4],
			"start_time": start_time_str,
			"end_time": end_time_str,
			"options": options
		})
	except Exception as e:
		print(f"Error fetching poll details: {str(e)}")
		return jsonify({"success": False, "message": f"Failed to fetch poll details: {str(e)}"}), 500
	finally:
		if conn:
			conn.close()


@app.route('/vote', methods=['POST'])
def vote():
	"""
	Records a user's vote for a specific poll option.
	Ensures a user can only vote once per poll.
	"""
	# --- IMPORTANT DEBUG PRINT ---
	try:
		incoming_data = request.get_json()
		print(f"Backend received vote data: {incoming_data}")
	except Exception as e:
		print(f"Error parsing incoming JSON for vote: {e}")
		return jsonify({"success": False, "message": "Invalid JSON in request"}), 400
	# --- END DEBUG PRINT ---

	conn = None
	try:
		data = incoming_data  # Use the already parsed data
		arid = data.get('arid_no')
		poll_id = data.get('poll_id')  # CORRECT: We expect 'poll_id' from the frontend
		option_id = data.get('option_id')

		# Debugging: Print values extracted from data
		print(f"Extracted: ARID={arid}, PollID={poll_id}, OptionID={option_id}")

		if not arid or not poll_id or not option_id:
			# More specific error message for backend debugging
			missing_fields = []
			if not arid: missing_fields.append("ARID number")
			if not poll_id: missing_fields.append("poll ID")
			if not option_id: missing_fields.append("option ID")
			return jsonify({"success": False, "message": f"Missing required fields: {', '.join(missing_fields)}"}), 400

		conn = get_db_connection()
		cursor = conn.cursor()

		# This check is crucial for preventing multiple votes per poll
		cursor.execute("""
            SELECT 1
            FROM Votes V
            JOIN PollOptions PO ON V.poll_option_id = PO.id
            WHERE V.user_arid_no = ? AND PO.poll_id = ?
        """, (arid, poll_id))  # Correctly uses poll_id here

		if cursor.fetchone():
			return jsonify({"success": False, "message": "You have already voted in this poll"}), 400

		cursor.execute("INSERT INTO Votes (user_arid_no, poll_option_id) VALUES (?, ?)", (arid, option_id))
		conn.commit()
		return jsonify({"success": True, "message": "Vote cast successfully"})
	except Exception as e:
		if conn:
			conn.rollback()
		print(f"Error casting vote: {str(e)}")
		return jsonify({"success": False, "message": f"Failed to cast vote: {str(e)}"}), 500
	finally:
		if conn:
			conn.close()


@app.route('/check_vote_status', methods=['POST'])
def check_vote_status():
	"""
	Checks if a specific user has already voted in a given poll.
	"""
	conn = None
	try:
		data = request.get_json()
		arid_no = data.get('arid_no')
		poll_id = data.get('poll_id')

		if not all([arid_no, poll_id]):
			return jsonify({"success": False, "message": "ARID number and poll ID are required"}), 400

		conn = get_db_connection()
		cursor = conn.cursor()

		cursor.execute("""
            SELECT 1
            FROM Votes V
            JOIN PollOptions PO ON V.poll_option_id = PO.id
            WHERE V.user_arid_no = ? AND PO.poll_id = ?
        """, (arid_no, poll_id))

		has_voted = cursor.fetchone() is not None
		return jsonify({"success": True, "has_voted": has_voted})
	except Exception as e:
		print(f"Error checking vote status: {str(e)}")
		return jsonify({"success": False, "message": f"Failed to check vote status: {str(e)}"}), 500
	finally:
		if conn:
			conn.close()


@app.route('/poll_results/<int:poll_id>', methods=['GET'])
def poll_results(poll_id):
	"""
	Retrieves the aggregated results (vote counts) for a specific poll, including Base64 image data.
	"""
	conn = None
	try:
		conn = get_db_connection()
		cursor = conn.cursor()
		cursor.execute("""
            SELECT PO.option_text, COUNT(V.id) as votes, PO.image_data
            FROM PollOptions PO
            LEFT JOIN Votes V ON PO.id = V.poll_option_id
            WHERE PO.poll_id = ?
            GROUP BY PO.option_text, PO.image_data
            ORDER BY votes DESC, PO.option_text ASC
        """, (poll_id,))

		results = []
		for row in cursor.fetchall():
			image_data_b64 = None
			if row[2]:  # If image_data is not None
				image_data_b64 = base64.b64encode(row[2]).decode('utf-8')  # Encode bytes to Base64 string
			results.append({"option": row[0], "votes": row[1], "imageData": image_data_b64})
		return jsonify(results)
	except Exception as e:
		print(f"Error fetching poll results: {str(e)}")
		return jsonify({"success": False, "message": f"Failed to fetch poll results: {str(e)}"}), 500
	finally:
		if conn:
			conn.close()


@app.route('/update_poll/<int:poll_id>', methods=['PUT'])
def update_poll(poll_id):
	"""
	Updates an existing poll's details and options, now accepting Base64 image data.
	Deletes existing options and re-inserts new ones.
	"""
	conn = None
	try:
		data = request.get_json()
		title = data.get('title')
		description = data.get('description')
		is_public = data.get('is_public')
		start_time_str = data.get('start_time')
		end_time_str = data.get('end_time')
		options = data.get('options', [])  # Expects list of dicts with 'text' and 'imageData'

		if not title or len(options) < 2:
			return jsonify({"success": False, "message": "Title and at least 2 options required"}), 400

		conn = get_db_connection()
		cursor = conn.cursor()

		start_time = datetime.fromisoformat(start_time_str) if start_time_str else None
		end_time = datetime.fromisoformat(end_time_str) if end_time_str else None

		cursor.execute("""
            UPDATE Polls
            SET title = ?, description = ?, is_public = ?, start_time = ?, end_time = ?
            WHERE id = ?
        """, (title, description, is_public, start_time, end_time, poll_id))

		# Delete existing options for this poll (cascade will handle associated votes)
		cursor.execute("DELETE FROM PollOptions WHERE poll_id = ?", (poll_id,))

		# Insert new options with their associated image data
		for opt in options:
			option_text = opt.get('text')
			image_data_b64 = opt.get('imageData')

			binary_image_data = None
			if image_data_b64:
				try:
					binary_image_data = base64.b64decode(image_data_b64)
				except Exception as b64_e:
					print(f"Error decoding base64 image data for update: {b64_e}")
					binary_image_data = None

			if option_text and option_text.strip():
				cursor.execute("INSERT INTO PollOptions (poll_id, option_text, image_data) VALUES (?, ?, ?)",
							   (poll_id, option_text.strip(), binary_image_data))

		conn.commit()
		return jsonify({"success": True, "message": "Poll updated successfully"})
	except Exception as e:
		if conn:
			conn.rollback()
		print(f"Error updating poll: {str(e)}")
		return jsonify({"success": False, "message": f"Failed to update poll: {str(e)}"}), 500
	finally:
		if conn:
			conn.close()


@app.route('/delete_poll/<int:poll_id>', methods=['DELETE'])
def delete_poll(poll_id):
	"""
	Deletes a poll and all its associated options and votes to maintain data integrity.
	"""
	conn = None
	try:
		conn = get_db_connection()
		cursor = conn.cursor()

		cursor.execute("DELETE FROM Votes WHERE poll_option_id IN (SELECT id FROM PollOptions WHERE poll_id = ?)",
					   (poll_id,))
		cursor.execute("DELETE FROM PollOptions WHERE poll_id = ?", (poll_id,))
		cursor.execute("DELETE FROM Polls WHERE id = ?", (poll_id,))

		conn.commit()
		return jsonify({"success": True, "message": "Poll and its data deleted successfully"})
	except Exception as e:
		if conn:
			conn.rollback()
		print(f"Error deleting poll: {str(e)}")
		return jsonify({"success": False, "message": f"Failed to delete poll: {str(e)}"}), 500
	finally:
		if conn:
			conn.close()


@app.route('/reset_password', methods=['POST'])
def reset_password():
	"""
	Resets a user's password to a new generated one.
	Requires arid_no and new_password.
	"""
	conn = None
	try:
		data = request.get_json()
		arid_no = data.get('arid_no')
		new_password = data.get('new_password')

		if not arid_no or not new_password:
			return jsonify({'success': False, 'error': 'Missing ARID or new password'}), 400

		conn = get_db_connection()
		cursor = conn.cursor()

		cursor.execute(
			"UPDATE Users SET password = ? WHERE arid_no = ?",
			(new_password, arid_no)
		)
		conn.commit()

		if cursor.rowcount == 0:
			return jsonify({'success': False, 'error': 'Student with this ARID number not found'}), 404

		return jsonify({'success': True, 'message': 'Password reset successfully'})

	except Exception as e:
		if conn:
			conn.rollback()
		print(f"Error resetting password: {str(e)}")
		return jsonify({'success': False, 'error': f"Failed to reset password: {str(e)}"}), 500
	finally:
		if conn:
			conn.close()


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)
