import typing as t
import json

from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from .controllers.beaches import BeachesController
from .controllers.forecast import ForecastController
from .controllers.users import UsersController
from .db import db
from .middlewares.auth import jwt

def setup_app(app: Flask) -> None:
    db.init_app(app)
    jwt.init_app(app)
    app.wsgi_app = ProxyFix(app.wsgi_app,x_for=1,x_proto=1, x_host=1, x_prefix=1)

def create_app(config: t.Union[str, None, t.Dict[str,str]] = None) -> Flask:
    app = Flask(__name__)
    if isinstance(config,dict):
        app.config.update(config)
    if isinstance(config,str) and config.endswith('.json'):
        json_config = json.load(open(config,mode='r'))
        app.config.update(json_config)
    else:
        app.config.from_object(config)
    setup_app(app)
    BeachesController.register(app)
    ForecastController.register(app)
    UsersController.register(app)
    return app
