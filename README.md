# Portfolio Management System

Sistema personal para gestionar la cartera de dividendos. Lee `holdings.csv`, compara contra `target.csv` aplicando las reglas de `STRATEGY.md`, y propone rebalanceos con precios en vivo.

## Setup rápido

```bash
cd /Users/kepa.cantero/Projects/portfolio
python3 -m venv .venv
source .venv/bin/activate
pip install -r scripts/requirements.txt
```

Renombra `holdings.csv.example` → `holdings.csv` y rellena con tu cartera real.

## Comandos disponibles (slash commands)

| Comando | Qué hace |
|---|---|
| `/prices` | Trae precios en vivo (Yahoo Finance) y los muestra en EUR. |
| `/analyze` | Estado actual: pesos, desviaciones vs target, P&L no realizado. |
| `/rebalance 3000` | Propone cómo desplegar 3.000 € nuevos según STRATEGY.md. |
| `/monthly-buy 3000` | Aplica la rutina mensual (O fijo + 2 más baratas). |
| `/monthly-buy 3000 --tech` | Igual pero sesgando el 3er tramo hacia AVGO. |
| `/deploy-cash 30000` | Despliegue grande: incluye venta de microposiciones + distribución. |

## Estructura

```
portfolio/
├── README.md                  # este archivo
├── PROFILE.md                 # perfil del inversor
├── STRATEGY.md                # reglas de decisión (FUENTE DE LA VERDAD)
├── TAX-ES.md                  # recordatorio fiscal España
├── decisions.md               # diario de decisiones (logging)
├── holdings.csv               # TU CARTERA (input principal)
├── target.csv                 # asignación objetivo
├── scripts/
│   ├── fetch_prices.py        # Yahoo Finance → JSON de precios en EUR
│   ├── analyze.py             # holdings + precios → análisis de desviaciones
│   ├── rebalance.py           # nueva pasta → asignación greedy por desviación
│   └── monthly_buy.py         # rutina mensual específica (O + 2)
└── .claude/
    ├── settings.json          # permisos
    └── commands/              # slash commands
```

## Workflow típico (ejemplo: rebalancear 3.000 €)

1. Asegura que `holdings.csv` está actualizado con tus posiciones reales.
2. Lanza `/rebalance 3000`.
3. Claude ejecuta los 3 scripts, lee STRATEGY.md, y te devuelve:
   - Tabla con qué comprar, a qué precio, cuántas acciones.
   - Validación de que respeta las reglas (no toca VWCE/VHYL, solo añade a acciones).
   - Alertas si alguna acción ha caído mucho (oportunidad de concentrar).
4. Loguea la decisión en `decisions.md`.

## Datos y privacidad

- **Precios**: Yahoo Finance vía librería `yfinance`. Gratis, sin API key, ~15 min delay. Suficiente para decisiones de rebalanceo mensual.
- **Holdings**: solo en tu disco local. El sistema nunca envía tu cartera fuera de tu máquina salvo que tú se lo pidas.
- **Divisas**: conversión automática USD→EUR con el tipo de cambio del día.

## Mantenimiento

- **Actualizar `target.csv`** cuando cambies la asignación objetivo (p.ej. subir AVGO al 6 %).
- **Actualizar `STRATEGY.md`** si cambian las reglas (p.ej. empezar a vender VHYL a los 8 años).
- **Anotar cada decisión en `decisions.md`**: sin esto no hay aprendizaje a largo plazo.

## Limitaciones

- Yahoo Finance puede tardar o fallar en horas pico. Reintentar.
- Los precios pueden tener ~15 min de delay. Para ejecución real usa el precio del broker.
- **No es asesoramiento financiero**. Es una herramienta para aplicar TU estrategia. Tú eres el único responsable de las decisiones.
