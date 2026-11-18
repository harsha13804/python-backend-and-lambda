
from flask import Flask, jsonify, request
import pymysql

app = Flask(__name__)

# =========================
# RDS MASTER / WRITER CONFIG
# =========================
RDS_HOST = 'hvrdb.caf4ksk2sbq9.us-east-1.rds.amazonaws.com'
RDS_USER = 'admin'
RDS_PASSWORD = '12345678'
RDS_DB_NAME = 'hvrdb'
TABLE_NAME = 'users'


# =========================
# DATABASE CONNECTION
# =========================
def get_connection():
    return pymysql.connect(
        host=RDS_HOST,
        user=RDS_USER,
        password=RDS_PASSWORD,
        database=RDS_DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )


# =========================
# GET ALL USERS
# =========================
@app.route('/users', methods=['GET'])
def get_users():
    try:
        connection = get_connection()

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users LIMIT 10")
            users = cursor.fetchall()

        connection.close()
        return jsonify(users), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================
# GET USER BY ID
# =========================
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        connection = get_connection()

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM users WHERE id = %s",
                (user_id,)
            )
            user = cursor.fetchone()

        connection.close()

        if user:
            return jsonify(user), 200

        return jsonify({"message": "User not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================
# POST - CREATE USER
# =========================
@app.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()

        if not data or not data.get('name') or not data.get('email'):
            return jsonify({
                "error": "Name and email are required"
            }), 400

        connection = get_connection()

        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO users (name, email) VALUES (%s, %s)",
                (data['name'], data['email'])
            )
            user_id = cursor.lastrowid

        connection.commit()
        connection.close()

        return jsonify({
            "message": "User created successfully",
            "id": user_id
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================
# PUT - UPDATE USER
# =========================
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        data = request.get_json()

        if not data or not data.get('name') or not data.get('email'):
            return jsonify({
                "error": "Name and email are required"
            }), 400

        connection = get_connection()

        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE users SET name=%s, email=%s WHERE id=%s",
                (data['name'], data['email'], user_id)
            )
            updated = cursor.rowcount

        connection.commit()
        connection.close()

        if updated == 0:
            return jsonify({"message": "User not found"}), 404

        return jsonify({
            "message": "User updated successfully"
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================
# DELETE USER
# =========================
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        connection = get_connection()

        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM users WHERE id=%s",
                (user_id,)
            )
            deleted = cursor.rowcount

        connection.commit()
        connection.close()

        if deleted == 0:
            return jsonify({"message": "User not found"}), 404

        return jsonify({
            "message": "User deleted successfully"
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================
# HEALTH CHECK
# =========================
@app.route('/')
def index():
    return "RDS Master API running"


# =========================
# ENTRY POINT
# =========================
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
