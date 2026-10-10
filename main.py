# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import pyodbc
# from datetime import datetime, timedelta

# app = Flask(__name__)
# CORS(app)
# DB_CONFIG = (
#     r"DRIVER={ODBC Driver 17 for SQL Server};"
#     r"SERVER=FARQULEET\SQLEXPRESS;"
#     r"DATABASE=Polling_SystemDB;"
#     r"UID=sa;"
#     r"PWD=123;"
#     r"Encrypt=no;"
#     r"TrustServerCertificate=yes;"
# )

# def get_db_connection():
#     """Establish database connection"""
#     conn_str = f"DRIVER={{{DB_CONFIG['driver']}}};SERVER={DB_CONFIG['server']};DATABASE={DB_CONFIG['database']};UID={DB_CONFIG['uid']};PWD={DB_CONFIG['pwd']}"
#     return pyodbc.connect(conn_str)


# def verify_admin(arid):
#     """Verify if user is admin"""
#     conn = None
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         cursor.execute("SELECT role FROM Users WHERE arid_no = ?", (arid,))
#         result = cursor.fetchone()
#         if result:
#             role = str(result[0]).strip().lower()
#             return role == 'admin'
#         return False
#     except Exception as e:
#         print(f"Admin verification error: {str(e)}")
#         return False
#     finally:
#         if conn:
#             conn.close()
# @app.route('/login', methods=['POST'])
# def login():
#     conn = None
#     try:
#         data = request.get_json()
#         arid = data.get("arid")
#         password = data.get("password")

#         conn = get_db_connection()
#         cursor = conn.cursor()
#         cursor.execute("""
#             SELECT role, name, arid_no
#             FROM Users
#             WHERE arid_no = ? AND password = ?
#         """, (arid, password))

#         user = cursor.fetchone()

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
# @app.route('/add_user', methods=['POST'])
# def add_user():
#     data = request.get_json()
#     arid_no = data.get('arid_no')
#     password = data.get('password')
#     role = data.get('role', 'student')  # Default to student
#     name = data.get('name')
#     admin_arid = data.get('admin_arid')  # Provided when admin adds a user

#     if not all([arid_no, password, name]):
#         return jsonify({"error": "All fields (arid_no, password, name) are required"}), 400

#     if role == 'admin' and not verify_admin(admin_arid):
#         return jsonify({"error": "Admin privileges required to add an admin user"}), 403

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

# @app.route('/create_poll', methods=['POST'])
# def create_poll():
#     try:
#         data = request.get_json()
#         print(f"Received payload: {data}")
#         title = data['title']
#         description = data.get('description')
#         created_by = data['created_by']
#         is_public = data.get('is_public', True)
#         start_time = data.get('start_time')
#         end_time = data.get('end_time')
#         options = data.get('options', [])

#         # Validate inputs
#         if not title or not created_by or len(options) < 2:
#             return jsonify({"success": False, "message": "Title, created_by, and at least 2 options are required"}), 400

#         conn = get_db_connection()
#         cursor = conn.cursor()

#         print(f"Inserting poll: title={title}, created_by={created_by}, start_time={start_time}, end_time={end_time}, is_public={is_public}, options={options}")

#         # Use OUTPUT clause to get the inserted id
#         cursor.execute("""
#             INSERT INTO Polls (title, description, created_by, is_public, start_time, end_time)
#             OUTPUT INSERTED.id
#             VALUES (?, ?, ?, ?, ?, ?)
#         """, (title, description, created_by, is_public, start_time, end_time))
#         poll_id_row = cursor.fetchone()
#         print(f"OUTPUT result: {poll_id_row}")

#         if not poll_id_row or poll_id_row[0] is None:
#             conn.rollback()
#             conn.close()
#             return jsonify({"success": False, "message": "Failed to retrieve poll ID"}), 500

#         poll_id = int(poll_id_row[0])
#         print(f"Retrieved poll_id: {poll_id}")

#         for opt in options:
#             cursor.execute("INSERT INTO PollOptions (poll_id, option_text) VALUES (?, ?)", (poll_id, opt))
#             print(f"Inserted option: {opt}")

