# Memoria de estrategia de inversión — versión auditable

**Fecha**: 2026-09-29 · **Estado**: post-ejecución tanda 1+1b (28-sep-2026)
**Propósito**: exponer la estrategia completa con suficiente detalle para ser auditada: cada cifra con su fuente, cada parámetro con su regla, cada supuesto con su sensibilidad y cada debilidad con su mitigación.
**Fuentes primarias**: `PROFILE.md`, `STRATEGY.md`, `RULES.md` (v1.1 con enmiendas 28-sep), `TAX-ES.md`, `BIBLIOGRAPHY.md`, `target.csv`, `holdings.csv`, `decisions.md`, `coverage/*-2026-09-28.json`, `coverage/scores-2026-09-22.json`.

---

## 0. Cómo auditar este documento

1. **Trazabilidad**: toda cifra lleva su origen entre paréntesis. Si una cifra no se puede reconstruir desde los archivos fuente, está mal etiquetada — repórtala.
2. **Jerarquía de fuentes** (en conflicto, gana la primera): Activity Statement IBKR > snapshot pegado por el usuario > `coverage/prices-*.json` > CSVs derivados de `data/`.
3. **Verificabilidad**: la §13 es un checklist de verificaciones abiertas con su archivo de destino. Una auditoría honesta termina ahí, no en lo que ya cuadra.
4. **Convención de divisa**: todo en EUR. Los 9 valores USA cotizan en USD nativo; conversiones al fx del día indicado en cada fuente. Limitación conocida: el coste EUR por lote real está pendiente de calcular desde `data/trades.csv` (§12).

---

## 1. Perfil del inversor y objetivos

| Campo | Valor | Fuente |
|---|---|---|
| País fiscal / moneda base | España / EUR | PROFILE.md |
| Edad | 44 años | Inception IBKR (investor profile) |
| Capacidad de ahorro | 3.000 €/mes (36.000 €/año) | PROFILE.md |
| Capital (28-sep-2026) | **112.366,72 € NLV** (cash 560,36 €) | snapshot IBKR 28-sep |
| Aportado lifetime | **96.700 €** (90.700 € hasta jun-2026 + 6.000 € sep-2026) | Inception + decisions.md 26/28-sep |
| Horizonte | 10–15 años (libertad financiera a ~56) | PROFILE.md |
| Tolerancia al riesgo | Moderada: estabilidad de dividendos > crecimiento puro | PROFILE.md |
| Broker | Interactive Brokers (U19253676), cuenta cash sin margen | snapshots |

### Objetivos cuantificados

| Objetivo | Métrica | Estado sep-2026 | Fuente |
|---|---|---|---|
| 1. Vacaciones con dividendos | ~2.300 €/año netos (meta 2026) | **NO se alcanzará**: proyección ~1.700–1.750 € (YTD 1.255 €) | PROFILE + dividends-inception.csv + cash |
| 1b. A 3–5 años | >4.000 €/año netos | Forward actual ~2.430–2.530 €/año | cálculo §6 |
| 2. Vivir de dividendos | 2.000–2.500 €/mes netos | Requiere 600–750 k€ *al 4 % neto* — ver §10 (supuesto en revisión) | PROFILE |

---

## 2. Filosofía: principios y anti-principios

### Principios operativos (STRATEGY.md)

1. **VWCE y VHYL son intocables** (base 67 % crudo / ~59 % normalizado). Venta parcial solo prevista a 8–10 años para convertir plusvalías en flujo.
2. **Cada euro nuevo va a acciones individuales de dividendo creciente.** Sin excepciones.
3. **No vender nunca para pagar gastos corrientes** — las vacaciones se pagan solo con dividendos.
4. **Reinvertir dividendos sobrantes** en las mismas acciones.
5. **Rebalanceo por compras, no por ventas** (constant-mix prohibido; ver Vías de salida §3.5).

### Anti-principios ("qué NO hacer", lecciones pagadas)

