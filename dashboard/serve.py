#!/usr/bin/env python3
"""Servidor del dashboard JARVIS — HTTP estático sobre dashboard/.

Prebuild:  python3 dashboard/build_data.py
Arrancar:  python3 dashboard/serve.py  →  http://localhost:8765
"""
import http.server, sys
from pathlib import Path

DASH = Path(__file__).resolve().parent
PORT = 8765

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(DASH), **kw)
    def end_headers(self):
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()

if __name__ == "__main__":
    if not (DASH / "data.json").exists():
        print("ERROR: run build_data.py first")
        sys.exit(1)
    print("JARVIS Dashboard: http://localhost:" + str(PORT))
    http.server.HTTPServer(("", PORT), Handler).serve_forever()
