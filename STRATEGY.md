# Estrategia de inversión

Última actualización: **2026-09-29 (v2 — cambio de premisas: retorno total)**. Cambios registrados en `decisions.md` y en el changelog de `RULES.md`.

## Principios generales (v2)

> El objetivo pasa de "dividendos" a **retorno total** (ver `PLAN-RETIRADA.md`). Vender activos según plan es una herramienta legítima DESDE el año objetivo — nunca antes.

1. **Vivir de la cartera por retorno total.** Dividendos que caigan solos + venta programada de VWCE (PLAN-RETIRADA §5). El marco "solo dividendos" y el objetivo "vacaciones con dividendos" quedan retirados (mandato 2026-09-29).
2. **Durante la acumulación, cero retiradas.** Ninguna venta para gasto antes del año objetivo [P2 pendiente; supuesto 2036–2038]. Únicas ventas posibles: Vías de salida de RULES.md y la transición de estructura que se apruebe.
3. **Destino por defecto de cada ingreso: VWCE** (cascada A8 de RULES.md: buffer 500 € → gap del sleeve SOLO si la estructura elegida lo mantiene → resto a VWCE). Ningún euro en cash sin regla; si el día 5 no hay decisión, se ejecuta el destino por defecto.
4. **Núcleo: VWCE, con IBTS como vehículo del glidepath de retirada.** El papel de VHYL y del sleeve de acciones queda a la espera de `ESTRUCTURA-DECISION-2026-09-29.md` (opciones A/B/C; recomendación: C con sleeve 12 %).
5. **En caídas no se vende equity para gastar** — se consume el colchón (guardrails de PLAN-RETIRADA §6; sustituye al antiguo "no vender nunca").

## Asset allocation objetivo (tras incorporar los 30k)

> **⚠ PENDIENTE DE ESTRUCTURA (2026-09-29):** la tabla siguiente es la asignación v1 (anterior al cambio de premisas). La composición futura la decide `ESTRUCTURA-DECISION-2026-09-29.md` (A: VWCE+IBTS · B: mantener · C: VWCE+IBTS+sleeve 12 %). Mientras se decide, **los aportes nuevos van a VWCE** (Principio 3).

| Instrumento | Peso | Función |
|---|---|---|
| VWCE | ~36 % | Crecimiento largo plazo (acumulación, sin dividendos). Máxima eficiencia fiscal. |
| VHYL | ~31 % | Flujo de caja estable para vacaciones (distribución trimestral). |
| O (Realty Income) | ~7,5 % | REIT mensual. Pilar del flujo vacaciones. |
| JNJ | ~6,5 % | Salud defensiva. Crecimiento constante del dividendo. |
| VZ (Verizon) | ~6,5 % | Teleco USA. Alto yield, flujo inmediato. |
| MO (Altria) | ~5,5 % | Consumo/tabaco. Alto yield, peso controlado por riesgo regulatorio. |
| XOM (Exxon) | ~5,0 % | Energía integrada. Aristócrata del dividendo. |
| AVGO (Broadcom) | ~4,5 % | Tecnología. Crecimiento del dividendo a doble dígito. |
| ENG (Enagás) | ~3,5 % | Energía España. Alto yield, diversificación euro. |
| T (AT&T) | ~3,5 % | Teleco USA. Complementa a VZ. |
| KO (Coca-Cola) | ~1,8 % | Consumo defensivo. Se mantiene sin reforzar. |
| GOOG (Alphabet) | ~1,6 % | Tecnología. Sin dividendo significativo, se deja como está. |
| IBTS | ~3,5 % | Bonos soberanos corto plazo. Colchón de seguridad. (2026-09-22: subido de ~0,5 % para formalizar el peso real — ver REBALANCEO-2026-09-22.md) |
| Efectivo | ~1 % | Para pequeñas oportunidades. |

**Resumen visual** (corregido 2026-09-22 — los pesos de la tabla son crudos y suman ~1,14, se normalizan a 1 internamente en `analyze.py`):
- ETFs (VWCE + VHYL) = 67 % crudo (~59 % normalizado) — base intocable.
- Acciones individuales = 46 % crudo (~40 % normalizado) — motor de vacaciones y futuro. *(Nota: el "≈33 %" anterior era inconsistente con la propia tabla.)*

> Nota: los pesos son "orientativos". El script `analyze.py` los normaliza a suma 1 internamente.

## Plan de acción con los 30.000 € (próximos días/semanas)

