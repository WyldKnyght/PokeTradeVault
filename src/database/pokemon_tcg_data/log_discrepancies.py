# src/database/pokemon_tcg_data/log_discrepancies.py
import os
from datetime import datetime

LOG_DIR = os.path.join(os.path.dirname(__file__), '../../logs')
os.makedirs(LOG_DIR, exist_ok=True)

card_log_file = os.path.join(LOG_DIR, f'card_update_log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt')
set_log_file = os.path.join(LOG_DIR, f'set_update_log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt')

def log_discrepancy(log_file, message):
    with open(log_file, 'a') as f:
        f.write(f"{message}\n")
