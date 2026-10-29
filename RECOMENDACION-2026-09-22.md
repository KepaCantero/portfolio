# Portfolio recomendado conforme a RULES.md — 22-sep-2026

> ## ⚠️ CORRECCIÓN misma tarde
> Los importes de gap de §2 se calcularon con la lectura EUR-equivalente del snapshot; la correcta es USD nativo × fx 0,89117 (ver `REBALANCEO-2026-09-22.md`). Gaps corregidos: VZ +4.560 € · O +1.956 € · XOM +2.596 € → tramo limpio total **~9.021 €** (163 acciones). El análisis de conformidad (§1) y las enmiendas (§5) siguen válidas. **El plan ejecutable definitivo está en `REBALANCEO-2026-09-22.md`.**

> Respuesta a: "¿qué portfolio me recomendarías para que cumpla todas las normas que tengo?"
> Basado en `ANALYSIS-2026-09-22.md` (mismos datos y fuentes). Pesos = escala normalizada de `analyze.py` (targets crudos ÷ 1,13).

## 0. La respuesta corta

**Tu portfolio objetivo (target.csv) no cumple hoy tus propias reglas.** Cuatro de sus diez acciones individuales están en cuarentena según la Capa 1/2 de RULES.md con datos de sep-2026 (T, ENG, MO, JNJ), otra está en su límite exacto de valoración (AVGO) y IBTS lleva desde junio rompiendo su banda. Con las reglas **como están escritas**, el dinero nuevo solo tiene dos—tres hogares conformes: **VZ, O y (con una salvedad) XOM**.

Dos salidas coherentes:
- **Plan B (recomendado)**: desplegar ya ~8.500 € en VZ + O + XOM (XOM con la limitación del DDM en cíclicas documentada), mantener el resto en cuarentena con condiciones de desbloqueo explícitas, y **enmendar 3 reglas** para que tu target vuelva a ser internamente consistente.
- **Plan A (estricto)**: solo VZ + O (~6.000 €); todo lo demás espera. Máxima pureza normativa, más cash sin desplegar.

## 1. Registro de conformidad (posición por posición, sep-2026)

| Posición | S1 payout ≤75 % | S2 ≥5y crecientes | S4/V4 P/E | DDM | Banda A1 | Veredicto |
|---|---|---|---|---|---|---|
| VWCE | — | — | — | — | ok (−3 %) | **Intocable** (Principio 1, A6) |
| VHYL | — | — | — | — | ok (+18 %) | **Intocable** |
| **O** | ✅ 74 % AFFO (justo) | ✅ 31 años | ✅ ~14× AFFO | ✅ UNDER | 🔴 −30 % | **COMPRA LIMPIA** |
| **VZ** | ✅ 56 % | ✅ ~20 años | ✅ 9,2× | ✅ UNDER | 🔴 −75 % | **COMPRA LIMPIA** (prioritaria) |
| **XOM** | ✅ 52 % | ✅ 43 años | ✅ 12,7× | ⚠️ OVER* | 🔴 −57 % | **COMPRA con salvedad*** |
| JNJ | ✅ ~55 % | ✅ 64 años | ❌ 25× > 15× (V4 dinero nuevo) | ⚠️ OVER | ok −22 % | Mantener, **sin añadir** |
| MO | ❌ ~78 % > 75 % | ✅ 57 años | ✅ 12,2× | ✅ UNDER | 🔴 −46 % | Mantener (B), **sin añadir** hasta payout ≤75 % |
| T | ✅ 48 % | ❌ congelado desde 2022 | ✅ 10,4× | ✅ FAIR | 🔴 −83 % | Mantener, **sin añadir** hasta reanudar subidas |
| ENG | ✅ 57 % | ❌ recorte 2024 | ✅ 9,6× | ✅ UNDER | 🔴 −31 % | Mantener, **sin añadir** hasta CNMC 2027+ |
| AVGO | ✅ 35 % | ✅ (+10 %) | ⚠️ 30× = límite exacto V4/A5 | ⚠️ OVER | 🔴 −70 % | Añadir **solo en debilidad** (<30× forward, ~<$350) |
| KO | ✅ 63 % | ✅ 64 años | ❌ 27× (no-add anyway) | ⚠️ OVER | ok | Mantener sin reforzar (STRATEGY) |
| GOOG | — | — | — | — | 🔴 −33 % | Mantener, no ampliar (A5) |
| IBTS | — | — | — | — | 🔴 **+628 %** | **Decisión pendiente** (ver §4) |

\* El DDM de Gordon (g=4 %) marca OVERVALUED sistemáticamente en cíclicas petroleras — limitación del modelo, no una señal. Todo lo demás en XOM es conforme. Estrictamente, la regla dice "marcar en rojo y proponer alternativa": por eso el Plan A lo excluye.

## 2. Plan B — Recomendado (reglas actuales + salvedad documentada)

Desplegable conforme **YA**: VZ 4.519 € + O 1.504 € + XOM 2.453 € = **8.476 €**.
Disponible oct–dic: 9.000 (backlog jul-sep) + 660 (cash) + 3.000 (nov) + 3.000 (dic) = **15.660 €**.

