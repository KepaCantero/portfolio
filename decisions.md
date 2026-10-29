# Diario de decisiones

Log cronológico de decisiones de inversión, rebalanceos y aprendizaje. Cada entrada debería explicar el **qué**, **por qué**, y **resultado esperado**.

## Plantilla de entrada

```
## YYYY-MM-DD — Título corto
**Contexto**: estado de la cartera / mercado en ese momento.
**Decisión**: qué se hizo (comprar/vender/mantener).
**Razón**: por qué (referencia a STRATEGY.md si aplica).
**Importe**: € desplegados / retirados.
**Resultado esperado**: qué se espera a 1 mes / 1 año.
**Revisión**: (a rellenar después) qué pasó realmente.
```

---

<!-- Las nuevas entradas se añaden debajo de esta línea, más recientes arriba -->

## 2026-10-01 — GRAFO SEMÁNTICO instalado (arquitectura Fukura adaptada)

**Contexto**: El usuario pide replicar el knowledge graph de Obsidian que tiene en Fukura (~/.fukura/obsidian-dashboard-hub). Adaptación de su arquitectura a este sistema.

**Decisión**: (1) `graph/graph.json` = fuente de verdad del grafo (68 entidades, 55 relaciones: posiciones, reglas con triggers, calendario, hilos abiertos, contradicciones, cuentas, goals, zonas casa). (2) `graph/build_notes.py` → proyección Obsidian en `graph/notes/` (9 carpetas, notas `generated: true`, INDEX.md) — abrir `graph/notes/` como vault. (3) Espejo consultable sembrado en MCP `knowledge-graph` (núcleo: posiciones críticas, reglas, eventos, hilos, contradicción VZ). (4) Paso "sync grafo" añadido como cierre de cada workflow en SISTEMA-NIVEL7 §5.

**Razón**: Bootstrap de sesión en una consulta (read_graph), consultas de impacto (regla→posición→evento→acción), contradicciones con ganador trazable, calendario como grafo, y visualización para el usuario.

**Importe**: 0 €.

**Resultado esperado**: Sesiones futuras arrancan con read_graph; el grafo no se pudre porque las cifras vivas siguen en target.csv/RULES/decisions (el grafo es índice relacional derivado).

**Revisión**: (pendiente) primer ciclo de sync real tras los fills de octubre.

---


## 2026-10-01 — NIVEL 7 ACTIVADO (opción A) + ingreso 3.000 €: XOM+VWCE

**Contexto**: El inversor activa la opción A (tramo satélite operativo ya; B elegida el 30-sep revertida al día siguiente). La elección estaba pre-registrada en el diseño del SISTEMA-NIVEL7 §8 → sin periodo de 30 días. Ingreso de 3.000 € anunciado. Aportaciones = variable exterior (corrección del 30-sep: no son plan ni regla).

**Decisión**: Aplicar la cascada nivel 7 al ingreso:
- **Tramo satélite (1/3 = 1.000 €) → XOM**: único elegible con hueco (O sobre tope 4,7 %>4 %; VZ/JNJ/MO en cuarentena). Hueco XOM: 1.208 € (tope 4 % × 112.145 € − 3.278 € actuales). Ticket: **+7 acciones @ ~160,60 $ (~990 €)** → XOM queda ~3,7 %.
- **Resto (2.000 €) → VWCE**: ticket **+11 acciones @ ~169,12 € (1.860 €)** (o 12 si se quiere apurar; deja 533 €).
- Cash final ~710 € (buffer 500 + slack fees/FX).
- Con esto **XOM queda esencialmente lleno** (~208 € de hueco): los próximos tramos, si llegan antes de los unlocks, irán 100 % a VWCE.

**Razón**: Regla del nivel 7 activada por el inversor. XOM pasa todos los filtros (43 años subiendo, payout fwd ~33 %, P/E fwd 12,8×) y captura el ex-div ~14-nov (subida anual esperable con la declaración de ~fines de oct).

**Importe**: 3.000 € ingresados; 2.850 € a desplegar (7 XOM + 11 VWCE).

**Resultado esperado**: XOM 3,7 % (techo 4 %); VWCE ~35,6 % del IBKR actual (crece con cada flujo); dividendo XOM dic ~27 € netos sobre 29,89 sh.

**Revisión**: (pendiente) fills reales → actualizar holdings; WF2 octubre (JNJ 13, VZ 26 — congelación dividendo —, MO 29 — payout al borde del trigger); Deka dic; polvo ene.

---

## 2026-09-30 (noche) — NIVEL 7: opción B elegida + maquinaria construida y operativa

**Contexto**: Tras el diseño completo del nivel 7 gestionado por agente (SISTEMA-NIVEL7.md), el inversor elige la **opción B**: toda la maquinaria opera ya, cero dinero nuevo en nombres individuales hasta el veredicto del 31-dic-2028. Fundamento revelado esta sesión: el sistema se diseñó agent-first — las objeciones de carga de trabajo contra estrategias activas no aplican; las de fiscalía y evidencia sí.

**Decisión**: Opción B + construcción inmediata:
1. **`scripts/sleeve_test.py`** (EL ÁRBITRO): XIRR del bloque congelado vs espejo VWCE. **Baseline fijado** (`coverage/sleeve-test-baseline.json`): bloque = 62.145,19 € (VHYL 39.686 + O 6.777 + JNJ 4.960 + VZ 4.591 + XOM 3.278 + MO 2.853) vs espejo = 367,4621 VWCE @ 169,12 €. Criterio pre-registrado: a 31-dic-2028, bloque < espejo → DISOLVER; ≥ → CONTINUA (y evidencia para reactivar nivel 7 el 1-ene-2029).
2. **`data/candidates.csv`**: watchlist con estados y unlocks, con los datos verificados del 29-sep.
3. **Upgrades `score.py`**: payout desconocido = 0 + flag DATO_FALTANTE (antes 50 — aprobado v1.2+); detección de dividendos congelados (S2); caché last-known-good en `coverage/fundamentals-cache.json` (mitiga el rate-limit recurrente de Yahoo).
4. Pendiente de construcción: `fetch_prices.py` robusto (backoff), `tax_2026.py` (Q4), modo --full-history del árbitro (requiere export completo de transacciones — trades.csv solo cubre 2025-03→2026-05).

**Razón**: Operar el nivel 7 sin financiar la apuesta antes de tener evidencia. La carga de gestión es del agente (sistema agent-first); el capital nuevo sigue íntegro en VWCE (óptimo fiscal/capital) mientras el bloque congelado compite con dinero ya comprometido.

**Importe**: 0 €.

**Resultado esperado**: WF2 en vivo desde octubre (JNJ 13-oct, VZ 26-oct — esclarecer congelación de dividendo —, MO 29-oct — payout al borde del trigger). Evaluación anual del árbitro cada 31-dic. Veredicto vinculante 31-dic-2028.

