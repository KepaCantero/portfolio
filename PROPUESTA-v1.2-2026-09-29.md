# PROPUESTA v1.2 — Auditoría y edición del sistema (2026-09-29)

> **Estado: NADA APLICADO.** Documento de diffs para aprobación. Encargado por mandato del 29-sep ("auditor y editor").
> Regla de trabajo cumplida: ninguna orden sugerida; cada cifra con fuente o marcada `supuesto`; tipos forales no verificables en fuente oficial esta sesión → `VERIFICAR CON ASESOR`.

## 0. Supuestos declarados (los corchetes del mandato venían vacíos)

| Placeholder | Supuesto usado | Base | Pendiente de ti |
|---|---|---|---|
| Gasto neto mensual | **2.250 €/mes (27.000 €/año)** | PROFILE.md ("2.000–2.500 €/mes") | **P1: cifra real** |
| Año objetivo | **2036–2038** | PROFILE.md (horizonte 10–12 años; edad 44) | **P2: año** |
| Fondo de emergencia | **Desconocido** | No consta en ningún archivo | **P3: ¿existe? importe** |
| Inflación (proyección real) | 2,25 %/año `supuesto` | — | ajustable |
| Aportación real futura | 36.000 €/año constante en términos reales `supuesto` | PROFILE 3.000 €/mes | ajustable |

---

## 1. Resumen de cambios propuestos (impacto en una línea)

| # | Cambio | Archivo | Impacto |
|---|---|---|---|
| 1 | Cascada de aportaciones (A8) + Principio 2 reescrito: desbordamiento a VWCE por defecto | RULES + STRATEGY | Ningún euro sin destino desde diciembre; elimina el cuello de botella del §5.2 |
| 2 | PLAN-RETIRADA.md nuevo: objetivo como retorno total, SWR 3,25/3,5/3,75 %, colchón 1–2 años, orden de retirada | nuevo archivo | El objetivo deja de depender del yield 4 %; capital objetivo 720–831 k€ (base) |
| 3 | Test del sleeve (A9): XIRR de flujos reales vs VWCE y VHYL; benchmark VDHG→VWCE | RULES + futuro script | Primera prueba empírica de si la selección activa aporta algo |
| 4 | Gobernanza: changelog + regla 30 días/pre-registro (asimétrica) + revisión de enmiendas 28-sep | RULES §Gobernanza | Corta la racionalización a posteriori; V2-bis/A7/IBTS se mantienen (ver §2.1.4) |
| 5 | TAX-ES: Bizkaia foral (VERIFICAR), Modelo 720, nota VHYL corregida | TAX-ES | Evita multas/errores de declaración; documenta el drag fiscal del flujo |
| 6 | Automatización: regla día 1/día 5 + mecanismo (recordatorios programables; orden recurrente IBKR a verificar) | STRATEGY + operativo | La pausa jul–sep (~525–630 €/año perdidos) no se repite |
| 7 | Simplificación: bandas absolutas, V1 y A4 a informativas, payout desconocido = 0, targets T/MO bajados, "RULES en una página" | RULES + target.csv | De 9 bandas rojas a 3 (MO, T, AVGO): alarmas que informan |
| 8 | Riesgos ausentes: fondo de emergencia, cluster de tipos O/VZ/ENG/T, correlación con carrera tech | STRATEGY | Hace creíble el "nunca vender"; nombra la correlación sueldo-cartera |

---

## 2. Diffs por archivo

### 2.1 RULES.md — v1.1 → v1.2

**2.1.1 NUEVO al inicio del archivo: "RULES en una página"**

