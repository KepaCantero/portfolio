#!/usr/bin/env python3
"""sleeve_test.py — EL ARBITRO del nivel 7 (RULES v1.4, test pre-registrado).

Compara el BLOQUE CONGELADO (VHYL + VZ/O/JNJ/XOM/MO) contra una cartera espejo
en VWCE con el mismo dinero, desde t0 = 30-sep-2026 (fecha de la congelacion).

Criterio pre-registrado (decisions.md 30-sep-2026):
  - Evaluacion: 31-dic de cada ano; VEREDICTO 31-dic-2028.
  - Si XIRR bloque < XIRR espejo VWCE  -> DISOLVER el bloque (vender -> VWCE).
  - Si XIRR bloque >= espejo           -> CONTINUA (y evidencia para reactivar nivel 7).

Modos:
  python3 sleeve_test.py baseline   # primera vez / reinicio: fija t0 con los valores actuales
  python3 sleeve_test.py evaluate   # calcula XIRR bloque vs espejo desde t0 hasta hoy

Fuentes:
  - Valores actuales: coverage/analysis-YYYY-MM-DD.json mas reciente (field value_eur).
  - Precio VWCE: coverage/prices-YYYY-MM-DD.json de la misma fecha.
  - Dividendos del bloque (flujos positivos): data/dividends-inception.csv, PayDate > t0.
    Limitacion: USD convertido a fx constante 0.879 (documentado; refinable con AS).

Limitaciones conocidas (v0):
  - El espejo asume ejecucion al precio VWCE de t0 sin comision/track.
  - No incluye el modo --full-history (flujos 2025-03+): requiere export completo de
    transacciones IBKR (data/transactions-full.csv) — pendiente del usuario. El test
    OFICIAL pre-registrado usa la ventana t0=30-sep-2026, que es exacta.
"""
from __future__ import annotations
import csv, json, sys
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COV = ROOT / "coverage"
BLOCK = ["VHYL", "VZ", "O", "JNJ", "XOM", "MO"]
BASELINE_FILE = COV / "sleeve-test-baseline.json"
USD_EUR = 0.879  # fx constante documentada
EUR_NATIVE = {"VHYL"}  # dentro del bloque


def latest(pattern):
    files = sorted(COV.glob(pattern))
    return files[-1] if files else None


def load_values():
    a = latest("analysis-*.json")
    p = latest("prices-*.json")
    if not a or not p:
        sys.exit("ERROR: no hay coverage/analysis-*.json o prices-*.json")
    A = json.loads(a.read_text())
    P = json.loads(p.read_text())
    vals = {h["ticker"]: h["value_eur"] for h in A["holdings"]}
    vwce_price = P["prices"]["VWCE"]["price_eur"]
    return vals, vwce_price, a.stem.replace("analysis-", ""), A


def dividends_since(paydate_after: str) -> list[tuple[str, float]]:
    """Dividendos del bloque con PayDate > paydate_after (YYYYMMDD). [(fecha, EUR bruto)]"""
    f = ROOT / "data" / "dividends-inception.csv"
    if not f.exists():
        return []
    out = []
    for r in csv.DictReader(f.open()):
        d = (r.get("PayDate") or "").strip()
        if not d or d <= paydate_after:
            continue
        sym = r.get("Symbol")
        if sym in BLOCK:
            amt = float(r.get("Amount") or 0)
            out.append((d, amt if sym in EUR_NATIVE else amt * USD_EUR))
    return out


def xnpv(rate: float, flows: list[tuple[float, float]]) -> float:
    t0 = min(t for t, _ in flows)
    return sum(cf / (1 + rate) ** ((t - t0) / 365.0) for t, cf in flows)


def xirr(flows: list[tuple[float, float]]) -> float | None:
    lo, hi = -0.99, 10.0
    f_lo, f_hi = xnpv(lo, flows), xnpv(hi, flows)
    if f_lo * f_hi > 0:
        return None
    for _ in range(200):
        mid = (lo + hi) / 2
        f_mid = xnpv(mid, flows)
        if abs(f_mid) < 1e-9:
            return mid
        if f_lo * f_mid < 0:
            hi, f_hi = mid, f_mid
        else:
            lo, f_lo = mid, f_mid
    return (lo + hi) / 2


def to_yearfrac(datestr: str) -> float:
    dt = datetime.strptime(datestr[:8], "%Y%m%d")
    return (dt - datetime(2026, 9, 30)).days / 365.0 + 0.0


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "evaluate"
    vals, vwce_price, as_of, A = load_values()

    if mode == "baseline":
        t0_vals = {t: vals[t] for t in BLOCK if t in vals}
        total_t0 = sum(t0_vals.values())
        base = {
            "t0": "2026-09-30",
            "fixed_with_data_of": as_of,
            "block_values_eur_t0": t0_vals,
            "block_total_eur_t0": round(total_t0, 2),
            "vwce_price_eur_t0": vwce_price,
            "mirror_shares": round(total_t0 / vwce_price, 4),
            "criterion": "31-dic-2028: XIRR bloque < XIRR espejo -> DISOLVER; >= -> CONTINUA",
            "fx_note": "dividendos USD convertidos a 0.879 constante",
        }
        BASELINE_FILE.write_text(json.dumps(base, indent=1, ensure_ascii=False))
        print(json.dumps(base, indent=1, ensure_ascii=False))
        return

    if not BASELINE_FILE.exists():
        sys.exit("No hay baseline: ejecuta primero 'python3 sleeve_test.py baseline'")
    B = json.loads(BASELINE_FILE.read_text())
    t0_total = B["block_total_eur_t0"]
    mirror_shares = B["mirror_shares"]

    # --- flujos del BLOQUE: -t0, +dividendos, +terminal ---
    divs = dividends_since("20260930")
    block_flows = [(0.0, -t0_total)]
    for d, amt in divs:
        block_flows.append((to_yearfrac(d), amt))
    terminal_block = sum(vals[t] for t in BLOCK if t in vals)
    today_frac = (date.today() - date(2026, 9, 30)).days / 365.0
    block_flows.append((today_frac, terminal_block))

    # --- espejo VWCE: -t0, +terminal (acumulativo, sin flujos intermedios) ---
    mirror_flows = [(0.0, -t0_total), (today_frac, mirror_shares * vwce_price)]

    r_block = xirr(block_flows)
    r_mirror = xirr(mirror_flows)

    out = {
        "evaluated_with_data_of": as_of,
        "years_elapsed": round(today_frac, 2),
        "block": {
            "t0_eur": t0_total,
            "dividends_received_eur": round(sum(a for _, a in divs), 2),
            "n_payments": len(divs),
            "terminal_eur": round(terminal_block, 2),
            "xirr_pct": round(r_block * 100, 2) if r_block is not None else None,
        },
        "mirror_vwce": {
            "shares": mirror_shares,
            "terminal_eur": round(mirror_shares * vwce_price, 2),
            "xirr_pct": round(r_mirror * 100, 2) if r_mirror is not None else None,
        },
    }
    if r_block is not None and r_mirror is not None and today_frac > 0.02:
        diff_pp = (r_block - r_mirror) * 100
        out["diff_pp"] = round(diff_pp, 2)
        out["signal"] = ("DISOLVER (por debajo del espejo)" if diff_pp < 0
                         else "CONTINUA (bate o iguala al espejo)")
        out["verdict_binding"] = "solo a 31-dic-2028 (criterio pre-registrado)"
    else:
        out["signal"] = "VENTANA INSUFICIENTE (baseline; sin XIRR significativo)"

    print(json.dumps(out, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
