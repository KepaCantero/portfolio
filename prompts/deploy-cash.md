---
task_category: Despliegue grande de capital + reorganización estructural
role: Estratega de cartera con sensibilidad fiscal
tone: Pragmático, equilibrado riesgo/regalo fiscal, orientado a plan ejecutable en 2 fases
output_format: Plan en 2 fases + tablas + estimación fiscal + checklist seguridad
target_audience: El propio inversor (decisor final)
detail_level: Comprehensive
thinking_effort: Max
task_horizon: Long-horizon (agentic)
constraints:
  - PROHIBIDO vender VWCE o VHYL (base intocable)
  - MANTENER IBTS (colchón bonos)
  - Ventas de microposiciones generan plusvalía/minúsv. estimar siempre impacto fiscal
  - Las compras tras limpieza respetan RULES.md (filtros safety + valuation)
  - Todos los importes en EUR
---

# Plantilla — Despliegue grande (10k+) con limpieza

> Caso de uso: **desplegar una cantidad grande** (10.000 €+) que **incluye ventas** de microposiciones y redistribución. Es el caso del despliegue de los 30k pendientes.
>
> Diferencia con `rebalance.md`: aquí **sí se vende** (microposiciones), por lo que el componente fiscal es crítico.

## 1) Prepara el contexto

Pega en este orden:

```
1. PROFILE.md
2. STRATEGY.md     (sección "Plan de acción con los 30.000 €")
3. RULES.md        (framework completo — safety, valuation, allocation)
4. TAX-ES.md       (CRÍTICO — calcular impacto fiscal de ventas)
5. holdings.csv    (con avg_cost_eur para calcular P&L al vender)
6. target.csv
7. decisions.md
8. prices.json     (fetch_prices.py)
9. scores.json     (score.py — safety/valuation de todas las posiciones)
```

## 2) Placeholders

- `{{capital_nuevo}}` — euros frescos a desplegar (ej. `30000`).
- `{{objetivo}}` — `limpiar_micros_y_distribuir` (default) | `solo_distribuir` | `solo_limpiar`.
- `{{fecha}}` — `YYYY-MM-DD`.

## 3) Instrucción (pega DESPUÉS del contexto)

```
Fecha: {{fecha}}
Capital nuevo a desplegar: {{capital_nuevo}} EUR
Objetivo: {{objetivo}}

Actúas como mi estratega para este despliegue grande. El plan está
en STRATEGY.md sección "Plan de acción con los 30.000 €". Aplica
RULES.md (filtros safety + señales valuation) y respeta TAX-ES.md
al estimar plusvalías.

TAREA

Entrega un plan en 2 FASES (markdown):

═══ FASE 1 — Limpiar microposiciones ═══

Lista las que aparezcan en holdings.csv de:
  RTX, PNC, TXN, AMGN, NOC, LMT, MVUS, IHYG, FGQI

Para cada una, tabla:
  | Ticker | Qty | Precio compra EUR | Precio hoy EUR | Valor EUR | P&L € | P&L % |

Reglas:
- MANTENER IBTS SIEMPRE (no aparece en la lista — es el colchón).
- Para cada venta: estimar plusvalía o minusvalía en EUR.
- Plusvalía: tipo 19% hasta 6.000 €, 21% hasta 50.000 €, 23% desde
  50.001 € (base ahorro agregada del año).
- Minusvalía: compensable con otras plusvalías del año.

Total FASE 1:
- Valor liberado: X €
- Plusvalía estimada: Y €
- Impuesto estimado: Z € (si Y > 0)
- Minusvalía compensable: W € (si Y < 0)
- Neto para reinvertir en FASE 2: X - Z €

═══ FASE 2 — Distribuir total disponible ═══

Total a deployar = {{capital_nuevo}} + (valor liberado FASE 1) - (impuesto FASE 1)

Tabla de propuesta:
  | Ticker | Nombre | Precio EUR | Acciones a comprar | Deploy EUR | Valor después | Target % después |

Reglas (de RULES.md):
- PROHIBIDO añadir a VWCE, VHYL, IBTS o Cash (salvo leftover).
- Solo tickers del sleeve Stock.
- Safety grade ≥ B (60+) en cada compra.
- KW signal ≠ EXPENSIVE y DDM signal ≠ OVERVALUED en cada compra.
- Si un ticker no cumple safety/valuation: reducir su peso y
  redistribuir al siguiente elegible.

═══ Resumen fiscal global ═══

- Plusvalía bruta FASE 1: A €
- Impuesto FASE 1: B €
- Operación FASE 2: solo compras → sin plusvalía.
- Coste fiscal neto del despliegue: B €

═══ Validación (checkboxes) ═══

[ ] No se vende VWCE ni VHYL
[ ] IBTS se mantiene
[ ] Todas las ventas FASE 1 son de la lista de microposiciones
[ ] Todas las compras FASE 2 son sleeve Stock
[ ] Safety grade ≥ B en cada compra FASE 2
[ ] Plusvalía estimada cita el cálculo (qty × delta precio)
[ ] Tipo impositivo correcto según tramo de base ahorro
[ ] Neto a reinvertir = liberado - impuesto (coincide con total FASE 2)

REGLAS

- Cero creatividad. Tickers solo de target.csv.
- Si una microposición genera plusvalía > 1.000 €, marcarla para
  revisión: ¿merece la pena venderla o esperar a enero del año
  siguiente para diferir el impuesto?
- Si una microposición genera minusvalía > 500 €, priorizarla (ayuda
  a compensar otras plusvalías del año).

CRITERIOS DE ACEPTACIÓN

[ ] Suma de "Deploy EUR" FASE 2 = neto a reinvertir.
[ ] Cada fila FASE 2 cumple safety + valuation checks.
[ ] Cálculo fiscal cita los tipos de TAX-ES.md.
[ ] Si circuit breaker macro activo, explicar cómo afecta (p.ej.
    "mercado en caída >20%: priorizar compras sobre ventas, posponer
    FASE 1 si las microposiciones están en minusvalía temporal").

Si algún check falla, recalcula.
```

## 4) Notas GLM 5.2

- **Thinking effort = Max**: despliegue grande = decisiones irreversibles (ventas generan evento fiscal). El razonamiento profundo evita errores caros.
- **Task horizon = Long-horizon (agentic)**: cadena cálculo-ventas → P&L → impuesto → redistribución → validación.
- **Ventana 1M tokens crítica**: pega TODO (scores.json con todos los fundamentales, decisions.md entero, holdings con avg_cost).
- Si GLM no tiene acceso a datos de fundamentales en tiempo real, **debes** pegar scores.json o el modelo inventará payout ratios.
- Para despliegues >50k, considera partir en 2 sesiones (FASE 1 primero, FASE 2 tras confirmar ejecución de ventas).
