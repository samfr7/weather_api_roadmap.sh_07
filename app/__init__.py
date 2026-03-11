from flask import Flask
from .api.routes import bp
from .extensions import cors, limiter
from .utils import register_error_handlers
from .config import ProductionConfig, TestingConfig, DevelopmentConfig
from logging_config import setup_logging
import os

def create_app():

    setup_logging()

    app = Flask(__name__)

    # Fetch an environment variable to determine the environment
    env = os.environ.get('FLASK_ENV', 'development')
    
    if env == 'production':
        app.config.from_object(ProductionConfig)
    elif env == 'testing':
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    # initiating with CORS

    cors.init_app(app=app)
    limiter.init_app(app=app)

    app.register_blueprint(blueprint=bp)

    register_error_handlers(app)

    return app


