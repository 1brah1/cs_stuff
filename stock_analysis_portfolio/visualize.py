"""
Stock Market Data Visualization
Simple visualizations of stock market data from SQL database
"""

import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

plt.style.use('dark_background')

def create_connection(db_path='stock_data.db'):
    """Create database connection"""
    return sqlite3.connect(db_path)

def load_stock_data(conn, symbols=None):
    """Load stock price data from database"""
    if symbols:
        placeholders = ','.join(['?'] * len(symbols))
        query = f"SELECT * FROM stock_prices WHERE symbol IN ({placeholders}) ORDER BY symbol, date"
        df = pd.read_sql_query(query, conn, params=symbols)
    else:
        query = "SELECT * FROM stock_prices ORDER BY symbol, date"
        df = pd.read_sql_query(query, conn)
    
    df['date'] = pd.to_datetime(df['date'])
    return df

def plot_price_trends(df, save_path='visualizations/price_trends.png'):
    """Plot stock price trends over time"""
    symbols = df['symbol'].unique()
    n_stocks = len(symbols)
    
    fig, axes = plt.subplots(n_stocks, 1, figsize=(14, 4 * n_stocks))
    if n_stocks == 1:
        axes = [axes]
    
    for idx, symbol in enumerate(sorted(symbols)):
        symbol_data = df[df['symbol'] == symbol].sort_values('date')
        ax = axes[idx]

        ax.plot(symbol_data['date'], symbol_data['close'],
               label='Close Price', linewidth=2, color='deepskyblue')
        ax.fill_between(symbol_data['date'], symbol_data['low'], symbol_data['high'],
                        alpha=0.25, color='deepskyblue', label='High-Low Range')
        
        ax.set_title(f'{symbol} - Stock Price Trend', fontsize=14, fontweight='bold')
        ax.set_xlabel('Date', fontsize=11)
        ax.set_ylabel('Price ($)', fontsize=11)
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Saved: {save_path}")
    plt.close()

def plot_volume_analysis(df, save_path='visualizations/volume_analysis.png'):
    """Plot trading volume over time"""
    symbols = df['symbol'].unique()
    n_stocks = len(symbols)
    
    fig, axes = plt.subplots(n_stocks, 1, figsize=(14, 4 * n_stocks))
    if n_stocks == 1:
        axes = [axes]
    
    for idx, symbol in enumerate(sorted(symbols)):
        symbol_data = df[df['symbol'] == symbol].sort_values('date')
        ax = axes[idx]

        ax.bar(symbol_data['date'], symbol_data['volume'] / 1e6,
               color='orange', alpha=0.75, width=1)
        
        ax.set_title(f'{symbol} - Trading Volume', fontsize=14, fontweight='bold')
        ax.set_xlabel('Date', fontsize=11)
        ax.set_ylabel('Volume (Millions)', fontsize=11)
        ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Saved: {save_path}")
    plt.close()

