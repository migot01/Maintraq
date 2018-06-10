""" run.py """
from app import views2,app
from app import create_app
import os

app = create_app("development")
if __name__ == '__main__':
    app.run(debug=True)