[![Build Status](https://travis-ci.org/migot01/Maintraq.svg?branch=challenge-2-develop)](https://travis-ci.org/migot01/Maintraq)
[![Coverage Status](https://coveralls.io/repos/github/migot01/Maintraq/badge.svg?branch=challenge-2-develop)](https://coveralls.io/github/migot01/Maintraq?branch=challenge-2-develop)
![license](https://img.shields.io/github/license/mashape/apistatus.svg)

# Maintraq
This is an application that provides users with the ability to reach out to operations or repairs department regarding repair or maintenance requests and monitor the status of their request.  

## API  
Prerequisites  
Python 3.6  
Virtual Environment  
Flask  
 
## Api Endpoints  
### Users Endpoints    
POST /api/v1/register Creates a user account    
POST /api/v1/login Logs in a user    
POST /api/v1/logout Logout a user  
### Request Endpoints  
POST /api/v1/request  Register a new business  
GET /api/v1/request  List all requests  
GET /api/v1/request/requestId  returns a single request  
PUT /api/v1/request/requestId  Update request  
DELETE /api/v2/request/requestId  deletes a request 

### User Interface Features  
* Users can [register](https://migot01.github.io/Maintraq/UI/register.html) for a free account.  
* Users can [log into their accounts.](https://migot01.github.io/Maintraq/UI/login.html)  
* Users can [make requests to the app.](https://migot01.github.io/Maintraq/UI/userrequest.html)  
* Users can [see all their requests.](https://migot01.github.io/Maintraq/UI/userrequest_list.html)   
* [Admin can respond to a request. ](https://migot01.github.io/Maintraq/UI/adminresponserequest.html) 
* [Admin can log in.](https://migot01.github.io/Maintraq/UI/login.html)  
* [Admin can view all requests made to this app and respond accordingly.](https://migot01.github.io/Maintraq/UI/adminpage.html)   
### How should this be manually tested?
Clone or download the repo. Navigate to the directory called UI and open any of the html file on any browser.

### Technology Used   
HTML  
CSS  
## Deployment  
Github Pages :https://migot01.github.io/Maintraq/UI/index.html


