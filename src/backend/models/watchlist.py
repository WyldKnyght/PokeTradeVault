# src/backend/models/watchlist.py
from sqlalchemy import Column, Integer, String, Numeric
from . import db

class Watchlist(db.Model):
    __tablename__ = 'watchlist'

    id = Column(Integer, primary_key=True)
    card_id = Column(String, nullable=False)
    target_price = Column(Numeric(10, 2))
    notes = Column(String)
