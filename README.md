[![Build Status](https://travis-ci.org/migot01/Maintraq.svg?branch=master)](https://travis-ci.org/migot01/Maintraq)
[![Coverage Status](https://coveralls.io/repos/github/migot01/Maintraq/badge.svg?branch=master)](https://coveralls.io/github/migot01/Maintraq?branch=master)
![license](https://img.shields.io/github/license/mashape/apistatus.svg)

# Maintraq
MainTraq (from Maintenance Tracker) is an online maintenance/repairs requests tracker that keeps record of maintenance tasks requested by its users within a particular facility. It provides a platform where a user can file a maintenance request online and obtain feedback about the same from the facility admin. The facility can be (but not limited to) an organisation or an organisation's department.

## Hosted versions of the API

https://maintraqa.herokuapp.com/

## API  
Prerequisites  
Python 3.6  
Virtual Environment  
Flask  
Postman  
Postgresql and have a user: postgres and a matching password.
 
## Api Endpoints  
API Endpoints
  
* POST	/api/v2/auth/register	Register a user.  
* POST	/api/v2/auth/login	Login a user.  
* GET	/api/v2/users/requests	Fetch all the requests of a logged in user.  
* GET	/api/v2/users/requests/<int:id>	Fetch a request that belongs to a logged in user.  
* POST	/api/v2/Auth/request	Create a request.  
* PUT	/api/v2/users/requests/<int:id>	Modify a request. This operation should not be possible when the admin has approved of the request.  
* GET	/api/v2/requests	Fetch all the requests. This is available only to admin users.  
* GET	/requests/<int:request_id>	Fetch any of existing requests. This is available only to admin users.  
* PUT	/api/v2/requests/<int:id>/approve	Approve request. This is available only to admin users. When this endpoint is called, the status of the request should be pending.    
* PUT	/api/v2/requests/<int:id>/disapprove	Disapprove request. This is available only to admin users.  
* PUT	/api/v2/requests/<int:id>/resolve	Resolve request. This is available only to admin users.  



### How should this be manually tested?
Clone or download the repo. Navigate to the directory called UI and open any of the html file on any browser.
Clone the repository

git clone https://github.com/migot01/Maintraq/

Change directory

cd Maintraq

Checkout on challenge-3-develop branch

git checkout challenge-3-develop

To view UI designs navigate to the UI/ directory.

cd ui/

Then open index.html on your browser.

To setup API locally, make sure you are in the base project folder Maintenance-Tracker

Set up a virtual environment and activate (python 3.6)

pip install virtualenv virtualenv -p python3.6 venv source venv/bin/activate

Install app dependencies

pip install -r requirements.txt

Set up the database and environment variables.

python migrations.py

     Provide your `postgres` user password.
     Provide a database name on which the app will run
     Ensure database setup is successful.
source .env

python migration.py

Run tests

Either

pytest or

nosetests --exe --with-coverage --cover-package=app

The nosetests give a more comprehensive report about test coverage.

Run the flask app

python run.py

### User Interface Features  
* Users can [register](https://migot01.github.io/Maintraq/UI/register.html) for a free account.  
* Users can [log into their accounts.](https://migot01.github.io/Maintraq/UI/login.html)  
* Users can [make requests to the app.](https://migot01.github.io/Maintraq/UI/userrequest.html)  
* Users can [see all their requests.](https://migot01.github.io/Maintraq/UI/userrequest_list.html)   
* [Admin can respond to a request. ](https://migot01.github.io/Maintraq/UI/adminresponserequest.html) 
* [Admin can log in.](https://migot01.github.io/Maintraq/UI/login.html)  
* [Admin can view all requests made to this app and respond accordingly.](https://migot01.github.io/Maintraq/UI/adminpage.html)   

### Technology Used   
HTML  
CSS  
## Deployment  
Github Pages :https://migot01.github.io/Maintraq/UI/index.html


