#!/usr/bin/env python3
"""Score each holding on the 3-layer framework from RULES.md:
   - Layer 1 SAFETY: payout, debt/equity, dividend history, P/E -> 0-100 score
   - Layer 2 VALUATION: Kelley Wright signal + DDM fair value + Graham P/E
   - Layer 3 ALLOCATION: Carlson BSD ranking, band alerts

Usage:
    python3 score.py                # score every holding
    python3 score.py < analysis.json   # use existing analysis for context

Reads holdings.csv + target.csv for the ticker list.
Uses yfinance for fundamentals (free, ~15min delay).
"""
from __future__ import annotations
import csv
import json
import sys
import time
from datetime import datetime
from pathlib import Path
import math

import yfinance as yf

PORTFOLIO_DIR = Path(__file__).resolve().parent.parent
HOLDINGS_CSV = PORTFOLIO_DIR / "holdings.csv"
TARGET_CSV = PORTFOLIO_DIR / "target.csv"

# Discount rates for DDM (per RULES.md V2)
DISCOUNT_RATE = 0.09
GROWTH_DEFAULT = 0.04
GROWTH_QUALITY = 0.06  # for AVGO

# Graham thresholds
PE_DEFENSIVE_MAX = 15
PE_KEEP_MAX = 25
PE_BUBBLE = 40

# Payout
PAYOUT_SAFE = 0.50
PAYOUT_HARD_MAX = 0.75
PAYOUT_VETO = 0.90

# Vanguard bands
BAND_RELATIVE = 0.25  # 25% relative


def load_target_tickers() -> dict[str, dict]:
    out = {}
    with TARGET_CSV.open() as f:
        for r in csv.DictReader(f):
            # skip cash + comment/metadata rows (target.csv lleva comentarios "#")
            if not r.get("ticker") or r["ticker"] == "CASH" or r["ticker"].startswith("#"):
                continue
            out[r["ticker"]] = r
    return out


def load_holdings_tickers() -> set[str]:
    with HOLDINGS_CSV.open() as f:
        return {r["ticker"] for r in csv.DictReader(f)}


def safe_get(info: dict, *keys, default=None):
    """Traverse nested dict."""
    cur = info
    for k in keys:
        if not isinstance(cur, dict):
            return default
        cur = cur.get(k, default)
    return cur if cur is not None else default


def fetch_fundamentals(yahoo_symbol: str) -> dict:
    cache_path = PORTFOLIO_DIR / "coverage" / "fundamentals-cache.json"
    cache = {}
    if cache_path.exists():
        try:
            cache = json.loads(cache_path.read_text())
        except Exception:
            cache = {}

    t = yf.Ticker(yahoo_symbol)
    try:
        info = t.info or {}
    except Exception:
        # fallback: última foto buena (marcada como stale)
        if yahoo_symbol in cache:
            f = dict(cache[yahoo_symbol])
            f["_cached"] = True
            return f
        raise

    # Dividend history (consecutive years with at least one payment) + deteccion de congelacion (S2)
    try:
        divs = t.dividends
        if not divs.empty:
            years_paid = divs.resample("YE").size()
            years_paid = years_paid[years_paid > 0]
            div_years = int(len(years_paid))
        else:
            div_years = 0
    except Exception:
        div_years = 0

    # Dividend growth (CAGR) over last 5y + congelacion: 2+ anos completos sin subida anual
    div_growth_5y = None
    dividend_frozen = False
    try:
        if not divs.empty:
            yearly = divs.resample("YE").sum()
            if len(yearly) >= 6:
                start = float(yearly.iloc[-6])
                end = float(yearly.iloc[-1])
                if start > 0:
                    div_growth_5y = (end / start) ** (1 / 5) - 1
            # congelacion: los 2 ultimos anos completos sin superar el maximo anual previo (+0,1% tolerancia)
            if len(yearly) >= 3:
                prev_max = float(yearly.iloc[:-2].max())
                dividend_frozen = all(float(y) <= prev_max * 1.001 for y in yearly.iloc[-2:])
    except Exception:
        pass

    out = {
        "payout_ratio": float(info.get("payoutRatio") or 0),
        "trailing_pe": float(info.get("trailingPE") or 0),
        "debt_to_equity": float(info.get("debtToEquity") or 0) / 100,  # yfinance returns %
        "dividend_rate": float(info.get("dividendRate") or 0),
        "dividend_yield": float(info.get("dividendYield") or info.get("yield") or 0),
        "five_year_avg_yield": float(info.get("fiveYearAvgDividendYield") or 0) / 100,
        "beta": float(info.get("beta") or 0),
        "current_price": float(info.get("currentPrice") or info.get("regularMarketPrice") or 0),
        "dividend_years": div_years,
        "dividend_growth_5y": div_growth_5y,
        "dividend_frozen": dividend_frozen,
    }
    cache[yahoo_symbol] = out
    try:
        cache_path.write_text(json.dumps(cache, indent=1, default=str))
    except Exception:
        pass
    return out