```diff
+# RULES en una página (v1.2 — la versión larga es documentación, esto gobierna)
+1. SOLO SE COMPRA: Safety ≥60, payout ≤75%, ≥5 años subiendo, P/E ≤15 (≤30 AVGO).
+2. SOLO SE VENDE (2 tramos): grado D, payout >90%, corte de dividendo, ruptura de tesis documentada.
+3. EN CAÍDAS >20%: prohibido vender; solo compras de oportunidad.
+4. CADA APORTE: buffer 500€ → gap ejecutable (activos) → resto a VWCE. Sin excepciones ni cash sin regla.
+5. BANDAS (alerta de revisión): ETF ±5pp · acciones ±2,5pp · IBTS ±1,5pp.
+6. CUARENTENA: hold sin añadir hasta su unlock; su target es semáforo, no rebaja… salvo decisión explícita (T, MO v1.2).
+7. NORMAS: endurecer = vigor inmediato · habilitar compra = 30 días o pre-registro previo.
+8. TEST DEL SLEEVE: XIRR real vs VWCE a 31-dic-2028 y 31-dic-2030 (criterio A9).
```

**2.1.2 A1 — bandas relativas → absolutas**

```diff
-### A1 — Vanguard relative bands (25 % relativos)
-Para cada sleeve principal (ETFs, Stocks), calcular peso actual vs target.
-- **ALERTA**: si cualquier peso se desvía ±25 % **relativo** del target → revisión manual obligatoria.
-  - Ejemplo: VWCE target 36 %. Banda: 27 % – 45 %. Fuera de banda → alerta.
-- **Ejecución automática** (rutina mensual): solo dentro de banda.
+### A1 — Bandas absolutas de revisión (v1.2; sustituye a las relativas ±25 %)
+Motivo del cambio: con 9 de 13 posiciones permanentemente en rojo, la alarma dejaba de informar
+(fatiga de señal). Bandas absolutas, proporcionales al papel de cada activo:
+| Grupo | Banda sobre target | Ejemplo VZ (6,5 %) |
+|---|---|---|
+| ETFs core (VWCE, VHYL) | ±5,0 pp | — |
+| Acciones | ±2,5 pp | banda 4,0 %–9,0 % |
+| IBTS | ±1,5 pp | — |
+Fuera de banda → revisión manual obligatoria (igual que antes). La ejecución sigue siendo la cascada A8.
+Estado a 28-sep con bandas nuevas: rojas solo **MO (2,55 % < 3,0), T (0,49 % < 1,0), AVGO (1,13 % < 2,0)**.
```

**2.1.3 V1 y A4 pasan a informativas; fix del score**

```diff
 ### V1 — Kelley Wright
+**[v1.2: INFORMATIVA — no veto ni orden de compra]** La σ estimada como 20 % de la media es
+pseudo-precisión; la señal se muestra pero no decide. El "cuándo" lo deciden V2/V2-bis y V4.
 ### A4 — O'Shaughnessy
+**[v1.2: INFORMATIVA — absorbida por A2]** El desempate Quality queda documentado pero el
+ranking operativo es Carlson (A2) solo.
```
Y en `scripts/score.py` (pendiente de aprobación, es código): `payout_ratio == 0 → payout_score = 0` con flag `DATO_FALTANTE` (antes: 50 — optimista en ausencia de dato).

**2.1.4 NUEVA sección "Gobernanza de reglas y changelog"**