Inmuebles vacacionales · perseguir crecimiento extremo (QQQM/Nasdaq: sin dividendo, no UCITS) · vender VWCE/VHYL por impaciencia · obsesionarse con microposiciones (liquidadas 26-jun-2026, +321,61 €) · dudar del plan en caídas del 20 %.

### Anclas conductuales (literal de STRATEGY.md)

"No necesito 2,5 millones. Con 750.000 € y un 4 % de yield, soy libre." · "VWCE es mi jubilación en piloto automático." · "VHYL es mi fábrica de vacaciones con cero esfuerzo."

---

## 3. Marco normativo (RULES.md v1.1, enmiendas 28-sep-2026 marcadas ★)

### 3.1 Capa 1 — SAFETY: ¿sigo confiando en este dividendo?

**Filtros duros** (veto a compras nuevas):

| ID | Regla | Umbral | Origen doctrinal |
|---|---|---|---|
| S1 | Payout ratio | ≤75 % FCF (aviso >75 %, veto/reducir >90 %) | Damodaran |
| S2 | Crecimiento de dividendo | ≥5 años consecutivos; existentes que fallan → *revisar, no vender* | Lowell Miller |
| S3 | Crecimiento ≥8 % anual (5y) | Solo AVGO, JNJ, XOM | Lichtenfeld 10-11-12 |
| S4 | P/E | ≤25 mantener · ≤15 compra defensiva · >40 flag burbuja | Graham |

**Score compuesto 0–100** (estilo Simply Safe Dividends, implementado en `scripts/score.py`): payout 30 % (100 si ≤0,50 → 0 si ≥0,90) · debt/equity 25 % (100 si ≤1,0 → 0 si ≥3,0+) · historial 25 % (mín(100, años×10)) · P/E 20 % (100 si ≤15 → 0 si >40).

**Grados**: A (80–100) mantener y ampliar · B (60–79) mantener, ampliar solo si valoración acompaña · C (40–59) mantener sin ampliar · **D (<40) vender en 2 tramos**.

**Circuit breaker (Housel)**: caída de mercado >20 % → prohibido proponer ventas (salvo corte de dividendo confirmado); solo compras de oportunidad.

### 3.2 Capa 2 — VALUATION: ¿está barato ahora?

| ID | Señal | Parámetros |
|---|---|---|
| V1 | Kelley Wright (yield vs media 5y) | >media+1σ REINFORCED_BUY · dentro ±1σ FAIR · <media−1σ EXPENSIVE. σ proxy = 20 % de la media (limitación, §11) |
| V2 | DDM Gordon | fair = D1/(r−g); r=9 %; g=4 % (AVGO 6 %); compra si precio ≤0,95·fair |
| **V2-bis ★** | **Ámbito del DDM** | Gordon solo para Yield+Value estable (O, VZ, MO, T, ENG, KO, JNJ). AVGO y cíclicas (XOM) se valoran por V4/A5 (P/E ≤30×/≤15×). Razón: Gordon penaliza estructuralmente yield-bajo en crecimiento y lee ciclos del crudo como tendencia |
| V3 | Macro Ibbotson | VHYL >4,5 % = acelerar · VHYL <3,5 % = caro. **Sep-2026: 2,43 % → señal CARA** (moot: no hay dinero nuevo a ETFs) |
| V4 | Graham margin of safety | P/E ≤15 defensivas (JNJ, KO, VZ, MO, T, ENG, XOM) · ≤30 AVGO/GOOG |

### 3.3 Capa 3 — ALLOCATION: ¿cuánto y cuándo?

| ID | Regla | Parámetro |
|---|---|---|
| A1 | Bandas relativas Vanguard | ±25 % relativo vs target → **alerta de revisión manual** (no ejecución forzada) |
| A2 | Carlson BSD | Ranking por yield + años de pago + debt/equity (desempata orden de compra) |
| A3 | Miller DQDI | Compra nueva: yield ≥2,5 % (exentos AVGO/GOOG) · ≥5y crecientes · payout ≤75 % |
| A4 | O'Shaughnessy | Desempate por Quality: ROE 5y, beneficios 5y, beta <1,2 |
| A5 | Berkin & Swedroe | Grupos factor: Quality+Growth (AVGO, P/E ≤30, yield bajo OK) · Yield+Value (resto, P/E ≤15, yield ≥2,5 %) · Growth puro (GOOG: mantener, no ampliar) |
| A6 | Bogle core protection | Nunca sustituir VWCE/VHYL por acciones individuales |
| **A7 ★** | **Targets duales** | `target.csv.status`: activo/mantener/intocable/cuarentena. `/analyze` distingue **gap ejecutable** (solo activos) de **gap total** (destino). Los targets de cuarentena no se rebajan: son semáforo de reentrada |

