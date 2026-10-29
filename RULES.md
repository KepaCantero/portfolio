# RULES — Framework doctrinal de decisión

Codifica los 20 recursos de `BIBLIOGRAPHY.md` en **reglas ejecutables** organizadas en 3 capas. Este archivo es la **fuente de la verdad** para `score.py` y para validar cualquier propuesta de rebalanceo.

> Lee junto con `STRATEGY.md` (reglas de alto nivel) y `TAX-ES.md` (impacto fiscal).

---

## Capa 1 — SAFETY: ¿sigo confiando en este dividendo?

Responde a: *"¿es seguro mantener/ampliar esta posición?"*

### Filtros duros (HARD FAIL = veto automático)

| # | Regla | Fuente | Aplicación |
|---|---|---|---|
| S1 | Payout ratio ≤ 75 % del FCF | Damodaran | Si > 75 % → flag rojo. Si > 90 % → reducir. |
| S2 | Dividend growth ≥ 5 años consecutivos | Lowell Miller (DQDI) | Excluir posición candidata a nueva compra si no cumple. Posiciones existentes: revisar. |
| S3 | Dividend growth ≥ 8 % anual (últimos 5y) | Lichtenfeld 10-11-12 | Solo para AVGO, JNJ, XOM. Si no cumple → revisar tesis. |
| S4 | P/E ≤ 25 para mantener; ≤ 15 para "defensive buy" nuevo | Graham | P/E > 40 → flag rojo (burbuja). |

### Score compuesto 0-100 (estilo Simply Safe Dividends)

Calculado en `scripts/score.py`. Pesos:

| Componente | Peso | Lógica |
|---|---|---|
| Payout ratio | 30 % | 100 si ≤ 0.50; lineal descenso hasta 0 a 0.90+. |
| Debt/Equity | 25 % | 100 si ≤ 1.0; lineal descenso hasta 0 a 3.0+. |
| Dividend history (años consecutivos) | 25 % | min(100, años × 10). |
| P/E razonable | 20 % | 100 si ≤ 15; 70 si 15-25; 30 si 25-40; 0 si > 40. |

**Interpretación**:
- **A (80-100)**: mantener y ampliar con tranquilidad.
- **B (60-79)**: mantener; ampliar solo si valoración acompaña.
- **C (40-59)**: mantener; **no ampliar** hasta recuperar B+.
- **D (<40)**: **vender** (reducir 50 % en 2 tramos).

### Circuit breaker macro (Housel) — reescrito v2 (2026-09-29)

- **Si el mercado cae > 20 % desde el último máximo**: no se venden activos para financiar gasto (se consume el colchón de IBTS — guardrails de `PLAN-RETIRADA.md` §6). Solo se contemplan **compras de oportunidad** y, en su caso, las ventas previstas por Vías de salida (recorte de dividendo, grado D).
- Razón: el coste real es vender en el fondo, no la volatilidad.

> **Alcance v2 (2026-09-29)**: con el cambio de premisas a retorno total, la Capa 1/2 de filtrado de dividendos solo gobierna el **sleeve de acciones** — y el alcance exacto de ese sleeve (incluida su posible disolución) queda **pendiente de `ESTRUCTURA-DECISION-2026-09-29.md`** (opciones A/B/C). El destino por defecto de aportes es VWCE (cascada A8).

### Changelog

| Versión | Fecha | Cambios | Ref |
|---|---|---|---|
| v1.0 | jun-2026 | Sistema original 3 capas | — |
| v1.1 | 28-sep-2026 | V2-bis (ámbito DDM) · A7 (targets duales + status) · Vías de salida · IBTS target 3,5 % · fix score.py filas # | decisions.md 28-sep |
| v1.2 | 29-sep-2026 | **Cambio de premisas**: retorno total, fuera "nunca vender"/"solo dividendos" · A8 cascada con VWCE por defecto · circuit breaker reescrito (guardrails de retirada) · alcance del sleeve pendiente de ESTRUCTURA-DECISION | decisions.md 29-sep · mandato usuario |
| v1.2+ | pendiente | Bandas absolutas · V1/A4 a informativas · payout desconocido=0 — aprobación y aplicación aún pendientes | PROPUESTA-v1.2 |
| **v1.3** | 29/30-sep-2026 | **ESTRUCTURA C ELEGIDA**: sleeve 12 % solo-mantenimiento (VZ/O/JNJ/XOM/MO) · target.csv v2 · A9 test del sleeve ACTIVADO (XIRR vs VWCE a 31-dic-2028 → disolver si va por debajo) · VHYL + AVGO/GOOG/T/KO/ENG + recortes programados para ene-2027 (Deka → VWCE en dic-2026) | decisions.md 29-sep noche · ESTRUCTURA-DECISION |
| **v1.4** | 30-sep-2026 (tarde) | **C modificada a DILUCIÓN por decisión del inversor** (evitar IRPF de VHYL): VHYL + las 5 congeladas (ni compras ni ventas; fricción ~500 €/año asumida como prima de opción) · solo se vende Deka (dic) + polvo AVGO/GOOG/T/KO/ENG (ene) · **test redefinido: bloque congelado completo vs VWCE a 31-dic-2028** · barra de mantenimiento de congeladas: corte de dividendo o payout fwd >90 % sostenido → venta puntual | decisions.md 30-sep · target.csv v3 |