```diff
+## Gobernanza (v1.2)
+1. Todo cambio de regla se registra en el changelog con fecha, motivo y referencia a decisions.md.
+2. **Asimetría de vigencia**: los cambios que ENDURECEN (vetan compras/ventas) entran en vigor
+   inmediato. Los que HABILITAN compras entran en vigor a 30 días, o inmediatamente si quedaron
+   registrados en decisions.md ANTES del ciclo de compra al que afectan.
+   (Motivo: esperar 30 días para protegerse es autodañino; esperar para comprar, prudente.)
+3. Ninguna compra puede invocar una regla con menos de 30 días de antigüedad sin citar el
+   pre-registro que la precedió.
+
+### Changelog
+| Versión | Fecha | Cambios | Ref |
+|---|---|---|---|
+| v1.0 | jun-2026 | Sistema original 3 capas | — |
+| v1.1 | 28-sep-2026 | V2-bis (ámbito DDM) · A7 (targets duales + status) · Vías de salida · IBTS target 3,5 % · fix score.py filas # | decisions.md 28-sep |
+| v1.2 | [pendiente aprobación] | Bandas absolutas · A8 cascada · A9 test sleeve · Gobernanza · V1/A4 informativas · T target 1 % · MO target 4 % · payout desconocido=0 | PROPUESTA v1.2 |
+
+### Revisión de las enmiendas del 28-sep bajo este criterio (mandato tarea 4)
+- **V2-bis: MANTENER.** (a) Se registró en decisions.md la mañana del 28-sep, antes de los fills
+  de las 15:30 — cumple la letra del pre-registro. (b) Evidencia exculpatoria: la compra de XOM
+  estaba planificada desde el 22-sep (RECOMENDACION-2026-09-22 §1: "casi — solo flag DDM cíclica")
+  con la salvedad documentada ANTES de que existiera la enmienda; no se creó la regla para la
+  compra. (c) AVGO, la única compra futura que la necesita, ejecutará >30 días después.
+  Riesgo residual asumido: el patrón podría repetirse; por eso la regla 2 (asimetría) existe ya.
+- **A7: MANTENER.** Sin dependencia de compra; es organización de targets.
+- **IBTS target 3,5 %: MANTENER.** No habilitó compra alguna.
```

**2.1.5 NUEVO A8 — Cascada de aportaciones (desbordamiento)**

```diff
+### A8 — Cascada de aportaciones (v1.2; ejecuta la rutina mensual de STRATEGY)
+Cada ingreso (p. ej. 3.000 €) sigue, en orden:
+1. **Buffer**: reponer cash operativo hasta 500 € (comisiones/FX).
+2. **Gap ejecutable**: repartir según rutina mensual (tramo fijo O + tramo variable) SOLO entre
+   filas `activo` de target.csv.
+3. **Desbordamiento**: si no hay gap ejecutable, o sobra tras el paso 2 → **100 % del resto a VWCE**
+   (orden a mercado, día 5). [Decisión pendiente del inversor: alternativa/variante — si VHYL
+   rinde >4,0 % ese mes, el desbordamiento va a VHYL. La propuesta por defecto es VWCE SIEMPRE:
+   simple, fiscalmente diferido, sin señal que vigilar.]
+4. **Cuarentenas** nunca reciben dinero; se reactivan solas cuando su condición de desbloqueo
+   ocurre (entonces vuelven al paso 2).
+5. **Ningún euro sin regla**: si el mercado está cerrado, la orden queda pendiente para la próxima
+   apertura. Casos del mandato: (a) sin gap → paso 3 directo. (b) valores en cuarentena → se
+   ignoran, el paso 2 usa solo los activos. (c) acciones a su peso → paso 3.
+Precedencia: A8 ejecuta; A1 solo alerta.
```

**2.1.6 NUEVO A9 — Test de resultados del sleeve**

