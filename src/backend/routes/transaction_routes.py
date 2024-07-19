from . import api
from flask import jsonify, request
from ..models import TransactionHistory
from ..extensions import db, cache

@api.route('/transactions', methods=['GET', 'POST'])
def transactions():
    if request.method == 'POST':
        try:
            data = request.json
            if not data or 'card_id' not in data or 'price' not in data or 'transaction_date' not in data or 'transaction_type' not in data:
                return jsonify({"error": "Invalid input"}), 400
            
            new_transaction = TransactionHistory(
                card_id=data['card_id'],
                price=data['price'],
                transaction_date=data['transaction_date'],
                transaction_type=data['transaction_type']
            )
            db.session.add(new_transaction)
            db.session.commit()
            cache.delete('transactions')  # Invalidate cache
            return jsonify(new_transaction.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500
    else:
        @cache.cached(timeout=300, key_prefix='transactions')
        def get_transactions():
            transactions = TransactionHistory.query.all()
            return [transaction.to_dict() for transaction in transactions]
        
        return jsonify(get_transactions())

@api.route('/transactions/<int:transaction_id>', methods=['GET', 'PUT', 'DELETE'])
def transaction(transaction_id):
    transaction = TransactionHistory.query.get_or_404(transaction_id)
    
    if request.method == 'GET':
        return jsonify(transaction.to_dict())
    
    elif request.method == 'PUT':
        try:
            data = request.json
            if 'card_id' in data:
                transaction.card_id = data['card_id']
            if 'price' in data:
                transaction.price = data['price']
            if 'transaction_date' in data:
                transaction.transaction_date = data['transaction_date']
            if 'transaction_type' in data:
                transaction.transaction_type = data['transaction_type']
            db.session.commit()
            cache.delete('transactions')  # Invalidate cache
            return jsonify(transaction.to_dict())
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500
    
    elif request.method == 'DELETE':
        try:
            db.session.delete(transaction)
            db.session.commit()
            cache.delete('transactions')  # Invalidate cache
            return '', 204
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500