### 3.4 Filtro de nuevas entradas (Morningstar 5-step)

Ticker nuevo necesita ≥3/5: moat · cobertura dividendo ≤75 % · balance (D/E ≤2,0 o IG) · sector no terminal · P/E ≤ sector o ≤ media propia 5y. *Razón práctica: la cartera ya tiene 10 líneas.*

### 3.5 Vías de salida ★

Solo se vende (parcial, 2 tramos) si: **(1)** grado D o payout >90 %; **(2)** corte/supresión de dividendo confirmado; **(3)** ruptura de tesis documentada en `decisions.md`; **(4)** horizonte 8–10 años (venta parcial programada de ETFs). Fuera de eso, el drift se corrige con dinero nuevo. Justificación fiscal: cada rotación con plusvalía adelanta 19–23 % de IRPF.

### 3.6 Precedencia en conflicto

Circuit breaker > filtros duros S1–S4 > STRATEGY.md > Capa 3 > Capa 2. *Safety decide el "si"; valoración decide el "cuándo/cuánto".*

---

## 4. Asignación objetivo (target.csv, pesos crudos — suman ~1,17; el sistema normaliza a 1)

| Activo | Peso crudo | Grupo factor | Status ★ | Nota |
|---|---:|---|---|---|
| VWCE | 36 % | Core crecimiento | intocable | Acumulativo, 0 € de flujo |
| VHYL | 31 % | Core flujo | intocable | Distribution yield 2,43 % (sep-26) |
| O | 7,5 % | Yield+Value (REIT) | **activo** | Pilar mensual |
| JNJ | 6,5 % | Yield+Value | cuarentena-pe≤15 | P/E 25×; yield 2,0 % también falla A3 |
| VZ | 6,5 % | Yield+Value | **activo** | Gap mayor del sleeve |
| MO | 5,5 % | Yield+Value | cuarentena-payout≤75 | Payout ~78 %; revisar 29-oct |
| XOM | 5,0 % | Cíclica | **activo** | DDM no aplica (V2-bis) |
| AVGO | 4,5 % | Quality+Growth | activo-pe<30 | 28,9× forward a 348 $ (28-sep) |
| ENG | 3,5 % | Yield+Value | cuarentena-cnmc | Suelo 1 €/acción solo hasta dic-2026 |
| T | 3,5 % | Yield+Value | cuarentena-subidas | Congelado desde 2022 |
| KO | 1,8 % | Yield+Value | mantener | P/E ~26×; sin reforzar |
| GOOG | 1,6 % | Growth puro | mantener | A5: no ampliar |
| IBTS | 3,5 % ★ | Bono corto | ok | Formalizado 28-sep (antes 0,5 %) |

---

## 5. Estado real a 28-sep-2026 (post-ejecución)

### 5.1 Posiciones (holdings.csv + snapshot 28-sep; fx 0,8803 de fills reales)

