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

from app.models import User,Requests

user_info=User()
request_model=Requests()


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
            if data['username'] in user_info.user_token:
                current_user = user_info.users[data['username']]
            else:
                return jsonify({"message": "You are not logged in"}), 401
        except:
            return jsonify({'message': 'Token is invalid or Expired!'}), 401

        return f(current_user, *args, **kwargs)
    return decorated

@app.route('/api/v1/register', methods=['POST'])
def register():
    """Route to create user, it will receive data through a post method"""
    try:
        data = request.get_json()  # get data from the api consumer
        if not data or not data['username'].strip() or not data["password"]:
            return jsonify({'message': "username or password missing"})
        if not re.match(r'\A[0-9a-zA-Z!@#$%&*]{6,20}\Z', data['password']):
            return jsonify({"Message": "Password must be 6-20 Characters"}), 406
        if data['username'].strip() in user_info.users:  # test if username exists
            return jsonify({"message": "Sorry!! Username taken!"})
        hashed_password = generate_password_hash(data['password'], method='sha256')
        user = user_info.add_user(data['username'].strip(),hashed_password,
                                   data['first_name'],
                                   data['last_name'])
        return jsonify({"message": "user created!", "Details": 
            {"id": user['id'],"username": user['username'],
                "first_name": user['first_name'],"last_name": user['last_name']
            }}), 201
    except Exception as e:
        return jsonify({
            "Error": "Error!, check you are sending correct information"}), 400

@app.route('/api/v1/login', methods=['POST'])
def login():
    """login route. users will login to the app via this route"""
    try:
        auth = request.get_json()
        if not auth or not auth['username'].strip() or not auth['password']:
            return jsonify({"message": "login required!"}), 401
        if auth['username'].strip() not in user_info.users.keys():
            return jsonify({"message": "Username not found!"}), 401
        user = user_info.users[auth['username'].strip()]
        if check_password_hash(user['password'], auth['password']):
            token = jwt.encode({
                'username': user['username'],
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=1000)},
                app.config["SECRET_KEY"]
            )
            user_info.user_token[user['username']] = token.decode('UTF-8')
            return jsonify({"auth_token": token.decode('UTF-8')}), 200
        return jsonify({"message": "Wrong password!"}), 401
    except Exception as e:
        return jsonify({
            "Error": "Error!, check you are sending correct information"}), 400

@app.route('/api/v1/request', methods=['POST'])
@login_required
def create_request(current_user):
    """endpoint to create a new request"""
    try:
        data = request.get_json()
        if not data or not data['title'].strip():
            return jsonify({"message": "Name cannot be empty!"}), 401
        for req in request_model.requests.values():
            if data['title'].strip() == req['title']:
                return jsonify({"message": "Sorry!! Name taken!"}), 401
        # update request
        user_id = current_user['username']
        create = request_model.add_requests(data['title'].strip(),
                                               data['location'], data['body'],user_id)
        return jsonify({
            "message": "Request created", 'request': create
        }), 201
    except Exception as e:
        return jsonify({
            "Error": "Error!, check you are sending correct information"
        }), 400