# --- LAYER 1: SAFETY ---

def score_safety(f: dict) -> dict:
    """Compute 0-100 safety score per RULES.md."""
    # Payout score (v1.2+ aprobado: payout desconocido = 0 con flag DATO_FALTANTE — antes 50, optimista)
    pr = f["payout_ratio"]
    if pr == 0:
        payout_score = 0
    elif pr <= PAYOUT_SAFE:
        payout_score = 100
    elif pr <= PAYOUT_HARD_MAX:
        payout_score = 100 - (pr - PAYOUT_SAFE) / (PAYOUT_HARD_MAX - PAYOUT_SAFE) * 30
    elif pr <= PAYOUT_VETO:
        payout_score = 70 - (pr - PAYOUT_HARD_MAX) / (PAYOUT_VETO - PAYOUT_HARD_MAX) * 50
    else:
        payout_score = 0

    # P/E score
    pe = f["trailing_pe"]
    if pe == 0:
        pe_score = 50
    elif pe <= PE_DEFENSIVE_MAX:
        pe_score = 100
    elif pe <= PE_KEEP_MAX:
        pe_score = 70
    elif pe < PE_BUBBLE:
        pe_score = 30
    else:
        pe_score = 0

    # Debt/Equity score (lower is better)
    de = f["debt_to_equity"]
    if de <= 1.0:
        de_score = 100
    elif de <= 2.0:
        de_score = 80 - (de - 1.0) * 30
    elif de <= 3.0:
        de_score = 50 - (de - 2.0) * 30
    else:
        de_score = max(0, 20 - (de - 3.0) * 10)

    # Dividend history
    years = f["dividend_years"]
    history_score = min(100, years * 10)

    # Weighted
    total = (payout_score * 0.30 + pe_score * 0.20 + de_score * 0.25 + history_score * 0.25)
    grade = "A" if total >= 80 else "B" if total >= 60 else "C" if total >= 40 else "D"

    return {
        "payout_ratio": round(pr, 4),
        "payout_score": round(payout_score, 1),
        "payout_dato_faltante": pr == 0,
        "dividend_frozen": bool(f.get("dividend_frozen")),
        "trailing_pe": round(pe, 2),
        "pe_score": round(pe_score, 1),
        "debt_to_equity": round(de, 2),
        "de_score": round(de_score, 1),
        "dividend_years": years,
        "history_score": round(history_score, 1),
        "safety_total": round(total, 1),
        "safety_grade": grade,
    }


# --- LAYER 2: VALUATION ---

