# `pscale insights` command reference

Verified from the official PlanetScale CLI v0.308.0 macOS arm64 release binary.

## Command group

```text
pscale insights [command]

Available Commands:
  anomalies       List detected resource anomalies (CPU, memory, IOPS, rows read/written)
  errors          List queries that are failing with errors
  queries         List the top queries by a performance metric
  recommendations List schema recommendations (unused/duplicate indexes, bloat, missing indexes)

Persistent flag:
  --org string    The organization for the current user
```

All commands also accept the root output flag:

```text
-f, --format string  Show output in a specific format: human, json, csv (default "human")
```

Prefer JSON for agents and automation.

## Queries

```text
pscale insights queries <database> <branch> [flags]

Flags:
  --dir string      Sort direction: asc or desc (default "desc")
  --limit int       Number of queries to return (default 15)
  --period string   Time period to aggregate over (e.g. 1h, 24h)
  --sort string     Metric used to rank queries (default "totalTime")
```

Valid sort keys:

```text
totalTime, count, errorCount, rowsRead, rowsReturned, rowsAffected,
rowsReadPerReturned, p50Latency, p99Latency, maxLatency, cpuTime,
ioTime, lastRun
```

Examples:

```bash
pscale insights queries mydb main --org myorg --format json
pscale insights queries mydb main --org myorg --sort rowsReadPerReturned --period 24h --format json
pscale insights queries mydb main --org myorg --sort p99Latency --period 1h --format json
```

JSON query records include fields such as normalized SQL, statement type, keyspace, tables, index usage, query/error counts, latency metrics, rows read/returned/affected, CPU/I/O duration, and last-run time.

## Errors

```text
pscale insights errors <database> <branch> [flags]

Flags:
  --limit int       Number of errors to return (default 15)
  --period string   Time period to aggregate over (e.g. 1h, 24h)
```

```bash
pscale insights errors mydb main --org myorg --period 24h --format json
```

## Anomalies

```text
pscale insights anomalies <database> <branch> [flags]
```

```bash
pscale insights anomalies mydb main --org myorg --format json
```

Anomalies represent detected resource violations such as CPU, memory, IOPS, and rows read/written. JSON preserves active state and period/duration fields.

## Recommendations

```text
pscale insights recommendations <database> [flags]

Alias:
  recommendation
```

```bash
pscale insights recommendations mydb --org myorg --format json
```

Recommendations are database-scoped rather than branch-scoped. They can cover unused or duplicate indexes, bloated tables/indexes, missing indexes derived from production query patterns, and sequence overflow risks. JSON output includes proposed DDL; review and approve it separately before execution.

## Scope and failure interpretation

- `queries`, `errors`, and `anomalies` require `<database> <branch>`.
- `recommendations` requires only `<database>`.
- A branch-scoped not-found response can mean the branch is absent or Query Insights is disabled for the database.
- These commands analyze server-side production-traffic data. Use `pscale inspect` for point-in-time engine statistics and live connection-level checks.
