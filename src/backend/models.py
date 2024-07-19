# src/backend/models.py
from sqlalchemy import Column, Integer, String, Numeric, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class SavedSearch(Base):
    __tablename__ = 'saved_searches'

    id = Column(Integer, primary_key=True)
    search_name = Column(String, nullable=False)
    search_parameters = Column(String, nullable=False)

class Watchlist(Base):
    __tablename__ = 'watchlist'

    id = Column(Integer, primary_key=True)
    card_id = Column(String, nullable=False)
    target_price = Column(Numeric(10, 2))
    notes = Column(String)

class TransactionHistory(Base):
    __tablename__ = 'transaction_history'

    id = Column(Integer, primary_key=True)
    card_id = Column(String, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    transaction_date = Column(Date, nullable=False)
    transaction_type = Column(String, nullable=False)  # 'buy' or 'sell'