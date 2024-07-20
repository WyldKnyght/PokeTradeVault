# src/database/pokemon_tcg_data/db_manager.py
from .db_operations import create_tables
from .card_operations import get_existing_card_ids, insert_new_card, update_existing_card
from .set_operations import process_card_sets
from .fetch_data import fetch_cards, fetch_card_sets
from .log_discrepancies import log_discrepancy, card_log_file

def populate_cards():
    existing_ids = get_existing_card_ids()
    total_cards = new_cards = updated_cards = 0
    page = 1

    while True:
        cards = fetch_cards(page)
        if not cards:
            break
        for card in cards:
            if card['id'] in existing_ids:
                if update_existing_card(card):
                    updated_cards += 1
                existing_ids.remove(card['id'])
            else:
                insert_new_card(card)
                new_cards += 1
            total_cards += 1
        print(f"Processed {total_cards} cards so far...")
        page += 1

    for removed_id in existing_ids:
        log_discrepancy(card_log_file, f"Removed card: {removed_id}")

    print(f"Total cards processed: {total_cards}")
    print(f"New cards added: {new_cards}")
    print(f"Cards updated: {updated_cards}")
    print(f"Cards potentially removed: {len(existing_ids)}")
    print(f"Log file created: {card_log_file}")

def populate_card_sets():
    if card_sets := fetch_card_sets():
        process_card_sets(card_sets)
    else:
        print("No card sets fetched.")