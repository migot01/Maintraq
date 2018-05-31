""" run.py """

import os

from app import views,app

if __name__ == '__main__':
    app.run(debug=True)