from pathlib import Path
import sqlite3

from query_loader import load_queries


base = Path(__file__).resolve().parent
with sqlite3.connect(":memory:") as db:
    db.executescript((base / "schema.sql").read_text(encoding="utf-8"))
    for index, query in enumerate(load_queries(base / "diagnostics.sql"), 1):
        rows = db.execute(query).fetchall()
        print(f"Q{index}: {rows}")
