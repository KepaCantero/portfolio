---
task_category: Ejecución disciplinada de rutina mensual de inversión
role: Ejecutor de disciplina mensual (no decide tesis, solo aplica reglas)
tone: Seco, operativo, sin teorizar
output_format: Tabla de 3 tramos + checklist de validación
target_audience: El propio inversor (decisor final)
detail_level: Moderate
thinking_effort: High
task_horizon: Single-step
constraints:
  - Tramo 1 SIEMPRE es O (Realty Income), sin discusión
  - Tramo 2 solo de {VZ, JNJ, MO, XOM, AVGO, ENG, T} — la más desviada a la baja
  - Tramo 3 = 2ª más desviada, o AVGO si flag --tech
  - PROHIBIDO añadir a VWCE/VHYL con nueva pasta
  - Todos los importes en EUR
---

# Plantilla — Rutina mensual (3.000 € / mes)

> Caso de uso: **ejecutar la rutina mensual fija** definida en `STRATEGY.md`. Es la operativa más repetitiva (12 veces al año) — por eso merece su propia plantilla optimizada para **velocidad** (no para exploración).
>
> Diferencia con `rebalance.md`: la rutina mensual tiene **reglas fijas** (O + 2 más baratas). `rebalance.md` es más flexible (greedy por desviación).

## 1) Prepara el contexto

Pega en este orden:

```
1. STRATEGY.md     (FUENTE DE LA VERDAD — rutina mensual definida ahí)
2. RULES.md        (solo las reglas safety S1-S4 + capa 3 A1 bandas)
3. TAX-ES.md
4. holdings.csv
5. target.csv
6. decisions.md    (últimas 3-5 entradas, para detectar caídas recientes)
7. prices.json     (salida de fetch_prices.py)
```

> No necesitas `score.py` para la rutina mensual — las posiciones ya están validadas. Solo se invoca safety check si hay una sorpresa.

## 2) Placeholders

- `{{fecha}}` — `YYYY-MM-DD`.
- `{{capital}}` — default `3000`. Admite cualquier múltiplo de 1.000.
- `{{flag_tech}}` — `--tech` o vacío. Si `--tech`, tramo 3 → AVGO.

## 3) Instrucción (pega DESPUÉS del contexto)

```
Fecha: {{fecha}}
Capital a desplegar: {{capital}} EUR
Flag --tech: {{flag_tech}}

Actúas como mi ejecutor de disciplina mensual. La rutina está en
STRATEGY.md sección "Rutina mensual con 3.000 €/mes". Aplícala
literalmente — sin reinterpretarla.

TAREA

Calcula la propuesta dividiendo {{capital}} EUR en 3 tramos iguales
de {{capital/3}} EUR cada uno.

ENTREGA (markdown, conciso):

A) Cifras (una línea):
   "Desplegar {{capital}} € | Deployado Y € | Sobrante Z €"

B) Tabla de 3 filas (una por tramo):
   | Tramo | Ticker | Razón | Precio EUR | Acciones | Deploy EUR |

   - Tramo 1: O (Realty Income). Razón: "Fijo según rutina".
   - Tramo 2: de {VZ, JNJ, MO, XOM, AVGO, ENG, T}, el ticker con
     mayor desviación negativa (current_weight - target_weight más
     bajo). Razón: "Mayor desviación a la baja vs target (X.XX pp)".
   - Tramo 3: si flag_tech=--tech → AVGO. Razón: "Acelerar tecnología".
     Si no → 2º más desviado. Razón: "Segunda mayor desviación".

C) Validación (checkboxes):
   [ ] Tramo 1 es O (no exceptions)
   [ ] Tramo 2 es del pool {VZ,JNJ,MO,XOM,AVGO,ENG,T}
   [ ] Tramo 3 respeta flag --tech
   [ ] Cada tramo son acciones enteras
   [ ] Sobrante total < 5% del capital

D) Comentario fiscal (una línea):
   "Solo compras. Sin plusvalía este año. W-8BEN vigente."

E) Alerta solo si aplica:
   - Si alguna acción del pool ha caído >5% último mes (ver
     decisions.md o prices.json vs avg_cost_eur), sugerir concentrar
     tramos 2+3 en ella (regla de flexibilidad STRATEGY.md).
   - Si circuit breaker macro activo (mercado caída >20%), aplicar
     igualmente — el plan es comprar en caídas.

REGLAS

- Cero creatividad. No propongas tickers fuera del pool.
- No añadas a VWCE, VHYL, IBTS ni Cash.
- Cero teoría: este prompt se ejecuta 12 veces al año — la tesis ya
  está en STRATEGY.md.

CRITERIOS DE ACEPTACIÓN

[ ] Suma de "Deploy EUR" + "Sobrante" = {{capital}}.
[ ] Tramo 1 ticker = O.
[ ] Tramos 2 y 3 son tickers distintos (salvo que el pool tenga
    menos de 2 opciones, lo cual no debería ocurrir).
[ ] Razones citan datos (desviación en pp, no "parece barato").

Si algún check falla, recalcula.
```

## 4) Notas GLM 5.2

- **Thinking effort = High** (no Max): esta plantilla es mecánica, no requiere razonamiento profundo. High es suficiente y más rápido.
- **Task horizon = Single-step**: la rutina es un cálculo directo, no una cadena agentic.
- Por eso esta plantilla es la **más barata** de ejecutar mensualmente.
- Si trae score.py output y ve safety D en algún ticker del pool, cambiar a Max effort y revisar manualmente.