**Revisión**: (pendiente) primeros ciclos WF2 de octubre; baseline del árbitro invariante (no re-baselinear jamás salvo error de dato).

---

## 2026-09-30 (tarde) — REVISIÓN DE LA C: congelación por dilución en vez de venta + re-verificación de las 5

**Contexto**: El inversor rechaza vender VHYL ("me comen los impuestos") y pide mejora de lo existente, no rediseño: "ya no invierta más y veo cómo evoluciona". Paralelamente llega la re-verificación web de VZ/O/JNJ/XOM/MO (datos 29-sep, mercado abierto).

**Decisión**: **C por DILUCIÓN** (sustituye la C por venta del mismo día):
1. **Congelados**: VHYL (~40 k) + VZ/O/JNJ/XOM/MO (~24,5 k) — ni compras ni ventas jamás; se diluyen con el flujo nuevo. Fricción asumida ~500 €/año = prima por no decidir hoy (vs ~1.240 € de IRPF único que se evita; equilibrio ~2,5-3,5 años; más allá, la congelación es más cara en expectativa — aceptado a cambio de la opción de decidir con datos).
2. **Se vende igual**: Deka dic-2026 (decisión previa) + polvo ene-2027 (AVGO/GOOG/T/KO/ENG: +233 € netos, las minusvalías de T/ENG/AVGO −320 € compensan plusvalías 2026 → fiscalmente ~positivo).
3. **Todo el dinero nuevo → VWCE** (Deka, aportaciones mensuales).
4. **Test 31-dic-2028** (redefine el A9): bloque congelado completo (VHYL + 5) vs VWCE desde el 30-sep-2026. Por debajo → vender con datos; igual/mejor → se queda. Barra de mantenimiento mientras tanto: corte de dividendo o payout fwd >90 % sostenido → venta puntual de ese nombre.
5. Dilución esperada de VHYL: 35,5 % → ~27 % (dic, con Deka) → ~22 % (fin-2027 con 36 k/año) → 16-19 % (2029). Con aportaciones bajas (18 k/año): más lenta.

**Re-verificación de las 5 (agente web, 29-sep)**:

| Ticker | Payout fwd | Múltiplo | Yield | Veredicto barra mantener | Novedad |
|---|---:|---:|---:|---|---|
| VZ | ~56 % | 9,2× fwd | 6,08 % | ✅ (WATCH) | ⚠️ **9-sep: dividendo CONGELADO ($0,7075 sin subida, rompe 19 años)** — contradicta por research previo (decía +2 %); sin impacto en plan (congelado igualmente), a esclarecer con Q3 26-oct |
| O | ~73 % AFFO | **12,4× AFFO** | 5,88 % | ✅ | Subida mensual nº136 (8-sep); ex-div 30-sep CAPTURADO; precio en mínimos 52 sem (downgrade Scotiabank) — precio, no dividendo |
| JNJ | ~49 % fwd | 24,2× fwd | 2,02 % | ✅ | Sin novedad; Q3 13-oct confirmado |
| XOM | ~33 % fwd | 12,8× fwd | 2,56 % | ✅ | Declaración anual ~fines oct (subida esperable) |
| MO | ~78-80 % fwd (GAAP trail ~93,5 %) | 12,0× fwd | 6,46 % | ✅ con vigilancia | **El más cercano al trigger**: payout GAAP >90 % crónico + equity negativa; Q3 29-oct decide |

Cambio real desde el 22-sep: ninguno negativo de dividendo. Los dos hechos de tesis (congelación VZ 9-sep, subida MO 27-ago) son previos a la ventana.

**Importe**: 0 € hoy. Plan: Deka dic (~1.980 € o menos con step-up) + polvo ene (~45 €, compensa 2026). Se evita la venta de enero (~1.240 €).

**Resultado esperado**: Cartera a 7 líneas IBKR en enero (VWCE, VHYL, 5 acciones, IBTS) + Deka fuera. Mantenimiento: comprar VWCE y vigilar la barra de mantenimiento de los congelados (cortes/payout). Test 2028 con datos.

**Revisión**: (pendiente) VZ Q3 26-oct (esclarecer congelación) · MO Q3 29-oct (payout GAAP) · JNJ 13-oct · XOM fines-oct · ejecutar Deka dic + polvo ene · sleeve_test.py adaptado al bloque congelado.

---

## 2026-09-30 — Auditoría externa de la C: aceptada con 2 acciones + 1 error corregido

**Contexto**: El inversor aporta crítica externa de la estructura C (96 % RV, sleeve concentra, fricción fiscal, USD ~65-70 %, variante VHYL-en-lugar-de-nombres).

**Decisión**: (1) **Confirmada C-nombres** (vs variante C-ETF con VHYL al 12 %): el test A9-2028 solo es experimento limpio con nombres propios y el engagement ha demostrado valor; la variante queda documentada como alternativa legítima (transición ~870 € vs 1.290 €) si algún día se prefiere mínimo mantenimiento. (2) La decisión ~96 % RV queda **documentada como deliberada** en STRATEGY §Riesgos (estabilización vive fuera: 70 k€ liquidez + glidepath 2032). (3) **Error corregido: IBTS es la versión USD Treasury 1-3y sin cubrir** (el target.csv lo describía como EUR Govt — el propio display IBKR del 28-sep lo etiquetaba "ISHARES USD TRSRY 1-3Y"). USD efectivo total ~68-70 %. Decisión USD vs deuda-euro diferida al glidepath (nota: en risk-off el colchón USD sube en euros — convexo).

**Razón**: La crítica confirma mayoritariamente nuestro propio diagnóstico (sleeve = overweight no diversificación; dividendos ≠ alfa; fricción fiscal conocida). Sus dos aportaciones accionables: la etiqueta IBTS errónea y la explicitación de la decisión 96 % RV.

**Importe**: 0 €.

**Resultado esperado**: Sistema con la C auditada dos veces (interna + externa). Re-verificación web del sleeve sigue en curso.

**Revisión**: (pendiente) agente de verificación; ejecución dic/ene sin cambios.

---

## 2026-09-29/30 — DECISIÓN: ESTRUCTURA C ELEGIDA + plan de ejecución dic/ene

**Contexto**: Tras el análisis A/B/C y la re-auditoría no circular (portfolio = "índice + apuesta activa del 46 % sin alfa demostrada"), el inversor elige la opción C. Yahoo sigue rate-limited (IP) → re-verificación del sleeve en curso vía research web fresca (agente).

**Decisión**: **Opción C** — VWCE ~84 % + IBTS ~4 % + sleeve 12 % solo-mantenimiento (VZ 3 · O 3 · JNJ 2,5 · XOM 2 · MO 1,5). El sleeve NO recibe dinero nuevo nunca; aportes 100 % a VWCE (cascada A8). Salida pre-registrada: **A9** (XIRR sleeve vs VWCE a 31-dic-2028 → disolver si va por debajo).