```diff
+### A9 — Test del sleeve de acciones (v1.2; mandato tarea 3)
+**Pregunta**: ¿la selección de acciones individuales aporta retorno total frente a poner esos
+mismos flujos en el core? Es la única regla que audita RESULTADOS, no coherencia.
+**Métrica**: XIRR (rentabilidad ponderada por dinero) de los flujos reales del sleeve (data/trades.csv,
+desde 2025-03) frente a **carteras espejo**: mismos importes, mismas fechas, invertidos en VWCE
+(benchmark principal, coherente con inversor EUR) y en VHYL (alternativa de renta). VDHG queda
+retirado como benchmark (fondo con sesgo australiano, elección de IBKR).
+**Implementación**: `scripts/sleeve_test.py` (pendiente construir; entra en la misma hornada que
+tax_2026.py). Mientras tanto, registro manual anual en decisions.md el 31-dic.
+**Criterios propuestos — UMBRALES A APROBAR POR EL INVERSOR**:
+| Fecha | Si XIRR sleeve < XIRR VWCE | Si XIRR sleeve ≥ X criterio |
+|---|---|---|
+| 31-dic-2028 (~3,8 años de datos) | Flujos nuevos se redirigen al core (A8 salta el paso 2); sleeve en piloto automático | continúa igual |
+| 31-dic-2030 (~5,8 años) | Igual + sleeve en "modo cosecha" (sin compras nunca; recortes solo por Vías de salida) | continúa igual |
+Tolerancia propuesta: 0 pp (simple y honesta). Alternativa: −1 pp/año admitido como empate técnico.
+Nota metodológica (discrepancia declarada): 3 años es estadísticamente débil para estrategias de
+dividendos (el yield-on-cost tarda); por eso el criterio de 2028 es "redirigir flujos" (reversible)
+y el de 2030 "cosecha" (estructural). Medición anual desde 2026 para ver la tendencia.
```

### 2.2 STRATEGY.md

```diff
-2. **Cada euro nuevo va a acciones individuales de dividendo creciente.** Sin excepciones. No se añade a VWCE/VHYL con dinero nuevo.
+2. **Cada euro nuevo sigue la cascada A8** (RULES.md): primero las acciones elegibles hasta cerrar
+   el gap ejecutable; el excedente alimenta VWCE por defecto. El sleeve de acciones deja de ser
+   destino ilimitado y pasa a ser destino prioritario. [v1.2 — requiere aprobación: cambia un
+   principio fundacional]
```

```diff
 ## Rutina mensual con 3.000 €  →  **Rutina mensual v2 (cascada A8)**
+| Paso | Regla |
+|---|---|
+| 0 | Reponer cash hasta 500 € |
+| 1 | Tramo fijo 1.000 € → O (si O está a peso, este tramo desborda) |
+| 2 | Tramo variable 2.000 € → siguiente activo con gap (VZ, XOM, AVGO<30×) |
+| 3 | **Desbordamiento**: resto → VWCE el día 5 |
+Regla de flexibilidad (caída >5 %): igual, solo entre activos.
```

```diff
+## Riesgos estructurales (v1.2 — nueva sección, mandato tarea 8)
+### Fondo de emergencia
+**[PENDIENTE P3]** El principio "no vender nunca para gastos" solo es creíble con liquidez fuera
+del broker. Regla propuesta: **6 meses de gasto (~13.500 € `supuesto`)** en cuenta remunerada o
+bonos del Estado fuera de IBKR. Dado el punto siguiente, 6–9 meses.
+### Cluster de tipos (O + VZ + ENG + T ≈ 13,5 % hoy; ~21 % a target)
+Cuatro posiciones que se comportan como bonos con cupón: subidas de tipos las castigan en precio
+juntas (semana del 21-sep: utilities −3,2 %, 10Y al 5,16 %). En acumulación es viento de cola
+(yield más alto al comprar); en NLV de corto plazo, viento en contra. Mitigaciones: cap implícito
+del cluster ≤21 % crudo, colchón IBTS, y no ampliar el cluster en subidas de tipos si el gap lo
+permite (orden de la rutina ya lo hace: VZ/XOM primero).
+### Correlación con la carrera (sector tecnológico)
+Tu renta depende del sector tech; la cartera lleva ~55–57 % de exposición USD efectiva con
+sesgo tecnológico (AVGO + GOOG + ~25 % de VWCE en big tech). Una contracción tech golpearía
+salario y cartera A LA VEZ — justo cuando más necesitarías vender. Mitigaciones: fondo de
+emergencia ampliado (6–9 meses), no exceder los targets de AVGO/GOOG ni un euro, y el colchón
+de retirada de PLAN-RETIRADA.md.
```

### 2.3 TAX-ES.md — Bizkaia + 720 + VHYL

