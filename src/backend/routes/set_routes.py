# src/backend/routes/set_routes.py
from . import api
from flask import jsonify, request
from ..services.pokemon_tcg_api import search_sets, get_set_details
from ..extensions import cache

@api.route('/sets', methods=['GET'])
@cache.cached(timeout=3600, query_string=True)
def search_set():
    query = request.args.get('q', '')
    results = search_sets(query)
    return jsonify([card_set.to_dict() for card_set in results])  

@api.route('/set/<string:set_id>', methods=['GET'])
@cache.cached(timeout=3600)
def set_details(set_id):
    card_set = get_set_details(set_id)  
    return jsonify(card_set.to_dict() if card_set else {})