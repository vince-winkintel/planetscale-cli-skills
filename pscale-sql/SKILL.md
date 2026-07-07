---
name: pscale-sql
description: Execute non-interactive PlanetScale SQL queries with pscale sql using ephemeral credentials. Use when running read-only SQL from agents or scripts, collecting JSON query results, querying replicas/keyspaces/Postgres dbnames, or when a user asks for pscale sql. Triggers on pscale sql, PlanetScale SQL query, non-interactive query, ephemeral credentials, --query.
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
```

## Roles and safety

- Default role is `reader`.
- Use `--role writer`, `--role readwriter`, or `--role admin` only when the user explicitly asked for a write-capable operation.
- Destructive SQL containing `DELETE`, `DROP`, or `TRUNCATE` is blocked unless `--force` is passed.
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
5. Return a concise summary and include row counts/results as appropriate.

## Flag placement

Place flags after positional arguments:

```bash
pscale sql <database> <branch> --org <org> --format json --query "SELECT 1"
```

## References

See [references/commands.md](references/commands.md) for current `pscale sql --help` output captured from pscale v0.293.0.
