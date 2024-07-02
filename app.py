from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import errorcode

app = Flask(__name__)
CORS(app)  # Permitir solicitudes CORS

# Configuración de la base de datos
config = {
    'user': 'florlasdica10',
    'password': 'levona1234+',
    'host': 'localhost',
    'database': 'userslevona'
}

def get_database_connection():
    try:
        cnx = mysql.connector.connect(**config)
        if cnx.is_connected():
            print('Connected to MySQL database')
        else:
            print('Connection to MySQL database failed')
        return cnx
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Error de acceso: Verifica tu nombre de usuario o contraseña.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print(f"Error de base de datos: La base de datos '{config['database']}' no existe.")
        else:
            print(f"Error de MySQL: {err}")
    return None

def build_user_data(data, include_id=False, user_id=None):
    user_data = (
        data['name'], 
        data['surname'], 
        data['email'], 
        data['password'], 
        data['phone'], 
        data['dni'], 
        data['address'], 
        data['state'], 
        data.get('admin', 0)
    )
    
    if include_id:
        user_data += (user_id,)
    
    return user_data

@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()

    cnx = get_database_connection()
    if cnx:
        cursor = cnx.cursor()
        add_user = ("INSERT INTO users "
                    "(name, surname, email, password, phone, dni, address, state, admin) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
        user_data = build_user_data(data)
        
        try:
            cursor.execute(add_user, user_data)
            cnx.commit()
            response = {"message": "User registered successfully"}
        except mysql.connector.Error as err:
            response = {"message": "Failed to register user", "error": str(err)}
        finally:
            cursor.close()
            cnx.close()
    else:
        response = {"message": "Failed to connect to the database"}

    return jsonify(response)

@app.route('/get/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    cnx = get_database_connection()
    if cnx:
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM users WHERE id = %s"
        
        try:
            cursor.execute(query, (user_id,))
            user = cursor.fetchone()
            response = user if user else {"message": "User not found"}
        except mysql.connector.Error as err:
            response = {"message": "Failed to get user", "error": str(err)}
        finally:
            cursor.close()
            cnx.close()
    else:
        response = {"message": "Failed to connect to the database"}

    return jsonify(response)

@app.route('/get_by_email/<string:email>', methods=['GET'])
def get_user_by_email(email):
    cnx = get_database_connection()
    if cnx:
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM users WHERE email = %s"
        
        try:
            cursor.execute(query, (email,))
            user = cursor.fetchone()
            response = user if user else {"message": "User not found"}
        except mysql.connector.Error as err:
            response = {"message": "Failed to get user", "error": str(err)}
        finally:
            cursor.close()
            cnx.close()
    else:
        response = {"message": "Failed to connect to the database"}

    return jsonify(response)

@app.route('/update/<int:user_id>', methods=['PUT'])
def update_user_by_id(user_id):
    data = request.get_json()

    cnx = get_database_connection()
    if cnx:
        cursor = cnx.cursor()
        update_query = ("UPDATE users SET name = %s, surname = %s, email = %s, "
                        "password = %s, phone = %s, dni = %s, address = %s, "
                        "state = %s, admin = %s WHERE id = %s")
        user_data = build_user_data(data, include_id=True, user_id=user_id)
        
        try:
            cursor.execute(update_query, user_data)
            cnx.commit()
            response = {"message": "User updated successfully"}
        except mysql.connector.Error as err:
            response = {"message": "Failed to update user", "error": str(err)}
        finally:
            cursor.close()
            cnx.close()
    else:
        response = {"message": "Failed to connect to the database"}

    return jsonify(response)

@app.route('/update_by_email/<string:email>', methods=['PUT'])
def update_user_by_email(email):
    data = request.get_json()

    cnx = get_database_connection()
    if cnx:
        cursor = cnx.cursor()
        update_query = ("UPDATE users SET name = %s, surname = %s, email = %s, "
                        "password = %s, phone = %s, dni = %s, address = %s, "
                        "state = %s, admin = %s WHERE email = %s")
        user_data = build_user_data(data, include_id=False)
        user_data += (email,)
        
        try:
            cursor.execute(update_query, user_data)
            cnx.commit()
            response = {"message": "User updated successfully"}
        except mysql.connector.Error as err:
            response = {"message": "Failed to update user", "error": str(err)}
        finally:
            cursor.close()
            cnx.close()
    else:
        response = {"message": "Failed to connect to the database"}

    return jsonify(response)

@app.route('/delete/<int:user_id>', methods=['DELETE'])
def delete_user_by_id(user_id):
    cnx = get_database_connection()
    if cnx:
        cursor = cnx.cursor()
        delete_query = "DELETE FROM users WHERE id = %s"
        
        try:
            cursor.execute(delete_query, (user_id,))
            cnx.commit()
            response = {"message": "User deleted successfully"}
        except mysql.connector.Error as err:
            response = {"message": "Failed to delete user", "error": str(err)}
        finally:
            cursor.close()
            cnx.close()
    else:
        response = {"message": "Failed to connect to the database"}

    return jsonify(response)

@app.route('/delete_by_email/<string:email>', methods=['DELETE'])
def delete_user_by_email(email):
    cnx = get_database_connection()
    if cnx:
        cursor = cnx.cursor()
        delete_query = "DELETE FROM users WHERE email = %s"
        
        try:
            cursor.execute(delete_query, (email,))
            cnx.commit()
            response = {"message": "User deleted successfully"}
        except mysql.connector.Error as err:
            response = {"message": "Failed to delete user", "error": str(err)}
        finally:
            cursor.close()
            cnx.close()
    else:
        response = {"message": "Failed to connect to the database"}

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
