"""Parse IBKR PortfolioAnalyst Inception CSV into structured outputs.

Reads:  ~/Downloads/Kepa_Cantero_Inception_June_24_2026.csv
Writes:
  coverage/inception-2026-06-24.json        - master JSON, all sections
  data/deposits-withdrawals.csv             - cash flow
  data/dividends-inception.csv              - comprehensive dividends
  data/corporate-actions.csv                - splits/spinoffs
  data/interest.csv                         - credit interest
  data/trade-summary.csv                    - aggregate trades per symbol
  data/performance-by-symbol.csv            - per-symbol perf with realized P&L
  data/projected-income.csv                 - forward yield
"""
from __future__ import annotations
import csv
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path("/Users/kepa.cantero/Projects/portfolio")
SRC = Path.home() / "Downloads" / "Kepa_Cantero_Inception_June_24_2026.csv"

COVERAGE = ROOT / "coverage"
DATA = ROOT / "data"
COVERAGE.mkdir(exist_ok=True)
DATA.mkdir(exist_ok=True)

# ---------- raw rows ----------
rows: list[list[str]] = []
with SRC.open(newline="") as f:
    reader = csv.reader(f)
    for r in reader:
        rows.append(r)

def section_rows(name: str) -> list[list[str]]:
    """Return only Data rows of a section (skip MetaInfo/Header)."""
    out = []
    in_section = False
    for r in rows:
        if not r:
            continue
        if r[0] == name:
            in_section = True
            continue
        if in_section and r[0].startswith(name):  # also catches "Performance by Symbol" matching "Performance"
            # be strict: section is exactly column[0]
            pass
        if in_section:
            if r[1] == "Data":
                out.append(r)
            elif r[0] != name:
                # we've left the section
                in_section = False
    return out

# Re-do with strict section matching
def section_data_rows(name: str) -> list[list[str]]:
    out = []
    for r in rows:
        if len(r) >= 2 and r[0] == name and r[1] == "Data":
            out.append(r[2:])  # strip section + "Data"
    return out

def section_header(name: str) -> list[str] | None:
    for r in rows:
        if len(r) >= 2 and r[0] == name and r[1] == "Header":
            return r[2:]
    return None

# ---------- profile ----------
profile = {}
for r in section_data_rows("Profile"):
    if len(r) >= 2:
        profile[r[0]] = r[1]

# ---------- key statistics ----------
ks_header = section_header("Key Statistics")
ks_data = section_data_rows("Key Statistics")
key_stats = {}
if ks_header and ks_data:
    for h, v in zip(ks_header, ks_data[0]):
        key_stats[h] = v

# ---------- historical performance (annualized) ----------
def parse_historical_perf():
    out = {"account_returns": {}, "monthly": {}, "quarterly": {}, "yearly": {}}
    cur_block = None
    for r in rows:
        if not r or len(r) < 2:
            continue
        if r[0] != "Historical Performance (Annualized)":
            continue
        if r[1] == "Header":
            if "Account" in r[2:]:
                cur_block = "account_returns"
            elif r[2] == "Month":
                cur_block = "monthly"
            elif r[2] == "Quarter":
                cur_block = "quarterly"
            elif r[2] == "Year":
                cur_block = "yearly"
            continue
        if r[1] == "Data" and cur_block:
            if cur_block == "account_returns":
                # Account, MTD, QTD, YTD, 1Year, SinceInception
                vals = r[2:]
                if len(vals) >= 6:
                    out["account_returns"][vals[0]] = {
                        "MTD": vals[1], "QTD": vals[2], "YTD": vals[3],
                        "1Year": vals[4], "SinceInception": vals[5],
                    }
            else:
                # Period, Account, Return
                if len(r) >= 5:
                    out[cur_block][r[2]] = r[4]
    return out

historical_perf = parse_historical_perf()

# ---------- historical benchmark comparison ----------
bench_perf = {}
for r in section_data_rows("Historical Performance Benchmark Comparison (Annualized)"):
    if len(r) >= 6:
        bench_perf[r[0]] = {
            "MTD": r[1], "QTD": r[2], "YTD": r[3], "1Year": r[4], "SinceInception": r[5],
        }