```diff
-# Fiscalidad (España) — Última actualización 2026-05
+# Fiscalidad (Bizkaia, régimen foral) — borrador v2 [pendiente verificación]
+> **AVISO v1.2**: resides en Bizkaia → IRPF foral, NO estatal. La escala del ahorro foral y los
+> formularios difieren de los estatales. No verificada en fuente oficial esta sesión →
+> **VERIFICAR CON ASESOR** antes de declarar. La tabla siguiente es la estatal, mantenida solo
+> como referencia de orden de magnitud (en tramos bajos los regímenes suelen alinearse — confirmar).
+
+## Declaración informativa de posiciones en el extranjero (antiguo Modelo 720)
+Cuenta IBKR (entidad extranjera) con >112.000 € en valores >> umbral 50.000 € → **OBLIGA**.
+- Presentación: enero–marzo del año siguiente. Régimen foral propio de Bizkaia: **VERIFICAR
+  ASESOR** (formulario y plazos forales).
+- Desde 2023, norma estatal (Ley 11/2021 antifraude): exención de volver a presentar si la
+  posición no varía >20.000 € vs la última declaración. Equivalente foral: **VERIFICAR**.
+- **Pregunta abierta P4**: ¿has presentado alguna vez la informativa por IBKR? Si no, el primer
+  ejercicio pendiente puede ser 2024/2025 — cuota de precedente, mejor resolverla con asesor.
+
+## Corrección de la nota VHYL ("sin doble imposición adicional" — era imprecisa)
+Dos capas distintas:
+1. **Dentro del fondo**: el 15 % de retención USA sobre los dividendos que VHYL cobra de sus
+   acciones estadounidenses NO se recupera (no aplican a fondos ni el Anexo A ni el W-8BEN).
+   Drag estructural ≈ 40 % peso USA × ~3 % yield × 15 % ≈ **0,18 %/año no recuperable** `estimación`.
+2. **En tu IRPF**: cada distribución de VHYL tributa íntegra como dividendo (base ahorro).
+Consecuencia de diseño: el flujo (VHYL/acciones) paga impuesto CADA AÑO; VWCE acumulativo difiere
+todo hasta la venta, y al vender solo tributa la plusvalía. Refuerza el desbordamiento A8→VWCE y
+la retirada por venta de PLAN-RETIRADA.md.
+
+## Checklist fiscal (fuente y fecha por dato)
+| Dato | Valor usado | Fuente | Fecha | Estado |
+|---|---|---|---|---|
+| Retención USA dividendos | 15 % (W-8BEN) | IRS treaty ES-USA | vigente | **confirmar W-8BEN activo en IBKR** |
+| Escala ahorro Bizkaia | — | — | — | **VERIFICAR CON ASESOR** |
+| Escala ahorro estatal (referencia) | 19/21/23 % | TAX-ES v1 | 2026-05 | referencia solo |
+| Informativa extranjería | aplica (>50 k€) | normativa estatal 720 | 2026 | **VERIFICAR foral** |
+| Drag VHYL interno | ~0,18 %/año | cálculo propio | 2026-09 | estimación |
+| Retención ENG | 19 % | convenio ES | vigente | ok |
```

### 2.4 PLAN-RETIRADA.md (NUEVO — contenido íntegro propuesto)

