-- inventory.db schema

CREATE TABLE IF NOT EXISTS inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    amount INTEGER NOT NULL CHECK (amount >= 0),
    purchase_price REAL NOT NULL CHECK (purchase_price >= 0),
    provider TEXT NOT NULL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL,
    amount INTEGER NOT NULL,
    price REAL NOT NULL,
    transaction_type TEXT CHECK(transaction_type IN ('purchase', 'sale', 'broken')) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (code) REFERENCES inventory(code) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS providers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS removed_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT,
    title TEXT,
    amount INTEGER,
    purchase_price REAL,
    provider TEXT,
    price REAL,
    removal_reason TEXT,
    removal_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