| Activo | Acciones | Coste medio | Peso | Target crudo | Banda ±25 % | Grado safety |
|---|---:|---:|---:|---:|---|---|
| VHYL | 494,0402 | 69,09 € | 35,48 % | 31 % | ✅ +14,4 % | — (ETF) |
| VWCE | 224,882 | 148,71 € | 34,00 % | 36 % | ✅ −5,6 % | — (ETF) |
| O | 138,7344 | 51,33 € (58,32 $) | 6,06 % | 7,5 % | ✅ **−19,2 % (verde 1.ª vez)** | A (91) |
| IBTS | 36,4759 | 121,64 € | 3,58 % | 3,5 % | ✅ +2,3 % | — (bono) |
| JNJ | 20,7198 | 163,90 € | 4,43 % | 6,5 % | 🔴 −31,8 % | A (92) |
| VZ | 111,7295 | 40,69 € (46,22 $) | 4,10 % | 6,5 % | 🔴 −36,9 % | A (84) |
| XOM | 22,8889 | 138,68 € (157,54 $) | 2,93 % | 5,0 % | 🔴 −41,4 % | A (99) |
| ENG | 156,2297 | 17,28 € | 2,33 % | 3,5 % | 🔴 −33,4 % | A (92) · WATCH |
| MO | 46,8771 | 50,60 € | 2,55 % | 5,5 % | 🔴 −53,6 % | B (63) · WATCH |
| KO | 22,4312 | 63,03 € | 1,54 % | 1,8 % | ✅ −14,4 % | B (71) |
| AVGO | 4,1055 | 343,67 € | 1,13 % | 4,5 % | 🔴 −75,0 % | A (81) · WATCH valoración |
| GOOG | 3,3082 | 224,62 € | 0,88 % | 1,6 % | 🔴 −45,0 % | B (69) |
| T | 24,8438 | 24,79 € | 0,49 % | 3,5 % | 🔴 −86,1 % | A (94) · congelado |
| Cash | | | 0,50 % | — | | 560,36 € |

Sleeves: **ETF 69,5 %** (target 67) · **Stocks 26,4 %** (era 21,6 % el 26-sep) · **Bond 3,6 %** · cash 0,5 %.

### 5.2 Ejecución reciente (decisions.md, 26–28 sep)

26-sep: ingreso 3.000 €. 28-sep: ingreso 3.000 € + compra **121 acciones** (O +38 @ 55,70 $ · VZ +75 @ 46,86 $ · XOM +8 @ 162,74 $) por **6.933,02 $ + 3 $ fees** (~6.106 €). Conversión IDEALPRO real: 5.523,75 € @ 1,136. Desviación vs plan: VZ 75 en vez de 86 (−11 sh).

**Pendiente del plan (gap ejecutable)**: VZ +32 (~1.315 €) · XOM +10 (~1.432 €) · AVGO +2 (~613 €) = **~3.360 €** vs cash 560,36 € → se cierra con el próximo ingreso.

### 5.3 Riesgo de mercado de referencia (Inception IBKR, jun-2026)

Sharpe 0,66 (VDHG 1,05) · Sortino 0,98 · MaxDD 9,15 % (feb–abr 2025, recuperación 7 meses) · beta 0,59 · YTD-26 +12,3 % vs VDHG +4,5 % · alpha 0,37 % · IR −3,72. Lectura: cartera defensiva que bate en retorno absoluto con peor riesgo ajustado.

---

## 6. Modelo de ingresos por dividendos

### 6.1 Método de cálculo

Forward anual neto = Σ(acciones × dividendo/accción anual declarado) × (1 − retención origen) convertido a EUR. Retenciones: 15 % USA (W-8BEN), 19 % ENG, 0 % ETFs irlandeses. *No incluye IRPF español posterior (§7).*

### 6.2 Cifras

| Concepto | Valor | Fuente/método |
|---|---:|---|
| YTD 2026 neto cobrado | ~1.255 € | 611,20 € (dividends-inception.csv, 23-jun, fx 0,879) + 644,33 € (Δcash 26-jun→22-sep sin trades) |
| Proyección cierre 2026 | ~1.700–1.750 € | Q4: O×3 meses, VHYL dic, KO, MO, VZ, T, JNJ, XOM |
| **Forward 12m (cartera 28-sep)** | **~2.430–2.530 € netos** | 494×~1,97 € VHYL + 138,73×3,26 $ O + 111,73×2,83 $ VZ + 156,23×1 € ENG + resto |
| Incremental tanda 28-sep | +~280 €/año | 38 O + 75 VZ + 8 XOM |
| Con gap ejecutable cerrado | ~2.650–2.750 € | +32 VZ, +10 XOM, +2 AVGO |

