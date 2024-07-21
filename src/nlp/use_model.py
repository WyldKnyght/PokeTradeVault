# src/nlp/use_model.py
import spacy
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
MODEL_PATH = os.getenv('MODEL_PATH')

def load_trained_model():
    return spacy.load(MODEL_PATH)

def predict(text: str):
    nlp = load_trained_model()
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]

if __name__ == "__main__":
    text = "What's the price of a Charizard card?"
    entities = predict(text)
    print(f"Text: {text}")
    print("Entities:", entities)