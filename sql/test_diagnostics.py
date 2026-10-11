"""Regression checks for the SQL exercise using an isolated SQLite database."""

from pathlib import Path
import sqlite3
import unittest


BASE = Path(__file__).resolve().parent


class ActiveIncidentCountsTest(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(":memory:")
        self.addCleanup(self.db.close)
        self.db.executescript((BASE / "schema.sql").read_text(encoding="utf-8"))
        # Strip full-line comments before splitting: the Q4 comment contains a semicolon.
        sql = "\n".join(
            line for line in (BASE / "diagnostics.sql").read_text(encoding="utf-8").splitlines()
            if not line.lstrip().startswith("--")
        )
        queries = [query.strip() for query in sql.split(";") if query.strip()]
        self.assertEqual(6, len(queries), "The exercise must contain Q1 through Q6")
        self.query = queries[3]
        self.expected = [
            ("FileQueue", 2), ("MailGateway", 1),
            ("AdminConsole", 2), ("EmptyService", 0),
        ]

    def test_product_without_incidents_has_zero_active_count(self):
        self.assertEqual(self.expected, self.db.execute(self.query).fetchall())

    def test_product_with_only_closed_incidents_has_zero_active_count(self):
        self.db.execute("INSERT INTO products VALUES (?, ?)", (5, "ClosedOnly"))
        self.db.execute(
            "INSERT INTO incidents VALUES (?, ?, ?, ?, ?, ?, ?)",
            (9, 5, "CLOSED", "P3", "engineer-a", 400, "2026-10-01"),
        )
        self.assertEqual(
            self.expected + [("ClosedOnly", 0)], self.db.execute(self.query).fetchall()
        )


if __name__ == "__main__":
    unittest.main()
