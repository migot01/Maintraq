from flask import request, jsonify, make_response, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
# from app import create_app
import os
from app import app
import datetime
from functools import wraps
import jwt
import re
from app.models2 import User,Requests


import uuid

from app.helpers import create_user , get_user,get_title,get_username,create_request,get_requests,\
get_request,updated_request,admin_get_all,admin_get_request_by_id ,approve_request,disapprove_request,\
resolve_request

views2 = Blueprint('views2', __name__)
user = User()

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
            email = data.get('sub')
            user.role = data.get('role')
            current_user = get_user(email)
            if not current_user:
                return jsonify({"message": "You are not logged in"}), 401
            
        except:
            return jsonify({'message': 'Token is invalid or Expired!'}), 401

        return f(current_user, *args, **kwargs)
    return decorated

def role_required(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if user.role not in roles:
                return jsonify({
                    'message': 'Permission denied!'
                }), 403
            return f(*args, **kwargs)
        return wrapped
    return wrapper

@views2.route('/api/v2/auth/login', methods=['POST'])
def login():
    """login route. users will login to the app via this route"""
    auth = request.get_json()
    if not auth or not auth['email'].strip() or not auth['password']:
        return jsonify({"message": "login required!"}), 401


    user = get_user(auth['email'])
    # return(jsonify(user))
    if user is None:
        return jsonify({"message": "User does not exist"}), 404
    
    if (user['password'] == auth['password']):
        token = User().generate_token(user['email'], user['first_name'], user['id'], user['role'])
            
        #get_token[user['username']] = token.decode('UTF-8')
        return jsonify({"auth_token": token.decode('UTF-8')}), 200
    return jsonify({"message": "Wrong password!"}), 401

@views2.route('/api/v2/auth/register', methods=['POST'])
def register():
    """Route to create user, it will receive data through a post method"""
    data = request.get_json()  # get data from the api consumer
    try:
        email = data['email'].strip(),
        first_name = data['first_name'].strip(),
        last_name = data['last_name'].strip(),
        password = data['password']
    except Exception:
        return jsonify({'message': "email or password missing"}), 400

    if not data or not email or not first_name or not last_name or not password:
        return jsonify({'message': "email or password missing"}), 400

    if not re.match(r'\A[0-9a-zA-Z!@#$%&*]{6,20}\Z', data['password']):
        return jsonify({"Message": "Password must be 6-20 Characters"}), 406

    user = User(email, first_name, last_name, password)
    result = user.save()
    print(result)
    if result[0] == "Fail":
        return jsonify({'message': "Email already exists"}), 409
    return jsonify({
            "message": result[1],
            "first_name": first_name,
            "last_name": last_name,
            "email": email
        }), 201

@views2.route('/api/v2/Auth/request', methods=['POST'])
@login_required
@role_required(0)
def create_requests(current_user):
    """endpoint to create a new request"""
    
    data = request.get_json()
    title = data['title'].strip(),
    location = data['location'].strip(),
    body = data['body'].strip(),
    #UserID = data['UserID']
    # return(current_user)
    UserID = current_user['id']
    requests = Requests(title,location,body,UserID)
    result=requests.add_requests()
    if result[0] == "Fail":
        return jsonify({
            "message": result[1]
        }), 201
    return jsonify({
        'message': "Created successfully",
        'request_title': title
    })

@views2.route('/api/v2/users/requests', methods=['GET'])
@login_required
@role_required(0)
def get_all_requests(current_user):

    """Gets all requests"""
    requests = get_requests(current_user['id'])
    return jsonify({'request': requests})

@views2.route('/api/v2/users/requests/<int:id>', methods=['GET'])
@login_required
@role_required(0)
def get_reqsts(current_user,id):
    requests = get_request(id,current_user["id"])
    return jsonify({'request': requests})

@views2.route('/api/v2/users/requests/<int:id>', methods=['PUT'])
@login_required
@role_required(0)
def update_request( current_user,id):
    
    """ Get request id and update request"""
    data = request.get_json()
    
    try:
        req = get_request(id, current_user['id'])
        if not req:
            return jsonify({"message": "request not found"})
        if req['userid'] == current_user['id']:
            location = data['location']
            title = data['title']
            body = data['body']
            updated_request(id,title,location,body)
            return jsonify({
                    "message": "request updated!",
                    "request": title
                }), 202
        else:
            return jsonify({
                'message': "Update request denied"
            }), 403
    except Exception as e:
        print(e)

@views2.route('/api/v2/requests', methods=['GET'])
@login_required
@role_required(1)
def admin_get_all_requests(current_user):

    """Gets all requests"""
    requests = admin_get_all(current_user['id'])
    return jsonify({'request': requests})

@views2.route('/api/v2/requests/<int:id>', methods=['GET'])
@login_required
@role_required(1)
def admin_get_request(current_user,id):

    """Gets a single  requests"""
    requests = admin_get_request_by_id(id)
    return jsonify({'request': requests})
        
