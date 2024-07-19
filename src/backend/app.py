from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from config import Config
from .services.pokemon_tcg_service import configure_api

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, static_folder='../static', template_folder='../frontend/public')
    app.config.from_object(Config)
    Config.init_app(app)
    
    db.init_app(app)
    configure_api()

    @app.route('/')
    def home():
        return render_template('index.html')

    return app