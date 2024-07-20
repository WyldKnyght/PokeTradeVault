import os
from dotenv import load_dotenv
from database.pokemon_tcg_data.pokemon_tcg_db import create_tables
from database.pokemon_tcg_data.populate_tcg_db import populate_cards, populate_card_sets
from train_model import train_model

def main():
    load_dotenv()
    
    print("Creating database tables...")
    create_tables()
    
    print("Populating cards...")
    populate_cards()
    
    print("Populating card sets...")
    populate_card_sets()
    
    print("Training model...")
    train_model()
    
    print("Training pipeline completed successfully!")

if __name__ == "__main__":
    main()