def plot_price_comparison(df, save_path='visualizations/price_comparison.png'):
    """Compare all stocks on a single chart (normalized)"""
    plt.figure(figsize=(14, 8))
    
    symbols = sorted(df['symbol'].unique())
    colors = plt.cm.tab10(np.linspace(0, 1, len(symbols)))
    
    for symbol, color in zip(symbols, colors):
        symbol_data = df[df['symbol'] == symbol].sort_values('date')
        # Normalize to starting price (100)
        normalized = (symbol_data['close'] / symbol_data['close'].iloc[0]) * 100
        plt.plot(symbol_data['date'], normalized, label=symbol, 
                linewidth=2, color=color, alpha=0.8)
    
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Normalized Price (Starting = 100)', fontsize=12)
    plt.title('Stock Price Comparison (Normalized)', fontsize=16, fontweight='bold', pad=20)
    plt.legend(loc='best', fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Saved: {save_path}")
    plt.close()

def plot_daily_changes(df, save_path='visualizations/daily_changes.png'):
    """Plot daily price changes"""
    symbols = df['symbol'].unique()
    n_stocks = len(symbols)
    
    fig, axes = plt.subplots(n_stocks, 1, figsize=(14, 4 * n_stocks))
    if n_stocks == 1:
        axes = [axes]
    
    for idx, symbol in enumerate(sorted(symbols)):
        symbol_data = df[df['symbol'] == symbol].sort_values('date').copy()
        symbol_data['daily_change'] = symbol_data['close'].pct_change() * 100
        symbol_data['daily_change_pct'] = symbol_data['daily_change']
        
        ax = axes[idx]
        colors = ['green' if x > 0 else 'red' if x < 0 else 'gray' 
                 for x in symbol_data['daily_change_pct']]
        
        ax.bar(symbol_data['date'], symbol_data['daily_change_pct'], 
              color=colors, alpha=0.7, width=1)
        ax.axhline(y=0, color='white', linestyle='-', linewidth=0.7, alpha=0.75)
        
        ax.set_title(f'{symbol} - Daily Price Changes (%)', fontsize=14, fontweight='bold')
        ax.set_xlabel('Date', fontsize=11)
        ax.set_ylabel('Daily Change (%)', fontsize=11)
        ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Saved: {save_path}")
    plt.close()

def plot_price_range(df, save_path='visualizations/price_range.png'):
    """Plot high-low price ranges"""
    plt.figure(figsize=(14, 8))
    
    symbols = sorted(df['symbol'].unique())
    colors = plt.cm.Set2(np.linspace(0, 1, len(symbols)))
    
    for symbol, color in zip(symbols, colors):
        symbol_data = df[df['symbol'] == symbol].sort_values('date')
        dates = symbol_data['date']
        
        # Plot high-low range
        plt.fill_between(dates, symbol_data['low'], symbol_data['high'],
                        alpha=0.3, color=color, label=f'{symbol} Range')
        # Plot close price line
        plt.plot(dates, symbol_data['close'], linewidth=2, 
                color=color, label=f'{symbol} Close', alpha=0.8)
    
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Price ($)', fontsize=12)
    plt.title('Stock Price Ranges (High-Low) and Close Prices', fontsize=16, fontweight='bold', pad=20)
    plt.legend(loc='best', fontsize=9, ncol=2)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Saved: {save_path}")
    plt.close()

def plot_summary_statistics(df, save_path='visualizations/summary_stats.png'):
    """Create summary statistics visualization"""
    summary_data = []
    
    for symbol in sorted(df['symbol'].unique()):
        symbol_data = df[df['symbol'] == symbol]
        summary_data.append({
            'Symbol': symbol,
            'Current Price': symbol_data['close'].iloc[-1],
            'Min Price': symbol_data['low'].min(),
            'Max Price': symbol_data['high'].max(),
            'Avg Volume (M)': symbol_data['volume'].mean() / 1e6
        })
    
    summary_df = pd.DataFrame(summary_data)
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Current prices
    axes[0, 0].bar(summary_df['Symbol'], summary_df['Current Price'], color='deepskyblue')
    axes[0, 0].set_title('Current Stock Prices', fontweight='bold')
    axes[0, 0].set_ylabel('Price ($)')
    axes[0, 0].grid(True, alpha=0.3, axis='y')
    
    # Price range
    x_pos = np.arange(len(summary_df))
    axes[0, 1].bar(x_pos, summary_df['Max Price'] - summary_df['Min Price'], 
                  color='orange', alpha=0.8)
    axes[0, 1].set_xticks(x_pos)
    axes[0, 1].set_xticklabels(summary_df['Symbol'])
    axes[0, 1].set_title('Price Range (Max - Min)', fontweight='bold')
    axes[0, 1].set_ylabel('Price Range ($)')
    axes[0, 1].grid(True, alpha=0.3, axis='y')
    
    # Average volume
    axes[1, 0].bar(summary_df['Symbol'], summary_df['Avg Volume (M)'], color='green', alpha=0.7)
    axes[1, 0].set_title('Average Trading Volume', fontweight='bold')
    axes[1, 0].set_ylabel('Volume (Millions)')
    axes[1, 0].grid(True, alpha=0.3, axis='y')
    
    # Price comparison
    axes[1, 1].scatter(summary_df['Symbol'], summary_df['Current Price'], 
                      s=summary_df['Avg Volume (M)'] * 10, alpha=0.6, c='purple')
    axes[1, 1].set_title('Price vs Volume (Bubble Size = Volume)', fontweight='bold')
    axes[1, 1].set_ylabel('Current Price ($)')
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Saved: {save_path}")
    plt.close()

def create_all_visualizations(db_path='stock_data.db', symbols=None):
    """Create all visualizations"""
    import os
    os.makedirs('visualizations', exist_ok=True)
    
    conn = create_connection(db_path)
    df = load_stock_data(conn, symbols)
    conn.close()
    
    if df.empty:
        print("No data found in database. Please run data_collector.py first.")
        return
    
    print("\nGenerating visualizations...")
    
    plot_price_trends(df, 'visualizations/price_trends.png')
    plot_volume_analysis(df, 'visualizations/volume_analysis.png')
    plot_price_comparison(df, 'visualizations/price_comparison.png')
    plot_daily_changes(df, 'visualizations/daily_changes.png')
    plot_price_range(df, 'visualizations/price_range.png')
    plot_summary_statistics(df, 'visualizations/summary_stats.png')
    
    print("\nAll visualizations created successfully!")
    print("Check the 'visualizations' folder for all charts.")

if __name__ == "__main__":
    create_all_visualizations()


