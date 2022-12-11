import datetime
import os

class Config:
    API_URL = 'https://api.stormglass.io/v2/'
    API_TOKEN = os.getenv('STORM_GLASS_API_TOKEN')
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 3600
    DEBUG = False
    MONGODB_SETTINGS = {
        'host': os.getenv('MONGODB_URL',"mongodb://localhost/surf-forecast"),
        'uuidRepresentation': 'standard'
    }
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(milliseconds=200_000_000)
    SECRET_KEY = os.getenv('SECRET_KEY')
    RATELIMIT_ENABLED = True
    SWAGGER = {
        "headers": [
            ('Access-Control-Allow-Origin', '*'),
            ('Access-Control-Allow-Methods', "GET, POST, PUT, DELETE, OPTIONS"),
            ('Access-Control-Allow-Credentials', "true"),
        ],
        "specs": [
            {
                "endpoint": 'apispec_1',
                "route": '/apispec_1.json',
                "rule_filter": lambda rule: True,  # all in
                "model_filter": lambda tag: True,  # all in
            }
        ],
        "openapi": "3.0.2",
        "static_url_path": "/flasgger_static",
        # "static_folder": "static",  # must be set by user
        "swagger_ui": True,
        "specs_route": "/docs/"
    }

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
    RATELIMIT_ENABLED = False