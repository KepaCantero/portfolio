#!/usr/bin/env python3
"""Analyze portfolio: read holdings.csv + prices.json, output weights & deviations.

Usage:
    python3 analyze.py prices.json > analysis.json
    python3 analyze.py -          # read prices from stdin
"""
from __future__ import annotations
import csv
import json
import sys
from pathlib import Path

PORTFOLIO_DIR = Path(__file__).resolve().parent.parent
HOLDINGS_CSV = PORTFOLIO_DIR / "holdings.csv"
TARGET_CSV = PORTFOLIO_DIR / "target.csv"


def load_csv(path: Path) -> list[dict]:
    with path.open() as f:
        return list(csv.DictReader(f))


def load_prices(prices_arg: str | None) -> dict:
    if not prices_arg or prices_arg == "-":
        return json.load(sys.stdin).get("prices", {})
    return json.loads(Path(prices_arg).read_text()).get("prices", {})


def main() -> int:
    prices_arg = sys.argv[1] if len(sys.argv) > 1 else "-"
    prices = load_prices(prices_arg)

    holdings = load_csv(HOLDINGS_CSV)
    target_rows = load_csv(TARGET_CSV)
    target = {r["ticker"]: r for r in target_rows}

    portfolio = []
    total_eur = 0.0
    for h in holdings:
        ticker = h["ticker"]
        qty = float(h.get("quantity") or 0)
        avg_cost = float(h.get("avg_cost_eur") or 0)
        price_eur = prices.get(ticker, {}).get("price_eur", 0) or avg_cost
        value = qty * price_eur
        cost = qty * avg_cost
        total_eur += value
        t = target.get(ticker, {})
        portfolio.append({
            "ticker": ticker,
            "name": t.get("name", h.get("notes", "")),
            "sleeve": t.get("sleeve", "Other"),
            "quantity": qty,
            "avg_cost_eur": avg_cost,
            "current_price_eur": round(price_eur, 4),
            "value_eur": round(value, 2),
            "cost_eur": round(cost, 2),
            "pnl_eur": round(value - cost, 2),
            "pnl_pct": round((value / cost - 1) * 100, 2) if cost > 0 else 0.0,
            "target_weight_raw": float(t.get("target_weight") or 0),
            "yahoo_symbol": t.get("yahoo_symbol", ""),
            "currency": t.get("currency", ""),
        })

    # normalize target weights so they sum to 1
    total_target = sum(p["target_weight_raw"] for p in portfolio if p["target_weight_raw"] > 0)
    for p in portfolio:
        p["target_weight"] = p["target_weight_raw"] / total_target if total_target > 0 else 0.0
        p["current_weight"] = p["value_eur"] / total_eur if total_eur > 0 else 0.0
        p["deviation_pct"] = round(p["current_weight"] - p["target_weight"], 4)
        p["deviation_eur"] = round(p["current_weight"] * total_eur - p["target_weight"] * total_eur, 2)

    # sleeve summary
    sleeves: dict[str, dict] = {}
    for p in portfolio:
        s = p["sleeve"]
        d = sleeves.setdefault(s, {"value_eur": 0.0, "current_weight": 0.0, "target_weight": 0.0})
        d["value_eur"] += p["value_eur"]
        d["target_weight"] += p["target_weight"]
    for d in sleeves.values():
        d["current_weight"] = round(d["value_eur"] / total_eur, 4) if total_eur > 0 else 0.0
        d["value_eur"] = round(d["value_eur"], 2)
        d["target_weight"] = round(d["target_weight"], 4)

    # sort by current value desc
    portfolio.sort(key=lambda x: -x["value_eur"])

    output = {
        "total_eur": round(total_eur, 2),
        "sleeves": sleeves,
        "holdings": portfolio,
    }
    json.dump(output, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
