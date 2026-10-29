#!/usr/bin/env python3
"""Dashboard data aggregator — construye dashboard/data.json desde 4 proyectos.

Proyectos: portfolio, casa, money, algoTrading
Uso: python3 dashboard/build_data.py
"""
from __future__ import annotations
import csv, json, re, os
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CASA = ROOT.parent / "casa"
MONEY = ROOT.parent / "money"
ALGO = ROOT.parent / "algoTrading"
OUT = ROOT / "dashboard" / "data.json"

def lj(p):
    try: return json.loads(Path(p).read_text())
    except: return {}

def latest(pattern):
    fs = sorted((ROOT/"coverage").glob(pattern))
    return fs[-1] if fs else None

# ─── PORTFOLIO ───────────────────────────────────────────────────────────────
def portfolio():
    snap = lj(latest("snapshot-*.json") or "/dev/null")
    an = lj(latest("analysis-*.json") or "/dev/null")
    s = snap.get("summary_eur", {})
    positions = []
    for h in (an.get("holdings") or []):
        if h["ticker"] == "CASH": continue
        positions.append({"t": h["ticker"], "v": h.get("value_eur",0), "w": h.get("current_weight",0),
                          "p": h.get("pnl_eur",0), "pp": h.get("pnl_pct",0), "s": h.get("sleeve","")})
    g = lj(ROOT/"graph"/"graph.json")
    threads = [{"n":e["name"],"d":e["obs"][0] if e.get("obs") else ""} for e in g.get("entities",[])
               if e.get("type")=="Thread" and any("ABIERTO" in o for o in e.get("obs",[]))]
    events = [{"n":e["name"],"d":e["obs"][0] if e.get("obs") else ""} for e in g.get("entities",[])
              if e.get("type")=="Event"]
    contras = [{"n":e["name"],"o":e.get("obs",[])} for e in g.get("entities",[])
               if e.get("type")=="Contradiction"]
    cands = {}
    cf = ROOT/"data"/"candidates.csv"
    if cf.exists():
        for r in csv.DictReader(cf.open()):
            cands[r["ticker"]] = {"st": r.get("status",""), "ul": r.get("unlock_condition","")}
    st = lj(ROOT/"coverage"/"sleeve-test-baseline.json")
    # decisions recientes
    decisions = []
    dfile = ROOT/"decisions.md"
    if dfile.exists():
        text = dfile.read_text()
        decisions = [{"t":m,"d":text[text.find(m):text.find(m)+200].replace("\n"," ")[:150]}
                     for m in re.findall(r'## \d{4}-\d{2}-\d{2}[^—]*—[^*]*', text)[:8]]
    return {"nlv": s.get("net_liquidation_value",0), "cash": s.get("settled_cash",0),
            "pnl": s.get("unrealized_pnl_header",0), "date": snap.get("snapshot_date","—"),
            "positions": positions, "sleeves": an.get("sleeves",{}),
            "candidates": cands, "threads": threads, "events": events,
            "contradictions": contras,
            "graph": {"e": len(g.get("entities",[])), "r": len(g.get("relations",[]))},
            "test2028": {"block": st.get("block_total_eur_t0",0), "sh": st.get("mirror_shares",0),
                         "px": st.get("vwce_price_eur_t0",0)},
            "decisions": decisions}

# ─── CASA ────────────────────────────────────────────────────────────────────
def casa():
    d = {"top": [], "perfil": {"ingresos": "4.200 €/mes", "sin_alquiler": True,
         "ahorros": "~70 k€ + Deka 33 k€", "techo_bizkaia": "210 k€", "techo_cantabria": "188 k€"}}
    reg = CASA/"08_registro"/"registro-global.md"
    if reg.exists():
        raw = reg.read_text()
        text = raw[:raw.find("## 1. Benchmarks")] if "## 1. Benchmarks" in raw else raw[:6000]
        for m in re.finditer(r'\|\s*(?:🟢|⚠️|🔴)?\s*\*{0,2}([A-Z0-9][-\w\s\.]+?)\*{0,2}\s*\|[^|]*\|([^|]*)\|([\d.,]+)\s*k?[€e]', text):
            calle = m.group(1).strip()
            try:
                precio = float(m.group(3).replace(".","").replace(",","."))
                if precio > 50: d["top"].append({"c": calle, "p": precio})
            except: pass
    return d

# ─── MONEY ───────────────────────────────────────────────────────────────────
def money():
    tracks = []
    for name, path in [("Micro-SaaS","02_micro-saas"),("Consultoría IA","03_consultoria")]:
        if (MONEY/path/"README.md").exists():
            tracks.append({"n": name, "st": "investigación", "files": len(list((MONEY/path).glob("*.md")))})
    return {"tracks": tracks, "informe": "ANALISIS_MODELOS_NEGOCIO.md v3.0"}

# ─── ALGOTRADING ─────────────────────────────────────────────────────────────
def algo():
    d = {"status": "inactivo", "last_commit": "—", "strategies": 0, "backtests": 0,
         "market_regime": "—", "signals": {}}
    strat_dir = ALGO/"app"/"domain"/"strategies"
    if strat_dir.exists():
        d["strategies"] = len([f for f in strat_dir.glob("*.py")
                               if f.stem not in ("__init__","base","factory","registry","strategy","models","protocols","config_loader")])
    reports = sorted((ALGO/"reports").glob("backtesting*.json")) if (ALGO/"reports").exists() else []
    d["backtests"] = len(reports)
    if reports:
        last = lj(reports[-1])
        sig = last.get("signals", {})
        d["signals"] = {"buy": sig.get("buy_signals",0), "sell": sig.get("sell_signals",0), "hold": sig.get("hold_signals",0)}
        d["last_backtest"] = reports[-1].stem.replace("backtesting_real_data_","")[:8]
        risk = last.get("risk", {})
        d["risk"] = f"{risk.get('risk_level','—')} ({risk.get('violation_count',0)} viol.)"
        # positions del último backtest
        alloc = last.get("allocation", {})
        d["positions"] = [p.get("symbol","") for p in (alloc.get("positions") or [])]
    dash_state = lj(ALGO/"outputs"/"dashboard_state.json")
    if dash_state:
        d["market_regime"] = dash_state.get("market_regime","—")
        d["volatility"] = dash_state.get("volatility",0)
        d["vol_regime"] = dash_state.get("volatility_regime","—")
    # git
    try:
        import subprocess
        r = subprocess.run(["git","-C",str(ALGO),"log","--oneline","-1"], capture_output=True, text=True, timeout=5)
        if r.returncode == 0: d["last_commit"] = r.stdout.strip()[:60]
    except: pass
    d["presentation_files"] = len(list((ALGO/"app"/"presentation").rglob("*.py"))) if (ALGO/"app"/"presentation").exists() else 0
    return d

# ─── MAIN ────────────────────────────────────────────────────────────────────
def main():
    data = {"generated": datetime.now().isoformat(timespec="minutes"),
            "portfolio": portfolio(), "casa": casa(), "money": money(), "algo": algo()}
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(data, indent=1, ensure_ascii=False, default=str))
    p = data["portfolio"]; a = data["algo"]
    print(f"✓ data.json — NLV {p['nlv']:,.0f}€ · {len(p['positions'])} pos · {len(p['threads'])} hilos · "
          f"grafo {p['graph']['e']}e/{p['graph']['r']}r · "
          f"casa {len(data['casa']['top'])} top · "
          f"algo {a['strategies']} strat/{a['backtests']} bt · "
          f"money {len(data['money']['tracks'])} tracks")

if __name__ == "__main__":
    main()
