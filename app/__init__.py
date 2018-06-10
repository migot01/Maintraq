from flask import Flask
app = Flask(__name__)
from config import app_config
from app.views2 import views2

app.config['SECRET_KEY'] = 'thisissecret'
def create_app(config_name):
    app = Flask(__name__)
    
    app.register_blueprint(views2)
    return app  