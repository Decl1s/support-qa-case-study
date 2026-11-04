"""Load the simple SELECT statements used by this SQL exercise."""

from pathlib import Path


def load_queries(path: Path) -> list[str]:
    # Strip full-line comments first: the Q4 description contains a semicolon.
    # This exercise has no semicolons inside SQL string literals or block comments.
    sql = "\n".join(
        line for line in path.read_text(encoding="utf-8").splitlines()
        if not line.lstrip().startswith("--")
    )
    return [query.strip() for query in sql.split(";") if query.strip()]
