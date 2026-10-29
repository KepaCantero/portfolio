# Rebalanceo total conforme a RULES.md — 22-sep-2026 (v2, datos corregidos)

> ## 📌 ADDENDA de ejecución — 26-sep-2026 (vIGENTE)
> Ingreso de 3.000 € hecho (cash total **3.664,24 €**, buying power íntegro). La tanda 1 se re-escala al cash disponible (la tabla original de §1 asumía ~6.5 k€ en octubre). **Tanda 1 — colocada lunes 28-sep** (corregido: la versión previa decía "29-sep" por error de etiqueta; Limit original → modificadas a Market/Day 07:35 ET, PreSubmitted hasta la apertura NYSE 15:30 CET; captura ex-div O 30-sep y record VZ 9-oct):
>
> | Orden | Acciones | Precio ref. | Importe |
> |---|---:|---:|---:|
> | **O** | +20 | 55,70 $ / 49,49 € | ~990 € |
> | **VZ** | +49 | 47,13 $ / 41,87 € | ~2.052 € |
> | **XOM** | +4 | 160,60 $ / 142,68 € | ~571 € |
> | **TOTAL** | 73 | | **~3.618 €** (comisiones ~6 €; buffer 46 €) |
>
> **Tanda 2** (cuando entre el próximo ingreso; ~5.317 €): VZ +58, O +18, XOM +14.
> **Novedad**: AVGO a 353,70 $ = **29,3× forward < 30× → ha entrado en su zona de compra** (A5/V4 cumplen; DDM flag sigue siendo limitación del modelo). Opcional en tanda 2: AVGO +1-2 acciones (~314 €/ud) además de completar VZ/O/XOM.
> Resultado tanda 1: O 5,3 % · VZ 3,2 % · XOM 2,4 % · ETFs 68,9 % — camino correcto, se completa con la tanda 2.
> *Nota de fechas: los archivos `*-2026-09-22` de esta sesión correspondían en realidad a finales de sep (error de etiqueta); esta addenda y los `coverage/*-2026-09-26.json` son los vigentes.*

> Ejecución del mandato: "rebalanceo total para que todo cumpla las normas, con las reglas como están".
> **Corrección misma tarde**: el análisis previo interpretaba las columnas USA del snapshot IBKR como EUR cuando estaban en USD nativo. Con fx implícito 0,89117 (EURUSD 1,1221) el patrimonio cuadra al céntimo con el NLV (106.788,91 €). Los pesos y gaps de abajo son los definitivos. Este documento sustituye a los importes de §2 de `ANALYSIS-2026-09-22.md` y `RECOMENDACION-2026-09-22.md`.

## 0. ¿Están bien tus normas? — respuesta directa

**Sí, el framework es sólido y no hay que cambiarlo**: capas con precedencia clara (safety decide el "si", valoración el "cuándo/cuánto"), circuit breaker anti-pánico, protección del núcleo ETF, sensibilidad fiscal española. Es una codificación seria de Damodaran/Graham/Miller/Carlson.

Dos matices que debes tener presentes (no son errores de filosofía, son fricciones documentadas):

1. **Tus reglas y tu target se contradicen**: con las reglas intactas, 4 posiciones (T, ENG, MO, JNJ) + AVGO no pueden recibir dinero nuevo hoy. Consecuencia: el sleeve de acciones converge a **~28,5 %**, no al 33 % del resumen de STRATEGY.md, hasta que los datos cambien (subidas de dividendo, payout, P/E o CNMC). Es una decisión consciente, no un fallo — pero apúntala.
2. **"Rebalanceo total" con ventas no existe en tu sistema — por diseño.** A6 prohíbe sustituir VWCE/VHYL por acciones; TAX-ES manda priorizar compras de rezagadas sobre ventas de pasadas; ninguna posición está en grado D (vender). El único rebalanceo conforme es **por la cara de compras** + decisiones documentadas. Eso es exactamente lo que sigue.

