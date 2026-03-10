from flask import Flask
from .api.routes import bp
from .extensions import cors, limiter

def create_app():

    app = Flask(__name__)

    # initiating with CORS

    cors.init_app(app=app)
    limiter.init_app(app=app)

    app.register_blueprint(blueprint=bp)

    return app


