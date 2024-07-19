# src/backend/models/transaction_history.py
from sqlalchemy import Column, Integer, String, Numeric, Date
from ..extensions import db

class TransactionHistory(db.Model):
    __tablename__ = 'transaction_history'

    id = Column(Integer, primary_key=True)
    card_id = Column(String, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    transaction_date = Column(Date, nullable=False)
    transaction_type = Column(String, nullable=False)  # 'buy' or 'sell'