#         conn.commit()
#         conn.close()
#         return jsonify({"success": True, "poll_id": poll_id})

#     except Exception as e:
#         print(f"Error creating poll: {str(e)}")
#         return jsonify({"success": False, "message": str(e)}), 500
# @app.route('/get_polls', methods=['GET'])
# def get_polls():
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute("SELECT id, title, description, is_public, start_time, end_time FROM Polls")
#     rows = cursor.fetchall()
#     conn.close()

#     polls = [{
#         "id": row[0],
#         "title": row[1],
#         "description": row[2],
#         "is_public": row[3],
#         "start_time": str(row[4]) if row[4] else None,
#         "end_time": str(row[5]) if row[5] else None,
#     } for row in rows]

#     return jsonify(polls)
# @app.route('/get_poll/<int:poll_id>', methods=['GET'])
# def get_poll(poll_id):
#     conn = get_db_connection()
#     cursor = conn.cursor()

#     cursor.execute("SELECT id, title, description FROM Polls WHERE id = ?", (poll_id,))
#     poll = cursor.fetchone()
#     if not poll:
#         return jsonify({"error": "Poll not found"}), 404

#     cursor.execute("SELECT id, option_text FROM PollOptions WHERE poll_id = ?", (poll_id,))
#     options = [{"id": row[0], "text": row[1]} for row in cursor.fetchall()]

#     conn.close()
#     return jsonify({
#         "id": poll[0],
#         "title": poll[1],
#         "description": poll[2],
#         "options": options
#     })

# @app.route('/vote', methods=['POST'])
# def vote():
#     data = request.get_json()
#     arid_no = data['arid_no']
#     option_id = data['option_id']

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

#     cursor.execute("INSERT INTO Votes (user_arid_no, poll_option_id) VALUES (?, ?)", (arid_no, option_id))
#     conn.commit()
#     conn.close()
#     return jsonify({"success": True})
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

#     results = [{"option": row[0], "votes": row[1]} for row in cursor.fetchall()]
#     conn.close()
#     return jsonify(results)

# @app.route('/update_poll/<int:poll_id>', methods=['PUT'])
# def update_poll(poll_id):
#     data = request.get_json()
#     title = data.get('title')
#     description = data.get('description')
#     #is_public = data.get('is_public', True)
#     is_public = data.get('is_public')
#     start_time = data.get('start_time')
#     end_time = data.get('end_time')
#     options = data.get('options', [])  # list of option texts

#     if not title or len(options) < 2:
#         return jsonify({"success": False, "message": "Title and at least 2 options required"}), 400

#     conn = get_db_connection()
#     cursor = conn.cursor()

#     # Update Poll main data
#     cursor.execute("""
#         UPDATE Polls
#         SET title = ?, description = ?, is_public = ?, start_time = ?, end_time = ?
#         WHERE id = ?
#     """, (title, description, is_public, start_time, end_time, poll_id))

#     # Delete existing options for the poll
#     cursor.execute("DELETE FROM PollOptions WHERE poll_id = ?", (poll_id,))

#     # Insert new options
#     for option_text in options:
#         cursor.execute("INSERT INTO PollOptions (poll_id, option_text) VALUES (?, ?)", (poll_id, option_text))

#     conn.commit()
#     conn.close()

#     return jsonify({"success": True, "message": "Poll updated successfully"})

# @app.route('/delete_poll/<int:poll_id>', methods=['DELETE'])
# def delete_poll(poll_id):
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute("DELETE FROM Votes WHERE poll_option_id IN (SELECT id FROM PollOptions WHERE poll_id = ?)", (poll_id,))
#     cursor.execute("DELETE FROM PollOptions WHERE poll_id = ?", (poll_id,))
#     cursor.execute("DELETE FROM Polls WHERE id = ?", (poll_id,))
#     conn.commit()
#     conn.close()
#     return jsonify({"success": True})

# @app.route('/reset_password', methods=['POST'])
# def reset_password():
#     data = request.get_json()
#     arid_no = data.get('arid_no')
#     new_password = data.get('new_password')

#     if not arid_no or not new_password:
#         return jsonify({'success': False, 'error': 'Missing ARID or password'}), 400

#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()