**Plan de ejecución** (para no apilar plusvalías en el ejercicio 2026):
1. **Dic-2026**: vender Deka (33.039 €) → SEPA → IBKR → VWCE. Plusvalía +10.010 € → IRPF ~1.980 € *o menos si aplica valor-de-adquisición-a-fecha-de-residencia (ASESOR)*. Antes: parar Sparplan si existe.
2. **Ene-2027 — transición C** (cálculo a precios 28-sep, fx 0,8803):
   - Ventas completas: **VHYL (39.844 €) · AVGO · GOOG · T · KO · ENG** = 46.965 € (ganancia +5.943 €)
   - Recortes a 12 %: O −3.417 · JNJ −2.156 · MO −1.171 · VZ −1.227 · XOM −1.037 = 9.008 € (ganancia ~+756 €, aprox. coste medio; FIFO real algo mayor en JNJ)
   - **Total: 55.972 € → VWCE · plusvalía ~6.700 € · IRPF ~1.290 €** (estatal ref; foral VERIFICAR)
3. Estado final IBKR: VWCE 94.120 (84 %) + sleeve 13.457 (12 %) + IBTS 4.007 (3,6 %). **Con Deka dentro: total ~145.200 € — VWCE 87,6 % · sleeve 9,3 % · IBTS 2,8 %** (sleeve por debajo del cap 12 %: correcto, es máximo).

**Aplicado en docs**: target.csv v2 (7 líneas), ESTRUCTURA-DECISION marcada ELEGIDA, RULES v1.3 (changelog + A9 activado), changelog registra que bandas absolutas/V1-A4 informativas siguen pendientes de aprobación.

**Importe**: 0 € ejecutados hoy. Coste total de transición estimado: **~2.270-3.270 €** (1.290 C + 600-1.980 Deka según step-up), recuperable en ~4-5 años vía drag fiscal + TER ahorrados.

**Resultado esperado**: Cartera coherente con premisas nuevas; drag fiscal ~580 → ~130 €/año; 5 entidades → 4; test A9 decide en 2028 si el sleeve sobrevive.

**Revisión**: (pendiente) (1) resultado de la re-verificación web del sleeve (agente en curso) — confirmar barra de mantenimiento en VZ/O/JNJ/XOM/MO; (2) MO Q3 29-oct (payout <90 % = barra mantener); (3) ejecutar dic/ene y loguear fills; (4) sleeve_test.py en Q4.

---

## 2026-09-29 (noche 2) — DECISIÓN EN PRINCIPIO: liquidar Deka y llevar a IBKR

**Contexto**: El usuario decide vender todo el depot Deka/SkkM (33.039 €, plusvalía +10.010 €) y transferir a IBKR, donde el destino es VWCE bajo cualquier estructura A/B/C.

**Decisión**: En principio, sí — ejecución condicionada a: (1) **VERIFICAR CON ASESOR el "valor de adquisición al día de inicio de residencia española"** (si el depot valía p. ej. ~30 k€ ese día, la ganancia tributable baja de ~10 k a ~3 k € → IRPF de ~1.980 a ~600 €; podría justificar esperar unas semanas); (2) parar cualquier Sparplan activo ANTES de vender; (3) no apilar con la transición C en el mismo ejercicio (Deka dic-2026 / transición ene-2027, o partir Deka); (4) reservar el IRPF (~600-2.000 €) para Renta 2027 — Alemania no retiene.

**Razón**: El Deka no encaja en ninguna estructura futura; TER ~1,5-2 % vs VWCE 0,20 % = ~450-600 €/año de coste puro; payback de la consolidación ~4 años (menos si aplica el step-up fiscal).

**Importe**: 33.039 € brutos a liquidar; IRPF estimado 600-1.980 € según punto (1).

**Resultado esperado**: IBKR recibe ~33 k → VWCE (fraccionable 1-3 meses). Cartera resultante pre-transición: VWCE ~69 k (~48 % del sleeve IBKR) — adelanta el estado final de la estructura C. Estructura total simplificada: fuera una entidad, fuera un CRS report.

**Revisión**: (pendiente) fecha inicio residencia ES + valor depot ese día (asesor); estado Sparplan; ejecutar y loguear fills.

---

## 2026-09-29 (noche) — Mapa cerrado casi del todo: Deka/SkkM 33.039 € (+43,5 %)

**Contexto**: El bloque alemán identificado: depot DekaBank en Stadtsparkasse München — fondos activos del grupo Deka. Kurswert 33.039,43 € · Kaufwert 23.029,55 € · **plusvalía latente +10.009,88 € (+43,47 %)** · YTD-26 +7,16 % · "sin perdedores". Posiciones concretas y existencia de Sparplan activo: pendientes. Patrimonio total recalculado: **~215.400 €** (IBKR 112,4 k + TR 40 k remunerada + Deka 33 k + BBVA 24 k + Revolut 6 k).

**Decisión**: Ninguna aún sobre el Deka (documentado). Análisis de opciones preparado para cuando lleguen las posiciones: (a) consolidar a IBKR/VWCE — coste ~1.900–2.100 € de IRPF, ahorro de ~450–600 €/año en comisiones (fondos Deka típicamente 1,5–2 % TER vs VWCE 0,20 %), payback ~4 años; (b) mantener sin aportar más. Cualquier Sparplan mensual activo → redirigir al plan (A8).

**Razón**: La banca alemana de ahorro vende fondos propios con comisiones altas; el +43,5 % habla de bolsa global alcista mantenida, no de gestión habilidosa. La cuenta es visible para Hacienda vía CRS.

**Importe**: 0 €.

**Resultado esperado**: Con las posiciones (Wertpapierübersicht) y el estado del Sparplan, decisión consolidar/mantener con números reales. Mientras: no añadir un euro más al Deka.

**Revisión**: (pendiente) paste de Wertpapierübersicht + Sparplanübersicht.

---

## 2026-09-29 (tarde) — Mapa patrimonial completo: ~212 k€ en 5 entidades

**Contexto**: El inversor revela el ahorro externo: Trade Republic 40 k€ (invertido) + banco alemán 30 k€ (invertido) + BBVA 24 k€ + Revolut 6 k€ = **~100 k€ externos**, además del "70 k€" mencionado antes (probablemente TR+alemán; pendiente confirmar). Patrimonio total ~212.400 € — la cartera IBKR gestionada hasta ahora era solo el 53 %. También confirma: P3 resuelto (fondo emergencia cubierto con holgura), P4 presentará la informativa en 2027 (ejercicio 2026; pendiente ver con asesor ejercicios 2024-25), P1 re-formulado (gasto variable por posible compra de casa).