### 6.3 Dividendos con fecha en el calendario

| Pago | Fecha | Importe esperado neto | Condición |
|---|---|---:|---|
| O | 15-oct-2026 | ~28 € | Ex-div 30-sep **capturado** (compra 28-sep, 138,7344 sh) |
| MO | 10-oct-2026 | ~36 € | Ex-div 15-sep ya pasado con posición |
| VZ | 2-nov-2026 | ~59 € | Record 9-oct con 111,7295 sh |
| XOM | ~10-dic-2026 | ~18 € | Ex-div ~14-nov con 22,8889 sh |

---

## 7. Fiscalidad (España)

| Concepto | Tratamiento | Estado 2026 |
|---|---|---|
| Dividendos USA | 15 % retención origen (W-8BEN) deducible Anexo A; tributan 19–21 % base ahorro | Brutos ~1.450–1.500 €, retención ~200–250 € (estimación a confirmar con AS Q4) |
| Dividendos ENG | 19 % retención, deducible | ~156 €/año bruto |
| VHYL (irlandés) | Sin doble imposición adicional | — |
| VWCE | Acumulativo: 0 € hasta venta | — |
| Plusvalías | 19 % ≤6.000 € · 21 % ≤50.000 € · 23 % >50.000 € | Realizadas 2026: ~893 € L/T (571 € 10 tickers + 322 € micros) + S/T pendiente → IRPF ~210–240 € |
| Ventas de ETF | Traspaso sin tributar NO permitido | Razón estructural del rebalanceo por compras |
| **Verificación pendiente** | **W-8BEN activo en IBKR** | Imprescindible para 15 % y no 30 % — confirmar vigencia |

---

## 8. Protocolo de ejecución operativa

### 8.1 Rutina mensual (3.000 €; adaptada a cuarentenas ★)

| Tramo | Regla original | Adaptación vigente |
|---|---|---|
| 1 — 1.000 € | O fijo | Sin cambios |
| 2 — 1.000 € | Más barata de {VZ, JNJ, MO, XOM, AVGO, ENG, T} | Más barata de **{VZ, XOM, AVGO<30×}** (activos) |
| 3 — 1.000 € | 2ª más barata o AVGO | 2ª activa; si no hay, retener |

Regla de flexibilidad: caída >5 % de un activo activo sin motivo grave → concentrar 2.000–3.000 € en él.

### 8.2 Mecánica de órdenes (aprendida 26–28 sep)

Ventana 15:30–17:30 CET (apertura NYSE solapada) · Limit ≤ techo de referencia o Market en valores líquidos · TIF Day · sin AON · **sin stop-loss** (coherente con Vías de salida) · verificar conversión EUR→USD (auto-FX activada o conversión manual IDEALPRO) · depósito disponible al instante (el rechazo de junio fue por *settled cash* de ventas, T+2, no aplica a ingresos).

### 8.3 Logging

Toda decisión → `decisions.md` (plantilla qué/por qué/importe/resultado esperado/revisión). Toda sesión de datos → `coverage/` con fecha. Los campos "Revisión" son deuda hasta rellenarse (§12).

---

## 9. Sistema de datos y trazabilidad

### 9.1 Cadena de datos

IBKR (paste/Activity Statement/Inception) → `coverage/snapshot-*.json` + `data/*.csv` → `scripts/analyze.py` (+`prices-*.json`) → `coverage/analysis-*.json` → validación manual vs `RULES.md` (`scripts/score.py` → `scores-*.json`).

### 9.2 Historial de correcciones (pista de auditoría)

