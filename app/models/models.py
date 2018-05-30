import uuid

class User(object):
   
   def __init__(self):
       self.users={}
       self.user_token={}

   def add_user(self,username,password,first_name,last_name):
       """
       creates a new user and appends to the list
       """
       data={"id":uuid.uuid4(),"username":username, "password":password ,
             "first_name":first_name,"last_name":last_name}
       self.users[username] = data
       return self.users[username]

class Requests(object):
    """request model. stores all request data"""
    def __init__(self):
        self.requests = {}

    def add_requests(self, title, location, category, body, user_id):
        """Adds a new request to the requests dictionary"""
        id=str(len(self.requests)+1)
        new_request = {
              "id" : id,
              "title": title,
              "location": location,
              "body": body,
              "user_id": user_id
        }
        self.requests[id] = new_request
        return self.requests[id]


 
