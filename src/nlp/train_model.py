import spacy
from spacy.training import Example
from pokemon_card_data import TRAIN_DATA

def train_model():
    nlp = spacy.blank("en")
    ner = nlp.add_pipe("ner")
    
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
    
    nlp.to_disk("./pokemon_card_model")
    print("Model trained and saved.")

if __name__ == "__main__":
    train_model()