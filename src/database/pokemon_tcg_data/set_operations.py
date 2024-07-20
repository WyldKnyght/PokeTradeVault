from typing import Dict, List
from .db_operations import get_db_cursor
from .log_discrepancies import log_discrepancy, set_log_file

def get_existing_set_ids():
    with get_db_cursor() as cursor:
        cursor.execute("SELECT id FROM card_sets")
        return {row[0] for row in cursor.fetchall()}

def process_card_sets(card_sets: List[Dict]):
    existing_ids = get_existing_set_ids()
    new_sets = updated_sets = 0

    with get_db_cursor() as cursor:
        for set_data in card_sets:
            set_id = set_data['id']
            if set_id in existing_ids:
                if update_existing_set(cursor, set_data, set_id):
                    updated_sets += 1
                existing_ids.remove(set_id)
            else:
                insert_new_set(cursor, set_data)
                new_sets += 1

        for removed_id in existing_ids:
            log_discrepancy(set_log_file, f"Removed set: {removed_id}")

    print(f"Processed {len(card_sets)} card sets.")
    print(f"New sets added: {new_sets}")
    print(f"Sets updated: {updated_sets}")
    print(f"Sets potentially removed: {len(existing_ids)}")
    print(f"Log file created: {set_log_file}")

def update_existing_set(cursor, set_data: Dict, set_id: str) -> bool:
    cursor.execute("SELECT * FROM card_sets WHERE id = ?", (set_id,))
    existing_data = cursor.fetchone()
    new_data = create_set_tuple(set_data)
    if new_data != existing_data:
        cursor.execute('''
            UPDATE card_sets SET name=?, series=?, printedTotal=?, total=?, legalities=?, 
            ptcgoCode=?, releaseDate=?, updatedAt=?, images=? WHERE id=?
        ''', new_data[1:] + (new_data[0],))
        log_discrepancy(set_log_file, f"Updated set: {set_id}")
        return True
    return False

def insert_new_set(cursor, set_data: Dict):
    new_data = create_set_tuple(set_data)
    cursor.execute('''
        INSERT INTO card_sets (id, name, series, printedTotal, total, legalities, 
        ptcgoCode, releaseDate, updatedAt, images)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', new_data)
    log_discrepancy(set_log_file, f"New set: {set_data['id']}")

def create_set_tuple(set_data: Dict):
    return (
        set_data['id'], set_data['name'], set_data.get('series', ''),
        set_data.get('printedTotal', 0), set_data.get('total', 0),
        str(set_data.get('legalities', {})), set_data.get('ptcgoCode', ''),
        set_data.get('releaseDate', ''), set_data.get('updatedAt', ''),
        str(set_data.get('images', {}))
    )