Incidencia de datos corregida hoy (transparencia): el gap "−2.599 € inexplicado" era un error de conversión mío al parsear el snapshot (columnas USA en USD nativo). Resuelto; el −2.499 € de junio tiene la misma firma. El `avg_cost_eur` de los 9 tickers USD quedó re-expresado a EUR (fx 0,89117) — pendiente coste por lote real desde `trades.csv` para fiscalidad.

## 1. Órdenes ejecutables (Módulo 1 — compras conformes)

Únicas compras 100 % conformes hoy: **VZ, O, XOM**. Total **+163 acciones ≈ 9.021 €** (backlog jul-sep 9.000 € + cash 660 € cubren octubre; noviembre se cubre con la aportación del mes).

| # | Cuándo | Ticker | Acciones | Precio ref. | Importe | Captura dividendo |
|---|---|---|---:|---:|---:|---|
| 1 | **Esta semana (antes de ~1-oct)** | **O** | +20 | $56,89 / 50,70 € | ~1.014 € | Ex-div ~1-oct, pago ~15-oct |
| 2 | **Esta semana (antes de ~8-oct)** | **VZ** | +70 | $47,61 / 42,43 € | ~2.970 € | Record 9-oct, pago 2-nov |
| 3 | **Esta semana** | **XOM** | +18 | $159,19 / 141,87 € | ~2.554 € | Ex-div ~14-nov, pago ~10-dic |
| 4 | Noviembre (aportación 3.000 €) | **VZ** | +37 | idem | ~1.570 € | Q1-2027 |
| 5 | Noviembre | **O** | +18 | idem | ~913 € | Dic/ene |
| | **TOTAL** | | **163** | | **~9.021 €** | |

- Deposit before buying: faltan ~5.900 € además del cash (ordena el depósito del backlog antes de las órdenes 1-3; ojo con settled cash T+2 si compras el mismo día — el rechazo de VZ en junio fue por esto).
- Órdenes limit o market en ventana líquida (16:00-17:30 CET como en junio). Precios de referencia del 22-sep; manda el precio del broker.
- Comisión estimada: ~5-8 € total (3-5 órdenes IBKR).

**Resultado del Módulo 1** (denominador ~115.810 €):

| Ticker | Antes | Después | Target raw | Banda tras compra |
|---|---:|---:|---:|---|
| VZ | 1,46 % | **5,27 %** | 6,5 % | ✅ dentro (−19 % rel) |
| O | 4,78 % | **6,08 %** | 7,5 % | ✅ dentro (−19 % rel) |
| XOM | 1,98 % | **4,03 %** | 5,0 % | ✅ dentro (−19 % rel) |
| VHYL | 37,47 % | 34,55 % | 31 % | ✅ vs raw (+11 %); ⚠️ +26 % vs escala normalizada (ver §4) |
| VWCE | 35,80 % | 33,01 % | 36 % | ✅ |
| Sleeve ETF | 73,3 % | **67,6 %** | 67 % | ✅ en target |
| Sleeve stocks | 22,4 % | **28,5 %** | (33 % resumen / 45,9 % suma tabla) | mejor posible sin tocar cuarentenas |

Dividendo forward: +~400 €/año brutos (~340 netos) → **~2.150-2.250 €/año netos** con la cartera resultante.

## 2. Módulo 2 — IBTS (la única banda al alza; se formaliza el colchón)

**Ejecutado en docs**: `target.csv` IBTS 0,5 % → **3,5 %** (peso actual 3,73 % → banda ✅). Cero trades, coherente con "Mantener IBTS (bonos seguros)" del plan 30k.
*Alternativa no ejecutada*: recortar ~3.100 € (minusvalía ~−450 € compensable vs +893 € plusvalías 2026). Si la prefieres, se revierte el target y se añade la orden de venta — dímelo.

