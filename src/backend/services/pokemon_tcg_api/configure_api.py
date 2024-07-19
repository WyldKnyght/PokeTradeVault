from pokemontcgsdk import RestClient
from ...config import Config

def configure_api():
    """Configure the Pokémon TCG API with the API key."""
    RestClient.configure(Config.POKEMON_TCG_API_KEY)
    print(f"API Key configured: {Config.POKEMON_TCG_API_KEY[:5]}...")