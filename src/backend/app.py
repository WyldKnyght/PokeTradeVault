from flask import Flask, render_template
from .config import Config
from .services.pokemon_tcg_api import configure_api
from .extensions import db, cache
from .routes import api
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
import spacy

# Initialize Flask app
flask_app = Flask(__name__)

# Initialize FastAPI app
fastapi_app = FastAPI()

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# FastAPI routes
@fastapi_app.get("/api/chat")
async def root():
    return {"message": "Welcome to PokéDealFinder Chat!"}

@fastapi_app.post("/api/chat")
async def chat(message: str):
    doc = nlp(message)
    # Basic NLP processing, to be expanded later
    return {"response": f"Received: {message}"}

# Mount FastAPI app under Flask app
flask_app.wsgi_app = WSGIMiddleware(fastapi_app)

'''
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
'''