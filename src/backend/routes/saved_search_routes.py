# src/backend/routes/saved_search_routes.py
from . import api
from flask import jsonify, request
from ..models import SavedSearch
from ..extensions import db, cache

@api.route('/saved_searches', methods=['GET', 'POST'])
def saved_searches():
    if request.method == 'POST':
        try:
            data = request.json
            if not data or 'search_name' not in data or 'search_parameters' not in data:
                return jsonify({"error": "Invalid input"}), 400
            
            new_search = SavedSearch(
                search_name=data['search_name'],
                search_parameters=data['search_parameters']
            )
            db.session.add(new_search)
            db.session.commit()
            cache.delete('saved_searches')  # Invalidate cache
            return jsonify(new_search.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500
    else:
        @cache.cached(timeout=300, key_prefix='saved_searches')
        def get_saved_searches():
            searches = SavedSearch.query.all()
            return [search.to_dict() for search in searches]
        
        return jsonify(get_saved_searches())

@api.route('/saved_searches/<int:search_id>', methods=['GET', 'PUT', 'DELETE'])
def saved_search(search_id):
    search = SavedSearch.query.get_or_404(search_id)
    
    if request.method == 'GET':
        return jsonify(search.to_dict())
    
    elif request.method == 'PUT':
        try:
            data = request.json
            if 'search_name' in data:
                search.search_name = data['search_name']
            if 'search_parameters' in data:
                search.search_parameters = data['search_parameters']
            db.session.commit()
            cache.delete('saved_searches')  # Invalidate cache
            return jsonify(search.to_dict())
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500
    
    elif request.method == 'DELETE':
        try:
            db.session.delete(search)
            db.session.commit()
            cache.delete('saved_searches')  # Invalidate cache
            return '', 204
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500