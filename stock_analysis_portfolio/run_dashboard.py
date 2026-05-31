#!/usr/bin/env python
"""Convenience entrypoint for the live stock dashboard."""

from app import app, run_etl_once, start_refresh_thread
from data_collector import STOCKS


if __name__ == "__main__":
    run_etl_once(STOCKS)
    start_refresh_thread()
    app.run(host="0.0.0.0", port=5000, debug=False)
