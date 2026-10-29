---
task_category: Estrategia de inversión / despliegue de capital nuevo
role: Estratega de cartera personal aplicando reglas propias del usuario
tone: Pragmático, directo, orientado a acción verificable
output_format: Markdown con tabla de propuesta + checklist de validación
target_audience: El propio inversor (decisor final)
detail_level: Comprehensive
thinking_effort: Max
task_horizon: Long-horizon (agentic)
constraints:
  - PROHIBIDO añadir a VWCE o VHYL con nueva pasta (principio #1 de STRATEGY.md)
  - PROHIBIDO añadir al sleeve Bond o Cash salvo leftover irreducible
  - Minimizar plusvalías: priorizar comprar desviados a la baja, no vender
  - Respetar share rounding (acciones enteras) y reportar leftover
  - No proponer venta de microposiciones aquí — usar /deploy-cash para eso
  - Todos los importes en EUR
---

# Plantilla — Rebalanceo con capital nuevo

> Caso de uso: **desplegar N euros nuevos** comprando acciones del sleeve individual según desviación vs target. No cubre ventas de microposiciones (para eso usa `deploy-cash.md` conceptualmente o el comando `/deploy-cash`).

## 1) Prepara el contexto

Pega en el chat (en este orden) el contenido de estos archivos:

```
1. PROFILE.md
2. STRATEGY.md     (FUENTE DE LA VERDAD — aplica las reglas literalmente)
3. RULES.md        (framework doctrinal: filtros safety + señales valuation + reglas allocation)
4. TAX-ES.md
5. holdings.csv    (cartera actual)
6. target.csv
7. decisions.md    (últimas entradas, para detectar caídas recientes)
8. prices.json     (salida de python3 scripts/fetch_prices.py — opcional pero recomendado)
9. scores.json     (salida de python3 scripts/score.py — opcional pero recomendado)
```

## 2) Placeholders a rellenar

- `{{capital_a_desplegar}}` — euros nuevos disponibles (ej. `3000`).
- `{{modo}}` — uno de: `estandar` (rutina mensual O + 2 más baratas) | `greedy` (puro por desviación) | `o_fijo` (solo a O).
- `{{fecha}}` — `YYYY-MM-DD`.

## 3) Instrucción (pega esto DESPUÉS del contexto)

```
Fecha: {{fecha}}
Capital a desplegar: {{capital_a_desplegar}} EUR
Modo: {{modo}}

Actúas como mi estratega de cartera. Mi perfil, estrategia y fiscalidad
están en el contexto; aplícalos sin reinterpretarlos.

TAREA

Propón cómo desplegar {{capital_a_desplegar}} EUR nuevos respetando
ESTRICTAMENTE STRATEGY.md. El algoritmo depende del modo:

- "estandar" → rutina mensual: 1/3 a O (fijo), 1/3 a la acción más
  barata (mayor desviación negativa) de {VZ, JNJ, MO, XOM, AVGO, ENG, T},
  1/3 a la segunda más barata o AVGO si se quiere acelerar tecnología.
- "greedy" → distribuye todo proporcional a la desviación negativa
  (solo tickers con gap < 0).
- "o_fijo" → todo a O.

ENTREGA (markdown):

A) Cifra clave (una línea):
   "Desplegar X € | Deployado Y € | Sobrante Z € (leftover)"

B) Tabla de propuesta (ordenada por deploy descendente):
   | Ticker | Nombre | Precio EUR (hoy) | Acciones a comprar | Deploy EUR | Valor después | Target después % | Gap residual EUR |

C) Validación de reglas (checkboxes — marca cada uno):
   [ ] No añade a VWCE ni VHYL (prohibido por principio #1)
   [ ] No añade a IBTS (Bond) ni Cash salvo leftover irreducible
   [ ] Solo compra tickers del sleeve Stock
   [ ] Cada compra son acciones enteras (no fracciones)
   [ ] Leftover < 5 % del capital total; si no, lo justifica
   [ ] Respeta "caída > 5 % → concentrar" si aplica (regla flexibilidad)
   [ ] Safety grade ≥ B (60+) en todos los tickers comprados (capa 1 RULES.md)
   [ ] Ningún ticker comprado con KW signal = EXPENSIVE o DDM = OVERVALUED
   [ ] Payout ratio ≤ 75% en todos los tickers comprados (S1 RULES.md)
   [ ] Circuit breaker macro inactivo (mercado no en caída >20%)

D) Comentario fiscal (2-3 líneas máximo, referencia TAX-ES.md):
   - Si solo compra: "Operación solo con nueva pasta — sin plusvalía,
     sin impacto fiscal este año. W-8BEN vigente para retención USA
     del 15 % en dividendos (deducible Anexo A)."
   - Si hubiera venta (no esperado en este modo): explica plusvalía
     estimada y tramo 19/21/23 %.

E) Oportunidades tácticas (solo si aplican):
   - Si alguna acción de la rutina ha caído > 5 % último mes según
     decisions.md o prices.json: propón concentrar 2.000-3.000 € en
     ella, citando el dato.

F) Próximo paso (una línea):
   "Loguear en decisions.md una vez ejecutada la orden con el formato
   del archivo."

REGLAS

- Cero creatividad: no propongas tickers fuera de target.csv.
- No modifiques los pesos objetivo — vienen dados.
- Si una compra rompe el principio #1 o #2 de STRATEGY.md, no la
  propongas aunque matemáticamente encaje.
- Si leftover > 5 %, repórtalo y propón destino (más acciones de
  un ticker o cash para próxima ventana).

CRITERIOS DE ACEPTACIÓN

Antes de devolver la propuesta, verifica internamente:

[ ] Suma de columna "Deploy EUR" = capital a desplegar − leftover.
[ ] Ningún ticker en la propuesta es VWCE, VHYL, IBTS o CASH.
[ ] "Valor después" = valor anterior + deploy para cada fila.
[ ] "Target después %" se recalcula sobre el total cartera tras
    despliegue, no sobre el total anterior.
[ ] El leftover está expresado en EUR y como % del capital.
[ ] Todas las filas tienen quantity entera > 0.

Si algún check falla, recalcula antes de entregar.
```

## 4) Notas GLM 5.2

- **Thinking effort = Max**: hay varias restricciones duras y aritmética financiera — el razonamiento profundo evita propuestas que violen STRATEGY.md.
- **Task horizon = Long-horizon (agentic)**: el modelo puede encadenar cálculos, validación y refinamiento iterativo.
- Los `constraints` del frontmatter están volcados explícitamente en el cuerpo para que el modelo no dependa del YAML.
- Para modelos con ventana menor, recorta `decisions.md` y omite `prices.json` si tienes los precios ya en `holdings.csv` o los pegas a mano.
