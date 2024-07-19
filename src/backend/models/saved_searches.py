# src/backend/models/saved_searches.py
from sqlalchemy import Column, Integer, String
from . import db

class SavedSearch(db.Model):
    __tablename__ = 'saved_searches'

    id = Column(Integer, primary_key=True)
    search_name = Column(String, nullable=False)
    search_parameters = Column(String, nullable=False)