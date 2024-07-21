# src/nlp/train_model.py
import spacy
from spacy.training import Example
import os
import sys
from dotenv import load_dotenv

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

from src.nlp.pokemon_card_data import generate_training_data

load_dotenv()
MODEL_PATH = os.getenv('MODEL_PATH')

def train_model(train_data_size=25, iterations=30):
    nlp = spacy.blank("en")
    ner = nlp.add_pipe("ner")
    
    TRAIN_DATA = generate_training_data(limit=train_data_size)
    
    for _, annotations in TRAIN_DATA:
        for ent in annotations.get("entities"):
            ner.add_label(ent[2])
    
    optimizer = nlp.begin_training()
    for iteration in range(iterations):
        losses = {}
        for text, annotations in TRAIN_DATA:
            example = Example.from_dict(nlp.make_doc(text), annotations)
            nlp.update([example], drop=0.5, losses=losses)
        print(f"Losses at iteration {iteration}: {losses}")
    
    nlp.to_disk(MODEL_PATH)
    print(f"Model trained on {train_data_size} examples and saved to {MODEL_PATH}")

if __name__ == "__main__":
    train_model(train_data_size=25, iterations=30)  # You can easily adjust these parameters