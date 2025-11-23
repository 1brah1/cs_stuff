"""
Simple Stock Data Collector
Fetches stock data from yFinance and stores it in SQLite database
"""

import yfinance as yf
import sqlite3
import pandas as pd
from datetime import datetime

# Tech stocks to analyze
STOCKS = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META']

def create_connection(db_path='stock_data.db'):
    """Create database connection"""
    conn = sqlite3.connect(db_path)
    return conn

def initialize_database(conn):
    """Initialize database with schema"""
    with open('schema.sql', 'r') as f:
        schema = f.read()
    conn.executescript(schema)
    conn.commit()
    print("Database initialized successfully")

def fetch_stock_data(symbol, period='1y'):
    """Fetch stock data from yFinance"""
    try:
        print(f"Fetching data for {symbol}...")
        ticker = yf.Ticker(symbol)
        data = ticker.history(period=period)
        data.reset_index(inplace=True)
        data['symbol'] = symbol
        return data
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

def store_price_data(conn, df):
    """Store price data in database"""
    df_to_store = df[['symbol', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close']].copy()
    df_to_store.columns = ['symbol', 'date', 'open', 'high', 'low', 'close', 'volume', 'adj_close']
    df_to_store['date'] = pd.to_datetime(df_to_store['date']).dt.date
    
    # Remove existing data for this symbol
    conn.execute("DELETE FROM stock_prices WHERE symbol = ?", (df_to_store['symbol'].iloc[0],))
    
    df_to_store.to_sql('stock_prices', conn, if_exists='append', index=False)
    conn.commit()
    print(f"Stored {len(df_to_store)} records for {df_to_store['symbol'].iloc[0]}")

def collect_all_data(stocks=STOCKS, db_path='stock_data.db'):
    """Collect data for all stocks"""
    conn = create_connection(db_path)
    
    # Initialize database
    try:
        initialize_database(conn)
    except Exception as e:
        print(f"Database initialization note: {e}")
    
    print(f"\nCollecting data for {len(stocks)} stocks...")
    
    for symbol in stocks:
        price_data = fetch_stock_data(symbol)
        if price_data is not None and len(price_data) > 0:
            store_price_data(conn, price_data)
    
    conn.close()
    print("\nData collection complete!")

if __name__ == "__main__":
    collect_all_data()
