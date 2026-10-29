# Decisión de estructura — A / B / C (2026-09-29)

> ## ✅ ELEGIDA: OPCIÓN C — 2026-09-29/30 ("la opción más lógica es que haré la C, re verifica")
> Ejecución: dic-2026 (Deka → VWCE, independiente) + **ene-2027 (transición C: VHYL + salidas + recortes, para no apilar plusvalías en el ejercicio 2026)**. `target.csv` v2 ya aplicado. Test A9 (salida C→A) activado.
> El resto del documento se conserva como análisis de soporte de la decisión.

## 0. Punto de partida (28-sep-2026, post-tanda; fx 0,8803)

NLV 112.367 € · cash 560 €. Plusvalías/minusvalías latentes por posición (IBKR 28-sep, convertidas):

| Posición | Valor € | P&L latente € | % gain |
|---|---:|---:|---:|
| VWCE | 38.148 | +4.690 | +14 % |
| VHYL | 39.844 | +5.710 | +17 % |
| JNJ | 4.960 | +1.567 | +46 % |
| MO | 2.853 | +481 | +20 % |
| KO | 1.725 | +311 | +22 % |
| GOOG | 985 | +242 | +32 % |
| XOM | 3.280 | +105 | +3 % |
| VZ | 4.591 | +45 | +1 % |
| O | 6.781 | **−333** | −5 % |
| ENG | 2.607 | **−98** | −4 % |
| T | 544 | **−71** | −11 % |
| AVGO | 1.259 | **−151** | −12 % |
| IBTS | 4.007 | **−430** | −10 % |
| **Sleeve (10 acciones)** | **29.578** | **+2.098 neto** | |

*(Coste por lote real desde `trades.csv` disponible para refinar; estas cifras usan el P&L latente total por posición, que es lo que tributa al vender todo un título. Escala estatal de referencia 19/21 % — **foral Bizkaia VERIFICAR CON ASESOR**.)*

## 1. Las tres arquitecturas

| | **A — VWCE + IBTS** | **B — Actual** | **C — Híbrido sleeve ≤12 %** |
|---|---|---|---|
| Composición final | VWCE ~94,5 % + IBTS ~3,6 % (glidepath) | VWCE 34 % + VHYL 35,5 % + sleeve 26,4 % + IBTS 3,6 % | VWCE ~84 % + IBTS ~4 % + sleeve 12 % (VHYL absorbida en VWCE) |
| Qué se vende | Todo el sleeve + VHYL (~67,7 k€) | Nada | VHYL + ~16 k€ del sleeve (AVGO, GOOG, T, KO, ENG completos + recortes O/VZ/XOM) |
| **Plusvalía realizada** | **+7.806 €** | 0 € | **+5.960 €** (VHYL 5.710 + sleeve ~250 neto: pérdidas de O/T/ENG/AVGO compensan ganancias de KO/GOGO/recortes) |
| **IRPF transición (una vez)** | **~1.520 €** | 0 € | **~1.130 €** |
| Drag fiscal anual (dividendos) | **~0 €** (VWCE acumula) | ~580 €/año (0,52 % del NLV) | ~130 €/año (0,12 %) |
| TER extra (VHYL 0,29 % vs VWCE 0,20 %) | ahorra ~36 €/año | — | ahorra ~36 €/año |
| **Payback de la transición** | ~2,8 años | — | **~2,5 años** |
| Comisiones/operativa anual | Mínima (2 fondos) | Máxima (10 líneas, cuarentenas, scoring) | Media (5 líneas, revisión semestral) |
| Riesgo idiosincrático | Ninguno de acciones sueltas | 10 nombres de 0,5–6 % | Acotado a 12 % con 5 nombres ≤3 % |
| Correlación con carrera tech | **Máxima** (VWCE ~25 % big-tech, ~60 %+ USD) | Media-alta | **Media** (VZ/JNJ/XOM/MO/O decorrelacionan de tech) |
| Carga de gobernanza | RULES casi queda vacío | Toda la maquinaria 3 capas | Capa 1 reducida a 5 valores + test A9 |
| Puerta de salida | Ninguna prevista (irreversible en la práctica) | Esta decisión | **A9: si a 31-dic-2028 el XIRR del sleeve < XIRR de VWCE → disolver sleeve (coste hoy ~2,8 k€ de ganancias)** |

