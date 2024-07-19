import os
from flask import Flask, render_template
from fastapi import FastAPI
from werkzeug.middleware.dispatcher import DispatcherMiddleware
import spacy
import webbrowser
import threading
from backend.config import Config
from backend.services.pokemon_tcg_api import configure_api
from backend.extensions import db, cache
from backend.routes import api as flask_api

# Get the absolute path to the project root
project_root = os.path.dirname(os.path.abspath(__file__))

# Print the template folder path for debugging
template_folder = os.path.join(project_root, 'backend', 'templates')
print(f"Template folder path: {template_folder}")
print(f"Index.html exists: {os.path.exists(os.path.join(template_folder, 'index.html'))}")

# Initialize FastAPI app
fastapi_app = FastAPI()

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# FastAPI routes
@fastapi_app.get("/chat")
async def root():
    return {"message": "Welcome to PokéDealFinder Chat!"}

@fastapi_app.post("/chat")
async def chat(message: str):
    doc = nlp(message)
    return {"response": f"Received: {message}"}

# Initialize Flask app
flask_app = Flask(__name__, 
                  static_folder=os.path.join(project_root, 'static'),
                  template_folder=template_folder)
flask_app.config.from_object(Config)
Config.init_app(flask_app)

db.init_app(flask_app)
cache.init_app(flask_app)
configure_api()

# Register Flask blueprints
flask_app.register_blueprint(flask_api, url_prefix='/api')

@flask_app.route('/')
def home():
    return render_template('index.html')

# Combine Flask and FastAPI apps using DispatcherMiddleware
app = DispatcherMiddleware(flask_app, {
    '/api/chat': fastapi_app
})

def open_browser():
    try:
        webbrowser.open('http://127.0.0.1:5000/')
    except Exception as e:
        print(f"Failed to open browser: {e}")

if __name__ == '__main__':
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        threading.Timer(1, open_browser).start()
    from werkzeug.serving import run_simple
    run_simple('127.0.0.1', 5000, app, use_reloader=True, use_debugger=True)