---
applyTo: "**/*.py"
---

When reviewing Python code, always check for and flag the following, ranked by
severity, with a concrete fix for each:

- **SQL injection** — string-interpolated or f-string SQL. Require parameterized
  queries (`cursor.execute(sql, params)`).
- **Hardcoded secrets** — API keys, passwords, or tokens committed in source.
  Require loading from environment variables or a secrets manager.
- **Plain-text passwords** — require hashing (e.g. bcrypt/argon2) before storage.
- **Missing input validation** on public functions that reach a database, file
  system, or shell.
- **Resource leaks** — database connections or file handles that are not closed;
  prefer context managers (`with`).
- **Bare `except:`** clauses that swallow errors silently.
- **Comparisons to None** using `==`/`!=` instead of `is`/`is not`.
- **Unguarded edge cases** such as division by zero.

Rank findings by severity (BLOCKER / HIGH / MEDIUM / LOW) and keep feedback
high-signal — only report real problems.