| Fecha | Error detectado | Corrección |
|---|---|---|
| 25-jun | dividends_ytd mezclaba accruals (460 € → 1.525 €) | Pagado real: 611 € YTD / 2.620 € lifetime (Inception) |
| 25-jun | "realized 9.099 €" era proceeds mal leídos | Real lifetime: 1.022,09 € (Inception by-symbol) |
| 26-jun | avg_cost_eur de 9 tickers USD eran nativos USD | Re-expresados (convención documentada; lote real pendiente) |
| 26-sep | **Gap −2.599 € "inexplicado"** | Columnas USA del paste IBKR estaban en USD nativo; fx implícito lo cuadra al céntimo. El −2.499 € de junio: misma causa |
| 28-sep | Campo "Dividends" del overview (353 €) | Son **accruals incluidos en el NLV**, no un periodo |
| 28-sep | score.py crasheaba con filas `#` de target.csv | Fix aplicado y verificado |
| 28-sep | Etiquetas de fecha 22-sep (era 26/28-sep) y "lunes 29" (era 28) | Corregidas en archivos vigentes |

---

## 10. Supuestos críticos y sensibilidades (núcleo de la auditoría)

### 10.1 El supuesto del 4 % de yield — el punto más débil del plan

PROFILE.md asume **750.000 € × 4 % neto = 2.500 €/mes**. La cartera objetivo a precios de sep-2026 rinde **~2,2 % neto blended** (VWCE 0 % + VHYL 2,43 % pesan 59 % normalizado). Sensibilidad:

| Yield neto blended | Capital para 2.000 €/mes | Comentario |
|---:|---:|---|
| 2,2 % (hoy) | ~1.090.000 € | +45 % de capital vs plan |
| 3,0 % | ~800.000 € | VHYL normalizando a ~3,3–3,5 % |
| 4,0 % (plan) | ~600.000 € | Requiere: crecimiento del dividendo 4–8 %/año durante ~8 años (yield-on-cost), comprar correcciones (regla flexibilidad), y/o sleeve maduro >45 % |

**Veredicto honesto**: el 4 % es alcanzable como *yield sobre coste a 8–10 años*, no como yield de mercado de hoy. El plan de capital (600–750 k€) es correcto *si* el horizonte incluye ese período de maduración; si no, el objetivo real de capital está entre 800 k€ y 1,1 M€.

### 10.2 Retorno total 7 % anual

Asunción de PROFILE para la proyección (100 k + 3 k/mes → ~694 k€ a 10 años). Sensibilidad: al 5 % → ~555 k€; al 9 % → ~860 k€. No se ha recalibrado con datos propios (TWR YTD-26 +12,3 %, favorable).

### 10.3 Sensibilidad a tipos de interés

10Y americano al 5,16 % (sep-2026) con subida adicional descontada para octubre. Los componentes de mayor yield (O REIT ~5,7 %, VZ ~5,9 %, ENG ~5,9 %) son sensibles a tipos: la semana del 21-sep utilities cayeron −3,2 %. **Implicación**: presión continuada de tipos = headwind de precio pero = oportunidad de compra de yield (asimetría favorable para acumulación, desfavorable para NLV de corto plazo).

### 10.4 Divisa

Exposición USD: ~24 % directa (9 valores) + ~60 % de VWCE + ~35 % de VHYL ≈ **55–57 % efectiva**. El gasto (objetivo) es en EUR → el flujo de dividendos de la mitad de la cartera fluctúa con EURUSD. Sin cobertura. Rango relevante 2026: 1,12–1,14.

### 10.5 Concentración

Actual: baja (69,5 % ETFs globales; mayor posición individual 6,1 %). A target completo: máximo sectorial teleco 10 % (VZ+T), energía 8,5 % (XOM+ENG), tabaco 5,5 % (MO). Máximo nombre individual 7,5 % (O). **Riesgo específico mayor**: MO (negocio en contracción estructural −3,2 % volúmenes, NJOY impairment) — mitigado por cuarentena y cap 5,5 %.

---

## 11. Riesgos del modelo y de las reglas

