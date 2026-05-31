"""
Live dashboard server for stock analysis portfolio.
Serves a dark themed UI and JSON APIs with periodic ETL refresh.
"""

import os
import threading
import time
from datetime import datetime, UTC

import pandas as pd
from flask import Flask, jsonify, render_template, request

from data_collector import STOCKS, collect_all_data, create_connection


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "stock_data.db")
REFRESH_SECONDS = int(os.getenv("STOCK_REFRESH_SECONDS", "300"))
FETCH_PERIOD = os.getenv("STOCK_FETCH_PERIOD", "5d")
FETCH_INTERVAL = os.getenv("STOCK_FETCH_INTERVAL", "1d")

app = Flask(__name__, template_folder="templates", static_folder="static")
refresh_state = {
    "last_success": None,
    "last_error": None,
    "is_running": False,
}
refresh_stop_event = threading.Event()


def _normalize_symbols(raw_symbols):
    if not raw_symbols:
        return STOCKS

    normalized = []
    for token in raw_symbols.split(","):
        symbol = token.strip().upper()
        if symbol and symbol in STOCKS:
            normalized.append(symbol)

    return normalized or STOCKS


def run_etl_once(stocks=None):
    symbols = stocks or STOCKS
    refresh_state["is_running"] = True
    try:
        collect_all_data(
            stocks=symbols,
            db_path=DB_PATH,
            period=FETCH_PERIOD,
            interval=FETCH_INTERVAL,
        )
        refresh_state["last_success"] = datetime.now(UTC).replace(microsecond=0).isoformat()
        refresh_state["last_error"] = None
    except Exception as exc:
        refresh_state["last_error"] = str(exc)
    finally:
        refresh_state["is_running"] = False


def refresh_loop():
    while not refresh_stop_event.is_set():
        run_etl_once(STOCKS)
        refresh_stop_event.wait(REFRESH_SECONDS)


def start_refresh_thread():
    thread = threading.Thread(target=refresh_loop, daemon=True)
    thread.start()
    return thread


def _query_timeseries(symbols):
    placeholders = ",".join(["?"] * len(symbols))
    query = (
        "SELECT symbol, date, open, high, low, close, volume, adj_close, updated_at "
        f"FROM stock_prices WHERE symbol IN ({placeholders}) ORDER BY date ASC"
    )

    conn = create_connection(DB_PATH)
    try:
        df = pd.read_sql_query(query, conn, params=symbols)
    finally:
        conn.close()

    if df.empty:
        return []

    df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")

    payload = []
    for symbol in symbols:
        symbol_df = df[df["symbol"] == symbol].copy()
        if symbol_df.empty:
            continue

        first_close = float(symbol_df["close"].iloc[0])
        normalized = ((symbol_df["close"] / first_close) * 100.0).round(2)
        changes = (symbol_df["close"].pct_change().fillna(0.0) * 100.0).round(3)

        payload.append(
            {
                "symbol": symbol,
                "dates": symbol_df["date"].tolist(),
                "close": symbol_df["close"].round(2).tolist(),
                "high": symbol_df["high"].round(2).tolist(),
                "low": symbol_df["low"].round(2).tolist(),
                "volume": symbol_df["volume"].fillna(0).astype(int).tolist(),
                "normalized": normalized.tolist(),
                "daily_change": changes.tolist(),
            }
        )

    return payload


def _query_summary(symbols):
    placeholders = ",".join(["?"] * len(symbols))
    query = (
        "SELECT symbol, MIN(low) AS min_price, MAX(high) AS max_price, "
        "AVG(volume) AS avg_volume, MAX(updated_at) AS updated_at "
        f"FROM stock_prices WHERE symbol IN ({placeholders}) GROUP BY symbol"
    )

    conn = create_connection(DB_PATH)
    try:
        summary_df = pd.read_sql_query(query, conn, params=symbols)
        latest_query = (
            "SELECT sp.symbol, sp.date, sp.close FROM stock_prices sp "
            "INNER JOIN (SELECT symbol, MAX(date) AS max_date FROM stock_prices GROUP BY symbol) latest "
            "ON sp.symbol = latest.symbol AND sp.date = latest.max_date "
            f"WHERE sp.symbol IN ({placeholders})"
        )
        latest_df = pd.read_sql_query(latest_query, conn, params=symbols)
    finally:
        conn.close()

    if summary_df.empty:
        return []

    merged = summary_df.merge(latest_df, on="symbol", how="left")
    merged["range"] = (merged["max_price"] - merged["min_price"]).round(2)
    merged["avg_volume_m"] = (merged["avg_volume"] / 1_000_000.0).round(2)
    merged["close"] = merged["close"].round(2)

    return merged[
        ["symbol", "close", "date", "min_price", "max_price", "range", "avg_volume_m", "updated_at"]
    ].to_dict(orient="records")


@app.route("/")
def dashboard():
    return render_template("dashboard.html", symbols=STOCKS, refresh_seconds=REFRESH_SECONDS)


@app.route("/api/timeseries")
def api_timeseries():
    symbols = _normalize_symbols(request.args.get("symbols"))
    return jsonify({"symbols": symbols, "series": _query_timeseries(symbols)})


@app.route("/api/summary")
def api_summary():
    symbols = _normalize_symbols(request.args.get("symbols"))
    return jsonify({"symbols": symbols, "summary": _query_summary(symbols)})


@app.route("/api/health")
def api_health():
    conn = create_connection(DB_PATH)
    try:
        row = conn.execute("SELECT MAX(updated_at), COUNT(*) FROM stock_prices").fetchone()
    finally:
        conn.close()

    return jsonify(
        {
            "refresh_seconds": REFRESH_SECONDS,
            "fetch_period": FETCH_PERIOD,
            "fetch_interval": FETCH_INTERVAL,
            "last_db_update": row[0] if row else None,
            "row_count": int(row[1]) if row else 0,
            "last_success": refresh_state["last_success"],
            "last_error": refresh_state["last_error"],
            "is_running": refresh_state["is_running"],
            "server_time_utc": datetime.now(UTC).replace(microsecond=0).isoformat(),
        }
    )


@app.route("/api/refresh", methods=["POST"])
def api_refresh():
    if not refresh_state["is_running"]:
        threading.Thread(target=run_etl_once, kwargs={"stocks": STOCKS}, daemon=True).start()
    return jsonify({"status": "started", "is_running": True})


if __name__ == "__main__":
    # Prime initial data quickly before the refresh loop starts.
    run_etl_once(STOCKS)
    start_refresh_thread()
    app.run(host="0.0.0.0", port=5000, debug=False)
