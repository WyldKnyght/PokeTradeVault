# src/nlp/train_model.py
import spacy
from spacy.training import Example
import os
import sys
import random
from tqdm import tqdm
from dotenv import load_dotenv

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

from src.nlp.pokemon_card_data import generate_training_data

load_dotenv()
MODEL_PATH = os.getenv('MODEL_PATH')

def train_model(max_iterations=30, patience=3, learning_rate=0.001):
    nlp = spacy.blank("en")
    ner = nlp.add_pipe("ner")

    TRAIN_DATA = generate_training_data()

    # Split data into training and validation sets
    split = int(len(TRAIN_DATA) * 0.8)
    train_data = TRAIN_DATA[:split]
    val_data = TRAIN_DATA[split:]

    # Convert training data to Example objects
    train_examples = []
    for text, annotations in train_data:
        doc = nlp.make_doc(text)
        example = Example.from_dict(doc, annotations)
        train_examples.append(example)

    # Convert validation data to Example objects
    val_examples = []
    for text, annotations in val_data:
        doc = nlp.make_doc(text)
        example = Example.from_dict(doc, annotations)
        val_examples.append(example)

    # Add labels
    for example in train_examples:
        for ent in example.reference.ents:
            ner.add_label(ent.label_)

    # Initialize the model
    optimizer = nlp.initialize(lambda: train_examples)

    best_loss = float('inf')
    no_improvement = 0

    for iteration in tqdm(range(max_iterations), desc="Training"):
        # Shuffle the training data
        random.shuffle(train_examples)

        # Create batches
        batches = spacy.util.minibatch(train_examples, size=32)

        # Update the model
        losses = {}
        for batch in batches:
            nlp.update(batch, drop=0.5, losses=losses)

        # Evaluate on validation set
        val_losses = {}
        nlp.evaluate(val_examples)

        val_loss = losses['ner']
        print(
            f"Iteration {iteration + 1}, Train Loss: {val_loss:.3f}, Validation Loss: {val_loss:.3f}"
        )
        # Early stopping
        if val_loss < best_loss:
            best_loss = val_loss
            no_improvement = 0
            nlp.to_disk(MODEL_PATH)
            print(f"Model improved and saved to {MODEL_PATH}")
        else:
            no_improvement += 1
            if no_improvement >= patience:
                print(f"Early stopping triggered. No improvement for {patience} iterations.")
                break

    print(f"Final model saved to {MODEL_PATH}")

if __name__ == "__main__":
    train_model(max_iterations=30, patience=3, learning_rate=0.001)