#         # Update the password in the database
#         cursor.execute(
#             "UPDATE Users SET password = ? WHERE arid_no = ?",
#             (new_password, arid_no)
#         )

#         conn.commit()

#         if cursor.rowcount == 0:
#             return jsonify({'success': False, 'error': 'Student not found'}), 404

#         return jsonify({'success': True}), 200

#     except Exception as e:
#         return jsonify({'success': False, 'error': str(e)}), 500

#     finally:
#         cursor.close()
#         conn.close()

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)
from flask import Flask, request, jsonify
from flask_cors import CORS
import pyodbc
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

# Database config as a dictionary
DB_CONFIG = {
    "driver": "ODBC Driver 17 for SQL Server",
    "server": "FARQULEET\\SQLEXPRESS",
    "database": "Polling_SystemDB",
    "uid": "sa",
    "pwd": "123"
}

def get_db_connection():
    """Establish database connection"""
    conn_str = (
        f"DRIVER={{{DB_CONFIG['driver']}}};"
        f"SERVER={DB_CONFIG['server']};"
        f"DATABASE={DB_CONFIG['database']};"
        f"UID={DB_CONFIG['uid']};"
        f"PWD={DB_CONFIG['pwd']};"
        f"Encrypt=no;"
        f"TrustServerCertificate=yes;"
    )
    return pyodbc.connect(conn_str)

def verify_admin(arid):
    """Verify if user is admin"""
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

