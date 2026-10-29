---
task_category: Análisis financiero / diagnóstico de cartera
role: Analista de cartera personal (dividendos, España, horizonte 10-15 años)
tone: Objetivo, conciso, numérico
output_format: Markdown estructurado con tablas + checkboxes de validación
target_audience: El propio inversor (decisor final)
detail_level: Comprehensive
thinking_effort: Max
task_horizon: Long-horizon (agentic)
output_language: Español
constraints:
  - No dar asesoramiento financiero genérico; aplicar solo STRATEGY.md + RULES.md + TAX-ES.md
  - Todos los importes en EUR
  - Fuentes de datos: `coverage/` (snapshots+precios+puntuarios) Y `data/` (transaction history: dividends.csv, trades.csv, activity-statement-*-extracts.json). No llamar a Yahoo Finance, no ejecutar scripts en caliente.
  - Citar cada cifra con su archivo + campo. Si conflicto entre sources, prioridad: Activity Statement extracts > snapshot IBKR > prices.json > CSV derivado.
  - Si un dato no existe en coverage/ ni data/, escribir "sin dato" — NO inventar, NO estimar.
  - Never invent fundamentals, prices, grades, or signals.
---

# Plantilla — Analizar cartera actual vs target

> Caso de uso: **diagnóstico periódico** de la cartera. Responde "¿cómo estoy hoy vs mi objetivo?" sin proponer compras (para compras usa `rebalance.md`).

## 0) Setup — sin red, sin scripts

No se ejecutan `fetch_prices.py`, `analyze.py`, ni `score.py`. Toda la información vive en `coverage/` (snapshots+precios+puntuarios estáticos) y `data/` (transaction history parseada + Activity Statement extracts), ambos generados por el usuario desde exportes IBKR.

```bash
ls ~/Projects/portfolio/coverage/
# prices-YYYY-MM-DD.json                       — FX + precios nativos y EUR por ticker
# snapshot-YYYY-MM-DD.json                     — NLV, cash, P&L, holdings, dividends_ytd, news_signals, ibkr_alerts, macro
# scores-YYYY-MM-DD.json                       — (opcional) safety + valuation por ticker

ls ~/Projects/portfolio/data/
# transactions.csv                              — raw IBKR Transaction History (input, NO editar)
# dividends.csv                                 — per-payment: date, ticker, gross_eur, withholding_eur, net_eur
# trades.csv                                    — per-trade: qty, price_native, gross_eur, commission_eur, net_eur
# activity-statement-YYYY-MM-DD-extracts.json   — authoritative YTD totals, cost basis, sold tickers, ISIN map, lot_dates
# README.md                                     — reconciliation status entre CSV y Activity Statement (LEER PRIMERO)
```

**Regla de frescura**: usa el archivo `*-YYYY-MM-DD.json` con la fecha más reciente disponible en `coverage/`. Si la fecha del snapshot no es la de hoy, anota la discrepancia al principio del informe ("Snapshot del YYYY-MM-DD; análisis hecho el YYYY-MM-DD").

**Regla de reconciliación**: antes de citar cualquier cifra YTD, comprueba `data/README.md` para ver si el CSV y el Activity Statement reconcilian. Si hay gap (como ocurre con dividends), cita el número del Activity Statement (authoritative para IRPF) y documenta la diferencia.

Si falta algún archivo (ej: no hay `scores-*.json`), la sección afectada se rellena con "sin dato — sin archivo en coverage/".

## 1) Contexto que el modelo debe tener acceso

Lee (o pega en el chat) en este orden — todos viven en `~/Projects/portfolio/`:

