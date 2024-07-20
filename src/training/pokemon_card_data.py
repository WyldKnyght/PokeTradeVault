# src\training\pokemon_card_data.py
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()
DB_PATH = os.getenv('DB_PATH')

def get_random_cards(n=5):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT name FROM cards ORDER BY RANDOM() LIMIT ?", (n,))
    cards = [row[0] for row in c.fetchall()]
    conn.close()
    return cards

def get_random_card_sets(n=3):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT name FROM card_sets ORDER BY RANDOM() LIMIT ?", (n,))
    card_sets = [row[0] for row in c.fetchall()]
    conn.close()
    return card_sets

def generate_training_data():
    cards = get_random_cards(10)
    card_sets = get_random_card_sets(5)
    
    train_data = [
        (f"What's the price of a {card} card?", {"entities": [(23, 23+len(card), "card_name")]})
        for card in cards
    ]
    train_data += [
        (f"Show me information about the {card_set} set", {"entities": [(27, 27+len(card_set), "set_name")]})
        for card_set in card_sets
    ]
    train_data += [
        (f"Is {cards[0]} from {card_sets[0]} set rare?", {"entities": [(3, 3+len(cards[0]), "card_name"), (3+len(cards[0])+6, 3+len(cards[0])+6+len(card_sets[0]), "set_name")]})
    ]
    
    return train_data

TRAIN_DATA = generate_training_data()
