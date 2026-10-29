# HANDOFF — sesión nueva

**Fecha**: 2026-06-25
**Estado**: IBKR Inception report completamente parseado. Coverage y data enriquecidos con 24 secciones consolidadas (desde julio 2024). Holdings.csv sigue con 3 errores pendientes (ver abajo).

## Contexto

El usuario pasó en sesiones anteriores:
1. **portfolio.txt** (2026-06-24 intraday) — snapshot IBKR. YA parseado → `holdings.csv` + `coverage/snapshot-2026-06-24.json`.
2. **Activity Statement** (Jun 23 2026) — pegado en chat. Extracts en `data/activity-statement-2026-06-23-extracts.json`.
3. **Transaction History CSV** — copiado a `data/transactions.csv`, YA parseado a `data/dividends.csv` (134 rows) y `data/trades.csv` (106 rows).

Y en esta sesión (2026-06-25):
4. **PortfolioAnalyst Inception CSV** (`~/Downloads/Kepa_Cantero_Inception_June_24_2026.csv`, 13,607 líneas, 24 secciones, lifetime 2024-07-02 a 2026-06-23). ES LA FUENTE MÁS CONSOLIDADA. Parseado a:
   - `coverage/inception-2026-06-24.json` — master JSON con todas las secciones.
   - 8 CSVs en `data/`: deposits-withdrawals.csv, dividends-inception.csv (207 rows lifetime), corporate-actions.csv, interest.csv, trade-summary.csv, performance-by-symbol.csv, projected-income.csv, investment-themes.csv.

## Lo que ya está hecho (sesión 2026-06-25)

- **`scripts/parse_inception.py`** — parser robusto, re-ejecutable (idempotente).
- **`coverage/inception-2026-06-24.json`** con 20 secciones top-level: profile, key_statistics, historical_performance (+ benchmark), time_period, cumulative (+ benchmark), open_positions, allocation (asset_class/financial_instrument/region/sector), performance (by_symbol/long_short/underlying/attribution_vs_BND), risk_measures (account + vs_VDHG + relative), value_at_risk, projected_income, concentration_top_holdings, investment_themes, cashflows.
- **`coverage/snapshot-2026-06-24.json`** enriquecido con sección `inception_2026_06_23` que incluye:
  - Key Statistics (NAV, returns YTD/1y/SinceInception, deposits, dividends lifetime, fees)
  - Risk Measures (Sharpe 0.66, Sortino 0.98, MaxDD 9.15%, Turnover 32.5%)
  - Benchmark vs VDHG (correlation 0.59, beta 0.59, alpha 0.37%, IR -3.72)
  - Monthly/Quarterly returns timeseries
  - Deposits breakdown (2024: €38.7k, 2025: €20k, 2026 YTD: €32k)
  - Corporate actions (AVGO split 2024-07-12, CMCSA spinoff 2026-01-02)
  - Investor profile (age 44, objectives Preservation/Growth/Income)
- **`decisions.md`** entrada del 2026-06-25 added.

## Correcciones importantes aplicadas

| Concepto | Antes (mal) | Ahora (correcto) | Fuente |
|---|---|---|---|
| `realized_pnl_lifetime` | 9099.57 L/T YTD (proceeds mal interpretado) | **1022.09 EUR** lifetime net gain | Inception Performance by Symbol |
| `dividends_lifetime` | confuso (460 accruals, 1525 mixto) | **2,619.99 EUR** lifetime paid (oficial) | Inception Key Statistics |
| `dividends_ytd_2026` paid-only | 1524.59 (incluye accruals) | **~610.81 EUR** (paid-only, FX≈0.87861) | dividends-inception.csv filtrado 2026 |
| `deposits_lifetime` | 32000 YTD solo | **90,700.01 EUR** lifetime | Inception Key Statistics |

## Errores pendientes en holdings.csv (arreglar en próxima sesión)

| Ticker | Actual (mal) | Correcto | Fuente |
|---|---|---|---|
| MVUS | USD, avg 83.00 | EUR, avg 94.15 | Activity Statement + Inception Open Positions |
| IHYG | USD, avg 82.80 | EUR, avg 93.92 | Activity Statement + Inception Open Positions |
| FGQI | EUR, avg 8.97 | USD nativo, avg_eur ≈ 7.89 | Activity Statement + Inception Open Positions |

**Alternativa más limpia**: usar directamente `coverage/inception-2026-06-24.json.open_positions` que ya tiene los 24 tickers con currency, quantity, close_price, value (EUR), cost_basis (EUR), unrealized_pl (EUR), fx_to_base. Reescribir holdings.csv desde ahí.

## Hallazgos clave del Inception (no en fuentes anteriores)

- **Sharpe Ratio 0.66 vs VDHG 1.05** — peor risk-adjusted pero YTD batiendo (12.3% vs 4.5%).
- **Max Drawdown 9.15%** en Feb-Apr 2025, recovery 7 meses. VDHG solo 6.18%.
- **Beta 0.59** — cartera claramente defensiva.
- **Realized P&L por símbolo lifetime**:
  - **Ganadores**: CSPX +€940, EQQQ +€533, MO +€730, VZ +€89, T +€56
  - **Perdedores**: STLA -€583, IBTS -€424, CMCSA -€195, PG -€55, PFE -€21, MSFT -€27, HD -€6, PEP -€5, VSNT -€10
  - **Neto**: +€1,022.09
