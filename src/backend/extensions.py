# src\backend\extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from fastapi import FastAPI
import spacy

# Initialize FastAPI
fastapi = FastAPI()

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

db = SQLAlchemy()
cache = Cache()