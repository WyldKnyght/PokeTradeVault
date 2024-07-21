# src/nlp/evaluate_model.py
import spacy
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
MODEL_PATH = os.getenv('MODEL_PATH')

def evaluate_model():
    nlp = spacy.load(MODEL_PATH)
    
    # Example evaluation data
    examples = [
        ("What's the price of a Charizard card?", {"entities": [(23, 31, "card_name")]}),
        ("Show me information about the Base Set set", {"entities": [(27, 35, "set_name")]}),
        ("Is Pikachu from Jungle set rare?", {"entities": [(3, 10, "card_name"), (16, 22, "set_name")]}),
    ]
    
    for text, annotations in examples:
        doc = nlp(text)
        print(f"Text: {text}")
        print("Entities:", [(ent.text, ent.label_) for ent in doc.ents])
        print("Expected:", annotations["entities"])
        print()

if __name__ == "__main__":
    evaluate_model()