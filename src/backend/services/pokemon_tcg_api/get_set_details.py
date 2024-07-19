# src\backend\services\pokemon_tcg_api\get_set_details.py
from pokemontcgsdk import Set

def get_set_details(set_id):
    """
    Get detailed information about a specific set.
    
    Args:
        set_id (str): The ID of the set to retrieve.
    
    Returns:
        Set: A Set object with detailed information, or None if an error occurs.
    """
    try:
        return Set.find(set_id)
    except Exception as e:
        print(f"Error getting set details: {type(e).__name__}: {str(e)}")
        return None
