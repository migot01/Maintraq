import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from app.helpers import create_user, check_email,get_title,create_request
from datetime import datetime, timedelta
import jwt
from app import app

class User(object):

   """ """
   def __init__(self, email=None, first_name=None, last_name=None, password=None):
       self.email = email
       self.password = password
       self.first_name = first_name
       self.last_name = last_name
       
       

   def save(self):
       """
       creates a new user and appends to the list
       """
       if check_email(self.email) is False:
           # return relevant message for email regestered
           return ("Fail", "Email already exists")
       else:
           #insert user
           self.password = self.password 
           res = create_user(self.email, self.first_name, self.last_name, self.password)
           return ("Success", "User created!")
   def generate_token(self, email, is_admin, UserID, role):
        """
            Generates the Auth Token for the currently logging in user
            :returns: string
        """
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=60),
                'iat': datetime.utcnow(),
                'sub': email,
                'user_id': UserID,
                'role': role
            }
            return jwt.encode(
                payload,
                app.config["SECRET_KEY"],
                algorithm='HS256'
            )
        except Exception as e:
            return e

class Requests(object):
    """request model. stores all request data"""
    def __init__(self, title=None, location=None, body=None,UserID=None):
        self.title = title
        self.location = location
        self.body = body
        self.UserID = UserID
       


    def add_requests(self):
        """Adds a new request to the requests dictionary"""
        if get_title(self.title):
            return ("Fail", "Title already exists")
        else:
            res = create_request(self.title,self.location,self.body,self.UserID)
            return ("Success", res)
