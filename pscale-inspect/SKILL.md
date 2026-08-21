---
name: pscale-inspect
description: Run read-only PlanetScale database diagnostics with pscale inspect for table/index size, scans, locks, long-running queries, bloat, autovacuum, replication, and related health checks. Use for point-in-time MySQL/Vitess or PostgreSQL diagnostics, exact shard targeting, replica inspection, or when a user asks for pscale inspect. Triggers on pscale inspect, database diagnostics, table sizes, index sizes, unused indexes, redundant indexes, sequential scans, long-running queries, blocking locks, bloat, vacuum stats, replication slots, subscriptions.
---

# pscale inspect

Run bounded, read-only diagnostic queries against a PlanetScale database branch using ephemeral credentials. Checks adapt to MySQL/Vitess or PostgreSQL and complement the server-side production-traffic analysis in `pscale insights`.

## Start with a combined report

```bash
# Machine-readable report of every applicable check
pscale inspect all <database> <branch> --org <org> --format json

# PostgreSQL: target the application database instead of the default "postgres"
pscale inspect all <database> <branch> --org <org> \
  --dbname <postgres-database> --format json

# Vitess: target one exact shard; no command fans out across every shard
pscale inspect all <database> <branch> --org <org> \
  --keyspace '<keyspace>/<shard>' --format json

# Run against a replica when primary-only evidence is unnecessary
pscale inspect all <database> <branch> --org <org> --replica --format json
```

Always pass `--org` explicitly in agent workflows so the organization target is unambiguous. The default ephemeral role is `reader`; keep it unless the connection itself fails for a justified permission reason. On PostgreSQL, `--dbname` defaults to `postgres`, the temporary connection uses `sslmode=verify-full` by default, and the reader role may lack `CONNECT` on another database. Use `--role admin` only after confirming that this is the actual failure and that elevated access is acceptable.

## Check catalog

```text
table-sizes          Tables by total size, largest first
index-sizes          Indexes by size, largest first
unused-indexes       Indexes with little or no use
redundant-indexes    Indexes made redundant by another index
invalid-indexes      Invalid PostgreSQL indexes
seq-scans            Tables receiving full-table scans
long-running-queries Queries running longer than five minutes
locks                Blocking locks and blocked sessions
outliers             Queries by cumulative time (PostgreSQL pg_stat_statements)
calls                Most-called queries (PostgreSQL pg_stat_statements)
bloat                PostgreSQL bloat or MySQL fragmentation
vacuum-stats         PostgreSQL autovacuum/autoanalyze health
replication-slots    PostgreSQL slot status, retained WAL, and lag
subscriptions        PostgreSQL logical-replication table progress
all                  Every applicable check in one report
```

Run one check with the same positional arguments and target flags:

```bash
pscale inspect locks <database> <branch> --org <org> --format json
pscale inspect seq-scans <database> <branch> --org <org> --replica --format json
pscale inspect table-sizes <database> <branch> --org <org> --keyspace '<keyspace>/<shard>' --format csv
```

Single checks support human, JSON, and CSV output. `inspect all` supports human and JSON; CSV is rejected because the checks have different result schemas.

## Engine and target semantics

- **Vitess/MySQL:** checks query `information_schema`, `mysql`, and `sys`. On sharded databases, one run reflects one shard's MySQL instance. Use `pscale sql <database> <branch> --query "SHOW VITESS_SHARDS"` to enumerate targets, then pass `--keyspace <keyspace>/<shard>`; append `@replica` when an exact tablet type is needed.
- **PostgreSQL:** checks query `pg_catalog` and `pg_stat` views for one PostgreSQL database selected by `--dbname`. `outliers` and `calls` require `pg_stat_statements`.
- Checks unavailable for the detected engine return a skipped explanation and, when available, a copy-pasteable `pscale insights` next step.
- Each check is bounded and has a 30-second query timeout. In `inspect all`, one failed check is recorded as skipped instead of aborting the remaining report.

## Investigation workflow

1. Confirm organization, database, branch, engine, and exact database/keyspace/shard target.
2. Run `inspect all ... --format json` with the default reader role.
3. Separate successful results, empty results, skipped checks, and failed/timed-out checks.
4. Follow the report's `next_steps` with `pscale insights queries|errors|anomalies|recommendations` for traffic-aware evidence.
5. Treat index, vacuum, lock, and query findings as diagnostic evidence—not automatic authorization to kill sessions or change schema.
6. For any write or destructive remediation, switch to the relevant skill/workflow and obtain explicit user approval.

## Related skills

- **pscale-insights** — server-side query statistics, errors, anomalies, and schema recommendations
- **pscale-sql** — deliberate one-off SQL with role and destructive-query safeguards
- **pscale-branch** — connection inspection and explicitly approved connection/query termination

## References

See [references/commands.md](references/commands.md) for the verified command synopsis, flags, and engine applicability.
