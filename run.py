""" run.py """
from app import create_app
import os

from app import views2,app

if __name__ == '__main__':
    app.run(debug=True)