# ---------- open positions ----------
open_positions = []
for r in section_data_rows("Open Position Summary"):
    # Date, FinancialInstrument, Currency, Symbol, Description, Sector, Quantity, ClosePrice, Value, Cost Basis, UnrealizedP&L, FXRateToBase
    if len(r) >= 12 and r[0] != "Total":
        open_positions.append({
            "date": r[0], "instrument": r[1], "currency": r[2], "symbol": r[3],
            "description": r[4], "sector": r[5], "quantity": r[6], "close_price": r[7],
            "value": r[8], "cost_basis": r[9], "unrealized_pl": r[10], "fx_to_base": r[11],
        })

# ---------- allocation: asset class / financial instrument ----------
def parse_alloc_table(section: str) -> list[dict]:
    h = section_header(section)
    out = []
    for r in section_data_rows(section):
        rec = {}
        for k, v in zip(h, r):
            rec[k] = v
        out.append(rec)
    return out

alloc_asset_class = parse_alloc_table("Allocation by Asset Class")
alloc_fin_instr = parse_alloc_table("Allocation by Financial Instrument")

# ---------- allocation & performance by region / sector ----------
def parse_alloc_perf(section: str) -> dict:
    """Two sub-blocks: Allocation by X, Performance by X."""
    out = {"allocation": [], "performance": []}
    cur = None
    for r in rows:
        if len(r) < 2 or r[0] != section:
            continue
        if r[1] == "Header":
            if "Allocation" in r[2]:
                cur = "allocation"
                hdr = r[2:]
            elif "Performance" in r[2]:
                cur = "performance"
                hdr = r[2:]
        elif r[1] == "Data" and cur:
            rec = {k: v for k, v in zip(hdr, r[2:])}
            if rec.get(hdr[0]) == "Total":
                cur_key = "total"
            else:
                cur_key = rec[hdr[0]]
            rec["_key"] = cur_key
            out[cur].append(rec)
    return out

alloc_perf_region = parse_alloc_perf("Allocation and Performance by Region")
alloc_perf_sector = parse_alloc_perf("Allocation and Performance by Sector")

# ---------- time period / cumulative performance ----------
def parse_period_perf(section: str) -> list[dict]:
    h = section_header(section)
    out = []
    for r in section_data_rows(section):
        rec = {k: v for k, v in zip(h, r)}
        out.append(rec)
    return out

time_period_perf = parse_period_perf("Time Period Performance Statistics")
cumulative_perf = parse_period_perf("Cumulative Performance Statistics")
time_period_bench = parse_period_perf("Time Period Benchmark Comparison")
cumulative_bench = parse_period_perf("Cumulative Benchmark Comparison")

# ---------- risk measures ----------
risk = {}
risk_header = section_header("Risk Measures")
for r in section_data_rows("Risk Measures"):
    if len(r) >= 3:
        # Risk Measure, Account, Account Value
        risk[r[0].rstrip(":")] = r[2]

risk_bench = {"account": {}, "benchmark": {}, "relative": {}}
cur_block = None
for r in rows:
    if len(r) < 2 or r[0] != "Risk Measures Benchmark Comparison":
        continue
    if r[1] == "Header":
        if "Risk Measure" in r[2] and "BM1" in r[3:]:
            cur_block = "compare"
        elif "Relative" in r[2]:
            cur_block = "relative"
        continue
    if r[1] == "Data":
        if cur_block == "compare":
            # Risk Measure:, BM1, value, Account, value
            if len(r) >= 6:
                risk_bench["benchmark"][r[2].rstrip(":")] = r[4]
                risk_bench["account"][r[2].rstrip(":")] = r[6]
        elif cur_block == "relative":
            if len(r) >= 5:
                risk_bench["relative"][r[2].rstrip(":")] = r[4]

# ---------- value at risk ----------
var_rows = []
var_header = ["Symbol", "Description", "Price", "Value (EUR)",
              "VC Price", "VC Change%", "VC P&L",
              "Hist Price", "Hist Change%", "Hist P&L"]
for r in section_data_rows("Value at Risk"):
    if len(r) >= 2 and r[0] in ("Sub-Portfolios", "Currency Risk Factors"):
        cur_block = r[0]
        continue
    if len(r) >= 10 and r[0] not in ("Total",):
        var_rows.append({
            "symbol": r[0], "description": r[1], "price": r[2], "value_eur": r[3],
            "var_cov_price": r[4], "var_cov_change_pct": r[5], "var_cov_pl": r[6],
            "hist_price": r[7], "hist_change_pct": r[8], "hist_pl": r[9],
        })

