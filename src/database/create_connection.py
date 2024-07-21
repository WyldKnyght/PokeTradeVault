# src/database/create_connection.py
import os
import sqlite3
from dotenv import load_dotenv
from .exceptions import DatabaseConnectionError

# Get the absolute path to the project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Load environment variables from .env file in the project root
load_dotenv(os.path.join(PROJECT_ROOT, '.env'))

CARD_DB_PATH = os.getenv('CARD_DB_PATH')

def create_connection():
    try:
        return sqlite3.connect(CARD_DB_PATH)
    except sqlite3.Error as e:
        raise DatabaseConnectionError(
            f"Error creating database connection: {e}"
        ) from e