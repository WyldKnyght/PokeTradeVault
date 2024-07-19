# src/backend/routes/watchlist_routes.py
from . import api
from flask import jsonify, request
from ..models import Watchlist
from ..extensions import db, cache

@api.route('/watchlist', methods=['GET', 'POST'])
def watchlist():
    if request.method == 'POST':
        try:
            data = request.json
            if not data or 'card_id' not in data:
                return jsonify({"error": "Invalid input"}), 400
            
            new_item = Watchlist(
                card_id=data['card_id'],
                target_price=data.get('target_price'),
                notes=data.get('notes')
            )
            db.session.add(new_item)
            db.session.commit()
            cache.delete('watchlist')
            return jsonify(new_item.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500
    else:
        @cache.cached(timeout=300, key_prefix='watchlist')
        def get_watchlist():
            items = Watchlist.query.all()
            return [item.to_dict() for item in items]
        
        return jsonify(get_watchlist())