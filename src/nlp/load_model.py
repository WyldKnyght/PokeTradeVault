import os
import spacy
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

MODEL_PATH = os.getenv('MODEL_PATH')

def load_model():
    if os.path.exists(MODEL_PATH):
        return spacy.load(MODEL_PATH)
    print("Custom model not found. Loading default English model.")
    return spacy.load("en_core_web_sm")



def process_text(nlp, text):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return {"entities": entities}

# Example usage
if __name__ == "__main__":
    nlp = load_model()
    result = process_text(nlp, "What's the value of a mint condition Blastoise from Base Set?")
    print(result)