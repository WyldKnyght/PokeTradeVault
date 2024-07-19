# src/database/schema.sql

CREATE TABLE saved_searches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    search_name TEXT NOT NULL,
    search_parameters TEXT NOT NULL
);

CREATE TABLE watchlist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    card_id TEXT NOT NULL,
    target_price DECIMAL(10, 2),
    notes TEXT
);

CREATE TABLE transaction_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    card_id TEXT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    transaction_date DATE NOT NULL,
    transaction_type TEXT NOT NULL  -- 'buy' or 'sell'
);