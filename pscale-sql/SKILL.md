---
name: pscale-sql
description: Execute non-interactive PlanetScale SQL queries with pscale sql using ephemeral credentials. Use when running read-only SQL from agents or scripts, collecting JSON query results, using human table or vertical output, querying replicas/keyspaces/Postgres dbnames, or when a user asks for pscale sql. Triggers on pscale sql, PlanetScale SQL query, non-interactive query, ephemeral credentials, --query, --vertical, trailing \\G.
---

# pscale sql

Execute a single SQL query against a PlanetScale database branch using ephemeral credentials.

`pscale sql` is intended for agents and scripts. For interactive exploratory sessions, use `pscale shell` instead.

## Common commands

```bash
# Read query with machine-readable output (default role is reader)
pscale sql <database> <branch> --org <org> --format json --query "SELECT 1"

# Read from replicas
pscale sql <database> <branch> --org <org> --format json --replica --query "SELECT count(*) FROM users"

# MySQL/Vitess: target a specific keyspace when needed
pscale sql <database> <branch> --org <org> --format json --keyspace <keyspace> --query "SELECT 1"

# PostgreSQL: target a database name; default is postgres
pscale sql <database> <branch> --org <org> --format json --dbname app --query "SELECT 1"

# Human output is a table by default; vertical output is available for wide rows
pscale sql <database> <branch> --org <org> --query "SHOW VITESS_TABLETS"
pscale sql <database> <branch> --org <org> --vertical --query "SHOW REPLICA STATUS"
pscale sql <database> <branch> --org <org> --query "SHOW REPLICA STATUS\\G"
```

For PostgreSQL targets, the CLI-created temporary connection uses `sslmode=verify-full` by default. Keep that verification in place unless the user has a specific, approved diagnostic reason to alter connection behavior outside this command.

## Roles and safety

- Default role is `reader`.
- Use `--role writer`, `--role readwriter`, or `--role admin` only when the user explicitly asked for a write-capable operation.
- Destructive SQL containing `DELETE`, `DROP`, or `TRUNCATE` is blocked unless `--force` is passed. The guard also detects data-modifying CTEs and `EXPLAIN ANALYZE`/`EXPLAIN ANALYSE` wrappers around destructive statements. MySQL executable comments such as `/*! DROP TABLE ... */` and version-gated `/*!80000 DELETE ... */` are live SQL and are included in this safety check; do not treat them as inert comments.
- Agents must ask for explicit user approval before using `--force`; show the exact query and target database/branch/org first.

```bash
# Write-capable role for a deliberate non-destructive write
pscale sql <database> <branch> --org <org> --role admin --query "UPDATE users SET disabled = true WHERE id = 123"

# Destructive operation: only after explicit user approval
pscale sql <database> <branch> --org <org> --role admin --force --query "DELETE FROM sessions WHERE expires_at < now()"
```

## Agent workflow

1. Identify `<org>`, `<database>`, `<branch>`, engine context (Vitess/MySQL vs Postgres), and whether the query is read-only.
2. For reads, prefer `--format json` and keep the default `reader` role.
3. For writes, confirm the target and exact SQL with the user before running.
4. Never add `--force` without explicit approval for the exact destructive query.
5. JSON-mode failures use a structured error envelope; parse the machine-readable `code`/message fields instead of scraping colored human output.
6. Return a concise summary and include row counts/results as appropriate.

## Human output

For human output, `pscale sql` now prints a table by default instead of Go map formatting. Multi-line cell values are padded across physical lines so the table remains closed. Use `--vertical` for one-column-per-line rows, or end the query with a MySQL-style trailing `\G`; the CLI strips trailing `\G` or `\g` before sending the SQL, and `\G` enables vertical output. JSON remains the preferred format for automation.

## Flag placement

Place flags after positional arguments:

```bash
pscale sql <database> <branch> --org <org> --format json --query "SELECT 1"
```

## References

See [references/commands.md](references/commands.md) for current `pscale sql --help` output.
