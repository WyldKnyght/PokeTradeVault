# src\database\pokemon_tcg_data\fetch_data.py
import os
import requests
from dotenv import load_dotenv
from typing import List, Dict, Optional
from requests.exceptions import RequestException

load_dotenv()

API_BASE_URL = "https://api.pokemontcg.io/v2"
POKEMON_TCG_API_KEY = os.getenv('POKEMON_TCG_API_KEY')
MAX_RETRIES = 3

def fetch_cards(page: int = 1, page_size: int = 250) -> Optional[List[Dict]]:
    url = f"{API_BASE_URL}/cards"
    params = {"page": page, "pageSize": page_size}
    headers = {"X-Api-Key": POKEMON_TCG_API_KEY}
    
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            return response.json()['data']
        except RequestException as e:
            print(f"Error fetching cards (attempt {attempt + 1}): {e}")
            if attempt == MAX_RETRIES - 1:
                print("Max retries reached. Giving up.")
                return None
    return None

def fetch_card_sets() -> Optional[List[Dict]]:
    url = f"{API_BASE_URL}/sets"
    headers = {"X-Api-Key": POKEMON_TCG_API_KEY}
    
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()['data']
        except RequestException as e:
            print(f"Error fetching card sets (attempt {attempt + 1}): {e}")
            if attempt == MAX_RETRIES - 1:
                print("Max retries reached. Giving up.")
                return None
    return None
