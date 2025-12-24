
### Quick Start - Run Complete Pipeline

**If using standard Python:**
```bash
python main.py
```

This will:
1. Collect stock data from yFinance
2. Store it in SQLite database
3. Generate all visualizations

### Individual Module Usage

#### 1. Collect Stock Data
```bash
python data_collector.py
```

#### 2. Create Visualizations
```bash
python visualize.py
```

## 📁 Project Structure

```
stock_analysis_portfolio/
│
├── schema.sql              # Database schema
├── data_collector.py      # Data collection module
├── visualize.py           # Visualization module
├── main.py                # Main pipeline script
├── requirements.txt       # Python dependencies
├── README.md              # This file
│
├── stock_data.db          # SQLite database (created automatically)
└── visualizations/        # Generated charts (created automatically)
    ├── price_trends.png
    ├── volume_analysis.png
    ├── price_comparison.png
    ├── daily_changes.png
    ├── price_range.png
    └── summary_stats.png
```

## 📊 Database Schema

The SQLite database contains one simple table:

- **stock_prices**: Daily price data (symbol, date, open, high, low, close, volume, adj_close)

## 🔍 Sample SQL Queries

### View all data for a specific stock
```sql
SELECT * FROM stock_prices 
WHERE symbol = 'AAPL' 
ORDER BY date DESC;
```

### Get latest prices for all stocks
```sql
SELECT symbol, date, close, volume 
FROM stock_prices 
WHERE date = (SELECT MAX(date) FROM stock_prices)
ORDER BY symbol;
```

### Find highest and lowest prices
```sql
SELECT 
    symbol,
    MIN(low) as min_price,
    MAX(high) as max_price,
    AVG(close) as avg_price
FROM stock_prices
GROUP BY symbol;
```

## 📈 Visualizations

All visualizations are saved in the `visualizations/` folder:

1. **price_trends.png**: Individual stock price charts with high-low ranges
2. **volume_analysis.png**: Trading volume bars for each stock
3. **price_comparison.png**: Normalized price comparison (all stocks start at 100)
4. **daily_changes.png**: Daily percentage changes (green = up, red = down)
5. **price_range.png**: High-low ranges with close price lines
6. **summary_stats.png**: Four-panel summary with current prices, ranges, volumes

## 🔧 Customization

### Add More Stocks
Edit `STOCKS` list in `data_collector.py`:
```python
STOCKS = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA', 'NVDA']
```

### Change Data Period
Modify the period parameter in `data_collector.py`:
```python
fetch_stock_data(symbol, period='2y')  # 2 years of data
```

### Customize Visualizations
Edit `visualize.py` to modify chart styles, colors, or add new visualizations.

## ⚠️ Important Notes

- **Rate Limiting**: The script includes basic error handling for API calls
- **Data Freshness**: Stock data is fetched in real-time from yFinance
- **Disclaimer**: This is for educational purposes only, not financial advice

## 📚 Dependencies

- `yfinance`: Stock data fetching
- `pandas`: Data manipulation
- `numpy`: Numerical operations
- `matplotlib`: Data visualization
- `sqlite3`: Database (built-in Python module)

## 🤝 Contributing

Feel free to fork this project and add your own visualizations!