| Cuándo | Compra | € | Justificación normativa |
|---|---|---:|---|
| Octubre | **VZ** | 3.000 | Mayor brecha (−75 %), Safety A, DDM UNDERVALUED, Graham 9,2× — el candidato más limpio de toda la lista |
| Octubre | **O** | 1.000 | Tramo fijo de la rutina mensual (STRATEGY), A, UNDERVALUED |
| Octubre | **XOM** | 2.400 | Carlson #1 entre supervivientes (17 pts), P/E 12,7×; salvedad DDM documentada (o Enmienda 1) |
| Noviembre | **VZ** | 1.500 | Cierra target (total 4.500 ≈ gap) |
| Noviembre | **O** | 500 | Cierra target |
| Noviembre | **XOM** | fin de gap (~50) | |
| Dic → | **Condicional** | — | MO si resultados 29-oct bajan payout ≤75 % ( improbable con guía 5,61-5,72: necesita EPS ≥5,92) · AVGO si cotiza claramente <30× (~<$350) |
| Si nada se desbloquea | **no depositar** el resto | ~7.200 € | "Cada euro nuevo va a acciones" — sin hogar conforme, el dinero espera fuera de IBKR (o se acepta el override de AVGO por escrito) |

**Resultado del Plan B** (denominador ~117.900 €): VZ 5,3 % · O 6,1 % · XOM 4,1 % — todos dentro de banda y a ~1 pp de sus targets. VHYL queda en 33,9 % vs 27,3 % normalizado = **+24 % relativo, rozando la banda superior** (motivo más para no venderla jamás y dejar que los stocks la diluyan). Dividendo incremental: **~+400 €/año brutos (~340 netos)**.

## 3. Plan A — Estricto (solo compras 100 % limpias)

VZ 4.519 + O 1.504 = **6.023 €** (oct–nov). XOM, MO, AVGO, T, ENG, JNJ: nada hasta que cambien los datos. ~9.600 € quedan sin desplegar a cierre de año. Es la lectura literal de RULES.md workflow §3 ("DDM no diga OVERVALUED en ningún buy").

## 4. IBTS — decisión obligatoria (única banda al alza)

| Opción | Qué | Consecuencia |
|---|---|---|
| **(a) Formalizar el colchón** | `target.csv`: IBTS 0,5 % → **3,5 %**, redistribuir | Cero trades, banda verde, honesto. Recomendada si valoras el colchón |
| (b) Recortar ~3.100 € | Vende hasta ~0,6 % | Realiza ~−450 € de minusvalía **compensable** vs ~893 € de plusvalías 2026 (TAX-ES ✓) y reinvierte a yield 2-4× mayor |

## 5. Las 3 enmiendas mínimas (para que tu target vuelva a ser conforme)

Sin ellas, tu target asigna dinero a posiciones que tus propios filtros vetan (T y ENG no pueden recibir jamás el dinero que su target implica; XOM/AVGO siempre saltarán el DDM):

1. **Valoración por grupos (extender A5 a la Capa 2)**: cíclicas (XOM) y growth (AVGO) se valoran por P/E (V4: ≤15× / ≤30×), no por DDM. El DDM queda para yield+value estables (O, VZ, MO, T, ENG, KO, JNJ). → Desbloquea XOM; AVGO queda sujeto a <30×.
2. **Categoría "yield puro" para T y ENG**: mantenibles, añadir solo con payout ≤60 % **y** dividendo reanudado (T) / claridad regulatoria (ENG), cap 3,5 % cada una. Alternativa más simple: excluirlos de la lista de compra de la rutina mensual y dejar sus gaps abiertos hasta que vuelvan a crecer el dividendo.
3. **IBTS target 3,5 %** (o ejecutar el recorte de §4b).

Con las 3 enmiendas, el portfolio objetivo es exactamente tu `target.csv` — y el Plan B pasa de "recomendado con salvedad" a "totalmente conforme".

## 6. Rutina mensual adaptada (desde octubre, hasta cerrar gaps)

| Tramo | Original (STRATEGY) | Adaptada conforme |
|---|---|---|
| 1 — 1.000 € | O fijo | **O fijo** (sin cambios) |
| 2 — 1.000 € | Más barata de {VZ, JNJ, MO, XOM, AVGO, ENG, T} | Más barata de **{VZ, XOM}** (los únicos elegibles; JNJ/MO/T/ENG/AVGO en cuarentena) |
| 3 — 1.000 € | 2ª más barata o AVGO | 2ª más barata de {VZ, XOM}; AVGO solo <30×; si no hay elegible → retener tramo |

Regla de flexibilidad (>5 % caída sin motivo): aplicable solo a posiciones fuera de cuarentena.

## 7. Impacto esperado

- Con solo el tramo limpio (8,5 k€): dividendo forward ~1.850 → **~2.190 €/año netos**; sleeve stocks ~24 % → ~28 %.
- Con target completo (18 k€, requiere enmiendas/unlocks): ~2.650-2.700 €/año netos, sleeve 33 %, meta 3-5 años (>4.000 €) en trayectoria.
- Fiscal: cero plusvalías realizadas en el Plan B (solo compras). Opción IBTS-(b) añade una minusvalía útil.

## 8. Lo que NO hay que hacer (según tus propias reglas)

- No vender VWCE/VHYL para financiar stocks (A6) — ni siquiera con VHYL rozando banda superior.
- No vender JNJ/KO por caras (TAX-ES: no tax-loss harvesting artificial con tesis intacta; JNJ +44 % generaría plusvalía).
- No comprar MO "porque el DDM lo dice" — A3 (payout ≤75 %) es filtro duro y está en 78 %.
- No forzar AVGO a 30× exactos — el límite es "hasta", no "en".

---
*No es asesoramiento financiero: es la lectura sistemática de STRATEGY.md + RULES.md + TAX-ES.md sobre los datos de sep-2026. Decisión final del inversor.*
