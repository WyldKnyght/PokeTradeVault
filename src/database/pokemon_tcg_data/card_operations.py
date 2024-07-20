from typing import Dict, Set
from .db_operations import get_db_cursor
from .log_discrepancies import log_discrepancy, card_log_file

def get_existing_card_ids() -> Set[str]:
    with get_db_cursor() as cursor:
        cursor.execute("SELECT id FROM cards")
        return {row[0] for row in cursor.fetchall()}

def insert_new_card(card: Dict):
    with get_db_cursor() as cursor:
        new_data = create_card_tuple(card, 0.0, '')
        cursor.execute('''
            INSERT INTO cards (id, name, supertype, subtypes, types, set_id, number, artist, rarity, 
            nationalPokedexNumbers, legalities, regulationMark, image_small, image_large, price, condition)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', new_data)
    log_discrepancy(card_log_file, f"New card: {card['id']}")

def update_existing_card(card: Dict):
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM cards WHERE id = ?", (card['id'],))
        existing_data = cursor.fetchone()
        new_data = create_card_tuple(card, existing_data[14], existing_data[15])
        if new_data != existing_data:
            cursor.execute('''
                UPDATE cards SET name=?, supertype=?, subtypes=?, types=?, set_id=?, number=?, artist=?, 
                rarity=?, nationalPokedexNumbers=?, legalities=?, regulationMark=?, image_small=?, 
                image_large=?, price=?, condition=? WHERE id=?
            ''', new_data[1:] + (new_data[0],))
            log_discrepancy(card_log_file, f"Updated card: {card['id']}")
            return True
    return False

def create_card_tuple(card: Dict, price: float, condition: str):
    return (
        card['id'], card['name'], card.get('supertype', ''),
        ','.join(card.get('subtypes', [])), ','.join(card.get('types', [])),
        card['set']['id'], card.get('number', ''), card.get('artist', ''),
        card.get('rarity', ''), ','.join(map(str, card.get('nationalPokedexNumbers', []))),
        str(card.get('legalities', {})), card.get('regulationMark', ''),
        card['images'].get('small', ''), card['images'].get('large', ''),
        price, condition
    )