from flask import jsonify, request
from app.models import User

def index():
    return jsonify({"message": "Hello World"})

def create_user():
    data = request.json
    new_user = User(name=data['name'], surname=data['surname'], email=data['email'], password=data['password'], phone=data['phone'], dni=data['dni'], address=data['address'], state=data['state'], admin=data['admin'])
    new_user.save()
    return jsonify({"message": "User created successfully"}), 201

def get_all_users():
    users = User.get_all()
    return jsonify([user.serialize() for user in users])

def get_user(id):
    user = User.get_by_id(id)
    if not user: 
        return jsonify({'message': "User not found"}), 404
    return jsonify(user.serialize())

def get_user_by_email(email):
    user = User.get_by_email(email)
    if not user:
        return jsonify({'message': "User not found"}), 404
    return jsonify(user.serialize())

def update_user(id):
    user = User.get_by_id(id)
    if not user: 
        return jsonify({'message': "User not found"}), 404
    data = request.json
    user.name = data['name']
    user.surname = data['surname']
    user.email = data['email']
    user.password = data['password']
    user.phone = data['phone']
    user.dni = data['dni']
    user.address = data['address']
    user.state = data['state']
    user.admin = data['admin']
    user.save()
    return jsonify({'message': "User updated successfully"})

def delete_user(id):
    user = User.get_by_id(id)
    if not user: 
        return jsonify({'message': "User not found"}), 404
    user.delete()
    return jsonify({'message': "User deleted successfully"})