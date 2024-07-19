# src/backend/init_db.py
import os
from app import create_app, db
from config import Config

app = create_app()

with app.app_context():
    # Ensure the data directory exists
    os.makedirs(Config.DATA_DIR, exist_ok=True)
    
    db.create_all()
    print(f"Database tables created in {Config.SQLALCHEMY_DATABASE_URI}")