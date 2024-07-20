import os
from flask import Flask
from flask import Flask, render_template
from fastapi import FastAPI
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from src.backend.config import Config
from src.backend.services.pokemon_tcg_api import configure_api
from src.backend.extensions import db, cache
from src.backend.routes import api as flask_api
from src.backend.routes.chat_routes import router as chat_router

def create_flask_app():
    project_root = os.getenv('PROJECT_ROOT')
    template_folder = os.path.join(project_root, 'src', 'backend', 'templates')
    static_folder = os.path.join(project_root, 'static')

    flask_app = Flask(__name__, 
                        static_folder=static_folder,
                        template_folder=template_folder)
    flask_app.config.from_object(Config)
    Config.init_app(flask_app)

    db.init_app(flask_app)
    cache.init_app(flask_app)
    configure_api()

    flask_app.register_blueprint(flask_api, url_prefix='/api')

    # Register the home route directly in the Flask app
    @flask_app.route('/')
    def home():
        return render_template('index.html')

    return flask_app

def create_fastapi_app():
    fastapi_app = FastAPI()
    fastapi_app.include_router(chat_router)
    return fastapi_app

def create_app():
    flask_app = create_flask_app()
    fastapi_app = create_fastapi_app()

    return DispatcherMiddleware(flask_app, {'/api/chat': fastapi_app})