**Decisión**: Actualización de documentos (sin trades): PROFILE (mapa patrimonial 5 entidades) y PLAN-RETIRADA (§1-bis vivienda con 3 escenarios y regla de casamiento hipoteca-retirada; §3-b proyección patrimonio completo). Nueva lectura: al 5 % real con todo invertido, objetivo (720-831 k€) en ~2035; al 3 %, ~2038 en todos los escenarios.

**Razón**: Las aportaciones (36 k€/año) dominan el resultado; el patrimonio completo adelanta la libertad 2-3 años. Los externos en cash al 0 % real cuestan ~55 k€ de capital a 2035.

**Importe**: 0 € movidos.

**Resultado esperado**: (1) Saber en qué están los 40 k de TR y 30 k del banco alemán (¿ETFs? ¿fondos? ¿caución?) y qué parte de BBVA/Revolut es liquidez — determina coherencia con la estrategia, coste fiscal de consolidar y reparto emergencia/casa. (2) Fiscal: rendimientos de cuentas alemanas declarables anualmente en Renta (¿se declaran?); 720: IBKR declara (>50 k); TR/alemán/Revolut individualmente <50 k (VERIFICAR criterios con asesor). (3) La decisión de estructura A/B/C sigue pendiente — el argumento C (diversificar riesgo tech) se refuerza a nivel patrimonio total si los externos acaban en VWCE.

**Revisión**: (pendiente) respuestas sobre composición de TR/alemán/BBVA/Revolut y elección A/B/C.

---

## 2026-09-29 — CAMBIO DE PREMISAS: retorno total + decisión de estructura pendiente

**Contexto**: Tras la auditoría externa del 29-sep (7 puntos), el inversor cambia las premisas del sistema: (1) vender activos para financiar gasto pasa a ser legítimo según plan; (2) fuera las restricciones "nunca vender" y "solo dividendos"; (3) fuera el objetivo "vacaciones con dividendos"; (4) destino por defecto de aportes: VWCE. Matiz aceptado: **cero retiradas durante la acumulación** — las ventas solo según PLAN-RETIRADA desde el año objetivo [P2].

**Decisión** (aplicada en docs, sin trades):
1. **PLAN-RETIRADA.md** (nuevo): objetivo por retorno total, SWR 3,25/3,5/3,75 % → capital objetivo **720–831 k€ reales** (gasto supuesto 27.000 €/año, P1 pendiente), glidepath IBTS 5 años antes de [2032 supuesto], colchón 1,5 años, orden: dividendos → VWCE mensual → colchón en años malos, FIFO/lote de mayor coste, reparto de plusvalías por tramos, escala foral Bizkaia VERIFICAR CON ASESOR. Tipo efectivo de retirada hoy: ~2,6 % (solo plusvalía) vs ~21 % dividendo.
2. **ESTRUCTURA-DECISION-2026-09-29.md** (nuevo): A (VWCE+IBTS; transición ~1.520 € IRPF, drag 0) vs B (actual; 0 € transición, drag ~580 €/año) vs **C recomendada (VWCE+IBTS+sleeve 12 % con VZ/O/JNJ/XOM/MO; transición ~1.130 €, drag ~130 €/año, payback 2,5 años, diversifica riesgo laboral tech)**. Elección PENDIENTE del inversor.
3. **STRATEGY.md v2**: principios reescritos (retorno total, cero retiradas en acumulación, cascada VWCE, guardrails), rutina mensual v2 (cascada), nueva sección Riesgos estructurales (fondo emergencia P3, cluster de tipos O/VZ/ENG/T, correlación carrera tech), frases ancla actualizadas.
4. **PROFILE.md v2**: objetivo único retorno total; objetivo vacaciones retirado; proyección en reales 3/5/7 %; P1-P4 pendientes listados.
5. **RULES.md v1.2**: changelog añadido, circuit breaker reescrito (guardrails), A6 reformulada (VHYL ya no intocable), A8 cascada (VWCE por defecto), alcance del sleeve pendiente de estructura. Paquete v1.2 adicional (bandas absolutas, A9, V1/A4 informativas, T/MO targets) SUSPENDIDO hasta elegir estructura.

**Razón**: El marco "solo dividendos" era fiscalmente ineficiente (drag ~0,5 %/año vs VWCE acumulativo), dependía de un yield del 4 % inexistente a precios de mercado (~2,2 % real) y creaba fricciones de gobernanza. El retorno total alinea objetivo, fiscalidad y simplicidad. La diversificación del riesgo laboral (sueldo tech) es el argumento para no ir a la opción A pura.

**Importe**: 0 € (solo documentos). Trades: ninguno. Próximo aporte (pendiente fecha): a VWCE por defecto.

**Resultado esperado**: Sistema coherente con el nuevo objetivo; decisión de estructura cierra la composición (si C: vender VHYL + ~16 k€ sleeve en diciembre, IRPF ~1.130 €, target.csv v2). PLAN-RETIRADA da la métrica de éxito (capital real vs 720–831 k€) y los guardrails conductuales.

**Revisión**: (pendiente). (1) Elegir A/B/C. (2) P1 gasto / P2 año / P3 emergencia / P4 720-foral. (3) Si C: ejecutar transición diciembre y regenerar target.csv. (4) Asesor foral Bizkaia. (5) sleeve_test.py para A9 2028.

---

## 2026-09-28 (tarde) — Tanda 1+1b EJECUTADA: +121 acciones por ~6.106 €

**Contexto**: Apertura NYSE 15:30 CET. Órdenes Market/Day modificadas a cantidades combinadas. Fills limpios a mejores precios que las referencias (VZ 46,86 $ vs 47,30 ref). FX real de conversión 1,136 (IDEALPRO, 5.523,75 € → 6.275,20 $; USD cash 660,82 agotado; cash final 560,36 €).

**Decisión** (ejecución del Módulo 1 del REBALANCEO):

| Ticker | Fill | Precio | Importe | Posición resultante |
|---|---:|---:|---:|---|
| O | +38 | 55,70 $ | 2.116,60 $ | 138,7344 sh @ 58,32 $ |
| VZ | +75 (2 fills: 20+55) | 46,86 $ | 3.514,50 $ | 111,7295 sh @ 46,22 $ |
| XOM | +8 | 162,74 $ | 1.301,92 $ | 22.8889 sh @ 157,54 $ |
| **Total** | **121** | | **6.933,02 $ + 3 $ fees** | |

**Desviación vs plan**: VZ 75 en vez de 86 (−11 sh, ~453 € no desplegados) → cash final 560,36 € en vez de ~85 €. Las 11 acciones pasan al tramo final.

**Razón**: Módulo 1 conforme — compras limpias (VZ/O/XOM), gap + banda + dividendos (ex-div O 30-sep CUBIERTO comprando el 28).

**Importe**: ~6.106 € desplegados (2º día consecutivo con ingreso de 3.000 €; total ingresado 6.000 € en 3 días).

