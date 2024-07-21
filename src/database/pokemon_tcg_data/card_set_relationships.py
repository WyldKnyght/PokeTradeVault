# src/database/pokemon_tcg_data/card_set_relationships.py

from typing import List, Dict
from .db_operations import execute_query

def fetch_card_set_info(limit: int = None) -> List[Dict]:
    query = """
    SELECT 
        c.id AS card_full_id,
        SUBSTR(c.id, 1, INSTR(c.id, '-') - 1) AS set_id,
        SUBSTR(c.id, INSTR(c.id, '-') + 1) AS card_number,
        c.name AS card_name,
        s.name AS set_name,
        s.series AS series_name
    FROM 
        cards c
    JOIN 
        card_sets s ON SUBSTR(c.id, 1, INSTR(c.id, '-') - 1) = s.id
    """
    if limit:
        query += f" LIMIT {limit}"
    
    rows = execute_query(query)
    return [
        {
            "card_full_id": row[0],
            "set_id": row[1],
            "card_number": row[2],
            "card_name": row[3],
            "set_name": row[4],
            "series": row[5],
        }
        for row in rows
    ]