```markdown
# Plan de retirada — retorno total (v1 propuesta)

> Objetivo reformulado (mandato 29-sep): vivir de la cartera por RETORNO TOTAL (dividendos +
> venta programada), no por yield del 4 %. El "4 %" como yield era el punto débil identificado
> (MEMORIA §10.1: blend real 2,2 %). Horizonte de retirada: 35–40 años. Gasto: [P1 pendiente].

## 1. Capital objetivo (euros REALES de hoy)
Supuesto de partida: gasto neto 27.000 €/año (2.250 €/mes). Tabla para ±20 %:

| SWR \ Gasto | 21.600 €/año | **27.000 €/año** | 32.400 €/año |
|---|---:|---:|---:|
| 3,25 % | 664.615 € | **830.769 €** | 996.923 € |
| 3,50 % | 617.143 € | **771.429 €** | 925.714 € |
| 3,75 % | 576.000 € | **720.000 €** | 864.000 € |

**Capital objetivo de trabajo: 720.000–830.000 € reales** (SWR prudente para 35–40 años).
El SWR se revisa con cada renovación de la literatura; 3,5 % como caso central.

## 2. Trayectoria (proyección REAL: capital 112.367 € @ 28-sep-26 + 36.000 €/año reales `supuesto`)

| Retorno real | 2031 | 2036 | 2038 | 2041 |
|---|---:|---:|---:|---:|
| 3 % | 321 k€ | 564 k€ | 671 k€ | **845 k€** |
| 5 % | 342 k€ | 636 k€ | **775 k€** | 1.010 k€ |
| 7 % | 365 k€ | **719 k€** | 897 k€ | 1.215 k€ |

Lectura honesta: al 5 % real el objetivo se alcanza ~2037–2039 (edad 55–57, coherente con
PROFILE). Al 3 % real se desliza a ~2041. El 7 % nominal de PROFILE ≈ 4,75 % real con inflación
2,25 % — la fila del 5 % es la traducción realista de tu supuesto histórico.

## 3. Colchón de retirada (secuencia de retornos)
Al llegar al 90 % del capital objetivo: trasladar **1,5 años de gasto (~40.500 €)** a IBTS/cash.
Regla de retirada en años malos: consumir colchón, no vender acciones. Reposición en años buenos.

## 4. Orden de retirada mensual (cuando llegue el día)
1. **Dividendos** caen solos (~2,2 % del blend ≈ 2/3 del gasto a 850 k€).
2. **Venta mensual/trimestral de VWCE** por la diferencia (FIFO; en IBKR se puede elegir lote —
   VERIFICAR operativa) — las Vías de salida nº 4 ya lo contemplaban.
3. **Colchón** como estabilizador en años de caída.
4. VHYL y sleeve de acciones: fuente de renta residual; su venta queda última (y MO/T/ENG solo
   por Vías de salida).

## 5. Por qué retirar vendiendo VWCE cuesta (mucho) menos impuesto que cobrar dividendos
- **Dividendo**: tributa el 100 % del importe. 10.000 € → ~1.900–2.100 € (escala estatal
  referencia; foral VERIFICAR).
- **Venta**: tributa SOLO la plusvalía. Ejemplo con datos reales actuales: VWCE coste medio
  148,71 € / precio ~170 € → plusvalía 12,5 %. Retirar 10.000 € vendiendo VWCE → plusvalía
  1.250 € → IRPF ~263 € → **tipo efectivo ~2,6 %** del importe retirado (vs ~21 % del dividendo).
- FIFO: se venden los lotes de 2025 primero (los más antiguos); a medida que la cartera crezca,
  el % de plusvalía por lote sube y con él el tipo efectivo — a re-calcular cada año.
- Además VWCE difirió todo el impuesto durante la acumulación (0 drag anual vs ~0,2–0,4 % del
  flujo) — la diferencia compuesta durante 10 años no es trivial.

## 6. Hitos de revisión
- Anual (31-dic): capital real vs objetivo, SWR vigente, colchón.
- Al 90 % del objetivo: activar §3 (traslado a IBTS).
- Cambio de gasto real >10 %: recalcular tabla §1.
```

---

## 3. Preguntas abiertas y decisiones tuyas

**Los tres datos que faltan (bloquean cifras finales, no el sistema):**
- **P1 — Gasto neto mensual objetivo** (uso 2.250 €; tu auditoría mencionaba 40–50 k€/año como posibilidad — si es ese el número, el capital objetivo sube a ~1,07–1,33 M€ y el plan de años cambia cualitativamente).
- **P2 — Año objetivo** (uso 2036–2038).
- **P3 — Fondo de emergencia**: ¿existe? ¿importe? (regla propuesta: 6 meses, 6–9 por la correlación tech).

