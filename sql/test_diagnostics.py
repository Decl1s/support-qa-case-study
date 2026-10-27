"""Regression checks for the SQL exercise using an isolated SQLite database."""

from pathlib import Path
import sqlite3
import unittest


BASE = Path(__file__).resolve().parent


class DiagnosticsTest(unittest.TestCase):
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
        self.queries = queries
        self.query = queries[3]
        self.expected = [
            ("FileQueue", 2), ("MailGateway", 1),
            ("AdminConsole", 2), ("EmptyService", 0),
        ]

    def test_all_queries_match_expected_rows(self):
        expected_results = [
            [(1, "OPEN"), (4, "OPEN")],
            [(1,), (5,)],
            [(1, "FileQueue"), (4, "MailGateway"), (5, "AdminConsole")],
            self.expected,
            [(500, 2), (503, 2)],
            [("P1", 1), ("P2", 1), ("P3", 1)],
        ]
        for number, (query, expected) in enumerate(zip(self.queries, expected_results), 1):
            with self.subTest(query=f"Q{number}"):
                self.assertEqual(expected, self.db.execute(query).fetchall())

    def test_server_error_groups_exclude_singletons_and_client_errors(self):
        # Existing server errors all repeat; add counterexamples for WHERE and HAVING.
        self.db.executemany(
            "INSERT INTO incidents VALUES (?, ?, ?, ?, ?, ?, ?)",
            [
                (9, 1, "OPEN", "P2", "engineer-a", 502, "2026-10-01"),
                (10, 1, "OPEN", "P2", "engineer-a", 404, "2026-10-01"),
            ],
        )
        self.assertEqual([(500, 2), (503, 2)], self.db.execute(self.queries[4]).fetchall())

    def test_unassigned_query_includes_in_progress_but_excludes_closed(self):
        self.db.executemany(
            "INSERT INTO incidents VALUES (?, ?, ?, ?, ?, ?, ?)",
            [
                (9, 1, "CLOSED", "P2", None, 500, "2026-10-01"),
                (10, 1, "IN_PROGRESS", "P2", None, 500, "2026-10-01"),
                (11, 1, "OPEN", "P2", "engineer-a", 500, "2026-10-01"),
            ],
        )
        self.assertEqual([(1,), (5,), (10,)], self.db.execute(self.queries[1]).fetchall())

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
