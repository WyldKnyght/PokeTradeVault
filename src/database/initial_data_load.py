# src/database/initial_data_load.py
import os
import sys

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

from src.database.pokemon_tcg_data.db_operations import create_tables
from src.database.pokemon_tcg_data.db_manager import populate_cards, populate_card_sets

def main():
    print("Creating database tables...")
    create_tables()
    
    print("Performing initial data load from API...")
    print("Populating cards...")
    populate_cards()
    
    print("Populating card sets...")
    populate_card_sets()
    
    print("Initial data load completed successfully!")

if __name__ == "__main__":
    main()