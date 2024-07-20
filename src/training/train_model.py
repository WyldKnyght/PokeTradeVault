# src\training\train_model.py
import spacy
from spacy.training import Example
import os
from training.pokemon_card_data import generate_training_data

def train_model():
    nlp = spacy.blank("en")
    ner = nlp.add_pipe("ner")
    
    TRAIN_DATA = generate_training_data()
    
    for _, annotations in TRAIN_DATA:
        for ent in annotations.get("entities"):
            ner.add_label(ent[2])
    
    optimizer = nlp.begin_training()
    for iteration in range(30):  # Adjust the number of iterations as needed
        losses = {}
        for text, annotations in TRAIN_DATA:
            example = Example.from_dict(nlp.make_doc(text), annotations)
            nlp.update([example], drop=0.5, losses=losses)
        print(f"Losses at iteration {iteration}: {losses}")
    
    model_path = os.path.join(os.path.dirname(__file__), '../../models/pokemon_card_model')
    nlp.to_disk(model_path)
    print(f"Model trained and saved to {model_path}")

if __name__ == "__main__":
    train_model()

def generate_training_data():
    cards = get_all_cards()
    card_sets = get_all_card_sets()
    
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