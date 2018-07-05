from flask import Flask
import os

app = Flask(__name__)
from app.views2 import views2
app.register_blueprint(views2)
from config import app_config
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY_API')