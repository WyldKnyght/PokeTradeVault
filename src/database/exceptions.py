# src/database/exceptions.py
class DatabaseConnectionError(Exception):
    """Raised when a database connection cannot be established."""
    pass