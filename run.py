""" run.py """
from app import create_app
import os

from app import views,app

if __name__ == '__main__':
    app.run(debug=True)