#!/usr/bin/env python3
"""
Parse IBKR Transaction History CSV into two structured outputs:

  data/dividends.csv  — one row per dividend payment (gross, withholding, net)
  data/trades.csv     — one row per Buy/Sell trade with native + EUR amounts

Source rows use IBKR's Transaction History schema (base currency EUR already
applied to Gross/Net Amount columns). Dividend and Foreign Tax Withholding
rows are paired by (date, ticker) to produce a single dividend payment record.
"""
import csv
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "transactions.csv"
DIV_OUT = ROOT / "data" / "dividends.csv"
TRADES_OUT = ROOT / "data" / "trades.csv"
FX_FALLBACK_USD_TO_EUR = 0.87861  # Activity Statement 2026-06-23 close rate


def parse_amount(s):
    if s is None or s == "" or s == "-":
        return None
    try:
        return float(s)
    except ValueError:
        return None


def parse_int(s):
    if s is None or s == "" or s == "-":
        return None
    try:
        return int(float(s))
    except ValueError:
        return None


def main():
    raw_rows = []
    with SRC.open() as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 12 and row[0] == "Transaction History" and row[1] == "Data":
                raw_rows.append(row)

    # Schema: [prefix, Data, Date, Account, Description, TxType, Symbol,
    #          Quantity, Price, PriceCurrency, GrossAmount, Commission, NetAmount]
    dividends_gross = []   # (date, ticker, gross_eur, description)
    withholding = {}       # (date, ticker) -> withholding_eur
    trades = []
    deposits = []
    interests = []
    adjustments = []

    for r in raw_rows:
        # Pad row defensively
        while len(r) < 12:
            r.append("")
        date, _acct, desc, tx_type, symbol = r[2], r[3], r[4], r[5], r[6]
        qty = parse_amount(r[7])
        price = parse_amount(r[8])
        price_ccy = r[9].strip()
        gross = parse_amount(r[10])
        commission = parse_amount(r[11])
        net = parse_amount(r[12]) if len(r) > 12 else None

        if tx_type == "Dividend":
            dividends_gross.append({
                "date": date, "ticker": symbol, "gross_eur": gross,
                "description": desc, "price_currency": price_ccy,
            })
        elif tx_type == "Foreign Tax Withholding":
            # Match by (date, ticker); accumulate if multiple on same date
            key = (date, symbol)
            withholding[key] = withholding.get(key, 0) + (gross or 0)
        elif tx_type in ("Buy", "Sell"):
            trades.append({
                "date": date, "ticker": symbol, "type": tx_type,
                "quantity": qty, "price_native": price,
                "price_currency": price_ccy or "",
                "gross_eur": gross, "commission_eur": commission,
                "net_eur": net, "description": desc,
            })
        elif tx_type == "Deposit":
            deposits.append({"date": date, "amount_eur": gross, "description": desc})
        elif tx_type == "Credit Interest":
            interests.append({"date": date, "amount_eur": gross, "description": desc})
        elif tx_type == "Adjustment":
            adjustments.append({"date": date, "amount_eur": gross, "description": desc})

    # Build dividends.csv: join gross + withholding by (date, ticker)
    div_rows = []
    for g in dividends_gross:
        key = (g["date"], g["ticker"])
        wh = withholding.get(key, 0.0)
        gross = g["gross_eur"] or 0.0
        div_rows.append({
            "date": g["date"],
            "ticker": g["ticker"],
            "gross_eur": round(gross, 2),
            "withholding_eur": round(abs(wh), 2),
            "net_eur": round(gross + wh, 2),  # wh is negative
            "description": g["description"],
        })

    div_rows.sort(key=lambda x: (x["date"], x["ticker"]), reverse=True)

    with DIV_OUT.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=[
            "date", "ticker", "gross_eur", "withholding_eur", "net_eur", "description"
        ])
        w.writeheader()
        w.writerows(div_rows)

    # Build trades.csv
    trades.sort(key=lambda x: (x["date"], x["ticker"]), reverse=True)
    with TRADES_OUT.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=[
            "date", "ticker", "type", "quantity", "price_native",
            "price_currency", "gross_eur", "commission_eur", "net_eur", "description"
        ])
        w.writeheader()
        w.writerows(trades)

    # Summary to stdout for verification
    total_div = sum(r["gross_eur"] for r in div_rows)
    total_wh = sum(r["withholding_eur"] for r in div_rows)
    total_dep = sum(r["amount_eur"] for r in deposits)
    total_int = sum(r["amount_eur"] for r in interests)
    total_buy = sum(r["gross_eur"] for r in trades if r["type"] == "Buy")
    total_sell = sum(r["gross_eur"] for r in trades if r["type"] == "Sell")

    print(f"Parsed: {len(div_rows)} dividend payments, {len(trades)} trades, "
          f"{len(deposits)} deposits, {len(interests)} interest, {len(adjustments)} adjustments")
    print(f"Dividends total gross: €{total_div:.2f}, withholding: €{total_wh:.2f}, net: €{total_div - total_wh:.2f}")
    print(f"Deposits: €{total_dep:.2f}, Interest: €{total_int:.2f}")
    print(f"Buys gross: €{abs(total_buy):.2f}, Sells gross: €{abs(total_sell):.2f}")
    print(f"Output: {DIV_OUT.relative_to(ROOT)}, {TRADES_OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
