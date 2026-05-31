"""
Simple Stock Data Collector
Fetches stock data from yFinance and stores it in SQLite database
"""

import yfinance as yf
import sqlite3
import pandas as pd
import os
from datetime import datetime, UTC

# Tech stocks to analyze
STOCKS = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META']

def create_connection(db_path='stock_data.db'):
    """Create database connection"""
    conn = sqlite3.connect(db_path)
    return conn

def initialize_database(conn):
    """Initialize database with schema"""
    schema_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'schema.sql')
    with open(schema_path, 'r', encoding='utf-8') as f:
        schema = f.read()
    conn.executescript(schema)
    _ensure_schema_columns(conn)
    conn.commit()
    print("Database initialized successfully")


def _ensure_schema_columns(conn):
    """Apply lightweight schema migrations for existing local databases."""
    cursor = conn.execute("PRAGMA table_info(stock_prices)")
    existing_columns = {row[1] for row in cursor.fetchall()}

    if 'updated_at' not in existing_columns:
        conn.execute("ALTER TABLE stock_prices ADD COLUMN updated_at TEXT")
        conn.execute("UPDATE stock_prices SET updated_at = datetime('now') WHERE updated_at IS NULL")

    if 'source' not in existing_columns:
        conn.execute("ALTER TABLE stock_prices ADD COLUMN source TEXT DEFAULT 'yfinance'")
        conn.execute("UPDATE stock_prices SET source = 'yfinance' WHERE source IS NULL")

def fetch_stock_data(symbol, period='5d', interval='1d'):
    """Fetch stock data from yFinance"""
    try:
        print(f"Fetching data for {symbol}...")
        ticker = yf.Ticker(symbol)
        data = ticker.history(period=period, interval=interval, auto_adjust=False)
        data.reset_index(inplace=True)
        data['symbol'] = symbol
        return data
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

def store_price_data(conn, df):
    """Store price data in database using incremental upserts."""
    if df is None or df.empty:
        return

    df_to_store = df[['symbol', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume']].copy()
    df_to_store['Adj Close'] = df['Close']
    df_to_store.columns = ['symbol', 'date', 'open', 'high', 'low', 'close', 'volume', 'adj_close']
    df_to_store['date'] = pd.to_datetime(df_to_store['date']).dt.date.astype(str)
    df_to_store['updated_at'] = datetime.now(UTC).replace(microsecond=0).isoformat()
    df_to_store['source'] = 'yfinance'

    records = [tuple(row) for row in df_to_store.to_numpy()]
    conn.executemany(
        """
        INSERT INTO stock_prices (symbol, date, open, high, low, close, volume, adj_close, updated_at, source)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(symbol, date) DO UPDATE SET
            open = excluded.open,
            high = excluded.high,
            low = excluded.low,
            close = excluded.close,
            volume = excluded.volume,
            adj_close = excluded.adj_close,
            updated_at = excluded.updated_at,
            source = excluded.source
        """,
        records,
    )
    conn.commit()
    print(f"Stored {len(df_to_store)} records for {df_to_store['symbol'].iloc[0]}")


def get_latest_update(conn):
    """Return the latest ETL update timestamp for status reporting."""
    row = conn.execute("SELECT MAX(updated_at) FROM stock_prices").fetchone()
    return row[0] if row and row[0] else None


def collect_all_data(stocks=STOCKS, db_path='stock_data.db', period='5d', interval='1d'):
    """Collect data for all stocks with incremental upserts."""
    conn = create_connection(db_path)
    
    # Initialize database
    try:
        initialize_database(conn)
    except Exception as e:
        print(f"Database initialization note: {e}")
    
    print(f"\nCollecting data for {len(stocks)} stocks...")
    
    for symbol in stocks:
        price_data = fetch_stock_data(symbol, period=period, interval=interval)
        if price_data is not None and len(price_data) > 0:
            store_price_data(conn, price_data)

    latest_update = get_latest_update(conn)
    conn.close()
    print("\nData collection complete!")
    if latest_update:
        print(f"Latest update timestamp: {latest_update}")

if __name__ == "__main__":
    collect_all_data()
