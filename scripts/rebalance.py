#!/usr/bin/env python3
"""Propose how to allocate NEW MONEY across the portfolio to minimize deviation vs target.

Strategy enforced (per STRATEGY.md):
- New money goes ONLY to the Stock sleeve (never to VWCE/VHYL with new cash).
- Allocation is greedy: at each step, add to the most underweight asset relative to target.
- Respects share rounding (buys whole shares, leftover cash reported).

Usage:
    python3 rebalance.py 3000 < analysis.json > proposal.json
"""
from __future__ import annotations
import json
import sys


def greedy_allocate(holdings: list[dict], total_now: float, new_money: float, step: float = 5.0) -> dict:
    """Iteratively give `step` EUR to the most underweight asset vs target."""
    eligible = [
        h for h in holdings
        if h["sleeve"] == "Stock" and h["target_weight"] > 0 and h["current_price_eur"] > 0
    ]
    state = {
        h["ticker"]: {
            "name": h["name"],
            "current_value": h["value_eur"],
            "current_price": h["current_price_eur"],
            "target_weight": h["target_weight"],
            "alloc": 0.0,
        }
        for h in eligible
    }
    total_after = total_now + new_money
    remaining = new_money
    while remaining >= step:
        best_ticker = None
        best_dev = -float("inf")
        for t, s in state.items():
            target_value = s["target_weight"] * total_after
            dev = target_value - (s["current_value"] + s["alloc"])
            if dev > best_dev:
                best_dev = dev
                best_ticker = t
        if best_ticker is None or best_dev <= 0:
            break
        state[best_ticker]["alloc"] += step
        remaining -= step
    return state


def main() -> int:
    new_money = float(sys.argv[1]) if len(sys.argv) > 1 else 3000.0
    analysis = json.load(sys.stdin)
    holdings = analysis["holdings"]
    total_now = analysis["total_eur"]

    state = greedy_allocate(holdings, total_now, new_money)

    proposal = []
    deployed = 0.0
    for ticker, s in sorted(state.items(), key=lambda kv: -kv[1]["alloc"]):
        if s["alloc"] <= 0:
            continue
        shares = int(s["alloc"] / s["current_price"])
        actual = shares * s["current_price"]
        deployed += actual
        target_value_after = s["target_weight"] * (total_now + new_money)
        value_after = s["current_value"] + actual
        proposal.append({
            "ticker": ticker,
            "name": s["name"],
            "current_price_eur": round(s["current_price"], 2),
            "current_value_eur": round(s["current_value"], 2),
            "shares_to_buy": shares,
            "deploy_eur": round(actual, 2),
            "value_after_eur": round(value_after, 2),
            "target_value_after_eur": round(target_value_after, 2),
            "gap_after_eur": round(target_value_after - value_after, 2),
        })

    output = {
        "new_money_eur": new_money,
        "total_before_eur": total_now,
        "total_after_eur": round(total_now + deployed, 2),
        "deployed_eur": round(deployed, 2),
        "leftover_eur": round(new_money - deployed, 2),
        "proposal": proposal,
        "rules_applied": [
            "New money only to Stock sleeve (per STRATEGY.md principle #2)",
            "Greedy allocation to most underweight asset vs target",
            "Whole shares; leftover cash reported",
        ],
    }
    json.dump(output, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
