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

from app.models2 import create_user , get_user,get_title,get_username,create_request
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'access-token' not in request.headers:
            return jsonify({
                'message': 'Token is missing, login to get token'
            }), 401
        try:
            token = request.headers['access-token']
            data = jwt.decode(token, app.config["SECRET_KEY"])
            username = data['username'].strip()
            current_user = get_user(username)
            if not current_user:
                return jsonify({"message": "You are not logged in"}), 401
            
        except:
            return jsonify({'message': 'Token is invalid or Expired!'}), 401

        return f(current_user, *args, **kwargs)
    return decorated

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
        #get_token[user['username']] = token.decode('UTF-8')
        return jsonify({"auth_token": token.decode('UTF-8')}), 200
    return jsonify({"message": "Wrong password!"}), 401

@app.route('/api/v2/Auth/request', methods=['POST'])
@login_required
def create_requests(current_user):
    """endpoint to create a new request"""
    
    data = request.get_json()
    #if not data or not data['title'].strip():
        #return jsonify({"message": "Name cannot be empty!"}), 401
    #title=data['title'].strip()
    #for req in get_title(title):
        #if data['title'].strip() == req['title']:
           # return jsonify({"message": "Sorry!! Name taken!"}), 401
    # create request
    UserID = current_user['id']
    
    requests = {
    "title": data['title'].strip(),
    "location": data['location'],
    "body": data['body'],
    "UserID" : UserID
    
    }
    create_request(requests)
    return jsonify({
        "message": "Request created", 'request': requests
    }), 201
   