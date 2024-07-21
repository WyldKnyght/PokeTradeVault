# Pokémon Card AI Assistant

   This project is an AI-powered assistant for buying and selling Pokémon cards. 
   It is still in development (may not have all functionality).

   ## Setup

   1. Clone the repository
   2. Create a virtual environment: `python -m venv venv`
   3. Activate the virtual environment:
      - Windows: `venv\Scripts\activate`
      - macOS/Linux: `source venv/bin/activate`
   4. Install dependencies: `pip install -r requirements.txt`
   5. Initialize your database: `python src/backend/init_db.py`


   ## Pokémon TCG API Integration: 
   1. You need sign up and generate an API key from the Pokémon TCG API website (https://dev.pokemontcg.io/).
   2. Add your API key to the .env_temp file, then rename it to .env
