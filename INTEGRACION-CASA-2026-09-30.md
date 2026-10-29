# Integración PORTFOLIO ⇄ CASA — 2026-09-30

> Fuente: proyecto `~/Projects/casa` (estado al 17-jul-2026): 382 listings analizados (260 Vizcaya + 122 Noja), ranking vivo con 28 candidatos puntuados, calculadora hipotecaria, costes de compra por CCAA. Datos con **2,5 meses de antigüedad** — refrescar antes de actuar.
> Faltan por rellenar en `casa/00_perfil/perfil-comprador.md`: ingresos netos, estado civil, fecha objetivo — **necesarios para la regla cuota/ingresos ≤33 %**.

## 1. Lo que el proyecto casa dice (resumen objetivo)

- **Zona real**: Bilbao (foco Zorroza) — vivienda habitual. **Noja** (Cantabria) = segunda residencia.
- **Top del ranking**: Z017 Zorroza 240 k€ (98 m², 8,0/10) · F005 Bolueta 185 k€ (7,75) · Z013a Zorroza 235 k€ · Z018 Zorroza 230 k€. **Rango realista: 185-275 k€**; el más barato interesante: Z007 Zorroza 139 k€.
- **Mercado caliente**: Bilbao +11,62 % interanual (Tinsa 2T-26), 3.927 €/m² ciudad (récord). Los precios del ranking de julio ya no son fiables.
- **Reglas del propio proyecto**: LTV ≤80 % · cuota/ingresos ≤33-35 % · colchón post-entrada 3-6 meses · ITP Bizkaia 4-7 % (tramo medio 6 %) · Noja: ITP 8-10 %.

## 2. La aritmética de los tres escenarios (entrada 20 %, ITP 6 %, gestiones ~2 k€)

| | **Z017 · 240 k€** | **F005 · 185 k€** | **Z007 · 139 k€** |
|---|---:|---:|---:|
| Cash necesario (entrada+costes) | **64,4 k€** | 49,9 k€ | 37,6 k€ |
| Ahorro externo disponible | 70 k€ | 70 k€ | 70 k€ |
| **Colchón restante tras compra** | **5,6 k€ ⚠️ (regla: ≥13,5 k)** | 20,1 k€ ✅ | 32,4 k€ ✅ |
| Hipoteca (80 %) | 192 k€ | 148 k€ | 111 k€ |
| Cuota (fijo 3,5 %, 25 años) | 961 €/mes | 741 €/mes | 557 €/mes |
| Cuota (fijo 4,0 %, 25 años) | 1.007 €/mes | 776 €/mes | 583 €/mes |
| Fin de hipoteca si se compra en 2027 | **2052** | 2052 | 2052 |

## 3. Los tres hallazgos que afectan al plan del portfolio

### 3.1 ⚠️ La decisión "Deka → VWCE" debe revisarse — el hallazgo principal
Con un candidato objetivo de **240 k€**, los 70 k€ externos **no bastan** respetando el fondo de emergencia (necesitas 64,4 + 13,5 = ~78 k€). El Deka (33 k€) es el único capital flexible del mapa. Opciones:

| Opción | Condiciones | Coste |
|---|---|---|
| **Deka → TR remunerada (reserva casa)** — recomendada SI la casa es probable a ≤12 meses y >200 k€ | esperar al certificado de residencia fiscal igualmente; el dinero gana ~3 % mientras decide | ~1-1,5 k€ de retorno esperado perdido si tarda 6 meses (vs entrar en VWCE ya) |
| **Deka → VWCE como estaba** — válida si la casa será ≤200 k€ o >18 meses | los 70 k€ cubren 185 k€ con colchón ✓ | ninguno extra |
| **Casa más barata** (Z007/F005) y Deka → VWCE | 139-185 k€ caben en los 70 k€ | espacio/calidad |

**Regla de decisión**: fecha-límite personal para decidir casa sí/no y en qué rango de precio → destino del Deka. Mientras no exista, el Deka es dinero sin dueño.

### 3.2 ⚠️ La regla "fin de hipoteca ≤ año de retirada" queda violada por el mercado
Hipoteca a 25 años firmada en 2027 termina en **2052**; tu retirada objetivo es 2035-38. Opciones reales con precios actuales: (a) **plazo 15-18 años** (cuota Z017 a 15y/3,5 %: ~1.373 €/mes — solo viable con ingresos altos), (b) plazo 25 + **amortizaciones anticipadas agresivas** con los flujos de años buenos (la opción realista), (c) aceptar cuota en la retirada → el gasto de jubilación sube ~1.000 €/mes → capital objetivo +~300-340 k€ (a SWR 3,5 %) — **descartada por coherencia con el plan**. Decisión pendiente tuya; documentarla al firmar.

### 3.3 Impacto en la capacidad de aportación (la variable que dijiste "no es plan")
Si hoy no pagas alquiler ≈ cuota neta nueva: 961-1.007 €/mes (Z017) → capacidad de aporte cae ~1 k€/mes → **fecha de libertad se desliza ~1,5-2 años por la tabla de sensibilidad** (2 k/mes → ~2038-39). Si hoy ya pagas alquiler similar → impacto ≈ 0. **Dato necesario: tu alquiler actual.** Y a favor: casa pagada = gasto de retirada SIN vivienda → el capital objetivo BAJA (escenario más favorable de PLAN-RETIRADA §1-bis).

## 4. Tensión doctrinal: Noja
Tu STRATEGY.md prohíbe "inmuebles vacacionales" (anti-principio nº1: iliquidez, gestión, impuestos) y el proyecto casa lleva 122 listings de Noja analizados (segunda residencia, ITP 8-10 %). No es ilegítimo — es un deseo legítimo fuera de la estrategia escrita. Si Noja es aspiración real: (a) reabrirla como decisión explícita de estilo de vida con su precio (compra ~250-300 k + mantenimiento + ITP alto), o (b) dejarla como "alquiler vacacional financiado por el plan" (más barato a tu frecuencia de uso, casi seguro). Recomendado: (b) hasta la libertad financiera; reevaluar entonces.

## 5. Checklist de integración

- [ ] Rellenar `casa/00_perfil/perfil-comprador.md` (ingresos, alquiler actual, fecha objetivo) — habilita la regla cuota/ingresos
- [ ] Refrescar el ranking (datos jul-26, mercado +11 % interanual: los top pueden estar vendidos)
- [ ] Decidir rango de precio objetivo (≤200 k vs ~240 k) → **determina el destino del Deka** (§3.1)
- [ ] Plazo de hipoteca + plan de amortización anticipada (§3.2) — con el asesor
- [ ] Noja: decidir explícitamente (§4)
- [ ] Al comprar: actualizar PLAN-RETIRADA (gasto de retirada sin vivienda, fecha recalculada) y este archivo
