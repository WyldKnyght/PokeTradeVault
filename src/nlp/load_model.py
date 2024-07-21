# src/nlp/load_model.py
import spacy
import os
from dotenv import load_dotenv

load_dotenv()
MODEL_PATH = os.getenv('MODEL_PATH')

def load_trained_model():
    return spacy.load(MODEL_PATH)

if __name__ == "__main__":
    nlp = load_trained_model()
    print("Model loaded successfully.")