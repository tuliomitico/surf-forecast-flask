import datetime
import os

class Config:
    DEBUG = False
    API_URL = 'https://api.stormglass.io/v2/'
    API_TOKEN = os.getenv('STORM_GLASS_API_TOKEN')
    MONGODB_SETTINGS = {
        'db': 'surf-forecast',
        'uuidRepresentation': 'standard'
    }
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(milliseconds=200_000_000)

class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True

class ProductionConfig(Config):
    pass

class TestingConfig(Config):
    TESTING=True
    API_TOKEN = 'test-token'
    MONGODB_SETTINGS = {
        'host': "mongomock://localhost",
        "db": 'surf-forecast-test'
    }
    SECRET_KEY = 'test'
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(milliseconds=10000)