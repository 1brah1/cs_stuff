## Stock Analysis Portfolio

Incremental ETL pipeline for stock data with:

1. SQLite upsert-based storage
2. Dark-themed static chart exports
3. Dark live dashboard with auto-refreshing charts

## Quick Start

Install dependencies:

```bash
pip install -r requirements.txt
```

Run classic pipeline (ETL + PNG chart export):

```bash
python main.py
```

Run live dark dashboard (auto-refresh):

```bash
python run_dashboard.py
```

Open http://localhost:5000 in your browser.

## What Changed

1. ETL now uses incremental upserts instead of deleting existing symbol data.
2. Schema now includes `updated_at` and `source` metadata.
3. Dashboard serves real-time-like charts using browser polling.
4. Static matplotlib charts are now dark-themed.

## Project Structure

```text
stock_analysis_portfolio/
├── app.py                  # Flask API + dashboard server + ETL refresh loop
├── run_dashboard.py        # Dashboard entrypoint
├── schema.sql              # Database schema
├── data_collector.py       # Incremental ETL collector
├── visualize.py            # Static dark PNG visualization generator
├── main.py                 # Classic ETL + static visualization pipeline
├── requirements.txt        # Python dependencies
├── templates/
│   └── dashboard.html      # Dark dashboard page
├── static/
│   ├── css/dashboard.css   # Dashboard styling
│   └── js/dashboard.js     # Chart rendering + polling logic
└── visualizations/         # Generated PNG charts
```

## Live Dashboard API

1. `GET /api/timeseries` - historical chart series for symbols
2. `GET /api/summary` - current summary cards
3. `GET /api/health` - ETL and refresh status
4. `POST /api/refresh` - manual ETL trigger

## Configuration

You can tune refresh/fetch behavior with environment variables:

1. `STOCK_REFRESH_SECONDS` (default `300`)
2. `STOCK_FETCH_PERIOD` (default `5d`)
3. `STOCK_FETCH_INTERVAL` (default `1d`)

Example:

```bash
set STOCK_REFRESH_SECONDS=120
python run_dashboard.py
```

## Database Notes

Table: `stock_prices`

Columns include price fields plus:

1. `updated_at` - UTC ETL write timestamp
2. `source` - data source label (default: `yfinance`)

Primary dedupe/upsert key:

1. `UNIQUE(symbol, date)`

## Static Visualizations

Running `python visualize.py` generates:

1. `visualizations/price_trends.png`
2. `visualizations/volume_analysis.png`
3. `visualizations/price_comparison.png`
4. `visualizations/daily_changes.png`
5. `visualizations/price_range.png`
6. `visualizations/summary_stats.png`

## Important Notes

1. yFinance data is delayed and should not be treated as tick-level trading data.
2. This project is for educational and portfolio use, not financial advice.
