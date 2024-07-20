# src\backend\routes\__init__.py
from flask import Blueprint, render_template

api = Blueprint('api', __name__)

@api.route('/')
def home():
    return render_template('index.html')

# Import other routes here
from . import card_routes, saved_search_routes, set_routes, transaction_routes, watchlist_routes, chat_routes