## 2. Recomendación: **C, con tope 12 %**

Argumentos, en orden de peso:

1. **Es la única opción que diversifica tu riesgo laboral.** Tu salario y el 55–57 % de tu cartera dependen del mismo ciclo tech; VWCE-solo lleva esa correlación al máximo (~25 % del fondo en big-tech USA). Un sleeve pequeño de defensivas (teleco, salud, energía, tabaco, REIT) es el único diversificador real que tendrías — el resto son variaciones del mismo riesgo.
2. **El coste se amortiza rápido y cada año posterior es ahorro neto**: ~1.130 € una vez vs ~450 €/año de drag+TER eliminados. A 10 años, C acumula ~4-5 k€ de ventaja fiscal sobre B.
3. **Daña acotado**: 12 % de sleeve equivocándote sistemáticamente (−1 %/año vs índice) cuesta ~0,12 %/año de cartera — tolerable y medible.
4. **Deja salida limpia y barata** (test A9 de 2028, coste de disolución ~600 € de IRPF sobre ~2,8 k€ de ganancias).

**Contra-argumento honesto (por qué A ganaría)**: si no valoras el engagement ni la diversificación laboral, A domina — misma amortización, drag 0, complejidad mínima. Y la evidencia disponible hoy NO apoya al sleeve: no ha batido al core (IR −3,72 en el último informe, benchmark defectuoso además). C es una apuesta a que el sleeve aporta algo que A no da; el test de 2028 la confirma o la mata. Si prefieres no hacer esa apuesta, A es perfectamente defendible y más simple.

**Por qué no B**: 26,4 % en 10 nombres con 4 cuarentenas, 9 bandas rojas y ~580 €/año de drag para un sleeve sin alfa demostrada — el coste de gobernanca es real y el beneficio no lo es (todavía).

## 3. sleeve C propuesto (12 %) — quién se queda

| Nombre | Peso | Razón de quedarse |
|---|---:|---|
| VZ | 3,0 % | Teleco, yield 5,9 %, A, decorrela de tech |
| O | 3,0 % | REIT mensual, decorrela (hoy en minusvalía: mantener no cuesta) |
| JNJ | 2,5 % | Salud defensiva (se compra así misma: 46 % de gain latente NO se realiza) |
| XOM | 2,0 % | Energía, cíclica, diversifica |
| MO | 1,5 % | Tabaco, yield 6,4 % — cap bajo por declive secular |
| *Salen:* AVGO, GOOG (tech-correlacionadas), T (congelado), KO (redundante con JNJ), ENG (regulatorio binario) | | *realizan: −151, +242, −71, +311, −98 = +233 € netos* |

## 4. Plan de transición de C (solo si la eliges — diciembre es buen mes: un solo ejercicio fiscal, o partir 2026/2027 si el asesor lo ve mejor por tramos)

1. Vender VHYL (todo, ~39,8 k€) → comprar VWCE mismo día.
2. Vender AVGO, GOOG, T, KO, ENG (completos) + recortes de O/VZ/XOM hasta los pesos del cuadro → VWCE.
3. IRPF: ~5.960 € de plusvalías en 2026 (sumadas a las ~893 € ya realizadas → tramo 21 % en la parte que exceda 6 k€, estatal-ref; foral VERIFICAR). Las minusvalías de O/T/ENG/AVGO (−653 €) compensan dentro de la base ahorro.
4. `target.csv` v2: VWCE 0,84 · IBTS 0,04 · VZ 0,03 · O 0,03 · JNJ 0,025 · XOM 0,02 · MO 0,015.
5. Desde entonces: aportes → VWCE siempre (el sleeve ya no recibe dinero nuevo; solo se mantiene). A9 decide en 2028 si disolver.

## 5. Qué evidencia haría cambiar de opción (pre-registrado)

| De → a | Gatillo | Coste |
|---|---|---|
| C → A | A9: XIRR sleeve < XIRR VWCE a 31-dic-2028 (tolerancia 0 pp) | ~600 € IRPF |
| B → C | Esta decisión (hoy) | ~1.130 € IRPF |
| B → A | Elegir A hoy | ~1.520 € IRPF |
| A → C | Cambio de circunstancias (no previsto) | recompra sleeve desde cero |
