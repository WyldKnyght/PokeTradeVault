from pokemontcgsdk import Card

def get_card_details(card_id):
    """
    Get detailed information about a specific card.
    
    Args:
        card_id (str): The ID of the card to retrieve.
    
    Returns:
        Card: A Card object with detailed information, or None if an error occurs.
    """
    try:
        return Card.find(card_id)
    except Exception as e:
        print(f"Error getting card details: {type(e).__name__}: {str(e)}")
        return None