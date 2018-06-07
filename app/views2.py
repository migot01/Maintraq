from flask import request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from app import app
import os
import datetime
from functools import wraps
import jwt
import re

import uuid

from app.models2 import create_user ,get_username, get_user


@app.route('/api/v2/auth/register', methods=['POST'])
def register():
    """Route to create user, it will receive data through a post method"""
    data = request.get_json()  # get data from the api consumer
    if not data or not data['username'].strip() or not data["password"]:
        return jsonify({'message': "username or password missing"})
    if not re.match(r'\A[0-9a-zA-Z!@#$%&*]{6,20}\Z', data['password']):
        return jsonify({"Message": "Password must be 6-20 Characters"}), 406
    username = data['username'].strip()
    if data['username'].strip() in get_username(username):  # test if username exists
        return jsonify({"message": "Sorry!! Username taken!"})
    hashed_password = generate_password_hash(data['password'], method='sha256')
    user = {
        "username": data['username'].strip(),
        "password": hashed_password,
        "first_name": data['first_name'],
        "last_name": data['last_name'],
        "email": data['email']}

    create_user(user)
    return jsonify({"message": "user created!", "Details": 
        {"username": user['username'],
            "first_name": user['first_name'],"last_name": user['last_name'],"email": user['email']
        }}), 201

@app.route('/api/v2/auth/login', methods=['POST'])
def login():
    """login route. users will login to the app via this route"""
    auth = request.get_json()
    if not auth or not auth['username'].strip() or not auth['password']:
        return jsonify({"message": "login required!"}), 401
    user = get_user(auth['username'])
    if user is None:
        return jsonify({"message": "User does not exist"}), 404

    if check_password_hash(user['password'], auth['password']):
        token = jwt.encode({
            'username': user['username'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=1000)},
            app.config["SECRET_KEY"]
        )
        # user_info.user_token[user['username']] = token.decode('UTF-8')
        return jsonify({"auth_token": token.decode('UTF-8')}), 200
    return jsonify({"message": "Wrong password!"}), 401