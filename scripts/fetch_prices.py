#!/usr/bin/env python3
"""Fetch current prices in EUR for all tracked tickers via Yahoo Finance.

Output: JSON to stdout with structure:
{
  "fetched_at": "2026-06-24T16:45:00",
  "usd_eur": 0.92,
  "prices": {
    "VWCE": {"name": "...", "currency": "EUR", "price_original": 100.5, "price_eur": 100.5, "yahoo": "VWCE.DE"},
    ...
  }
}

Reads target.csv for the ticker list. Falls back to 0.92 USD->EUR if FX fetch fails.
"""
from __future__ import annotations
import csv
import json
import sys
import time
from datetime import datetime
from pathlib import Path

import yfinance as yf

PORTFOLIO_DIR = Path(__file__).resolve().parent.parent
TARGET_CSV = PORTFOLIO_DIR / "target.csv"


def load_target() -> list[dict]:
    rows = []
    with TARGET_CSV.open() as f:
        for r in csv.DictReader(f):
            if r["ticker"] == "CASH":
                continue
            rows.append(r)
    return rows


def fetch_usd_eur() -> float:
    try:
        hist = yf.Ticker("USDEUR=X").history(period="1d")
        if not hist.empty:
            return float(hist["Close"].iloc[-1])
    except Exception as e:
        print(f"WARN: FX fetch failed: {e}", file=sys.stderr)
    return 0.92  # fallback


def fetch_price(yahoo_symbol: str) -> tuple[float, str | None]:
    try:
        hist = yf.Ticker(yahoo_symbol).history(period="1d")
        if hist.empty:
            return 0.0, "no data returned"
        price = float(hist["Close"].iloc[-1])
        if price <= 0:
            return 0.0, "zero/negative price"
        return price, None
    except Exception as e:
        return 0.0, str(e)


def main() -> int:
    target = load_target()
    usd_eur = fetch_usd_eur()

    prices = {}
    for row in target:
        ticker = row["ticker"]
        yahoo = row["yahoo_symbol"]
        currency = row["currency"]
        price_orig, err = fetch_price(yahoo)
        time.sleep(0.05)  # be polite
        if err:
            prices[ticker] = {
                "name": row["name"],
                "currency": currency,
                "yahoo": yahoo,
                "error": err,
            }
            print(f"WARN: {ticker} ({yahoo}): {err}", file=sys.stderr)
            continue
        price_eur = price_orig if currency == "EUR" else price_orig * usd_eur
        prices[ticker] = {
            "name": row["name"],
            "currency": currency,
            "yahoo": yahoo,
            "price_original": round(price_orig, 4),
            "price_eur": round(price_eur, 4),
        }

    output = {
        "fetched_at": datetime.now().isoformat(timespec="seconds"),
        "usd_eur": round(usd_eur, 4),
        "prices": prices,
    }
    json.dump(output, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
