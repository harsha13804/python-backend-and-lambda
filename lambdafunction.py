
import json
import os
import pymysql

# =========================
# RDS CONFIGURATION
# =========================
RDS_HOST = 'hvrdb.caf4ksk2sbq9.us-east-1.rds.amazonaws.com'
RDS_USER = 'admin'
RDS_PASSWORD = '12345678'
RDS_DB_NAME = 'dev'


# =========================
# DATABASE CONNECTION
# =========================
def get_connection():
    return pymysql.connect(
        host=RDS_HOST,
        user=RDS_USER,
        password=RDS_PASSWORD,
        database=RDS_DB_NAME,
        cursorclass=pymysql.cursors.DictCursor,
        connect_timeout=5
    )


# =========================
# RESPONSE FORMAT
# =========================
def response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        },
        'body': json.dumps(body, default=str)
    }


# =========================
# LAMBDA HANDLER
# =========================
def lambda_handler(event, context):

    method = (
        event.get('requestContext', {})
        .get('http', {})
        .get('method')
        or event.get('httpMethod', '')
    )

    path = event.get('rawPath') or event.get('path', '')

    # Remove trailing slash
    path = path.rstrip('/')

    # Health check
    if method == 'GET' and path == '':
        return response(200, {
            'message': 'RDS Lambda API running'
        })

    # CORS preflight
    if method == 'OPTIONS':
        return response(200, {'message': 'OK'})

    # Identify user ID
    parts = path.split('/')
    user_id = None

    if len(parts) == 3 and parts[1] == 'users':
        try:
            user_id = int(parts[2])
        except ValueError:
            return response(400, {'error': 'Invalid user ID'})

    elif path != '/users':
        return response(404, {'error': 'Route not found'})

    # Parse request body
    data = {}

    if method in ('POST', 'PUT'):
        try:
            data = json.loads(event.get('body') or '{}')
        except (json.JSONDecodeError, TypeError):
            return response(400, {'error': 'Invalid JSON body'})

        if not isinstance(data, dict):
            return response(400, {'error': 'JSON body must be an object'})

        if not data.get('name') or not data.get('email'):
            return response(400, {
                'error': 'Name and email are required'
            })

    connection = None

    try:
        connection = get_connection()

        with connection.cursor() as cursor:

            # =========================
            # GET ALL USERS
            # =========================
            if method == 'GET' and path == '/users':

                cursor.execute(
                    "SELECT * FROM users LIMIT 10"
                )

                users = cursor.fetchall()

                return response(200, users)

            # =========================
            # GET USER BY ID
            # =========================
            elif method == 'GET' and user_id is not None:

                cursor.execute(
                    "SELECT * FROM users WHERE id = %s",
                    (user_id,)
                )

                user = cursor.fetchone()

                if not user:
                    return response(404, {
                        'message': 'User not found'
                    })

                return response(200, user)

            # =========================
            # POST - CREATE USER
            # =========================
            elif method == 'POST' and path == '/users':

                cursor.execute(
                    "INSERT INTO users (name, email) VALUES (%s, %s)",
                    (data['name'], data['email'])
                )

                new_id = cursor.lastrowid
                connection.commit()

                return response(201, {
                    'message': 'User created successfully',
                    'id': new_id
                })

            # =========================
            # PUT - UPDATE USER
            # =========================
            elif method == 'PUT' and user_id is not None:

                cursor.execute(
                    "SELECT id FROM users WHERE id = %s",
                    (user_id,)
                )

                if not cursor.fetchone():
                    return response(404, {
                        'message': 'User not found'
                    })

                cursor.execute(
                    "UPDATE users SET name=%s, email=%s WHERE id=%s",
                    (data['name'], data['email'], user_id)
                )

                connection.commit()

                return response(200, {
                    'message': 'User updated successfully'
                })

            # =========================
            # DELETE USER
            # =========================
            elif method == 'DELETE' and user_id is not None:

                cursor.execute(
                    "DELETE FROM users WHERE id = %s",
                    (user_id,)
                )

                deleted = cursor.rowcount

                if deleted == 0:
                    return response(404, {
                        'message': 'User not found'
                    })

                connection.commit()

                return response(200, {
                    'message': 'User deleted successfully'
                })

            else:
                return response(405, {
                    'error': 'Method not allowed'
                })

    except Exception as e:
        if connection:
            connection.rollback()

        print("Database error:", str(e))

        return response(500, {
            'error': 'Internal server error'
        })

    finally:
        if connection:
            connection.close()
