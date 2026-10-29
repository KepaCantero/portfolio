# SISTEMA NIVEL 7 — Portfolio gestionado por agente (diseño v1, 30-sep-2026)

> **Qué es esto**: el blueprint completo del nivel 7 bajo las premisas nuevas: **VWCE como núcleo + satélite activo de acciones seleccionadas por la maquinaria de RULES.md, operado por el agente**. El satélite persigue retorno total (batir a VWCE), NO renta — la renta murió con las premisas viejas.
> **Estado**: diseño aprobado para construcción. **Activación pendiente de 1 decisión** (§8). Las reglas vigentes no cambian hasta activación (RULES sigue en v1.4).

---

## 1. El portfolio

| Bloque | Peso objetivo | Regla de flujo |
|---|---:|---|
| **VWCE (núcleo)** | ~78 % | Destino por defecto de todo dinero nuevo no asignado al satélite |
| **Satélite activo** | **15-20 % (cap 20 %, nunca más)** | Recibe SOLO el tramo mensual designado, y SOLO en nombres que pasen el pipeline completo de filtros ese mes |
| **IBTS** | 4 % | Ballast; crece en el glidepath (~2032) |
| **Cash** | ~0,5 % | Buffer 500 € |

**Composición del satélite al activar** (per-nombre ≤4 %): O 4 · VZ 4 (pendiente confirmar Q3 26-oct) · JNJ 3 (comprable solo a P/E ≤15) · XOM 3 · MO 2 (payout ≤75 %) · **flex 2 %** para re-admisiones (AVGO <30×, ENG post-CNMC, T con subidas reanudadas).

**Rutina mensual nivel 7** (modifica A8 sin romper su espíritu):
1. Buffer 500 €.
2. **Tramo satélite (1.000 € o 1/3 del aporte)**: SOLO si hay candidatos elegibles verificados ese mes → ranking Carlson + gap. **Si no hay elegibles, el tramo entero va a VWCE** (el default jamás se viola).
3. Resto → VWCE el día 5 (con decisión o sin ella).
4. Regla de flexibilidad (caída >5 % de un elegible sin motivo grave): concentrar el tramo satélite del mes en él.

**Disciplina de venta**: sin cambios — Vías de salida (grado D, payout >90 %, corte confirmado, ruptura de tesis documentada) + barra de mantenimiento trimestral.

## 2. Arquitectura integrada (5 capas, qué existe y qué falta construir)

| Capa | Componente | Estado |
|---|---|---|
| **Datos** | Pastes IBKR del usuario (snapshot/posiciones/órdenes/trades) | ✅ flujo probado |
| | Activity Statement trimestral | ⚠️ pendiente rutina (Q4) |
| | Fundamentals vía yfinance | ⚠️ frágil (rate-limit por IP recurrente → **construir caché last-known-good + backoff** en fetch/score) |
| | Fallback: subagentes de investigación web con fuentes fechadas | ✅ probado (2 pasadas completas) |
| **Analítica** | `analyze.py` (pesos, gaps, bandas) | ✅ (mejorar: bandas absolutas, atribución satélite) |
| | `score.py` (Capa 1-2 de RULES) | ✅ (mejoras pendientes: payout desconocido=0, detectar dividendos congelados en S2, caché) |
| | **`sleeve_test.py`** — XIRR flujos reales del satélite vs cartera espejo VWCE | ❌ **construir — es el árbitro del sistema** |
| | **`tax_2026.py`** — borrador IRPF | ❌ construir (Q4) |
| | **`candidates.csv`** — watchlist con estado (elegible/cuarentena/unlock) | ❌ crear |
| **Decisión** | RULES.md (filtros, precedencia, gobernanza) | ✅ v1.4 → v1.5 al activar |
| | target.csv (targets nivel 7) | listo al activar |
| | decisions.md (log de cada decisión) | ✅ |
| **Ejecución** | Protocolo de tickets IBKR campo a campo (Limit/Day/sin stops; ventanas 15:30-17:30 CET) | ✅ probado (tanda 28-sep) |
| **Verificación** | Agente trimestral de resultados (spec §4-WF2) | ✅ patrón probado |
| | Auditoría anual de gobernanza (changelog, pre-registros) | ❌ rutina a estrenar |