# ---------- performance attribution ----------
attrib = {"contribution_to_return": [], "attribution_effect": []}
cur = None
for r in rows:
    if len(r) < 2 or r[0] != "Performance Attribution vs. Vanguard Total Bond Market ETF":
        continue
    if r[1] == "Header":
        if "Contribution To Return" in r[2:4]:
            cur = "contribution_to_return"
            hdr = r[2:]
        elif "Attribution Effect" in r[2:4]:
            cur = "attribution_effect"
            hdr = r[2:]
    elif r[1] == "Data" and cur:
        rec = {k: v for k, v in zip(hdr, r[2:])}
        attrib[cur].append(rec)

# ---------- performance by asset class / financial instrument / symbol ----------
perf_asset_class = parse_alloc_table("Performance by Asset Class")
perf_fin_instr = parse_alloc_table("Performance by Financial Instrument")

def parse_perf_symbol(section: str) -> list[dict]:
    h = section_header(section)
    out = []
    for r in section_data_rows(section):
        rec = {k: v for k, v in zip(h, r)}
        out.append(rec)
    return out

perf_symbol = parse_perf_symbol("Performance by Symbol")
perf_long_short = parse_perf_symbol("Performance by Long Short")
perf_underlying = parse_perf_symbol("Performance by Underlying")

# ---------- projected income ----------
proj_hdr = section_header("Projected Income")
proj = []
for r in section_data_rows("Projected Income"):
    rec = {k: v for k, v in zip(proj_hdr, r)}
    proj.append(rec)

# ---------- trade summary ----------
ts_hdr = section_header("Trade Summary")
trade_summary = []
for r in section_data_rows("Trade Summary"):
    rec = {k: v for k, v in zip(ts_hdr, r)}
    trade_summary.append(rec)

# ---------- deposits & withdrawals ----------
dw_hdr = section_header("Deposits And Withdrawals")
deposits = []
for r in section_data_rows("Deposits And Withdrawals"):
    rec = {k: v for k, v in zip(dw_hdr, r)}
    deposits.append(rec)

# ---------- corporate actions ----------
ca_hdr = section_header("Corporate Actions")
corp_actions = []
for r in section_data_rows("Corporate Actions"):
    rec = {k: v for k, v in zip(ca_hdr, r)}
    corp_actions.append(rec)

# ---------- dividends ----------
div_hdr = section_header("Dividends")
dividends = []
for r in section_data_rows("Dividends"):
    rec = {k: v for k, v in zip(div_hdr, r)}
    dividends.append(rec)

# ---------- interest ----------
int_hdr = section_header("Interest Details")
interest = []
for r in section_data_rows("Interest Details"):
    rec = {k: v for k, v in zip(int_hdr, r)}
    interest.append(rec)

# ---------- investment themes ----------
themes_hdr = section_header("Investment Themes")
themes = []
for r in section_data_rows("Investment Themes"):
    rec = {k: v for k, v in zip(themes_hdr, r)}
    themes.append(rec)

# ---------- concentration summary (just top-level holdings + totals) ----------
concentration_holdings = []
in_holdings = False
for r in rows:
    if len(r) < 2 or r[0] != "Concentration":
        continue
    if r[1] == "Header" and r[2] == "SubSection":
        # next data is start of a new subsection
        continue
    if r[1] == "Data":
        sub = r[2]
        if sub == "Holdings" and not r[3].startswith(" "):
            # top-level holding row (not indented breakdown)
            concentration_holdings.append({
                "symbol": r[3], "description": r[4], "sector": r[5],
                "long_value": r[6], "short_value": r[7], "net_value": r[8],
                "long_weight_pct": r[9], "short_weight_pct": r[10], "net_weight_pct": r[11],
            })

