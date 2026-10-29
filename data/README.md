# data/ — IBKR transactional data

## Files

| File | Source | Purpose |
|---|---|---|
| `transactions.csv` | IBKR Transaction History export (2025-03-27 → 2026-06-12, 429 rows) | Raw input, no modifications |
| `dividends.csv` | Parsed from transactions.csv via `scripts/parse_transactions.py` | One row per dividend payment: date, ticker, gross_eur, withholding_eur, net_eur |
| `trades.csv` | Parsed from transactions.csv | One row per Buy/Sell: qty, price_native, gross_eur, commission_eur, net_eur |
| `activity-statement-2026-06-23-extracts.json` | Manual extracts from pasted IBKR Activity Statement + Tax Lots report | YTD totals, cost basis authoritative, sold tickers, ISIN map |

## Reconciliation status (2026-06-24)

| Metric | transactions.csv (2026 YTD) | Activity Statement (2026 YTD) | Status |
|---|---|---|---|
| **Deposits** | €32,000 (3 entries May 2026) | €32,000 | ✅ Match |
| **Trades purchases** | €57,731 (80 buys) | €68,572 | ⚠️ Gap €10.8k — CSV may exclude early-2026 trades or Forex components not parsed |
| **Trades sales** | €17,585 (26 sells) | €34,937 | ⚠️ Gap €17.4k — same cause |
| **Dividends gross** | €635 (134 payments, of which ~75 in 2026) | €1,524.59 | ⚠️ Gap €889 — Activity Statement likely includes accruals / book entries not in transaction-level CSV |
| **Withholding** | €52.61 | €103.23 | ⚠️ Same proportional gap as dividends |

## Why dividends don't reconcile

The IBKR Transaction History CSV records cash bookings (cash that hit the account on a given date). The Activity Statement's Cash Report includes:
- Cash bookings (same as Transaction History)
- **Accruals** (dividends declared but not yet paid by statement close)
- **Payment in lieu of dividend** (if shares were on loan)
- Reclassifications/adjustments

For **tax filing (IRPF 2026)**, the authoritative number is the Activity Statement total: **€1,524.59 gross, €103.23 withholding, €1,421.36 net**.

For **per-payment detail** (e.g., verifying a specific dividend), use `dividends.csv` — but know that it under-counts vs the statement.

## How to regenerate

```bash
python3 scripts/parse_transactions.py
# → writes data/dividends.csv (134 rows) + data/trades.csv (106 rows)
```

## ISIN map

Full ISIN map in `activity-statement-2026-06-23-extracts.json["isin_map"]`. Useful for Modelo 720 / Anexo A depreciation tracking.
