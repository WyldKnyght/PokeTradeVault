from pokemontcgsdk import Set

def search_sets(query):
    """
    Search for Pokémon card sets.
    
    Args:
        query (str): The search query for sets.
    
    Returns:
        list: A list of Set objects matching the search criteria.
    """
    try:
        results = Set.where(q=query)
        print(f"Search successful, found {len(results)} sets")
        return results
    except Exception as e:
        print(f"Error searching sets: {type(e).__name__}: {str(e)}")
        return []