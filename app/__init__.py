from flask import Flask
app = Flask(__name__)
from config import app_config


app.config['SECRET_KEY'] = 'thisissecret'

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])