```
1. PROFILE.md                                perfil inversor (España, EUR, ahorro 3k/mes, objetivo 750k)
2. STRATEGY.md                               reglas alto nivel — FUENTE DE LA VERDAD
3. RULES.md                                  framework 3 capas: safety / valuation / allocation
4. TAX-ES.md                                 fiscalidad España (plusvalías, W-8BEN, doble imposición)
5. holdings.csv                              cartera real (incluye fila CASH; microposiciones al final)
6. target.csv                                asignación objetivo (pesos crudos suman ~1.14 → normalizar a 1.0). Columna `status` (enmienda 2026-09-28, RULES.md A7): activo/mantener/intocable/cuarentena. El informe debe mostrar DOS gaps: **gap ejecutable** (solo filas `activo` — a dónde puede ir dinero nuevo hoy) y **gap total** (todas las filas — el destino). Las bandas rojas de filas `cuarentena` son semáforo de reentrada, no errores; citar su condición de desbloqueo (pe<15 / payout<=75 / subidas / cnmc).
7. decisions.md                              últimas 5 entradas — memoria de decisiones
8. coverage/prices-YYYY-MM-DD.json           FX + precios en EUR — evita alucinar precios
9. coverage/snapshot-YYYY-MM-DD.json         snapshot IBKR: NLV, cash, holdings, P&L, dividends_ytd, news_signals
10. coverage/scores-YYYY-MM-DD.json          (opcional) safety + valuation por ticker
11. data/README.md                           reconciliation status CSV vs Activity Statement — LEER PRIMERO
12. data/activity-statement-YYYY-MM-DD-extracts.json   authoritative: YTD totals, cost_basis, sold_tickers, lot_dates, ISIN map
13. data/dividends.csv                       per-payment: cada dividendo con su fecha/ticker/withholding
14. data/trades.csv                          per-trade: cada Buy/Sell con precio nativo + EUR + comisión
```

**Prioridad de sources en conflicto**:
- **Activity Statement extracts (12)** es la fuente autoritativa para YTD fiscal (dividends, withholding, realized gains) y para cost_basis nativo por ticker. Su número va primero.
- **Snapshot IBKR (9)** es la única fuente para: NLV real, unrealized P&L, market_value_eur por holding, news/alerts/macro intradía. Cárgalo siempre.
- **prices (8)** es la única fuente para FX EUR/USD y precios nativos por ticker.
- **dividends.csv (13) y trades.csv (14)** son trazabilidad (per-payment / per-trade), NO totalizadores. Úsalos para detalle o desglose por ticker, nunca para cifras de cabecera.

## 2) Placeholders

- `{{fecha_análisis}}` — `YYYY-MM-DD` (fecha en la que se ejecuta el análisis).
- `{{fecha_snapshot}}` — `YYYY-MM-DD` del archivo más reciente en `coverage/`.
- `{{año_snapshot}}` — `YYYY` (año de `fecha_snapshot`, usado para filtrar dividends.csv).
- `{{fecha_activity_statement}}` — `YYYY-MM-DD` del extracts más reciente en `data/`.

## 3) Instrucción (pega esto DESPUÉS del contexto)