| **v1.5** | 1-oct-2026 | **NIVEL 7 ACTIVADO (opción A)**: tramo satélite operativo — 1/3 de cada ingreso a elegibles con hueco (hoy solo XOM), resto VWCE · caps: satélite ≤20 %, nombre ≤4 % · opción B (30-sep) revertida por el inversor; árbitro y veredicto 2028 vigentes · aportaciones = variable exterior (no plan) | decisions.md 1-oct · SISTEMA-NIVEL7 §8 |
---

## Capa 2 — VALUATION: ¿está barato ahora mismo?

Responde a: *"¿es buen momento para comprar más?"*

### V1 — Kelley Wright: Dividend Value Line

- Calcula el yield actual y su media histórica de 5 años + 1 desviación típica.
- **REINFORCED_BUY**: yield actual > media + 1σ (precio anormalmente bajo).
- **FAIR**: dentro de ±1σ.
- **EXPENSIVE**: yield actual < media − 1σ (caro).

### V2 — DDM (Gordon simplificado, CFA Institute)

```
fair_value = D1 / (r - g)
D1 = dividendo por acción esperado próximo año
r  = 9 % (tasa de descuento conservadora para dividend growth)
g  = 4 % (crecimiento sostenible largo plazo; usar 6 % para AVGO)
```

- **UNDERVALUED**: precio < fair_value × 0.95 → compra prioritaria.
- **FAIR**: ±5 % del fair value.
- **OVERVALUED**: precio > fair_value × 1.05 → esperar o reducir.

### V2-bis — Ámbito del DDM (enmienda 2026-09-28)

El modelo Gordon solo se aplica al grupo **Yield+Value de dividendo estable** (O, VZ, MO, T, ENG, KO, JNJ). Para **Quality+Growth (AVGO)** y **cíclicas de materia prima (XOM)**, la valoración de compra es exclusivamente V4/A5 (P/E ≤30× / ≤15×).

**Razón**: Gordon penaliza estructuralmente a los yield bajos en fase de crecimiento (fair = D1/(r−g) acota el múltiplo sin importar el crecimiento del beneficio) y lee los ciclos del crudo como tendencias de dividendo. Son limitaciones del modelo, no señales. La agrupación ya existía en A5 para el P/E; esta enmienda extiende el mismo criterio a la Capa 2.

### V3 — Macro signal (Ibbotson)

- Si el yield de **VHYL > 4.5 %** → **acelerar acumulación** (mercado general barato).
- Si yield VHYL < 3.5 % → desacelerar compras de VHYL (caro).

### V4 — Graham margin of safety

- Para nuevas compras: no pagar más de **15x beneficios** (P/E ≤ 15) en acciones defensivas (JNJ, KO, VZ, MO, T, ENG, XOM).
- AVGO y GOOG admiten P/E hasta 30 por su sesgo growth.

---

## Capa 3 — ALLOCATION: ¿cuánto y cuándo este mes?

Responde a: *"¿cuántos euros va a cada ticker?"*

### A1 — Vanguard relative bands (25 % relativos)

- Para cada sleeve principal (ETFs, Stocks), calcular peso actual vs target.
- **ALERTA**: si cualquier peso se desvía ±25 % **relativo** del target → revisión manual obligatoria.
  - Ejemplo: VWCE target 36 %. Banda: 27 % – 45 %. Fuera de banda → alerta.
- **Ejecución automática** (rutina mensual): solo dentro de banda.

### A2 — Carlson BSD score (3 variables)

Antes de cada compra mensual, ordenar candidatos por suma de:

1. Yield actual (más alto = más puntos).
2. Historial de pago (más años = más puntos).
3. Solidez del balance (debt/equity más bajo = más puntos).

Mayor score = primera compra del tramo 2/3.

### A3 — Miller DQDI filter

Toda nueva compra individual debe cumplir:
- Yield ≥ 2.5 % (excepto AVGO, GOOG que se permiten por growth).
- ≥ 5 años de dividendos crecientes.
- Payout ratio ≤ 75 %.

Si una posición existente deja de cumplir → revisar (capa 1).

### A4 — O'Shaughnessy ranking (yield + quality)

Cuando haya empate en Carlson BSD, desempatar por **Quality**:
- ROE estable 5y.
- Beneficios positivos 5y.
- Volatilidad baja (beta < 1.2).

### A5 — Berkin & Swedroe factor classification

Tratar cada grupo con criterios distintos:

| Grupo | Tickers | Factor dominante | Permitido |
|---|---|---|---|
| **Quality+Growth** | AVGO | Quality + Dividend Growth | Tolerar P/E hasta 30. Yield bajo OK. |
| **Yield+Value** | O, VZ, JNJ, MO, XOM, ENG, T, KO | High Yield + Value | P/E ≤ 15 (Graham). Yield ≥ 2.5 %. |
| **Growth puro** | GOOG | Sin dividendo significativo | Mantener; no ampliar (fuera de estrategia dividend). |

### A6 — Bogle core protection (reformulada v1.2)

**Nunca se sustituye el núcleo (VWCE) por acciones individuales**, sin importar caídas o euforias. Nota v2: con el cambio de premisas, VHYL deja de ser núcleo intocable — su destino lo decide ESTRUCTURA-DECISION.

### A9 — Test del sleeve de acciones (v1.3, activado con la elección de la estructura C)

**Pregunta**: ¿el sleeve de mantenimiento (VZ, O, JNJ, XOM, MO — 12 % máx, sin nuevas aportaciones) sigue mereciendo existir frente a VWCE? Es la única regla que audita RESULTADOS.

**Métrica**: XIRR (rentabilidad ponderada por dinero) de los flujos reales del sleeve (`data/trades.csv`, desde 2025-03, incluidas las compras de sep-2026 y el efecto de las ventas de la transición C) frente a cartera espejo: mismos importes y fechas en VWCE. VDHG retirado como benchmark (sesgo australiano).

**Implementación**: `scripts/sleeve_test.py` (pendiente construir, Q4-2026). Mientras: registro manual anual el 31-dic.

**Criterio (pre-registrado 29-sep-2026, umbrales aprobados con la elección de C)**:

| Fecha | Si XIRR sleeve < XIRR VWCE | Si XIRR sleeve ≥ |
|---|---|---|
| **31-dic-2028** (~3,8 años de datos) | Disolver el sleeve (vender los 5, → VWCE). Coste estimado hoy: ~1,3-2 k€ de IRPF | mantener |
| 31-dic-2030 | (si ya no se disolvió) re-evaluar | mantener |

Tolerancia: 0 pp. Nota: el sleeve no recibe dinero nuevo desde la elección de C, así que el test solo decide MANTENER vs DISOLVER — no hay flujos que redirigir.

### A8 — Cascada de aportaciones (v1.2, 2026-09-29)

Cada ingreso sigue, en orden:
1. **Buffer**: reponer cash operativo hasta 500 €.
2. **Gap del sleeve SOLO si la estructura aprobada lo mantiene** (opción B o C de ESTRUCTURA-DECISION); nunca hacia posiciones en cuarentena.
3. **Desbordamiento / destino por defecto**: todo lo demás → **VWCE** (día 5; sin decisión, se ejecuta igual).
4. **Ningún euro en cash sin regla**; mercado cerrado → orden pendiente para la próxima apertura.

Precedencia: A8 ejecuta; A1 solo alerta.

### A7 — Targets duales: destino vs camino (enmienda 2026-09-28)

El target expresa el **destino**; las reglas (Capa 1 + V4) expresan las **condiciones del camino**. No son la misma cosa y el sistema los separa:

- `target.csv` lleva columna `status`: **activo** (recibe dinero nuevo) · **mantener** (no ampliar por estrategia: KO, GOOG per A5) · **intocable** (VWCE/VHYL, Principio 1/A6) · **cuarentena** (hold sin añadir hasta su condición de desbloqueo, anotada junto al ticker).
- `/analyze` muestra dos números: **gap ejecutable** (solo filas `activo` — a dónde puede ir el dinero hoy) y **gap total** (todas — el destino).
- Los targets de cuarentena **no se rebajan**: son el destino. Se reactivan solos cuando el desbloqueo ocurre (p. ej. T reanuda subidas, MO baja de 75 % de payout, JNJ comprime P/E, ENG aclara CNMC). Las bandas rojas de cuarentena son un **semáforo de reentrada**, no ruido ni errores.
- Consecuencia asumida y documentada: mientras haya cuarentenas activas, el sleeve de acciones converge a su nivel *ejecutable* (~30 % con las enmiendas V2-bis), no al total del target. Es decisión consciente, no fallo.

---

## Capa NEW POSITION — Filtro de entradas (Morningstar 5-step)

Cualquier ticker **nuevo** que entre en cartera debe superar **≥ 3 de 5**:

1. **Moat económico**: ventaja competitiva durable (roca, patentes, red, marca).
2. **Cobertura del dividendo**: payout ≤ 75 % FCF (igual que S1).
3. **Solidez del balance**: debt/equity ≤ 2.0 o rating investment grade.
4. **Sostenibilidad del negocio**: sector no en declive terminal.
5. **Valoración relativa**: P/E actual ≤ media sectorial o ≤ propia media 5y.

Razón práctica: la cartera ya tiene 10 líneas individuales. Cualquier entrada nueva debe justificarse duro.

---

## Vías de salida (enmienda 2026-09-28)

Este sistema **corrige el drift por la cara de compras con dinero nuevo**, no con constant-mix (vender ganadoras/comprar perdedoras). "Rebalanceo" aquí = contribuciones dirigidas. La venta no está prohibida: está **reglada**. Solo se vende —parcialmente y en 2 tramos— si ocurre una de estas cuatro cosas:

1. **Safety en grado D** (<40 puntos) o payout >90 % sostenido (S1 en su nivel de veto).
2. **Recorte o supresión de dividendo confirmado** (la excepción ya prevista en el circuit breaker de Housel).
3. **Ruptura de tesis documentada en `decisions.md`** (p. ej. un rebase regulatorio que recorte estructuralmente el dividendo de ENG post-2026, o deterioro terminal del negocio de MO).
4. **Horizonte 8–10 años**: venta parcial programada de VWCE/VHYL para convertir plusvalías en flujo de dividendos (ya previsto en STRATEGY.md Principio 1).

Fuera de esos cuatro triggers, no vender. La razón fiscal es la de siempre: cada rotación con plusvalía adelanta 19–23 % de IRPF y rompe el interés compuesto.

---

## Conflicto de reglas y precedencia

Si dos reglas entran en conflicto, este es el orden de precedencia:

1. **Circuit breaker macro** (Housel) — veto absoluto en caídas > 20 %.
2. **Hard filters Capa 1** (S1-S4) — veto a nuevas compras.
3. **Reglas de STRATEGY.md** (no tocar VWCE/VHYL, nueva pasta solo a Stock sleeve).
4. **Capa 3 allocation** (bandas, rutina mensual).
5. **Capa 2 valuation** (señales de momento).

Valoración y allocation solo deciden **el orden y tamaño**, no **si** se compra. Safety y estrategia deciden el **si**.

---

## Reglas descartadas (constancia)

| Recurso | Regla propuesta | Por qué se descarta |
|---|---|---|
| Research Affiliates (rebalancing premium) | Rebalanceo trimestral, no mensual | La rutina mensual está ligada al flujo de 3.000 €/mes de ahorro. Cambiar a trimestral rompe la disciplina. |
| MSCI (Yield+LowVol) | Filtrar solo low-vol | Solapado con Quality; no añade signal distinto. |
| Bogleheads tax placement | VWCE en cuenta principal, US en paralelo | España sin cuenta de pensiones separada → todo en IBKR. Sin impacto operativo. |

---

## Cómo se aplican las reglas (workflow)

1. **`/analyze`** ejecuta `score.py` → muestra safety + valuation por cada ticker.
2. **`/rebalance [€]`** o **`/monthly-buy [€]`** generan propuesta.
3. Claude valida la propuesta contra `RULES.md`:
   - ¿Safety ≥ 60 en todos los compras?
   - ¿Kelley Wright no dice EXPENSIVE en ningún buy?
   - ¿DDM no dice OVERVALUED en ningún buy?
   - ¿Banda ±25 % respetada para VWCE/VHYL?
4. Si alguna regla falla → marcar en rojo y proponer alternativa.