- **Trade Summary lifetime**: comprado ~€68k / vendido ~€14.5k. (No confundir €14k proceeds con €9k gains — eran fuentes distintas.)
- **Projected income 2026**: €2,088.78 EUR anual estimado (yield 3.23% sobre €64,631 invertido).
- **Investment Themes top**: AI Inference 10.16%, Machine Learning 9.24%, Generative AI 9.16% — alta exposición indirecta a AI vía GOOG, AVGO, TXN.
- **Allocation current** (Jun 23 2026):
  - Asset class: Equities 90.4%, Fixed Income 4.6%, Real Estate 4.5%, Cash 0.6%
  - Region: Europe 79.8% (Ireland 79.4% por UCITS), North America 20.2%
  - Sector: Broad 75.5% (fondos), Consumer Non-Cyc 4.4%, Healthcare 4.3%, Real Estate 4.5%, Government 3.9%, Energy 2.0%, Tech 3.4%
- **Corporate actions**:
  - 2024-07-12: AVGO 10-for-1 split (ratio 0.5112 → post-split qty ajustada)
  - 2026-01-02: CMCSA spinoff 1-for-25 from LILAK (qty 0.7886) — posteriormente vendido en ene-2026

## Próximos pasos sugeridos (sesión nueva)

1. **Arreglar holdings.csv desde inception open_positions** (mejor que arreglar los 3 errores a mano). Script: leer `coverage/inception-2026-06-24.json` → `holdings.csv` regenerado con currency, qty, value_eur, cost_basis_eur, unrealized_pl_eur correctos.
2. **Consolidar dividends**: los 3 archivos (`data/dividends.csv` de transactions, `data/dividends-inception.csv` nueva, y extracts del activity statement) tienen overlaps. Decidir uno como fuente única (recomendado: dividends-inception.csv por ser más completo) y borrar los otros o marcar como deprecated en `data/README.md`.
3. **Actualizar `prompts/analyze-portfolio.md` Section A** para que el agente use `inception_2026_06_23` del snapshot cuando exista (con fallback a `summary_eur` para sesiones sin Inception).
4. **Calculadora fiscal IRPF 2026**: con dividends-inception.csv + interest.csv + corporate-actions.csv + realized P&L por symbol, se puede construir un script `scripts/tax_2026.py` que produzca los importes a declarar (dividends brutos, withholding deducible, ganancias L/T vs S/T, intereses).

## Mapa de archivos relevantes

```
portfolio/
├── data/
│   ├── transactions.csv                                    ← IBKR Transaction History 2025-03 a 2026-06
│   ├── dividends.csv                                       ← parseado de transactions (134 rows YTD 2026)
│   ├── trades.csv                                          ← parseado de transactions (106 rows)
│   ├── dividends-inception.csv                             ← ★ NUEVO: 207 rows lifetime dividends
│   ├── deposits-withdrawals.csv                            ← ★ NUEVO: 21 deposits 2024-2026
│   ├── corporate-actions.csv                               ← ★ NUEVO: AVGO split + CMCSA spinoff
│   ├── interest.csv                                        ← ★ NUEVO: 4 rows credit interest
│   ├── trade-summary.csv                                   ← ★ NUEVO: 33 símbolos agregado lifetime
│   ├── performance-by-symbol.csv                           ← ★ NUEVO: 38 símbolos con realized+unrealized P&L
│   ├── projected-income.csv                                ← ★ NUEVO: 23 posiciones, yield forward 12m
│   ├── investment-themes.csv                               ← ★ NUEVO: 492 temas con weight %
│   ├── activity-statement-2026-06-23-extracts.json
│   └── README.md
├── coverage/
│   ├── inception-2026-06-24.json                           ← ★ NUEVO: master JSON, 20 secciones
│   ├── snapshot-2026-06-24.json                            ← enriquecido con inception_2026_06_23
│   └── prices-2026-06-24.json
├── raw/
│   └── portfolio-2026-06-24.txt
├── holdings.csv                                            ← 22 posiciones, PERO con 3 errores pendientes
├── target.csv                                              ← OK
├── scripts/
│   ├── parse_inception.py                                  ← ★ NUEVO parser, re-ejecutable
│   ├── analyze.py, fetch_prices.py, monthly_buy.py, rebalance.py, score.py
├── prompts/
│   ├── analyze-portfolio.md
│   ├── rebalance.md
│   └── README.md
├── PROFILE.md, STRATEGY.md, RULES.md, TAX-ES.md
└── decisions.md                                            ← entrada 2026-06-25 añadida
```

## Cómo arrancar la nueva sesión

Decirle a Claude algo como: *"Lee HANDOFF.md y coverage/inception-2026-06-24.json. (1) Regenera holdings.csv desde inception.open_positions. (2) Decide qué CSV de dividends es la fuente única y consolida. (3) Actualiza prompts/analyze-portfolio.md Section A para usar inception_2026_06_23."*