**Resultado esperado**:
- Pesos: **O 6,06 % (target 7,5) → banda VERDE por primera vez**; VZ 4,10 % (−36,9 % rel, era −77,5 %); XOM 2,93 % (−41,4 %); sleeve ETF 69,5 % (target 67); stocks 26,4 % (era 21,6 %).
- Dividendos esperados: O ~28 € netos (15-oct), VZ ~59 € netos (2-nov), XOM ~18 € (dic) → forward anual ~2.430-2.530 € netos (+~280 vs antes de la tanda).
- Restante del plan: VZ +32, XOM +10, AVGO +2 ≈ **3.360 €** vs cash 560,36 € → próximo ingreso lo cierra.

**Revisión**: (pendiente). (1) Verificar pago O 15-oct sobre 138,7344 sh. (2) Activity Statement Q3-Q4: confirmar fees 3 $ y conversión 5.523,75 €. (3) El residual NLV ~0,1-0,4 % entre display y marks sigue presente — cerrar con AS. (4) Próximo ingreso → tanda final VZ/XOM/AVGO y rebalanceo Módulo 1 COMPLETO.

---

## 2026-09-28 — Enmiendas RULES v1.1 (V2-bis + A7 + Vías de salida) + 2º ingreso 3.000 € + tanda 1 a mercado

**Contexto**: Mandato de eliminar las 2 fricciones documentadas el 22-sep sin cambiar filosofía ("las normas están bien"). Además: la addenda del REBALANCEO decía "lunes 29-sep" por error de etiqueta — el lunes era 28-sep (corregido). Día a día: 26-sep ingreso 1º de 3.000 € + órdenes tanda 1 colocadas como Limit; 28-sep 07:35 ET las 3 órdenes modificadas a **Market/Day** (PreSubmitted, esperando apertura NYSE 15:30 CET) e **ingreso 2º de 3.000 €** (cash 6.664,95 €, NLV 112.568,09, fx implícito ~0,879 / EURUSD 1,1378).

**Decisión**:
1. **Enmienda A — RULES.md V2-bis (ámbito del DDM)**: Gordon solo para Yield+Value estable (O, VZ, MO, T, ENG, KO, JNJ); AVGO y cíclicas (XOM) se valoran por V4/A5 (P/E ≤30×/≤15×). Desbloquea XOM (queda conforme) y AVGO <30× (actualmente 29,3×).
2. **Enmienda B — RULES.md A7 (targets duales) + columna `status` en target.csv**: activo/mantener/intocable/cuarentena con unlocks anotados. `/analyze` pasa a mostrar gap ejecutable vs gap total. Actualizado prompts/analyze-portfolio.md §1.6.
3. **Enmienda C — RULES.md sección "Vías de salida"**: 4 triggers explícitos de venta (grado D/payout>90 %, corte confirmado, ruptura de tesis documentada, horizonte 8-10 años ETFs). El resto se corrige por compras.
4. Fix menor score.py: filas `#` de target.csv ya no generan entradas basura.
5. Ejecución: tanda 1 (O+20 / VZ+49 / XOM+4, IDs 459863132/134/136) a mercado en la apertura. Con el 2º ingreso, tras rellenar quedan ~3.050 € → **tanda 1b** inmediata: VZ+37, O+18, XOM+4 (~2.980 €). AVGO queda para el próximo ingreso.

**Razón**: dos de los cinco vetos eran artefactos del modelo Gordon fuera de su ámbito; las cuarentenas reales se mantienen como semáforo de reentrada. El sleeve ejecutable pasa de ~28,5 % a ~30-31 % al entrar AVGO. El "no vender" pasa de prohibición implícita a regla con 4 puertas.

**Importe**: 3.000 € ingresados (2º). Docs: RULES.md ×3 secciones, target.csv, prompts/analyze-portfolio.md, score.py.

**Resultado esperado**: Tras tanda 1+1b (~6.560 €): VZ ~5,3 %, O ~6,1 %, XOM ~2,9 % → resto del gap (VZ +21, XOM +10, AVGO +2.9k) con el próximo ingreso. Fricciones 1 y 2 eliminadas del sistema.

**Revisión**: (pendiente). Al llegar los fills de hoy: actualizar holdings.csv, calcular avg costs nuevos, verificar captura ex-div O (30-sep). En el próximo /analyze: comprobar que el gap dual se muestra y que score.py no emite WARN por filas #.

---

## 2026-09-26 — Ingreso 3.000 € + tanda 1 del rebalanceo (propuesta, pendiente ejecución)

**Contexto**: Usuario ingresa 3.000 € (cash 3.664,24 €, NLV 109.685,53, fx implícito 0,88843). Precios del día: VZ 47,13 $ · O 55,70 $ · XOM 160,60 $ · AVGO 353,70 $. Nota: archivos previos de la sesión etiquetados 09-22 por error de fecha; hoy 26-sep quedan los `coverage/*-2026-09-26.json` como vigentes.

**Decisión**: Tanda 1 escalada al cash disponible (REBALANCEO addenda): **O +20 · VZ +49 · XOM +4 ≈ 3.618 €**, ejecución lunes 29-sep (captura ex-div O ~1-oct y record VZ 9-oct). Tanda 2 pendiente de próximo ingreso (~5.317 €): VZ +58, O +18, XOM +14, opcional AVGO +1-2 (353,70 $ = 29,3× forward, ya bajo el techo de 30× de A5/V4).

**Razón**: Módulo 1 del rebalanceo conforme — solo compras limpias (VZ/O/XOM), prioridad por gap (VZ −77 %) + pilar mensual (O) + Carlson (XOM). AVGO desbloqueado por precio sin tocar reglas.

**Importe**: 3.000 € ingresados; 3.618 € de compras propuestos (0 ejecutados aún).

**Resultado esperado**: Tras tanda 1: O 5,3 % · VZ 3,2 % · XOM 2,4 % · ETFs ~68,9 % · cash ~46 €. Tras tanda 2: VZ 5,3 % · O 6,1 % · XOM 4,0 % (bandas verdes), dividendo forward ~2.150-2.250 €/año netos.

**Revisión**: (pendiente). Tras ejecutar: actualizar holdings.csv (qty/avg/cash), loguear fills reales, y confirmar captura de ex-div de octubre.

---

## 2026-09-22 (tarde) — Corrección de divisa del snapshot + plan de rebalanceo total conforme

**Contexto**: Al diseñar el rebalanceo solicitado ("todo debe cumplir las normas, reglas como están") se detectó un error en el parseo matinal del snapshot IBKR: las columnas Last/Market Value de las 9 posiciones USA están en **USD nativo**, no en EUR. Con fx implícito 0,89117 (EURUSD 1,1221), Σ(MV)+cash cuadra al céntimo con el NLV 106.788,91 € — el gap "−2.599 € inexplicado" era este error (el −2.499 € del 26-jun tiene la misma firma y queda explicado provisionalmente).