## 3. Módulo 3 — Revisiones documentadas (lo que A1 exige para las alertas restantes)

Tras los Módulos 1-2 quedan 7 alertas de banda, **todas en posiciones en cuarentena (mantener, no añadir)**. Tu regla A1 no exige comprar hasta target: exige "revisión manual obligatoria" — esta tabla ES esa revisión y queda archivada:

| Ticker | Peso → | Condición de desbloqueo (se re-evalúa cada mes en `/analyze`) |
|---|---:|---|
| T | 0,49 % | Reanudación de subidas del dividendo (lleva congelado desde 2022) |
| AVGO | 1,14 % | P/E forward claramente <30× (~<$350) — comprar solo en debilidad |
| MO | 2,48 % | Payout ≤75 % (resultados 29-oct: improbable con guía 5,61-5,72 $) |
| GOOG | 0,90 % | Sin desbloqueo por diseño (A5: mantener, no ampliar) |
| JNJ | 4,28 % | P/E ≤15× (V4) — o enmienda de valoración por grupos |
| ENG | 2,27 % | CNMC 2027-2032 + dividendo post-2026 comprometido |
| VHYL (escala norm.) | 34,6 % | No es breach real: artifacto de la doble escala (ver §4) |

Nada de esto exige vender: ningún grado D, ningún corte de dividendo, TAX-ES desaconseja vender ganadoras (JNJ +44 %, KO +22 %).

## 4. Fix de sistema recomendado (1 línea, no cambia filosofía)

La tabla de STRATEGY suma 113,5 % en crudo y su resumen dice "acciones ≈33 %" cuando la tabla suma 45,9 %. Normalizado (lo que usa `analyze.py`): ETFs 59 %, acciones 40 %, bonos 0,4 %. **Propuesta**: corregir el resumen de STRATEGY.md a los números reales de la tabla y añadir una línea "pesos crudos, normalizados a 1 internamente". Evita que cada análisis tenga dos verdades.

## 5. Estado de conformidad final (tras ejecutar Módulos 1-2)

| Posición | Regla aplicable | Estado |
|---|---|---|
| VWCE / VHYL | Principio 1 + A6 (intocables) | ✅ |
| O, VZ, XOM | S1-S4 + V4 + banda | ✅ en target, banda verde |
| IBTS | Banda A1 | ✅ (target formalizado 3,5 %) |
| KO, GOOG, JNJ | Hold sin añadir (estrategia/V4) | ✅ como tenencia |
| T, ENG, MO, AVGO | S2/A3 cuarentena + revisión A1 | ✅ revisión documentada (§3) |
| Fiscal | TAX-ES: compras, no ventas | ✅ cero plusvalías realizadas en el paquete |
| Cash | Residual | ✅ ~0 % tras noviembre |

**Todo pasa las normas en el único sentido en que tu sistema lo permite: sin vetos, sin ventas forzadas, alertas revisadas y documentadas.** El resto del camino al 33 % de stocks depende de que los datos (no las reglas) cambien.

## 6. Checklist operativo

- [ ] Depositar ~6.000 € (backlog) en IBKR **antes** de las órdenes 1-3 (settled cash).
- [ ] Semana del 22-29 sep: comprar O +20, VZ +70, XOM +18 (capturan los ex-div de oct/nov).
- [ ] Actualizar `holdings.csv` tras ejecutar (qty + avg cost + cash).
- [ ] Noviembre: VZ +37, O +18 con la aportación mensual.
- [ ] Loguear ambas tandas en `decisions.md` (plantilla estándar).
- [ ] 29-oct: revisar MO (¿payout ≤75 %?). Nov: vigilar AVGO <$350.
- [ ] Q4: Activity Statement Q3 → cerrar reconciliaciones + `tax_2026.py`.

---
*No es asesoramiento financiero. Precios de referencia 22-sep-2026 (fx 0,89117); manda el broker. Decisión final del inversor.*
