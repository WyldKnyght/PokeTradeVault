# src\backend\services\pokemon_tcg_api\search_cards.py
from pokemontcgsdk import Card

def search_cards(query, page=1, page_size=20):
    """
    Search for cards based on a query string.
    
    Args:
        query (str): The search query.
        page (int): The page number for pagination.
        page_size (int): The number of results per page.
    
    Returns:
        list: A list of Card objects matching the search criteria.
    """
    try:
        print(f"Searching for cards with query: {query}, page: {page}, page_size: {page_size}")
        results = Card.where(q=query, page=page, pageSize=page_size)
        print(f"Search successful, found {len(results)} cards")
        return results
    except Exception as e:
        print(f"Error searching cards: {type(e).__name__}: {str(e)}")
        if hasattr(e, 'read'):
            error_details = e.read()
            print(f"Error details: {error_details.decode('utf-8') if isinstance(error_details, bytes) else error_details}")
        return []
