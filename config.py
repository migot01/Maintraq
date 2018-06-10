import os
import psycopg2

base_dir = os.path.abspath(os.path.dirname(__file__))

try:
    #connect to database
    conn = psycopg2.connect("dbname='maintraq_test' user='postgres' host='localhost' password='myadmin01?'")
    
    
except:
    print("database not connected")

# config.py
class Config(object):
    """Default configuration"""

    DEBUG = True
    TESTING = True

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = True

class ProductionConfig(Config):
    """Development configuration"""
    DEBUG = False
    TESTING = False

app_config = {
    "development" : DevelopmentConfig,
    "production" : ProductionConfig,
    "testing" : TestingConfig
}