**Decisión**:
1. Datos corregidos: `coverage/prices-2026-09-22.json` (price_eur = nativo × 0,89117), `snapshot-2026-09-22.json` (reconciliación RESUELTA), `analysis-2026-09-22.json` re-ejecutado (pnl_pct replica exactamente IBKR: O −4,0 %, JNJ +44,0 %…), `holdings.csv` avg_cost_eur de los 9 USD re-expresados (O 52,84; JNJ 165,95; MO 51,22; XOM 137,85; KO 63,81; VZ 39,99; AVGO 347,83; GOOG 227,38; T 25,10). Pendiente: coste EUR real por lote desde trades.csv (fiscalidad).
2. **Rebalanceo total conforme** diseñado en `REBALANCEO-2026-09-22.md`: Módulo 1 compras VZ+70 / O+20 / XOM+18 (oct, ~6.538 €) + VZ+37 / O+18 (nov, ~2.483 €) = 163 acciones ~9.021 €. Módulo 2: **IBTS target formalizado 3,5 %** (target.csv + STRATEGY.md actualizados; banda verde sin trades). Módulo 3: revisiones A1 documentadas para las 7 cuarentenas (T, AVGO, MO, GOOG, JNJ, ENG, escala VHYL).
3. STRATEGY.md: resumen visual corregido (tabla cruda suma ~1,14 → ETFs 67 % crudo/59 % norm, acciones 46 %/40 %; el "≈33 %" era inconsistente con la propia tabla).

**Razón**: Las reglas están bien y se mantienen sin cambios (mandato del usuario). Un rebalanceo con ventas no es conforme (A6 + TAX-ES + ningún grado D): el único camino es compras + decisiones documentadas. Únicas compras limpias hoy: VZ, O, XOM (9.021 € cierran sus gaps a banda verde).

**Importe**: 0 € ejecutados (plan pendiente de ejecución por el usuario en IBKR). Docs: target.csv, STRATEGY.md, 3 informes.

**Resultado esperado**: Tras Módulos 1-2: VZ 5,3 % / O 6,1 % / XOM 4,0 % (banda verde), ETFs 67,6 %, stocks 28,5 %, IBTS en banda, dividendo forward ~2.150-2.250 €/año netos. Sin plusvalías realizadas. Sleeve stocks queda a 28,5 % (no 33 %) mientras las cuarentenas persistan — decisión consciente con reglas intactas.

**Revisión**: (pendiente). Tras ejecutar octubre y noviembre: actualizar holdings, loguear tandas, y verificar que MO (29-oct) / AVGO (<$350) no se desbloquean sin registrar.

---

## 2026-09-22 — Análisis trimestral (cartera + sistema). Sin movimientos de capital

**Contexto**: Primer análisis desde el 26-jun. Snapshot IBKR pegado en vivo (NLV 106.788,91 €, cash 660,80 €, unrealized +12.457 €). Cantidades idénticas a junio: **cero trades y cero depósitos en 88 días**. Yahoo Finance rate-limited todo el día → fundamentals vía research web.

**Decisión**: Sin compras/ventas. Solo diagnóstico + propuesta de plan de catch-up (ver `ANALYSIS-2026-09-22.md`).

**Razón**: Mantener disciplina — nada rompe la Capa 1 (ninguna posición en D, ningún corte de dividendo). El problema detectado es de **ejecución**, no de tesis: rutina mensual parada 3 meses (~9 k€ sin desplegar ≈ ~525-630 €/año de dividendo futuro no creado) y 8 bandas Vanguard rojas a la baja + IBTS +628 % al alza.

**Importe**: N/A. Datos actualizados: `holdings.csv` (CASH → 660,80), `coverage/{prices,snapshot,analysis,scores}-2026-09-22.json`.

**Resultado esperado**:
- Catch-up octubre ~12.700 €: VZ + O + XOM primero (gaps −75 %/−30 %/−57 %, todos Safety A, DDM/Graham favorables salvo XOM por limitación del modelo en cíclicas).
- Meta dividendos 2026 (~2.300 €) NO se alcanzará: proyección ~1.700-1.750 € netos (YTD 1.255 €). Run-rate forward ~1.800-1.900 €; con gap cerrado → ~2.650-2.700 € en 2027.
- Vigilancias: MO (WATCH: contracción cigarrillo, payout 78 %, revisar 29-oct), ENG (WATCH: suelo 1 € solo hasta dic-2026, CNMC pendiente), AVGO (solo comprar en debilidad, P/E al límite 30×), T (dividendo congelado desde 2022 → **conflicto con regla S2/A3**, decidir exclusión o enmienda).
- Señal V3: VHYL 2,43 % < 3,5 % → mercado caro (moot para ETFs, refuerza disciplina Graham en acciones).

**Revisión**: (pendiente). Cuando se ejecute el catch-up de octubre y llegue el Activity Statement Q3: (1) verificar las 3 reconciliaciones abiertas — gap NLV −2.599 € (recurrente, era −2.499 € en jun), header vs columna unrealized −322 €, "Dividends 350,83" periodo desconocido; (2) rellenar las Revisiones de las 4 entradas anteriores; (3) decidir IBTS (formalizar target ~3,5 % o recortar ~3.100 € con minusvalía compensable).

---

## 2026-06-26 — Deploy €3.357 cash → ENG + O (VZ rechazado por IBKR)

**Contexto**: Tras limpieza de las 9 microposiciones (entrada anterior), cash disponible en IBKR: 3.357,24 €. Mercados EU+US abiertos, ventana óptima 16:00 CET. Ex-div O 30-jun (4 días), ex-div ENG 30-jun (4 días), ex-div VZ 10-jul (14 días). Captura de dividendos activa.

