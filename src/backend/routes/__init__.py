# src\backend\routes\__init__.py
from flask import Blueprint

api = Blueprint('api', __name__)

from . import card_routes, set_routes, watchlist_routes, saved_search_routes, transaction_routes