from flask import Flask

app = Flask(__name__)
from app.views2 import views2
app.register_blueprint(views2)
from config import app_config
app.config['SECRET_KEY'] = 'thisissecret'