| Riesgo | Descripción | Mitigación en el sistema |
|---|---|---|
| Datos de terceros | score.py depende de Yahoo (rate-limits repetidos en sep-26) | Fallback manual-web documentado (scores-2026-09-22 method: MANUAL-WEB); pendiente caché last-known-good |
| Kelley Wright con σ proxy 20 % | Señal aproximada | V2-bis reduce su peso; DDM/Graham mandan |
| Score no detecta dividendos congelados | `dividend_years` cuenta años con pago, no subidas | Detectado en T; A7 status cuarentena-subidas lo cubre manualmente; mejora del script en §12 |
| Payout desconocido puntúa 50 | Optimista en falta de datos | Conocido; verificar con fuentes al comprar |
| Doble escala de pesos (crudo 1,17 vs normalizado) | Confusión en bandas | Corregida la doc de STRATEGY; `analyze.py` normaliza siempre |
| Comportamental | 3 meses de pausa (jul–sep 2026) costaron ~525–630 €/año de flujo no creado | Lección registrada; propuesta de recordatorio mensual (§12) |
| Ejecución | Rechazos por settled cash (jun) | Protocolo §8.2 |

---

## 12. Limitaciones conocidas y deudas técnicas

1. **Coste EUR por lote real** desde `data/trades.csv` (los avg_cost_eur usan fx del día — insuficiente para fiscalidad de ventas).
2. **`scripts/tax_2026.py`** no existe: el borrador IRPF 2026 es manual (§7).
3. **Fuentes de dividendos triplicadas** (dividends.csv, dividends-inception.csv, activity extracts) — consolidación recomendada.
4. **4 entradas de decisions.md con "Revisión" sin rellenar** + las de septiembre.
5. **Residual NLV ~0,1–0,4 %** entre display y marks — cerrar con Activity Statement Q4.
6. **Recordatorio mensual** (1.º de mes: pegar snapshot + `/monthly-buy`) — propuesto, sin implementar.
7. **Activity Statement Q3/Q4 pendiente** de descarga para cerrar: fees reales, conversiones, realized YTD, dividends brutos/retenciones.
8. Métricas de riesgo (Sharpe etc.) congeladas en jun-2026 (Inception) — refrescar con el próximo reporte.

## 13. Checklist de auditoría (verificaciones abiertas)

| # | Verificación | Cuándo | Archivo destino |
|---|---|---|---|
| 1 | Pago O 15-oct sobre 138,7344 sh (~28 € netos) | 15-oct | decisions.md (Revisión) |
| 2 | Pago MO 10-oct (~36 €) | 10-oct | idem |
| 3 | Pago VZ 2-nov sobre 111,7295 sh (~59 €) | 2-nov | idem |
| 4 | MO Q3: ¿payout ≤75 %? (guía actual lo impide) | 29-oct | scores-*.json + status target.csv |
| 5 | Tanda final VZ +32 / XOM +10 / AVGO +2 (~3.360 €) | próximo ingreso | holdings + decisions |
| 6 | W-8BEN vigente en IBKR | ya | checklist fiscal |
| 7 | Activity Statement Q3/Q4: fees, FX, realized, dividends | Q4 | data/ + snapshot |
| 8 | Coste EUR por lote (trades.csv) | Q4 | holdings.csv v2 |
| 9 | `tax_2026.py` borrador IRPF | Q4 | scripts/ |
| 10 | Consolidar fuentes de dividendos | Q4 | data/README.md |
| 11 | Revisar bandas con gap dual tras tanda final | nov | analysis-*.json |
| 12 | Auditoría de rendimiento: ¿batiendo VDHG? | dic (nuevo Inception) | coverage/ |

## 14. Mapa doctrinal (BIBLIOGRAPHY.md → reglas)

20 fuentes (10 libros + 10 artículos). Cadena crítica: **Miller** (DQDI: el filtro de selección) → **Simply Safe Dividends** (el score) → **Graham** (la disciplina de precio) → **Carlson** (el orden) → **Vanguard** (las bandas) → **Bogle** (la base intocable) → **Housel** (el circuit breaker) → **Damodaran** (el payout) → **Lichtenfeld** (el crecimiento) → **Berkin&Swedroe** (los grupos factor). 3 fuentes descartadas con razón documentada (Research Affiliates, MSCI, Bogleheads tax placement).

---

*No es asesoramiento financiero. Documento descriptivo del sistema propio del inversor; decisión final siempre suya. Errores u omisiones: contrastar contra los archivos fuente citados.*