1. **Vender microposiciones** que generan ruido y no aportan: RTX, PNC, TXN, AMGN, NOC, LMT, MVUS, IHYG, FGQI. **Mantener IBTS** (bonos seguros).
2. **Distribuir ~32.000 €** (30k + ~2k de ventas) según pesos objetivo del sleeve de acciones individuales.

| Acción | Aportación orientativa | Peso final |
|---|---|---|
| O | 6.000 € | ~7,5 % |
| VZ | 5.000 € | ~6,5 % |
| JNJ | 5.000 € | ~6,5 % |
| MO | 4.000 € | ~5,5 % |
| XOM | 4.000 € | ~5,0 % |
| AVGO | 4.000 € | ~4,5 % |
| ENG | 2.000 € | ~3,5 % |
| T | 2.000 € | ~3,5 % |

## Rutina mensual con 3.000 € (v2 — cascada, 2026-09-29)

| Paso | Acción |
|---|---|
| 0 | Reponer cash operativo hasta 500 € |
| 1 | Solo si la estructura aprobada mantiene sleeve con gap: tramo fijo 1.000 € → O y tramo 2.000 € → siguiente activo con gap |
| 2 | **Resto (o todo, si no hay gap): VWCE** — destino por defecto, ejecución el día 5 |
| 3 | Si el día 5 no has decidido: se ejecuta el paso 2 sin más (acción por defecto) |

**Regla de flexibilidad** (solo con sleeve): caída >5 % de un activo elegible sin motivo grave → concentrar el tramo variable en él.

## Riesgos estructurales (v2, 2026-09-29)

### Fondo de emergencia [P3 pendiente]
Regla propuesta: **6–9 meses de gasto (13.500–20.250 € `supuesto`)** fuera del broker (cuenta remunerada o Letras del Tesoro). Con la venta ya permitida en retirada, el fondo es lo que impide vender MAL en una caída por una emergencia.

### Cluster de tipos (O + VZ + ENG + T ≈ 13,5 % hoy)
Cuatro posiciones que se comportan como bonos con cupón: suben y bajan juntas con el 10Y (5,16 % en sep-2026). En acumulación es viento de cola (yield más alto al comprar); en NLV de corto plazo, viento en contra. Si se aprueba la estructura C, el cluster baja a ~6–9 % (sin T ni ENG).

### Decisión deliberada: ~96 % renta variable en la cartera de inversión (30-sep-2026)
Aceptada a propósito tras auditoría externa. La estabilización del plan VIVE FUERA de la cartera: ~70 k€ de liquidez externa (emergencia + casa ≈ 32 % del patrimonio total), 36 k€/año de flujo, cero retiradas hasta el año objetivo, y glidepath de IBTS desde ~2032. Una caída del 40-50 % (~58-73 k€ en pantalla) es escenario esperado y asumido; la defensa son los guardrails de PLAN-RETIRADA, no la renta fija. Nota: IBTS es la versión USD sin cubrir (etiqueta corregida el 30-sep — gracias, auditoría externa): en risk-off el dólar tiende a subir, colchón accidentalmente convexo; la decisión USD vs deuda-euro se toma en el glidepath.

### Correlación con la carrera (sector tecnológico)
Salario tech + 55–60 % de exposición USD/tech en cartera: el mismo shock puede golpear renta y patrimonio a la vez. Mitigaciones: fondo de emergencia ampliado, no exceder (o eliminar, opción C) los targets de AVGO/GOOG, y el colchón de retirada.

## Qué NO hacer (lecciones aprendidas)

1. **No invertir en inmuebles vacacionales** (Tailandia, España, etc.). Iliquidez, gestión, impuestos altos, riesgo divisa.
2. **No perseguir estrategias de concentración total** (Nasdaq, QQQM). Más variabilidad sin prima esperada y no son UCITS.
3. **No retirar capital antes del año objetivo.** El interés compuesto necesita tiempo; las retiradas siguen PLAN-RETIRADA, no el ánimo.
4. **No obsesionarse con microposiciones.** Venderlas al llegar los 30k y olvidarse (hecho, jun-2026).
5. **No dudar del plan cuando el mercado caiga 20 %.** En caídas: guardrails (colchón), nunca pánico vendedor.

## Frases ancla (v2)

- "VWCE es mi jubilación en piloto automático."
- "El plan de retirada ya está escrito; mi único trabajo ahora es aportar y no tocar."
- "No necesito 2,5 millones. Con ~830.000 € reales y un 3,25–3,5 % de retirada, soy libre."
- "En años malos gasto del colchón, nunca de la cartera."
