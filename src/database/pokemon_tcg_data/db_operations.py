# src/database/pokemon_tcg_data/db_operations.py

import sqlite3
from typing import List, Tuple
from contextlib import contextmanager
from ..create_connection import create_connection
from ..exceptions import DatabaseConnectionError

@contextmanager
def get_db_cursor():
    conn = create_connection()
    if conn is None:
        raise DatabaseConnectionError("Failed to create database connection")
    try:
        yield conn.cursor()
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise DatabaseConnectionError(f"Database error occurred: {e}") from e
    finally:
        conn.close()

def table_exists(cursor, table_name):
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    return cursor.fetchone() is not None

def table_has_data(cursor, table_name):
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    return cursor.fetchone()[0] > 0

def create_tables():
    with get_db_cursor() as cursor:
        if table_exists(cursor, 'cards') and table_has_data(cursor, 'cards'):
            print("Table 'cards' already exists and contains data. Skipping creation.")
        else:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS cards (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    supertype TEXT,
                    subtypes TEXT,
                    types TEXT,
                    set_id TEXT,
                    number TEXT,
                    artist TEXT,
                    rarity TEXT,
                    nationalPokedexNumbers TEXT,
                    legalities TEXT,
                    regulationMark TEXT,
                    image_small TEXT,
                    image_large TEXT,
                    price REAL,
                    condition TEXT
                )
            ''')
            print("Table 'cards' created successfully.")

        if table_exists(cursor, 'card_sets') and table_has_data(cursor, 'card_sets'):
            print("Table 'card_sets' already exists and contains data. Skipping creation.")
        else:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS card_sets (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    series TEXT,
                    printedTotal INTEGER,
                    total INTEGER,
                    legalities TEXT,
                    ptcgoCode TEXT,
                    releaseDate TEXT,
                    updatedAt TEXT,
                    images TEXT
                )
            ''')
            print("Table 'card_sets' created successfully.")

def execute_query(query: str, params: Tuple = ()) -> List[Tuple]:
    with get_db_cursor() as cursor:
        cursor.execute(query, params)
        return cursor.fetchall()