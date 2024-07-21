# src/nlp/pokemon_card_data.py
from typing import List, Dict, Tuple
import spacy
from ..database.pokemon_tcg_data.card_set_relationships import fetch_card_set_info

def create_aligned_entities(nlp, text: str, entity_text: str, entity_label: str) -> List[Tuple[int, int, str]]:
    doc = nlp(text)
    return next(
        ([(token.idx, token.idx + len(token.text), entity_label)]
         for token in doc if token.text == entity_text),
        [],
    )

def create_example(nlp, text: str, entities_dict: Dict[str, str]) -> Tuple[str, Dict[str, List[Tuple[int, int, str]]]]:
    entities = []
    for entity_text, entity_label in entities_dict.items():
        entities.extend(create_aligned_entities(nlp, text, str(entity_text), entity_label))
    return (text, {"entities": entities})

def generate_card_price_example(nlp, card: Dict) -> Tuple[str, Dict[str, List[Tuple[int, int, str]]]]:
    text = f"What's the price of {card['card_name']} ({card['card_number']}) from the {card['set_name']} set?"
    entities = {
        str(card['card_name']): "card_name",
        str(card['card_number']): "card_number",
        str(card['set_name']): "set_name"
    }
    return create_example(nlp, text, entities)

def generate_set_info_example(nlp, card: Dict) -> Tuple[str, Dict[str, List[Tuple[int, int, str]]]]:
    text = f"How many cards are in the {card['set_name']} set?"
    entities = {str(card['set_name']): "set_name"}
    return create_example(nlp, text, entities)

def generate_series_example(nlp, card: Dict) -> Tuple[str, Dict[str, List[Tuple[int, int, str]]]]:
    text = f"Which series does the {card['set_name']} set belong to?"
    entities = {str(card['set_name']): "set_name"}
    return create_example(nlp, text, entities)

def generate_combined_example(nlp, card: Dict) -> Tuple[str, Dict[str, List[Tuple[int, int, str]]]]:
    text = f"Is {card['card_name']} ({card['card_number']}) from the {card['set_name']} set in the {card['series']} series rare?"
    entities = {
        str(card['card_name']): "card_name",
        str(card['card_number']): "card_number",
        str(card['set_name']): "set_name",
        str(card['series']): "series_name"
    }
    return create_example(nlp, text, entities)

def generate_training_data() -> List[Tuple[str, Dict]]:
    nlp = spacy.blank("en")
    cards_with_sets = fetch_card_set_info()  # Fetch all available data

    train_data = []

    for card in cards_with_sets:
        train_data.extend(
            (
                generate_card_price_example(nlp, card),
                generate_set_info_example(nlp, card),
                generate_series_example(nlp, card),
            )
        )
    
    # Add combined examples
    train_data.extend(
        generate_combined_example(nlp, card) for card in cards_with_sets
    )
    
    return train_data