```
Fecha del análisis: {{fecha_análisis}}
Fecha del snapshot usado: {{fecha_snapshot}}

Actúas como mi analista de cartera personal. Aplica literalmente STRATEGY.md,
RULES.md y TAX-ES.md (en el contexto). No reinterpretas las reglas.

TAREA

Calcula, para cada holding, desde coverage/snapshot-YYYY-MM-DD.json:
  valor_eur      = quantity × market_value_eur / quantity   (= market_value_eur directamente)
  denominador    = SUM(market_value_eur de todos los holdings) + snapshot["cash_breakdown"]["total_eur"]
                   [USA ESTE denominador interno, NO el net_liquidation_value reportado.
                    Razón: snapshot["nlv_reconciliation_note"] documenta que NLV IBKR
                    difiere ~0.3% de la suma de holdings por intraday vs close + FX marks.
                    Usar el denominador interno hace que los pesos sumen exactamente 100%.]
  peso_actual    = valor_eur / denominador
  peso_target    = target_weight_raw / suma(target_weight_raw)   [suma cruda = 1.14]
  desviacion_pp  = (peso_actual - peso_target) × 100
  pnl_eur        = snapshot["holdings"][i]["unrealized_pnl_eur"]
  pnl_pct        = pnl_eur / (valor_eur - pnl_eur) × 100
  div_ytd_eur    = SUM(gross_eur en data/dividends.csv donde ticker = T y date[0:4] = año_snapshot)
                   [SOLO para desglose. El TOTAL YTD autoritativo viene del snapshot
                    (que a su vez lo importa del Activity Statement); el CSV sub-contabiliza.]

Produce un informe markdown con seis secciones (A-F):

A) Resumen ejecutivo (8 bullets máx.)
   - Valor total en EUR = snapshot["summary_eur"]["net_liquidation_value"].
   - Peso por sleeve (ETF / Stock / Bond / Other / Cash) calculado sumando pesos de holdings.
   - Mayor desviación absoluta vs target normalizado (ticker + pp).
   - P&L no realizado total en EUR = snapshot["summary_eur"]["unrealized_pnl"];
     % sobre coste medio = unrealized_pnl / (NLV − unrealized_pnl) × 100.
   - **Dividendos YTD en EUR = snapshot["summary_eur"]["dividends_ytd"] (1,524.59)**.
     Indicar €/mes promedio (€2,541/mes proyectado si mantienen ~9 pagadores/mes).
     Aclarar que es el total del Activity Statement (no del transaction CSV, que sub-contabiliza).
   - **Withholding tax YTD = snapshot["summary_eur"]["withholding_tax_ytd"] (103.23)**.
     Deducible en Anexo A (doble imposición). Acciones USA: 15% retenido (W-8BEN vigente).
   - **Realizado YTD = snapshot["summary_eur"]["realized_lt_ytd"] (9,099.57 L/T profit)** +
     realized_st_ytd (1,464.67 net). Tributa IRPF 2026 base ahorro:
     19% hasta €6k, 21% hasta €50k, 23% sobre el resto. L/T loss €490 compensable.
   - TWR YTD si existe en snapshot["portfolio_performance"]["twr_ytd_pct"] (6.74%);
     también citar deposits_ytd (€32,000) para contexto de crecimiento orgánico vs aportaciones.

B) Tabla por activo (ordenada por peso actual desc):
   | Ticker | Nombre | Qty | Precio EUR hoy | Valor EUR | Peso actual % | Target % | Desviación pp | P&L € | P&L % | Div YTD € |
   - Precio EUR hoy = snapshot["holdings"][i]["market_value_eur"] / quantity
     (cruza con coverage/prices-YYYY-MM-DD.json[ticker]["price_eur"] para sanity-check).
   - Div YTD € = suma de gross_eur en data/dividends.csv filtrado por ticker y año_snapshot.
     Para tickers sin pago en el año: "—". Para VWCE (acumulativo): "— (accumulating)".
   - Tickers en sleeve "Other" (no están en target.csv): Target % = 0; nota "Other".
   - Fila CASH: Precio EUR = 1.00 (convención), Div YTD € = broker_interest_ytd del snapshot.
   - Al pie de la tabla:
     "FX EUR/USD intraday snapshot = coverage/prices[date]['fx_eur_usd']; FX cierre Activity Statement = 0.87861."
     "Denominador pesos = SUM(market_value_eur) + cash = X € (NO NLV reportado, ver nlv_reconciliation_note)."

C) Tabla por sleeve:
   | Sleeve | Valor EUR | Peso actual % | Target % | Desviación pp |
   - Target por sleeve = suma de target_weight_raw de los tickers del sleeve / 1.14.

D) Capa 1 SAFETY + Capa 2 VALUATION — solo tickers del sleeve Stock
   (excluye ETFs, Bonds, Cash, Other/microposiciones).
   Fuente preferente: coverage/scores-YYYY-MM-DD.json[ticker]. Si no existe el archivo
   o el ticker no está, fila con "sin dato — sin scores en coverage/".
   | Ticker | Safety total | Grade | Payout ratio | Trailing P/E | Debt/Eq | Dividend years | KW signal | DDM signal | Graham check |

   Leyendas (de RULES.md, incluidas aquí para que no dependas de re-leerlo):
   - Grade:        A ≥ 80 · B 60-79 · C 40-59 · D < 40.
   - KW signal:    REINFORCED_BUY (verde) · FAIR · EXPENSIVE (rojo) · NO_DATA.
   - DDM signal:   UNDERVALUED (verde) · FAIR · OVERVALUED (rojo) · NO_PRICE · NO_DIVIDEND.
   - Graham check: PASS (P/E ≤ 15) · OK_KEEP (15-25) · FAIL (> 25 ó > 40 burbuja).
   - Filtros duros Capa 1: payout ≤ 0.75 (S1) · div growth ≥ 5y (S2) · P/E ≤ 25 (S4).

   Marcado visual en la tabla:
   - Rojo: Grade C/D · KW=EXPENSIVE · DDM=OVERVALUED · Graham=FAIL · Payout > 0.75 · P/E > 25.
   - Verde: Grade A · KW=REINFORCED_BUY · DDM=UNDERVALUED.

E) Alertas (ordena por severidad; si ninguna aplica, escribe "Sin alertas"):
   - CRÍTICO — Safety grade D en cualquier ticker → plan de venta (reducir 50% en 2 tramos).
   - CRÍTICO — Circuit breaker macro (Housel): SPX > 20% bajo máximo 52 semanal.
              Calcular con snapshot["market_data"]["SPX"]["level"] y el 52w high (si existen).
              Si no hay dato de SPX ni 52w high, escribir
              "sin dato — preguntar al usuario por SPX vs 52w high" (NO asumir ni inventar).
   - ALTO — Grade C, KW=EXPENSIVE, DDM=OVERVALUED o Graham=FAIL en cualquier Stock.
   - ALTO — Banda Vanguard 25% relativo rota (regla A1): para VWCE (target ~36%)
            y VHYL (target ~31%), fuera de banda si peso actual relativo difiere > 25%.
   - ALTO — Cash < 1% del portfolio (dry powder agotado). Target cash = 1.1%.
   - ALTO — Cualquier item de snapshot["ibkr_for_you_alerts"] con severity="high"
            (ej: gran cambio de precio, volumen anómalo, 52w high/low). Citar el texto.
   - MEDIO — News signals de snapshot["news_signals_*"] que afecten a holdings
            con señal Bearish o Mixed. Para Bullish, mencionar como oportunidad táctica.
   - MEDIO — Desviación absoluta > 2 pp en cualquier ticker.
   - MEDIO — Payout > 0.75 rompe S1; P/E > 25 rompe S4.
   - BAJO — Microposiciones vivas en sleeve "Other": RTX, PNC, TXN, AMGN, NOC, LMT,
            MVUS, IHYG, FGQI. Proponer limpieza vía /deploy-cash, NO aquí.
   - BAJO — Caída > 5% último mes en algún holding. Si el snapshot no incluye histórico,
            marcar "sin dato — decisions.md no registra".
   - INFO — Contexto macro de snapshot["market_overview_macro"]["headline"] (1 línea).
   - INFO — W-8BEN vigente (asumido) para acciones USA: retención 15% en dividendos.
   - INFO — Realizado L/T YTD vs tramos IRPF base ahorro (19% ≤€6k, 21% ≤€50k, 23% >€50k).
            Si realized_lt_ytd + nuevo realizado planeado cruza tramo, mencionar oportunidad
            de esperar a enero 2027 para diferir. Citado desde snapshot["summary_eur"]["realized_lt_ytd"].
   - INFO — Tickers vendidos YTD (snapshot["sold_tickers_ytd_2026"]): listar 1 línea con mayor
            |ytd_lt_realized_eur| (top 3) — contexto para no recomprarlos en vano.

F) Próximo paso sugerido (una sola línea, justificado en 1 frase):
   - "/monthly-buy 3000" si cash > 1.000 € Y sleeve Stock bajo target.
   - "/deploy-cash N"    si cash > 3% del portfolio O hay microposiciones pendientes.
   - "Mantener"          si desviaciones < 2 pp en todo Y no hay alerts CRÍTICOS ni ALTOS.

REGLAS

- Diagnóstico únicamente. Cero propuestas de compra/venta concretas (usar rebalance.md).
- No invoques fetch_prices.py, analyze.py, ni score.py. No consultas Yahoo Finance.
- Si coverage/scores-*.json no existe o falta un ticker, fila D con "sin dato" y continúa.
- Todas las cantidades en EUR. FX para acciones USD tomado de
  coverage/prices-*.json["fx_eur_usd"]; indica el tipo usado al pie de la tabla B.
- Cada cifra en B/C/D debe poder reconstruirse desde coverage/ + data/ + holdings.csv + target.csv.
- **Fiscal (TAX-ES.md)**: cifras YTD autoritativas (dividends, withholding, realized) provienen
  del Activity Statement via snapshot. dividends.csv es solo trazabilidad per-payment.
- **Cross-validation**: si una cifra en snapshot difiere >1% de la suma equivalente en data/,
  documentar la discrepancia explícitamente (ver data/README.md reconciliation status).

CRITERIOS DE ACEPTACIÓN (verifica antes de entregar)

[ ] Suma "Valor EUR" en B + cash = denominador interno usado para pesos (NO se exige igualar NLV).
    Reportar diferencia vs snapshot["summary_eur"]["net_liquidation_value"] (esperada ~0.3%).
[ ] Suma "Peso actual %" en B = 100 % (±0,5 pp) usando denominador interno.
[ ] Suma "Target %" en B = 100 % (±0,5 pp) tras normalización (dividir por 1.14).
[ ] Dividendos YTD, withholding, realizado L/T y unrealized_pnl citados en A provienen literalmente del snapshot.
[ ] Div YTD € por ticker en B proviene de data/dividends.csv filtrado por año_snapshot.
[ ] Suma "Div YTD €" en B se acerca a (pero es menor que) snapshot dividends_ytd — documentar gap.
[ ] Toda alerta en E cita (ticker + valor + archivo fuente en coverage/ o data/).
[ ] News signals e IBKR alerts en E referencian el snapshot literalmente.
[ ] Tabla D solo incluye sleeve Stock (excluye ETF, Bond, Cash, Other).
[ ] Grades y signals en D son literales de coverage/scores-*.json — no invención.
    Si no hay archivo, todas las celdas D = "sin dato — sin scores en coverage/".
[ ] Ninguna recomendación de compra/venta concreta en el informe.
[ ] FX EUR/USD intraday (snapshot) y cierre Activity Statement (0.87861) se citan ambos al pie de B.

Si algún check falla, corrige antes de entregar.
```