**Decisiones de diseño (con mi recomendación):**
1. Desbordamiento por defecto **VWCE siempre** [recomendado] vs variante VHYL >4 % [más parámetros].
2. Umbrales del test del sleeve: tolerancia **0 pp** [recomendado] vs −1 pp.
3. Target T: **3,5 % → 1,0 %** [recomendado: dividendo congelado 4 años]. Target MO: **5,5 % → 4,0 %** [recomendado: declive secular]. JNJ y ENG se mantienen.
4. Bandas absolutas: **ETF ±5 pp / acciones ±2,5 / IBTS ±1,5** [recomendado] — u otros valores.
5. Mecanismo de automatización: recordatorios programables día 1 y día 5 [disponible ya] y/o orden recurrente IBKR en VWCE como raíl por defecto [VERIFICAR si tu cuenta la ofrece] — recomiendo empezar con recordatorios + regla escrita, migrar a recurrente cuando confíes en la cascada.
6. Asimetría de vigencia (endurecer = ya; habilitar = 30 días) — aceptada tal cual, o 30 días planos.

## 4. Checklist de verificación con fechas

| # | Verificación | Cuándo | Estado |
|---|---|---|---|
| 1 | W-8BEN activo en IBKR (15 % y no 30 %) | ya | pendiente |
| 2 | Escala ahorro Bizkaia + formularios forales — asesor | oct-2026 | VERIFICAR |
| 3 | Informativa extranjería (720 foral): ¿presentada alguna vez? | oct-2026 | P4 |
| 4 | Gasto/año + fondo emergencia confirmados → recalcular PLAN-RETIRADA | oct-2026 | P1/P3 |
| 5 | Aprobación diffs v1.2 → aplicar archivos | cuando decidas | esta propuesta |
| 6 | `scripts/sleeve_test.py` (XIRR espejo VWCE/VHYL) | Q4-2026 | construir |
| 7 | `scripts/tax_2026.py` | Q4-2026 | construir |
| 8 | Pagos O (15-oct ~28 €) / MO (10-oct ~36 €) / VZ (2-nov ~59 €) | oct–nov | verificar |
| 9 | Tanda final VZ+32 / XOM+10 / AVGO+2 (~3.360 €) | próximo ingreso | plan |
| 10 | MO Q3: ¿payout ≤75 %? | 29-oct | cuarentena |
| 11 | Activity Statement Q3/Q4 (fees, FX, realized, dividendos) | ene-2027 | pendiente |
| 12 | Medición anual sleeve test (manual si no hay script) | 31-dic-2026 | nuevo |

---

### Discrepancias declaradas (mandato: "no me des la razón por defecto")

1. **Con "que el sistema quepa en una página"**: entrego la página (§2.1.1), pero mantengo RULES.md largo como documentación. Una página gobierna; veinte fuentes explican. Eliminar el archivo largo perdería la pista de auditoría que nos ha servido esta semana.
2. **Con el test a 3 años**: 3 años es poco para dividendos (lo digo en A9). Tu criterio de 2028 como "redirigir flujos" (reversible) + 2030 como "cosecha" (estructural) me parece bien; un veredicto único e irreversible a 3 años habría sido prematuro.
3. **Con MO**: propongo bajar su target a la vez que T, aunque tu auditoría solo pedía T. Argumento: el payout al 78 % no es un mal año — es la estructura del negocio en contracción; esperar que baje de 75 % es esperar que MO recorte dividendo, que es justo la señal de salida. Prefiero target honesto a semáforo perpetuo.
4. **Con la regla de 30 días plana**: propongo la asimetría (endurecer = ya). Retrasar 30 días una regla que protege es darse un mes de permiso para hacer lo que la regla prohíbe.
```
