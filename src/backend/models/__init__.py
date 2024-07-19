# src/backend/models/__init__.py
from .watchlist import Watchlist
from .saved_searches import SavedSearch
from .transaction_history import TransactionHistory
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

Base = db.Model