## 4) Notas GLM 5.2

- **Thinking effort = Max**: el cruce holdings × precios × target × 3 capas de RULES.md × fiscalidad TAX-ES.md × trazabilidad transacciones se beneficia mucho del modo profundo.
- **Task horizon = Long-horizon (agentic)**: lectura secuencial de los 14 archivos, validación cruzada coverage↔data, y refinamiento iterativo de alertas. GLM 5.2 está diseñado para esto.
- **Ventana 1M**: pega TODO el bundle (7 archivos base + 2-3 JSON de coverage + 4 archivos de data/). Si trabajas con un modelo de ventana menor, recorta primero `decisions.md` y `data/trades.csv` (este último es el más grande y menos crítico para diagnóstico).
- **Sin dependencia de red**: todo el cómputo se hace desde `coverage/` + `data/`. Esto elimina el problema de rate-limit de Yahoo Finance y hace el análisis reproducible.
- **Cross-validation coverage vs data**: el snapshot se enriquece con cifras del Activity Statement via extracts JSON. Siempre que cites un YTD total, comprueba que el per-ticker sumatorio en dividends.csv/trades.csv se acerca — si no, documenta el gap (no es error, son accruals).
- **En Claude Code**: los slash commands `/analyze` y `/rebalance` pueden leer directamente de `coverage/` y `data/`; esta plantilla es para **uso fuera de Claude Code o segunda opinión con otro modelo** (GLM 5.2, Gemini, etc.).
