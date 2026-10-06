from pathlib import Path
import sqlite3

base = Path(__file__).resolve().parent
with sqlite3.connect(":memory:") as db:
    db.executescript((base / "schema.sql").read_text())
    sql = "\n".join(line for line in (base / "diagnostics.sql").read_text().splitlines() if not line.lstrip().startswith("--"))
    for index, query in enumerate(sql.split(";"), 1):
        if query.strip():
            rows = db.execute(query).fetchall()
            print(f"Q{index}: {rows}")
