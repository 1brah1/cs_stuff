-- Simple Stock Data Database Schema
CREATE TABLE IF NOT EXISTS stock_prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL,
    date DATE NOT NULL,
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    volume INTEGER,
    adj_close REAL,
    updated_at TEXT,
    source TEXT DEFAULT 'yfinance',
    UNIQUE(symbol, date)
);

CREATE INDEX IF NOT EXISTS idx_stock_prices_symbol_date ON stock_prices(symbol, date);
