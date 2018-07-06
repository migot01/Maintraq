from flask import Flask
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
from app.views2 import views2
app.register_blueprint(views2)
from config import app_config
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY_API')