#!/usr/bin/env python3
"""Apply the monthly routine defined in STRATEGY.md:
   Tranche 1 (1/3): O (Realty Income) fixed
   Tranche 2 (1/3): most underweight of {VZ, JNJ, MO, XOM, AVGO, ENG, T}
   Tranche 3 (1/3): 2nd most underweight, or AVGO if --tech flag

Usage:
    python3 monthly_buy.py 3000 < analysis.json > proposal.json
    python3 monthly_buy.py 3000 --tech < analysis.json > proposal.json
"""
from __future__ import annotations
import json
import sys

ROUTINE_POOL = ["VZ", "JNJ", "MO", "XOM", "AVGO", "ENG", "T"]


def main() -> int:
    args = sys.argv[1:]
    amount = float(args[0]) if args and not args[0].startswith("--") else 3000.0
    accelerate_tech = "--tech" in args

    analysis = json.load(sys.stdin)
    holdings = analysis["holdings"]
    total_now = analysis["total_eur"]
    by_ticker = {h["ticker"]: h for h in holdings}

    tranche = amount / 3.0
    proposal = []
    deployed = 0.0

    # Tranche 1: O (Realty Income) - fixed
    o = by_ticker.get("O")
    if o and o["current_price_eur"] > 0:
        shares = int(tranche / o["current_price_eur"])
        actual = shares * o["current_price_eur"]
        deployed += actual
        proposal.append({
            "tranche": 1,
            "ticker": "O",
            "name": o.get("name", "Realty Income"),
            "current_price_eur": round(o["current_price_eur"], 2),
            "shares_to_buy": shares,
            "deploy_eur": round(actual, 2),
            "reason": "Fijo segun rutina mensual (pilar del flujo)",
        })
    else:
        proposal.append({
            "tranche": 1,
            "ticker": "O",
            "error": "O no encontrado en holdings o sin precio",
        })

    # Tranche 2: most underweight of routine pool
    candidates = []
    for t in ROUTINE_POOL:
        h = by_ticker.get(t)
        if not h or h["current_price_eur"] <= 0:
            continue
        dev = h["target_weight"] - h["current_weight"]  # >0 means underweight
        candidates.append((t, dev, h))
    candidates.sort(key=lambda x: -x[1])

    tranche2 = None
    if candidates:
        t, dev, h = candidates[0]
        shares = int(tranche / h["current_price_eur"])
        actual = shares * h["current_price_eur"]
        deployed += actual
        tranche2 = {
            "tranche": 2,
            "ticker": t,
            "name": h["name"],
            "current_price_eur": round(h["current_price_eur"], 2),
            "shares_to_buy": shares,
            "deploy_eur": round(actual, 2),
            "reason": f"Mayor desviacion a la baja vs target ({dev*100:+.2f} pp)",
        }
        proposal.append(tranche2)

    # Tranche 3: 2nd most underweight, or AVGO if --tech
    if accelerate_tech and "AVGO" in by_ticker:
        h3 = by_ticker["AVGO"]
        t3 = "AVGO"
        reason = "Acelerar tecnologia (flag --tech)"
    elif len(candidates) > 1:
        t3, dev, h3 = candidates[1]
        reason = f"Segunda mayor desviacion a la baja ({dev*100:+.2f} pp)"
    else:
        h3 = None
        t3 = None
        reason = ""

    if h3 and h3["current_price_eur"] > 0:
        shares = int(tranche / h3["current_price_eur"])
        actual = shares * h3["current_price_eur"]
        deployed += actual
        proposal.append({
            "tranche": 3,
            "ticker": t3,
            "name": h3["name"],
            "current_price_eur": round(h3["current_price_eur"], 2),
            "shares_to_buy": shares,
            "deploy_eur": round(actual, 2),
            "reason": reason,
        })

    output = {
        "new_money_eur": amount,
        "accelerate_tech": accelerate_tech,
        "total_before_eur": total_now,
        "total_after_eur": round(total_now + deployed, 2),
        "deployed_eur": round(deployed, 2),
        "leftover_eur": round(amount - deployed, 2),
        "proposal": proposal,
        "rules_applied": [
            "Tranche 1 fija en O (Realty Income)",
            f"Tranche 2 a la accion mas barata de {', '.join(ROUTINE_POOL)}",
            "Tranche 3: 2a mas barata, o AVGO si flag --tech",
        ],
    }
    json.dump(output, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
