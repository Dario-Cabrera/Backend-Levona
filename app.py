from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import errorcode

app = Flask(__name__)
CORS(app)  # Esto permite todas las solicitudes CORS, puedes configurarlo para permitir solo ciertos dominios

# Configuración de la base de datos
config = {
    'user': 'florlasdica10',
    'password': 'levona1234+',
    'host': 'localhost',  # Cambia esto si tu host es diferente
    'database': 'Levona1'
}

def connect_to_database():
    try:
        cnx = mysql.connector.connect(**config)
        return cnx
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Algo está mal con tu nombre de usuario o contraseña")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("La base de datos no existe")
        else:
            print(err)
    return None

@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    name = data['name']
    surname = data['surname']
    email = data['email']
    password = data['password']
    phone = data['phone']
    dni = data['dni']
    address = data['address']
    state = data['state']
    admin = data.get('admin', 0)

    cnx = connect_to_database()
    if cnx:
        cursor = cnx.cursor()
        add_user = ("INSERT INTO users "
                    "(name, surname, email, password, phone, dni, address, state, admin) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
        user_data = (name, surname, email, password, phone, dni, address, state, admin)
        
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

if __name__ == '__main__':
    app.run(debug=True)