@app.route('/login', methods=['POST'])
def login():
    conn = None
    try:
        data = request.get_json()
        arid = data.get("arid")
        password = data.get("password")

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT role, name, arid_no
            FROM Users 
            WHERE arid_no = ? AND password = ?
        """, (arid, password))

        user = cursor.fetchone()

        if user:
            role = str(user[0]).strip().lower()
            return jsonify({
                "success": True,
                "role": role,
                "name": user[1],
                'arid_no': user[2]
            })
        return jsonify({"success": False, "message": "Invalid credentials"}), 401
        if conn:
            conn.close()
    except Exception as e:
        print(f"Login error: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        pass

@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    arid_no = data.get('arid_no')
    password = data.get('password')
    role = data.get('role', 'student')
    name = data.get('name')
    admin_arid = data.get('admin_arid')

    if not all([arid_no, password, name]):
        return jsonify({"error": "All fields (arid_no, password, name) are required"}), 400

    if role == 'admin' and not verify_admin(admin_arid):
        return jsonify({"error": "Admin privileges required to add an admin user"}), 403

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO Users (arid_no, password, role, name) VALUES (?, ?, ?, ?)",
            (arid_no, password, role, name)
        )
        conn.commit()
        return jsonify({"success": True, "message": "User added successfully"})
    except pyodbc.IntegrityError as e:
        if "Violation of PRIMARY KEY constraint" in str(e):
            return jsonify({"error": "User already has an account"}), 400
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Error adding user: {str(e)}"}), 500
    finally:
        conn.close()

@app.route('/create_poll', methods=['POST'])
def create_poll():
    try:
        data = request.get_json()
        title = data['title']
        description = data.get('description')
        created_by = data['created_by']
        is_public = data.get('is_public', True)
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        options = data.get('options', [])

        if not title or not created_by or len(options) < 2:
            return jsonify({"success": False, "message": "Title, created_by, and at least 2 options are required"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO Polls (title, description, created_by, is_public, start_time, end_time)
            OUTPUT INSERTED.id
            VALUES (?, ?, ?, ?, ?, ?)
        """, (title, description, created_by, is_public, start_time, end_time))
        poll_id_row = cursor.fetchone()

        if not poll_id_row or poll_id_row[0] is None:
            conn.rollback()
            conn.close()
            return jsonify({"success": False, "message": "Failed to retrieve poll ID"}), 500

        poll_id = int(poll_id_row[0])

        for opt in options:
            cursor.execute("INSERT INTO PollOptions (poll_id, option_text) VALUES (?, ?)", (poll_id, opt))

        conn.commit()
        conn.close()
        return jsonify({"success": True, "poll_id": poll_id})

    except Exception as e:
        print(f"Error creating poll: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/get_polls', methods=['GET'])
def get_polls():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, description, is_public, start_time, end_time FROM Polls")
    rows = cursor.fetchall()
    conn.close()

    polls = [{
        "id": row[0],
        "title": row[1],
        "description": row[2],
        "is_public": row[3],
        "start_time": str(row[4]) if row[4] else None,
        "end_time": str(row[5]) if row[5] else None,
    } for row in rows]

    return jsonify(polls)

@app.route('/get_poll/<int:poll_id>', methods=['GET'])
def get_poll(poll_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, title, description FROM Polls WHERE id = ?", (poll_id,))
    poll = cursor.fetchone()
    if not poll:
        return jsonify({"error": "Poll not found"}), 404

    cursor.execute("SELECT id, option_text FROM PollOptions WHERE poll_id = ?", (poll_id,))
    options = [{"id": row[0], "text": row[1]} for row in cursor.fetchall()]

    conn.close()
    return jsonify({
        "id": poll[0],
        "title": poll[1],
        "description": poll[2],
        "options": options
    })

@app.route('/vote', methods=['POST'])
def vote():
    data = request.get_json()
    arid_no = data['arid_no']
    option_id = data['option_id']


    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 1 FROM Votes WHERE user_arid_no = ? AND poll_option_id IN (
            SELECT id FROM PollOptions WHERE poll_id = (
                SELECT poll_id FROM PollOptions WHERE id = ?
            )
        )
    """, (arid_no, option_id))
    if cursor.fetchone():
        conn.close()
        return jsonify({"success": False, "message": "You already voted"}), 400

    cursor.execute("INSERT INTO Votes (user_arid_no, poll_option_id) VALUES (?, ?)", (arid_no, option_id))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

@app.route('/poll_results/<int:poll_id>', methods=['GET'])
def poll_results(poll_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT PO.option_text, COUNT(V.id) as votes
        FROM PollOptions PO
        LEFT JOIN Votes V ON PO.id = V.poll_option_id
        WHERE PO.poll_id = ?
        GROUP BY PO.option_text
    """, (poll_id,))

    results = [{"option": row[0], "votes": row[1]} for row in cursor.fetchall()]
    conn.close()
    return jsonify(results)

@app.route('/update_poll/<int:poll_id>', methods=['PUT'])
def update_poll(poll_id):
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    is_public = data.get('is_public')
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    options = data.get('options', [])

    if not title or len(options) < 2:
        return jsonify({"success": False, "message": "Title and at least 2 options required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE Polls
        SET title = ?, description = ?, is_public = ?, start_time = ?, end_time = ?
        WHERE id = ?
    """, (title, description, is_public, start_time, end_time, poll_id))

    cursor.execute("DELETE FROM PollOptions WHERE poll_id = ?", (poll_id,))
    for option_text in options:
        cursor.execute("INSERT INTO PollOptions (poll_id, option_text) VALUES (?, ?)", (poll_id, option_text))

    conn.commit()
    conn.close()
    return jsonify({"success": True, "message": "Poll updated successfully"})

@app.route('/delete_poll/<int:poll_id>', methods=['DELETE'])
def delete_poll(poll_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Delete all related votes
    cursor.execute("DELETE FROM Votes WHERE poll_option_id IN (SELECT id FROM PollOptions WHERE poll_id = ?)", (poll_id,))

    # Delete poll options
    cursor.execute("DELETE FROM PollOptions WHERE poll_id = ?", (poll_id,))

    # Delete the poll
    cursor.execute("DELETE FROM Polls WHERE id = ?", (poll_id,))

    conn.commit()
    conn.close()

    return jsonify({"success": True, "message": "Poll deleted successfully"})
@app.route('/reset_password', methods=['POST'])
def reset_password():
    data = request.get_json()
    arid_no = data.get('arid_no')
    new_password = data.get('new_password')

    if not arid_no or not new_password:
        return jsonify({'success': False, 'error': 'Missing ARID or password'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Update the password in the database
        cursor.execute(
            "UPDATE Users SET password = ? WHERE arid_no = ?",
            (new_password, arid_no)
        )

        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({'success': False, 'error': 'Student not found'}), 404

        return jsonify({'success': True}), 200

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