def score_valuation(f: dict, ticker: str, growth_assumption: float = None) -> dict:
    if growth_assumption is None:
        growth_assumption = GROWTH_QUALITY if ticker == "AVGO" else GROWTH_DEFAULT

    # Kelley Wright signal
    cur_yield = f["dividend_yield"]
    avg_yield = f["five_year_avg_yield"]
    # estimate 1 sigma as 20% of mean (rough proxy without full distribution)
    sigma_proxy = max(avg_yield * 0.20, 0.005) if avg_yield > 0 else 0
    if avg_yield > 0:
        if cur_yield > avg_yield + sigma_proxy:
            kw_signal = "REINFORCED_BUY"
        elif cur_yield < avg_yield - sigma_proxy:
            kw_signal = "EXPENSIVE"
        else:
            kw_signal = "FAIR"
    else:
        kw_signal = "NO_DATA"

    # DDM Gordon model: fair = D1 / (r - g)
    div_rate = f["dividend_rate"]
    price = f["current_price"]
    if div_rate > 0 and growth_assumption < DISCOUNT_RATE:
        d1 = div_rate * (1 + growth_assumption)
        fair_value = d1 / (DISCOUNT_RATE - growth_assumption)
        if price > 0:
            ratio = price / fair_value
            if ratio < 0.95:
                ddm_signal = "UNDERVALUED"
            elif ratio > 1.05:
                ddm_signal = "OVERVALUED"
            else:
                ddm_signal = "FAIR"
        else:
            ddm_signal = "NO_PRICE"
    else:
        fair_value = None
        ddm_signal = "NO_DIVIDEND"

    # Graham check
    pe = f["trailing_pe"]
    if pe == 0:
        graham = "NO_DATA"
    elif pe <= PE_DEFENSIVE_MAX:
        graham = "PASS"
    elif pe <= PE_KEEP_MAX:
        graham = "OK_KEEP"
    else:
        graham = "FAIL"

    return {
        "current_yield_pct": round(cur_yield * 100, 2),
        "five_year_avg_yield_pct": round(avg_yield * 100, 2) if avg_yield > 0 else None,
        "kelley_wright_signal": kw_signal,
        "ddm_fair_value": round(fair_value, 2) if fair_value else None,
        "ddm_current_price": round(price, 2) if price else None,
        "ddm_signal": ddm_signal,
        "graham_pe_check": graham,
        "growth_assumption": growth_assumption,
    }


# --- LAYER 3: ALLOCATION flags ---

def band_alert(current_weight: float, target_weight: float) -> str | None:
    """Vanguard 25% relative band."""
    if target_weight <= 0:
        return None
    deviation_rel = abs(current_weight - target_weight) / target_weight
    if deviation_rel > BAND_RELATIVE:
        direction = "OVERWEIGHT" if current_weight > target_weight else "UNDERWEIGHT"
        return f"BAND_BREACH_{direction}"
    return None


def main() -> int:
    targets = load_target_tickers()
    holdings_tickers = load_holdings_tickers()
    tickers_to_score = sorted(set(targets) | holdings_tickers)

    # Optional: read existing analysis for current weights
    analysis = None
    if not sys.stdin.isatty():
        try:
            analysis = json.load(sys.stdin)
        except Exception:
            analysis = None

    weights_by_ticker = {}
    if analysis:
        for h in analysis.get("holdings", []):
            weights_by_ticker[h["ticker"]] = h["current_weight"]

    results = {}
    for ticker in tickers_to_score:
        meta = targets.get(ticker, {})
        yahoo = meta.get("yahoo_symbol", ticker)
        try:
            f = fetch_fundamentals(yahoo)
            time.sleep(0.1)
            safety = score_safety(f)
            valuation = score_valuation(f, ticker)
            cw = weights_by_ticker.get(ticker, 0)
            tw = float(meta.get("target_weight") or 0)
            band = band_alert(cw, tw) if analysis else None
            results[ticker] = {
                "name": meta.get("name", ""),
                "sleeve": meta.get("sleeve", ""),
                "yahoo": yahoo,
                "fundamentals": f,
                "safety": safety,
                "valuation": valuation,
                "current_weight": round(cw, 4),
                "target_weight": round(tw, 4),
                "band_alert": band,
            }
        except Exception as e:
            results[ticker] = {"error": str(e), "yahoo": yahoo}
            print(f"WARN: {ticker} ({yahoo}): {e}", file=sys.stderr)

    output = {
        "scored_at": datetime.now().isoformat(timespec="seconds"),
        "rules_version": "RULES.md v1",
        "scores": results,
    }
    json.dump(output, sys.stdout, indent=2, default=str)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
