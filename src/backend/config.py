# src/backend/config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..', '..'))
    DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(DATA_DIR, 'pokemon_cards.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    POKEMON_TCG_API_KEY = os.environ.get('POKEMON_TCG_API_KEY')

    CACHE_TYPE = "SimpleCache"  # You can change this to "RedisCache" or others in production
    CACHE_DEFAULT_TIMEOUT = 300  # 5 minutes
    
    @staticmethod
    def init_app(app):
        if not Config.POKEMON_TCG_API_KEY:
            raise ValueError("No POKEMON_TCG_API_KEY set for this application")
