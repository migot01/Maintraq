from flask import request, jsonify
from app import app
import uuid

from app.models import User,Requests

user_info=User()
request_model=Requests()

@app.route('/api/v1/register', methods=['POST'])
def register():
    """Route to create user that receive data through a post method"""
    data = request.get_json() #gets data from the api consumer
    if data["username"] in user_info.users:
         return jsonify ({"message":"sorry username taken"})
    data = user_info.add_user(data["username"],
                               data["password"],
                               data["first_name"],
                               data["last_name"]
                               )
    return jsonify({"message":"user created!"})


  
