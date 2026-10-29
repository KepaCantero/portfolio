# Plantillas de prompts (estilo Promptslove / GLM 5.2)

Plantillas reutilizables para analizar y rebalancear la cartera desde **cualquier LLM** (GLM 5.2, Claude, Gemini, DeepSeek…) fuera de Claude Code. Pensadas para copiar-pegar en `chat.z.ai` o equivalente.

## Estructura

```
prompts/
├── README.md                # este índice
├── analyze-portfolio.md     # diagnosticar cartera actual vs target
├── rebalance.md             # proponer despliegue de N € nuevos
├── monthly-routine.md       # rutina mensual fija (O + 2 más baratas)
└── deploy-cash.md           # despliegue grande + limpieza microposiciones
```

## Cómo se usan

1. Abre el `.md` del caso de uso.
2. Sustituye los placeholders `{{...}}` por tus valores.
3. Copia el bloque "CONTEXTO" (archivos del proyecto) y pégalo en el chat primero.
4. Copia el bloque "INSTRUCCIÓN" y pégalo **después** del contexto.
5. GLM 5.2: usa **Max effort** para estos casos (multi-step, razonamiento largo).

## Filosofía GLM 5.2 aplicada

- **Reducir ambigüedad, no inspirar**: goal, boundaries, inputs y success criteria explícitos.
- **Contexto primero, instrucción después**: aprovecha la ventana de 1M tokens — pega todo.
- **Tools nombradas** (`fetch_prices.py`, `analyze.py`, `score.py`, `rebalance.py`, `monthly_buy.py`): el modelo sabe qué scripts puede pedir.
- **Criterios de aceptación verificables**: el output incluye checkboxes que tú puedes auditar.

## Bundle de contexto (inclúyelo siempre)

Orden recomendado al pegar:

```
1. PROFILE.md          # perfil inversor
2. STRATEGY.md         # reglas alto nivel
3. RULES.md            # framework doctrinal 3 capas (safety/valuation/allocation)
4. TAX-ES.md           # fiscalidad España
5. BIBLIOGRAPHY.md     # opcional — solo si vas a discutir tesis
6. target.csv          # asignación objetivo
7. holdings.csv        # TU cartera
8. decisions.md        # últimas 5-10 entradas (memoria reciente)
9. /tmp/prices.json    # salida de fetch_prices.py
10. /tmp/scores.json   # salida de score.py (safety + valuation por ticker)
```

## Features investigadas y usadas

| Feature | Origen | Aplicada en |
|---|---|---|
| Ventana 1M tokens | GLM 5.2 | Bundle de contexto completo pegado en cada prompt |
| Thinking effort Max | GLM 5.2 | Plantilla rebalance + analyze (cruzan muchas reglas) |
| Long-horizon agentic | GLM 5.2 | rebalance + deploy-cash (cadenas de decisión) |
| Sub-agentes | Claude Code | Opcional: `portfolio-analyst`, `tax-reviewer` en `.claude/agents/` (no crítico para plantillas externas) |
| Skills / slash commands | Claude Code | Equivalente dentro de Claude Code: `/analyze`, `/rebalance`, `/monthly-buy`, `/deploy-cash` |
| MCP servers (Yahoo Finance) | Claude Code | Integrado vía `scripts/fetch_prices.py` (no requiere MCP) |
| Frontmatter estructurado | Promptslove | Cabecera YAML en cada plantilla con los campos del generador |
| Rules file | convención open-source | `RULES.md` como fuente de verdad operativa |

## Cuándo NO usar estas plantillas

- Si estás en Claude Code, usa directamente `/analyze` o `/rebalance €N` — son más rápidos y ya integran los scripts.
- Estas plantillas son para cuando trabajas **fuera** de Claude Code o quieres **una segunda opinión** con otro modelo (GLM 5.2, Gemini, etc.).

## Mantenimiento

- Si cambias `STRATEGY.md` o `RULES.md`, revisa que las plantillas sigan citando las reglas correctas.
- Si añades un ticker nuevo a `target.csv`, las plantillas no necesitan cambios (lo leen del CSV).
- Si cambias la rutina mensual, actualiza `monthly-routine.md`.
