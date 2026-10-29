#!/usr/bin/env python3
"""Genera la proyección Obsidian del grafo desde graph.json (la fuente de verdad).

Arquitectura (adaptada de Fukura):
  graph/graph.json  = FUENTE (editar aquí)
  graph/notes/**    = proyección GENERADA — nunca editar a mano (frontmatter generated: true)
  MCP knowledge-graph = espejo consultable (sembrado aparte por el agente)

Uso: python3 graph/build_notes.py   (idempotente: regenera notes/ e INDEX.md)
"""
from __future__ import annotations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
G = json.loads((HERE / "graph.json").read_text())

TYPE_ORDER = ["Person", "Goal", "Rule", "Position", "Account", "Event",
              "Thread", "Contradiction", "Zone", "Property", "Document"]
TYPE_FOLDER = {"Person": "core", "Goal": "core", "Rule": "rules", "Position": "positions",
               "Account": "accounts", "Event": "calendar", "Thread": "threads",
               "Contradiction": "contradictions", "Zone": "casa", "Property": "casa",
               "Document": "docs"}
EMOJI = {"Person": "👤", "Goal": "🎯", "Rule": "📐", "Position": "📈", "Account": "🏦",
         "Event": "📅", "Thread": "🧵", "Contradiction": "⚠️", "Zone": "🗺️",
         "Property": "🏠", "Document": "📄"}


def wiki(name: str) -> str:
    return f"[[{name}]]"


def main() -> None:
    notes = HERE / "notes"
    notes.mkdir(exist_ok=True)
    entities = {e["name"]: e for e in G["entities"]}
    rels_out: dict[str, list] = {n: [] for n in entities}
    rels_in: dict[str, list] = {n: [] for n in entities}
    for r in G["relations"]:
        f, t, rt = r["from"], r["to"], r["type"]
        if f in rels_out:
            rels_out[f].append(f"- {rt} → {wiki(t)}")
        if t in rels_in:
            rels_in[t].append(f"- {rt} ← {wiki(f)}")

    index_lines = [f"# Índice del grafo — {G['updated']}", "",
                   "> Generado desde `graph.json` — no editar a mano. Regenerar: `python3 graph/build_notes.py`", ""]
    for ty in TYPE_ORDER:
        group = [e for e in G["entities"] if e["type"] == ty]
        if not group:
            continue
        folder = TYPE_FOLDER[ty]
        (notes / folder).mkdir(exist_ok=True)
        index_lines += [f"## {EMOJI[ty]} {ty} ({len(group)})", ""]
        for e in sorted(group, key=lambda x: x["name"]):
            name = e["name"]
            body = [
                "---",
                f"generated: true",
                f"type: {ty}",
                f"graph_version: {G['version']}",
                f"updated: {G['updated']}",
                "---",
                "",
                f"# {EMOJI[ty]} {name}",
                "",
            ] + [f"- {o}" for o in e.get("obs", [])] + [""]
            if rels_out.get(name):
                body += ["## Relaciones (salientes)", ""] + rels_out[name] + [""]
            if rels_in.get(name):
                body += ["## Relaciones (entrantes)", ""] + rels_in[name] + [""]
            (notes / folder / f"{name}.md").write_text("\n".join(body))
            index_lines.append(f"- {EMOJI[ty]} {wiki(name)}")
        index_lines.append("")

    (notes / "INDEX.md").write_text("\n".join(index_lines))
    (HERE / "README.md").write_text(
        "# Grafo semántico del portfolio\n\n"
        "Fuente de verdad: `graph.json` → proyección `notes/` (abrir esta carpeta como vault de Obsidian).\n\n"
        "- Regenerar: `python3 graph/build_notes.py`\n"
        "- Nunca editar notas con `generated: true` — corregir `graph.json` y regenerar.\n"
        f"- Cifras actuales: {G['updated']} → {len(G['entities'])} entidades, {len(G['relations'])} relaciones.\n"
        "- Las cifras operativas vivas siguen en target.csv/RULES.md/decisions.md — esto es un índice relacional.\n"
    )
    print(f"OK: {len(G['entities'])} notas + INDEX.md en {notes}")


if __name__ == "__main__":
    main()
