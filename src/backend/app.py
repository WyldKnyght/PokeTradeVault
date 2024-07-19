from flask import Flask, render_template
from .config import Config
from .services.pokemon_tcg_api import configure_api
from .extensions import db, cache
from .routes import api

def create_app():
    app = Flask(__name__, static_folder='../static', template_folder='../frontend/public')
    app.config.from_object(Config)
    Config.init_app(app)
    
    db.init_app(app)
    cache.init_app(app)
    configure_api()

    # Register blueprints
    app.register_blueprint(api, url_prefix='/api')

    @app.route('/')
    def home():
        return render_template('index.html')

    return app