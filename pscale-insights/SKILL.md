---
name: pscale-insights
description: Query PlanetScale server-side performance insights, query errors, anomalies, and schema recommendations. Use when ranking slow or expensive queries, investigating production query failures or resource anomalies, reviewing index/schema recommendations, or when a user asks for pscale insights. Triggers on pscale insights, query insights, slow queries, query errors, anomalies, schema recommendations, missing indexes, unused indexes, database bloat.
---

# pscale insights

Use PlanetScale's server-side analysis of production traffic to investigate query performance and schema health. These commands complement the point-in-time, connection-level checks in `pscale inspect`.

## Common commands

```bash
# Rank queries by cumulative execution time (default sort)
pscale insights queries <database> <branch> --org <org> --format json

# Find inefficient read patterns over the last 24 hours
pscale insights queries <database> <branch> --org <org> \
  --sort rowsReadPerReturned --period 24h --limit 25 --format json

# Find high-tail-latency queries over the last hour
pscale insights queries <database> <branch> --org <org> \
  --sort p99Latency --period 1h --format json

# Inspect aggregated query failures and detected resource anomalies
pscale insights errors <database> <branch> --org <org> --period 24h --format json
pscale insights anomalies <database> <branch> --org <org> --format json

# Review database-level schema recommendations and their proposed DDL
pscale insights recommendations <database> --org <org> --format json
```

Always pass `--org` explicitly in agent workflows so the organization target is unambiguous. Prefer `--format json` so full normalized SQL, metrics, recommendation details, and proposed DDL remain machine-readable.

## Query ranking

`pscale insights queries` defaults to `--sort totalTime --dir desc --limit 15`. Supported sort keys are:

- `totalTime`, `count`, `errorCount`
- `rowsRead`, `rowsReturned`, `rowsAffected`, `rowsReadPerReturned`
- `p50Latency`, `p99Latency`, `maxLatency`
- `cpuTime`, `ioTime`, `lastRun`

Use `--dir asc|desc`, `--limit <n>`, and an API-supported period such as `1h` or `24h` to keep comparisons explicit. Do not compare differently scoped periods as though they represented the same workload.

## Investigation workflow

1. Confirm the organization, database, branch, and time window.
2. Rank queries by the metric related to the symptom (`totalTime`, `p99Latency`, `rowsReadPerReturned`, or `errorCount`).
3. Inspect `errors` and `anomalies` for the same branch and time window.
4. Run `pscale inspect all <database> <branch> --org <org> --format json` for live connection-level evidence.
5. Review database-level `recommendations` for index, bloat, and sequence-risk findings.
6. Summarize evidence separately from proposed changes.

A not-found response for branch-scoped insights can mean the database/branch does not exist **or** Query Insights is not enabled. Verify both before concluding that there is no data.

## Recommendation safety

Recommendations can include ready-to-apply DDL in JSON output. Treat that DDL as a proposal, not an instruction to execute automatically:

- Confirm engine, keyspace/schema, table, and production target.
- Check whether an index is still required by a low-frequency or seasonal workload.
- Review lock/runtime impact and use a branch plus deploy-request workflow where supported.
- Obtain explicit user approval before executing schema changes.
- Verify the result and keep a rollback plan.

## Related skills

- **pscale-inspect** — point-in-time, read-only diagnostics against one database connection target
- **pscale-sql** — deliberate one-off SQL queries with role and destructive-query safeguards
- **pscale-deploy-request** — reviewed Vitess/MySQL schema deployment workflow

## References

See [references/commands.md](references/commands.md) for the verified command synopsis and flags.