# ============ write master JSON ============
master = {
    "_source": "Kepa_Cantero_Inception_June_24_2026.csv",
    "_as_of": "2026-06-23",
    "_analysis_period": "2024-07-02 to 2026-06-23",
    "profile": profile,
    "key_statistics": key_stats,
    "historical_performance": historical_perf,
    "historical_performance_benchmark": bench_perf,
    "time_period_performance": time_period_perf,
    "cumulative_performance": cumulative_perf,
    "time_period_benchmark": time_period_bench,
    "cumulative_benchmark": cumulative_bench,
    "open_positions": open_positions,
    "allocation": {
        "asset_class_timeseries": alloc_asset_class,
        "financial_instrument_timeseries": alloc_fin_instr,
        "region": alloc_perf_region,
        "sector": alloc_perf_sector,
    },
    "performance": {
        "by_asset_class": perf_asset_class,
        "by_financial_instrument": perf_fin_instr,
        "by_symbol": perf_symbol,
        "by_long_short": perf_long_short,
        "by_underlying": perf_underlying,
        "attribution_vs_BND": attrib,
    },
    "risk_measures": {
        "account": risk,
        "vs_VDHG": risk_bench,
    },
    "value_at_risk": var_rows,
    "projected_income": proj,
    "concentration_top_holdings": concentration_holdings[:100],
    "investment_themes": themes,
    "cashflows": {
        "deposits_withdrawals_count": len(deposits),
        "deposits_withdrawals_total_eur": sum(
            float(r["Amount"]) for r in deposits if r.get("Amount") and r["Amount"] not in ("-", "")
        ),
        "dividends_count": len(dividends),
        "dividends_lifetime_eur": sum(
            float(r["Amount"]) for r in dividends if r.get("Amount") and r["Amount"] not in ("-", "")
        ),
        "interest_count": len(interest),
        "interest_lifetime_eur": sum(
            float(r["Amount"]) for r in interest if r.get("Amount") and r["Amount"] not in ("-", "")
        ),
        "corporate_actions_count": len(corp_actions),
    },
}

(COVERAGE / "inception-2026-06-24.json").write_text(
    json.dumps(master, indent=2, ensure_ascii=False)
)

# ============ write data/*.csv ============
def write_csv(path: Path, header: list[str], rows: list[dict]):
    with path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        for r in rows:
            w.writerow([r.get(h, "") for h in header])

# Deposits & withdrawals
write_csv(
    DATA / "deposits-withdrawals.csv",
    ["Date", "Type", "Description", "Amount"],
    deposits,
)

# Dividends (comprehensive lifetime)
write_csv(
    DATA / "dividends-inception.csv",
    ["PayDate", "ExDate", "Symbol", "Quantity", "DividendPerShare", "Amount"],
    dividends,
)

# Corporate actions
write_csv(
    DATA / "corporate-actions.csv",
    ["Date", "Type", "Description", "Quantity"],
    corp_actions,
)

# Interest
write_csv(
    DATA / "interest.csv",
    ["Date", "Description", "Amount"],
    interest,
)

# Trade summary (per-symbol aggregate)
write_csv(
    DATA / "trade-summary.csv",
    ["FinancialInstrument", "Currency", "Symbol", "Description", "Sector",
     "QuantityBought", "AvgPriceBought", "ProceedsBought", "ProceedsBoughtBase",
     "QuantitySold", "AvgPriceSold", "ProceedsSold", "ProceedsSoldBase"],
    trade_summary,
)

# Performance by symbol (has realized/unrealized P&L)
write_csv(
    DATA / "performance-by-symbol.csv",
    ["Symbol", "Description", "FinancialInstrument", "Sector",
     "AvgWeight", "Return", "Contribution",
     "Unrealized_PL", "Realized_PL", "Open"],
    perf_symbol,
)

# Projected income
write_csv(
    DATA / "projected-income.csv",
    ["FinancialInst", "Symbol", "Description", "Frequency", "Quantity",
     "Price", "Value", "CurrentYieldPct", "Principal",
     "EstAnnualIncome", "Est2026RemainingIncome"],
    proj,
)

# Investment themes
write_csv(
    DATA / "investment-themes.csv",
    ["Theme", "CompanyCount", "Description", "WeightPct", "RankAdjustedWeightPct"],
    themes,
)

# Report
print(f"Wrote coverage/inception-2026-06-24.json")
print(f"Wrote data/deposits-withdrawals.csv ({len(deposits)} rows)")
print(f"Wrote data/dividends-inception.csv ({len(dividends)} rows)")
print(f"Wrote data/corporate-actions.csv ({len(corp_actions)} rows)")
print(f"Wrote data/interest.csv ({len(interest)} rows)")
print(f"Wrote data/trade-summary.csv ({len(trade_summary)} rows)")
print(f"Wrote data/performance-by-symbol.csv ({len(perf_symbol)} rows)")
print(f"Wrote data/projected-income.csv ({len(proj)} rows)")
print(f"Wrote data/investment-themes.csv ({len(themes)} rows)")
print()
print(f"Deposits lifetime: {master['cashflows']['deposits_withdrawals_total_eur']:.2f} EUR")
print(f"Dividends lifetime: {master['cashflows']['dividends_lifetime_eur']:.2f} EUR")
print(f"Interest lifetime: {master['cashflows']['interest_lifetime_eur']:.2f} EUR")
