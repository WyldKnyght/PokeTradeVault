# src/backend/routes/card_routes.py
from . import api
from flask import jsonify, request
from ..services.pokemon_tcg_api import search_cards, get_card_details, get_card_price_history
from ..extensions import cache

@api.route('/search', methods=['GET'])
@cache.cached(timeout=60, query_string=True)
def search():
    query = request.args.get('q', '')
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('pageSize', 20))
    results = search_cards(query, page, page_size)
    return jsonify([card.to_dict() for card in results])

@api.route('/card/<string:card_id>', methods=['GET'])
@cache.cached(timeout=3600)
def card_details(card_id):
    card = get_card_details(card_id)
    return jsonify(card.to_dict() if card else {})

@api.route('/card/<string:card_id>/price_history', methods=['GET'])
@cache.cached(timeout=3600)
def card_price_history(card_id):
    history = get_card_price_history(card_id)
    return jsonify(history or {})