## 3. Actores y responsabilidades

| Actor | Hace | Nunca hace |
|---|---|---|
| **Usuario** | Pega snapshots; deposita; **ejecuta órdenes en IBKR**; aprueba cambios de reglas y activaciones; aporta el "no" humano | — |
| **Agente principal (ZCode)** | Orquesta todos los workflows; aplica RULES sin excepciones; prepara propuestas de orden; mantiene holdings/coverage/decisions/memoria; lanza subagentes | **Ejecutar órdenes**; cambiar reglas sin changelog/pre-registro; comprar fuera del pipeline de filtros |
| **Subagentes de research** (general-purpose + WebSearch) | Verificación trimestral de holdings; screening de candidatos nuevos (Morningstar 5-step + fuentes fechadas); verificaciones fiscales puntuales | Decidir (solo informan) |
| **Scripts** (deterministas) | analyze/score/sleeve_test/tax: números reproducibles | — |
| **Asesor fiscal (humano, externo)** | Bizkaia foral, 720, step-up Deka, escala ahorro | — (todos los datos foral llevan sello VERIFICAR CON ASESOR hasta que él firme) |

## 4. Workflows (SOPs operativos)

**WF1 — Sesión mensual (día 1-5)** — *trigger: usuario pega snapshot; actor: agente; artefactos: coverage/*-fecha.json, propuesta de orden, entrada decisions.md*
1. Parsear snapshot → prices/snapshot/analysis del día (fx implícito reconciliando NLV).
2. score.py (o fallback manual-web) → set de elegibles este mes.
3. Propuesta: tramo satélite (elegibles por Carlson+gap) + resto VWCE, con importes y límites de precio.
4. Usuario ejecuta → pega fills → agente actualiza holdings.csv, cierra la entrada con Revisión.
5. **Regla día 5**: sin decisión del usuario → todo a VWCE (nunca cash sin regla).

**WF2 — Verificación trimestral (ene/abr/jul/oct, temporada de resultados)** — *trigger: calendario; actores: subagentes + agente; artefacto: scores + changes de estado en candidates.csv/target*
1. Un agente verifica cada nombre del satélite: payout, dividendo (¿subida/congelación/corte?), guía, eventos desde la última pasada — con fuentes y fechas.
2. Agente cruza con la barra de mantenimiento → unlock/cuarentena/venta puntual (Vías de salida) → changelog si cambia algo estructural.
3. Calendario 2026-27: JNJ 13-oct · VZ 26-oct · MO 29-oct · XOM ~fines oct · O mensual (8-ish de cada mes) · declaraciones AVGO dic/mar.

**WF3 — Sesión anual (31-dic)** — *actor: agente; artefactos: informe anual + test*
1. **`sleeve_test.py`: XIRR del satélite vs espejo VWCE** (flujos reales desde 2025-03, incluidas ventas). Es EL número del sistema.
2. Recalibrar: SWR vigente, capital objetivo, % plusvalía por euro de VWCE (retirada), colchón.
3. Auditoría de gobernanza: ¿se cumplió el changelog? ¿algún pre-registro omitido?
4. **Veredicto 31-dic-2028 (pre-registrado)**: satélite < VWCE acumulado → disolver (nivel 5); ≥ → continúa (y es evidencia para ampliar cap).

**WF4 — Evento (ad hoc)** — *triggers*: corte/supresión de dividendo confirmado · caída >5 % de un elegible sin motivo grave · caída mercado >20 % desde máximos (modo circuit breaker: cero ventas, solo compras de oportunidad con colchón externo) · ruptura de tesis (siempre documentada en decisions.md antes de vender).

**WF5 — Fiscal (Q4 → Renta)** — tax_2026.py → borrador → asesor (foral, 720, Anexo A, intereses extranjeros) → firma humana.

**WF6 — Admisión de candidato nuevo (raro, por diseño)** — *gate Morningstar ≥3/5* → subagente verifica (moat, payout, balance, sector, valoración vs 5y) → propuesta con informe → aprobación usuario → si requiere tocar reglas: 30 días/pre-registro → entrada inicial ≤1,5 % del portfolio.

## 5. Skills instaladas (`.claude/commands/`)

| Skill | Trigger | WF que cubre |
|---|---|---|
| **`/state`** | Arranque de sesión | Bootstrap: grafo + hilos + calendario + pesos |
| **`/monthly`** | Día 1-5, con snapshot | WF1: parse → scoring → orden cascada A8 → registro |
| **`/quarterly`** | Temporada resultados | WF2: subagentes → barra → estados |
| **`/annual-test`** | 31-dic | WF3: sleeve_test + recalibración + veredicto |
| **`/casa-extract`** | Usuario abre tabs | Refresco catálogo inmobiliario |
| **`/casa-dd [REF]`** | Candidato concreto | Ficha due diligence |
| **`/deka-liquidar`** | Paso 0 listo | Guía liquidación Deka |
| **`/tax`** | Q4 → Renta | WF5: borrador IRPF |
| **`/research [TICKER]`** | Ad hoc | Verificación puntual |
| **`/graph-sync`** | Cierre de CADA workflow | Mantenimiento del knowledge graph |

**Regla**: todo workflow termina con `/graph-sync` — sin eso el grafo se pudre.
## 6. Hoja de ruta de construcción (antes de activar nada)

| Semana | Construir | Detalle |
|---|---|---|
| 1 | `candidates.csv` + upgrades `score.py` | payout desconocido=0; S2 detecta congelaciones (T/VZ); caché last-known-good |
| 1-2 | `sleeve_test.py` | XIRR + espejo VWCE; sirve YA con el bloque congelado (línea base del test 2028) |
| 2 | `fetch_prices.py` robusto | backoff + caché; fallback manual documentado |
| 3 | `tax_2026.py` | borrador IRPF (necesario pase lo que pase) |
| continua | WF2 en vivo | JNJ 13-oct, VZ 26-oct, MO 29-oct: primeros tres ciclos reales del flujo trimestral |
| Q1-2027 | Informe anual v1 | primer WF3 completo |

## 7. Gobernanza y kill-switch

- Todo cambio de regla → changelog RULES + asimetría (endurecer=ya; habilitar compras=30 días o pre-registro).
- **Ninguna compra de satélite fuera del pipeline de filtros** — discrecionalidad cero sin log.
- **Kill-switch doble**: (a) veredicto 31-dic-2028 (disolver si satélite < VWCE); (b) suave anual: satélite < VWCE por >2 pp en ventana móvil 3 años → congelar compras nuevas hasta revisión con el usuario.
- Límite de daño estructural: satélite ≤20 %, per-nombre ≤4 % → el peor escenario activo cuesta <1 % del patrimonio.

## 8. Decisión de activación — **OPCIÓN A ELEGIDA (1-oct-2026, antes B el 30-sep)**

> Historial: B elegida el 30-sep; el 1-oct el inversor activa A (tramo satélite operativo YA). La decisión estaba pre-registrada en este diseño (§8 original), por lo que no requiere periodo de 30 días. El árbitro y el veredicto 31-dic-2028 siguen vigentes igual.

### (B previa, 30-sep)

La maquinaria completa opera YA (WF2-WF6, árbitro, candidates); **cero dinero nuevo en nombres individuales hasta el veredicto del 31-dic-2028**. El bloque congelado es el satélite de prueba con dinero ya comprometido. Si el test gana → activar tramo satélite el 1-ene-2029 con evidencia propia.

**Construcción iniciada el mismo día**: `data/candidates.csv` ✅ · upgrades `score.py` (payout desconocido=0 + flag, detección de dividendos congelados S2, caché last-known-good en `coverage/fundamentals-cache.json`) ✅ · **`scripts/sleeve_test.py` ✅ con baseline fijado** (`coverage/sleeve-test-baseline.json`: bloque 62.145,19 € vs espejo 367,4621 VWCE @ 169,12 €). Pendiente: `fetch_prices.py` robusto (backoff), `tax_2026.py` (Q4), modo --full-history del árbitro (requiere export completo de transacciones del usuario).
