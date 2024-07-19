from pokemontcgsdk import Card

def get_card_price_history(card_id):
    """
    Get price history for a specific card.
    
    Args:
        card_id (str): The ID of the card to retrieve price history for.
    
    Returns:
        dict: A dictionary containing price history information, or None if an error occurs.
    """
    try:
        card = Card.find(card_id)
        return card.tcgplayer.prices if card.tcgplayer else None
    except Exception as e:
        print(f"Error getting card price history: {type(e).__name__}: {str(e)}")
        return None