**Decisión**: Deploy priorizando Carlson BSD top ranks (ENG #2, VZ #3, O #4) + Capa 2 valuation (P/E ≤15 para todos):

| Ticker | Plan | Real | Precio exec | EUR spent |
|---|---|---|---|---:|
| ENG | +67 shares | **+141 shares** | 17,6848 € (Mkt) | 2.493,55 € |
| O | +17 shares | **+15,27 shares** | ~62,93 € | 960,91 € |
| VZ | +29 shares | **0** (rechazado IBKR) | — | 0 € |
| **TOTAL** | | | | **3.454,46 €** |

**Razón del override ENG vs O**:
- IBKR rechazó orden VZ 26 shares con "insufficient settled cash [-1.042,50 EUR for 20260629]". Causa probable: cash de ventas de micros no settlado (T+2 = 29-jun) + orden O ya working reservando cash.
- En lugar de pelear con IBKR, se priorizó **ENG** (EUR nativo, sin FX complication, top BSD rank #2, mayor yield 6,8 %).
- Resultado: se compraron **141 shares de ENG** (2,1× el plan original) a precio de mercado 17,6848 € (según transaction history IBKR).
- O se llenó por debajo del plan (15 vs 17) por constraint de cash.

**Importe (cifras IBKR autoritativas 19:00 CET)**:
- NLV antes: 103.204,33 € → NLV después: **103.652,33 €** (△ +448 € por mercado)
- Cash antes: 3.357,24 € → **Cash después: 16,47 €** (EUR 0,00 + USD 18,80)
- Deploy teórico: 3.454,46 € vs cash consumido: 3.340,77 € → **gap ~114 €** probable por FX snapshot (USD→EUR) y comisiones (~4,50 €), sin cuadra exacta posible hasta Activity Statement Q3.
- Realizado hoy: +268,45 € (micros limpieza, cuadra con cálculo)

**Cambios en posiciones**:
- O: 85,4637 → **100,7344 shares** (avg cost 58,66 → **59,30 €**)
- ENG: 15,2297 → **156,2297 shares** (avg cost 13,53 → **17,28 €**) — cuadra con IBKR display 17,32 (diff 0,04 por redondeo lot-level)
- VZ: sin cambios (orden rechazada)

**Resultado esperado**:
- Dividendos capturados próximos 30 días:
  - O: 100,7344 × $0,271 = $27,30 brutos → 30 % WH → **$19,11 net = ~16,75 €**
  - ENG: 156,2297 × 0,60 € = 93,74 € brutos → 19 % WH → **75,93 € net**
  - **Total dividendos netos próximos: ~92,68 €** (vs 50,70 € del plan original, casi el doble)
- Sleeve stocks: 22,25 % → **25,58 %** (△ +3,33 pp), target 33 %, gap residual ~7,4 pp
- ENG: 0,26 % → 2,66 % (target 3,5 %) → gap casi cerrado
- O: 5,17 % → 6,11 % (target 7,5 %) → mejora pero todavía bajo
- VZ: 1,64 % → 1,63 % (target 6,5 %) → **gap sin cerrar, prioritario para julio**

**Otros cambios hechos en esta sesión**:
- holdings.csv: qty y avg_cost_eur actualizados para O y ENG. CASH: 3.357 → 16,47 €.
- PROFILE.md: línea "Efectivo pendiente ~30k" eliminada (era stale desde mayo).
- 9 tickers USD con avg_cost_eur corregidos (ratio ×1,13433) — O, JNJ, MO, XOM, KO, VZ, AVGO, GOOG, T.

**Revisión**: (pendiente). Próximas verificaciones cuando llegue Activity Statement Q3:
1. Realized P&L hoy = 268,45 € → cuadra con IRPF 2026 base ahorro.
2. NLV reconciliation gap: suma posiciones + cash (106.151 €) vs NLV reportado (103.652 €) = **−2.499 € sin explicar**. Usuario confirma que no hay más datos disponibles hoy. Pendiente Activity Statement Q3 para cerrar.
3. Cash deploy gap: ~114 € sin cuadrar entre teórico (3.454,46 €) y consumido (3.340,77 €). Probable FX + comisiones, sin confirmar hasta Q3.

---

## 2026-06-26 — Venta de las 9 microposiciones (limpieza STRATEGY.md) — CIERRE COMPLETO

**Contexto**: STRATEGY.md §"Plan de acción con los 30.000 €" llevaba desde mayo-2026 listando 9 microposiciones a limpiar: RTX, PNC, TXN, AMGN, NOC, LMT, MVUS, IHYG, FGQI. Hoy 26-jun-2026 se ejecutan las 9 en dos bloques (7 + 2) vía IBKR Market orders "Close Position" en horario óptimo (15:27–15:35 CET, solapando US open + EU close). Mercado US y EU abiertos, sin circuit-breaker macro (Housel OK).

**Decisión**: 9 Market orders en IBKR, settlement T+2:

| Ticker | Qty | Precio exec | Ccy | Realized P&L (IBKR) |
|---|---:|---:|---|---:|
| LMT | 0,2141 | 508,64 | USD | +7,81 |
| AMGN | 0,3205 | 355,19 | USD | +12,90 |
| FGQI | 33,0000 | 11,16 | EUR | +73,30 |
| TXN | 0,4955 | 302,40 | USD | +48,30 |
| RTX | 0,9803 | 187,28 | USD | +82,60 |
| IHYG | 7,0164 | 90,95 | EUR | −20,40 |
| MVUS | 15,7413 | 97,49 | EUR | +54,00 |
| PNC | 0,6138 | 244,14 | USD | +48,90 |
| NOC | 0,2291 | 502,64 | USD | +14,20 |
| **TOTAL** | | | | **+321,61** |

IBKR "Realized P&L" YTD display: **+268,29 €** (la diferencia ~€53 con la suma anterior se debe a FIFO lot matching y/o tramos vendidos previamente en 2026; la cifra final para IRPF saldrá del Activity Statement Q4).

**Razón**:
- STRATEGY.md marca liquidación de microposiciones como paso 1 del plan 30k. Llevaban ~2 meses pendientes.
- Coste de oportunidad superado: cada mes de retraso ≈ €175 de dividendos futuros perdidos a yield 7 %.
- 8 de 9 ventas son plusvalías (solo IHYG cierra con −€20).
- Impacto fiscal marginal: +€321 se suman a L/T gains YTD ~€9.099 → tramo 21 % → **+€67 de IRPF 2026** aprox.

**Importe (cifras IBKR autoritativas)**:
- NLV antes (24-jun): 103.885,61 €
- NLV después (26-jun): 103.204,33 € (△ −681 € por mercado, no por ventas)
- Cash antes: 158,53 € → **Cash después: 3.357,24 €** (EUR 2.284,93 + USD 1.224,85 ≈ €1.072 @ 1,142)
- Plusvalía realizada hoy: **+321,61 €** (IBKR sum) / +268,29 € (IBKR display YTD)
- Comisiones pagadas: 4 × $1 + €10 = **13,51 €** totales

**Otros cambios hechos en esta sesión**:
- holdings.csv: eliminadas 9 líneas, actualizada línea CASH a 3.357,24 €.
- holdings.csv: **corregidos avg_cost_eur para 9 tickers USD** (O, JNJ, MO, XOM, KO, VZ, AVGO, GOOG, T) — estaban a precio USD en vez de EUR. Ratio correcto ×1,13433 (FX EUR/USD snapshot). Ahora coincide con IBKR "Cost Basis / Qty".
- PROFILE.md: pendiente actualizar (anotado más abajo).

**Resultado esperado**:
- Cartera pasa de 22 → 13 líneas activas + cash (mucho más limpia).
- Cash disponible para deploy YA: **3.357,24 €**.
- Con aportación mensual julio 3.000 €: **~6.357 €** para deploy este mes.
- Cartera lista para re-balancear hacia target (stocks 24 % vs target 33 %).

**Revisión**: (pendiente). Cuando se ejecute el deploy de julio, completar. Verificar también que el próximo Activity Statement Q3 refleja los ~€322 de gains y los €14 de fees correctamente.

---

## 2026-06-24 — Snapshot IBKR parsed a holdings.csv
**Contexto**: Captura IBKR con cartera real (NLV €103,885.61, cash €158.53, P&L no realizado €+10,383.52, dividendos YTD €460.41). 9 microposiciones siguen vivas (RTX, TXN, PNC, NOC, AMGN, LMT, MVUS, IHYG, FGQI) sumando ~€1,500 EUR en total.
**Decisión**: Parsear portfolio.txt → holdings.csv (real, no example) + archivar raw + snapshot JSON estructurado en coverage/.
**Razón**: Disponer de datos reales para ejecutar /analyze y /rebalance sin depender del CSV de ejemplo.
**Importe**: N/A (snapshot, sin movimiento de capital).
**Resultado esperado**: holdings.csv refleja la cartera IBKR real; analyze.py calculará desviaciones vs target.csv correctamente.
**Revisión**: (a rellenar después).

---

## 2026-06-24 — Correcciones post-Activity Statement + parse transactions.csv

**Contexto**: Tras parsear el Activity Statement IBKR (2026-06-23) y el Transaction History CSV (2025-03-27 a 2026-06-12), detectados 3 errores en holdings.csv + snapshot con dividends_ytd mal (460 era accrual, no YTD real).

**Decisión**: 
1. Corregir holdings.csv: MVUS avg 83.00→94.15 (EUR native), IHYG avg 82.80→93.92 (EUR native), FGQI avg 8.97→7.89 (USD 8.974 × 0.87861).
2. Actualizar snapshot dividends_ytd 460.41→1524.59 (Activity Statement source of truth). Añadidos withholding_tax_ytd=103.23, realized_lt_ytd=9099.57, deposits_ytd=32000, sold_tickers_ytd_2026 (10 tickers).
3. Fix snapshot currency labels: MVUS USD→EUR, IHYG USD→EUR, FGQI EUR→USD (con market_value_eur recalculado).
4. Parse data/transactions.csv → data/dividends.csv (134 rows) + data/trades.csv (106 rows) + data/README.md con reconciliation status.
5. Actualizar prompts/analyze-portfolio.md Section A: 6→8 bullets para incluir withholding, realizado L/T, deposits_ytd.

**Razón**: 
- dividends_ytd correcto es crítico para IRPF 2026 (base ahorro).
- Withholding €103 deducible Anexo A (doble imposición).
- Realizado L/T €9,099 tributa a 19-21% en IRPF 2026.
- Currency labels correctos evitan distorsión en pesos por activo (MVUS +€181, IHYG +€75 vs parse anterior).
- transactions.csv parseado da trazabilidad por pago para auditoría.

**Importe**: Sin movimiento de capital. Snapshot + CSV corrections only.

**Resultado esperado**: 
- analyze.py y prompts/analyze-portfolio.md ahora muestran cifras fiscales correctas.
- NLV reconciliation: suma holdings corregida = €103,575 vs NLV reportado €103,885 (diferencia €310 = 0.3% por intraday vs close + FX marks).
- Dividends CSV (€635 YTD) no reconcilia con Activity Statement (€1,525) → ver data/README.md.

**Revisión**: Pendiente. Cuando el usuario vuelva a pegar Activity Statement Q3, verificar que realized_lt_ytd se acumula correctamente.

---

## 2026-06-25 — Parse IBKR Inception CSV (consolidado 2024-07-02 a 2026-06-23)

**Contexto**: Usuario trae el reporte PortfolioAnalyst "Inception" de IBKR (`~/Downloads/Kepa_Cantero_Inception_June_24_2026.csv`, 13,607 líneas, 24 secciones). Es la fuente más consolidada hasta la fecha: cubre toda la vida de la cuenta (desde julio 2024) e incluye secciones no disponibles en el Activity Statement ni en el Transaction History (Performance Attribution, Risk Measures vs Benchmark, Investment Themes, Value at Risk, Greeks, Cumulative Performance, Allocation timeseries, Projected Income).

**Decisión**:
1. Escribir `scripts/parse_inception.py` que lee el CSV y produce:
   - `coverage/inception-2026-06-24.json` — master JSON con todas las secciones excepto el detalle lot-level de Concentration (12k líneas, no vale la pena).
   - 8 CSVs en `data/`: deposits-withdrawals.csv (21 filas), dividends-inception.csv (207 filas — toda la vida), corporate-actions.csv (2: AVGO split + CMCSA spinoff), interest.csv (4), trade-summary.csv (33), performance-by-symbol.csv (38 — con realized y unrealized P&L), projected-income.csv (23), investment-themes.csv (492).
2. Actualizar `coverage/snapshot-2026-06-24.json` con nueva sección `inception_2026_06_23` que consolida Key Statistics, Risk Measures, Benchmark vs VDHG (correlation 0.59, beta 0.59, alpha 0.37%, Sharpe 0.66 vs VDHG 1.05), monthly/quarterly returns, deposits breakdown, corporate actions, investor profile.
3. Corregir `summary_eur.dividends_lifetime_eur = 2619.99` (anteriormente solo YTD mal parseado). Añadir nota explicando que el "YTD 1524.59" del Activity Statement incluye accruals no pagados, mientras que el Inception cuenta solo paid dividends.
4. Corregir `summary_eur.realized_pnl_lifetime_eur = 1022.09`. **Importante**: el "realized_lt_ytd 9099.57" del handoff anterior era erróneo — probablemente eran proceeds (~€14,486 lifetime), no gains. La cifra correcta de gains realizados lifetime es €1,022.09.

**Razón**: 
- El Inception es la única fuente con datos consolidados para calcular Sharpe, drawdown, alpha vs benchmark — métricas clave para evaluar si la estrategia está funcionando.
- Las cifras fiscales YTD anteriores eran mezcla confusa de paid + accruals. Ahora hay dos cifras claras: lifetime paid (€2,620) y YTD aproximado paid-only (~€611).
- El YTD 2026 Sharpe 0.66 vs VDHG 1.05 significa que la cartera está batiendo al benchmark en retorno (YTD 12.3% vs 4.5%) PERO con peor risk-adjusted return — concentración en MO/defensivas ayuda en drawdowns pero frena en rallies.

**Importe**: Sin movimiento de capital. Solo parseo y estructuración de datos preexistentes.

**Resultado esperado**:
- prompts/analyze-portfolio.md puede ahora invocar inception_2026_06_23 del snapshot para responder preguntas de performance attribution, risk benchmark, themes — sin red.
- Los 8 CSVs en data/ permiten análisis fiscal y de performance offline.
- Próxima sesión puede corregir holdings.csv con los avg_price_native del Open Position Summary (más limpio que los cálculos a mano).

**Revisión**: Pendiente. Validar en la próxima sesión de /analyze que las cifras del Inception se usan y que no hay doble-conteo con los extracts anteriores.
