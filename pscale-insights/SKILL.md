---
name: pscale-insights
description: Use when analyzing PlanetScale query performance, execution samples, query tags, error fingerprints, anomalies or correlated queries; reviewing, showing, or dismissing schema recommendations; listing or showing Insights Agent runs and schedules; or requesting approved agent run creation, cancellation, or schedule changes. Triggers on pscale insights, slow queries, query show, query summary, query samples, query tags, traffic budgets, sqlcommenter, query errors, anomalies, correlated queries, recommendation show, dismiss schema recommendation, missing or unused indexes, database bloat, Insights Agent, agent runs, and agent schedules.
---

# pscale insights

Use PlanetScale's server-side analysis of production traffic to investigate query performance and schema health. These commands complement the point-in-time, connection-level checks in `pscale inspect`.

## Common commands

```bash
# Rank queries by cumulative execution time (default sort)
pscale insights queries <database> <branch> --org <org> --format json

# Find inefficient read patterns over the last day
pscale insights queries <database> <branch> --org <org> \
  --sort rowsReadPerReturned --period 1d --limit 25 --format json

# Find high-tail-latency queries over the last hour
pscale insights queries <database> <branch> --org <org> \
  --sort p99Latency --period 1h --format json

# Drill into recent executions using fingerprint and keyspace from the query list
pscale insights queries samples <database> <branch> <fingerprint> --org <org> \
  --keyspace <keyspace> --period 1h --limit 25 --format json
pscale insights queries show <database> <branch> <query-id> --org <org> --format json
pscale insights queries summary <database> <branch> <fingerprint> --org <org> \
  --keyspace <keyspace> --period 1h --format json
pscale insights queries traffic-budgets <database> <branch> <fingerprint> --org <org> \
  --keyspace <keyspace> --page 1 --per-page 25 --format json

# Attribute load by friendly query-tag names from the Insights UI
pscale insights tags <database> <branch> --org <org> --format json
pscale insights tags summaries <database> <branch> --org <org> \
  --tags username --tags app --sort totalTime --format json

# Inspect aggregated query failures and detected resource anomalies
pscale insights errors <database> <branch> --org <org> --period 1d --format json
pscale insights errors show <database> <branch> <full-error-fingerprint> --org <org> --period 1d --format json
pscale insights anomalies <database> <branch> --org <org> --format json
pscale insights anomalies show <database> <branch> <anomaly-id> --org <org> --format json

# Review database-level schema recommendations and their proposed DDL
pscale insights recommendations <database> --org <org> --format json
pscale insights recommendations show <database> <number> --org <org> --format json
```

Always pass `--org` explicitly in agent workflows so the organization target is unambiguous. Prefer `--format json` so full normalized SQL, metrics, recommendation details, and proposed DDL remain machine-readable.

## Query ranking

`pscale insights queries` defaults to `--sort totalTime --dir desc --limit 15`. Supported sort keys are:

- `totalTime`, `count`, `errorCount`
- `rowsRead`, `rowsReturned`, `rowsAffected`, `rowsReadPerReturned`
- `p50Latency`, `p99Latency`, `maxLatency`
- `cpuTime`, `ioTime`, `lastRun`

Use `--dir asc|desc`, `--limit <n>`, and an API-supported period such as `1h` or `1d` to keep comparisons explicit. Do not compare differently scoped periods as though they represented the same workload.

## Execution samples

Each JSON record from `pscale insights queries` includes a `fingerprint` and `keyspace`. Pass both to `queries samples`; `--keyspace` is required because the same fingerprint can exist in more than one keyspace.

Samples expose individual executions, including start time, duration, user, rows read/returned, normalized SQL, errors, and attached tags. Use them to validate whether an aggregate represents one outlier or a recurring pattern. Query samples can contain sensitive SQL context, usernames, addresses, or tag values, so do not paste raw output into public issues or logs without review.

`queries show` reads one query execution by query ID. `queries summary` reads fingerprint-level aggregate statistics for one fingerprint/keyspace/time window. `queries traffic-budgets` lists Traffic Control budgets that apply to one fingerprint/keyspace and is paginated; empty later pages mean no rows on that page, not necessarily that no budget exists.

```bash
pscale insights queries show <database> <branch> <query-id> --org <org> --format json
pscale insights queries summary <database> <branch> <fingerprint> \
  --org <org> --keyspace <keyspace> --period 1h --format json
pscale insights queries traffic-budgets <database> <branch> <fingerprint> \
  --org <org> --keyspace <keyspace> --page 1 --per-page 25 --format json
```

Use the exact query ID, fingerprint, and keyspace returned by Insights. These Insights commands forward identifiers to the API as-is, and metrics query selectors are also forwarded opaquely; if a command returns no data or not-found, verify the selector before concluding the query had no activity or budgets.

## Error and anomaly details

The human `errors` table displays the full fingerprint. For JSON automation, copy `error_fingerprint` from the list and pass it unchanged to `errors show`; do not use a shortened display ID. The detail command returns individual failed executions, including users, keyspaces, statements, and error messages.

```bash
pscale insights errors <database> <branch> --org <org> --period 1h --format json
pscale insights errors show <database> <branch> <error_fingerprint> \
  --org <org> --period 1h --limit 25 --format json
```

`anomalies show` returns one anomaly plus queries whose activity correlates with it. Correlation is evidence for investigation, not proof that a query caused the resource event.

```bash
pscale insights anomalies <database> <branch> --org <org> --format json
pscale insights anomalies show <database> <branch> <anomaly-id> \
  --org <org> --format json
```

Treat detailed executions and normalized SQL as potentially sensitive. Compare the anomaly interval with query timing, metrics, and application changes before proposing a fix.

## Query tags

Use `pscale insights tags` to list observed sqlcommenter and system tag keys. The command returns friendly names matching the PlanetScale Insights UI, such as `app`, `controller`, and `username`.

```bash
# Show values observed for one friendly tag name
pscale insights tags show <database> <branch> app --org <org> --period 1h --format json

# Group workload by one or more repeatable tag keys
pscale insights tags summaries <database> <branch> --org <org> \
  --tags app --tags controller --sort p99Latency --period 1d --format json
```

List tags before using `show` or `summaries`. Pass friendly names, not internal `S...`/`B...` IDs. If a friendly name exists in both sources, disambiguate it as `sql:<name>` or `system:<name>`. Optional `--fingerprint` and `--keyspace` filters on `tags` narrow attribution to the intended query or keyspace.

## Investigation workflow

1. Confirm the organization, database, branch, and time window.
2. Rank queries by the metric related to the symptom (`totalTime`, `p99Latency`, `rowsReadPerReturned`, or `errorCount`).
3. Use the returned fingerprint and keyspace to inspect recent `queries samples` when execution-level evidence is needed.
4. List and summarize query tags to attribute the workload to applications, controllers, users, or other observed dimensions.
5. Inspect `errors` and `anomalies` for the same branch and time window, then drill into the relevant full error fingerprint or anomaly ID.
6. Use `queries summary`, `queries show`, or `queries traffic-budgets` when one query needs execution detail, aggregate context, or Traffic Control attribution.
7. Run `pscale inspect all <database> <branch> --org <org> --format json` for live connection-level evidence.
8. Review database-level `recommendations` and `recommendations show` for index, bloat, and sequence-risk findings.
9. Summarize evidence separately from proposed changes.

A not-found response for branch-scoped insights can mean the database/branch does not exist **or** Query Insights is not enabled. Verify both before concluding that there is no data.

## Recommendation safety

Recommendations can include ready-to-apply DDL in JSON output. Use `pscale insights recommendations show <database> <number>` to inspect one recommendation and its full DDL before proposing action. Treat that DDL as a proposal, not an instruction to execute automatically:

- Confirm engine, keyspace/schema, table, and production target.
- Check whether an index is still required by a low-frequency or seasonal workload.
- Review lock/runtime impact and use a branch plus deploy-request workflow where supported.
- Obtain explicit user approval before executing schema changes.
- Verify the result and keep a rollback plan.

Dismissal is also a write: `pscale insights recommendations dismiss <database> <number>`. Confirm the organization, database, and recommendation sequence number from the current list/show output, explain why the finding is inapplicable, and obtain explicit approval before dismissing it. Prefer an informative `--reason`; use `--force` only for already-approved non-interactive execution, then verify the recommendation state.

## Insights Agent runs and schedules

`insights agent` requires **CLI v0.354.0 or later** and works against the repository connected to a database. Runs belong to an organization/database/branch and review slow queries or implement schema recommendations, opening a pull request with their changes. List/show operations read state; starting a run is potentially billable work and an external repository write. Scheduling enables future work; cancellation mutates a pending/running run. A diagnostic request alone does not authorize any of these writes.

```bash
# Read-only discovery; list commands are the runnable parents, without a list child
pscale insights agent runs <database> <branch> --org <org> --format json
pscale insights agent runs show <database> <branch> <number> --org <org> --format json
pscale insights agent schedules <database> <branch> --org <org> --format json
```

Before creation, inspect fresh query fingerprints/keyspaces or database-level recommendation numbers with the commands above, confirm their eligibility on the intended branch, the connected repository, selected targets, cost, and intended changes. Obtain explicit approval for that exact scope. Choose **one** mode: up to five `--fingerprint` values with their shared `--keyspace`, or up to five integer `--schema-recommendation` numbers. Both selectors accept repetition or comma separation. Creation has no confirmation or dry-run flag; do not invoke it as a probe.

```bash
# After approval for this branch, connected repository, cost, and exact query targets
pscale insights agent runs create <database> <branch> --org <org> \
  --fingerprint <fingerprint> --keyspace <keyspace> --format json
# Alternative, after approval for these recommendations and repository changes
pscale insights agent runs create <database> <branch> --org <org> \
  --schema-recommendation <number> --format json
# Inspect the returned positive run number; creation success is not completed work
pscale insights agent runs show <database> <branch> <number> --org <org> --format json
# Only after exact-run cancellation and --force approval for a headless session
pscale insights agent runs cancel <database> <branch> <number> --org <org> --force --format json
pscale insights agent runs show <database> <branch> <number> --org <org> --format json
```

Inspect state, outcome, failure, stages, and any pull request before reporting success. Review proposed code/DDL separately; an agent run does not authorize merge, deployment, schema execution, or cleanup. After an ambiguous create result, inspect runs before retrying to avoid duplicate work. Cancellation is not a promise to revert repository changes or remove a pull request.

For schedules, inspect current state first and obtain explicit approval for the exact organization/database/branch, `slow_query` or `schema_recommendation` run type, enabled state, recurrence, local time, IANA time zone, repository impact, and ongoing cost. Scheduled slow-query runs select from the last 24 hours; schema-recommendation runs select the branch's open recommendations; runs with no targets are skipped. No manual fingerprint/recommendation selector is accepted on schedule update.

```bash
# After approval for this recurring work and its cost
pscale insights agent schedules update <database> <branch> slow_query --org <org> \
  --enabled=true --frequency week --day-of-week 1 --time 03:00 --time-zone UTC --format json
pscale insights agent schedules <database> <branch> --org <org> --format json
# After separate approval to disable future runs of this type
pscale insights agent schedules update <database> <branch> slow_query --org <org> \
  --enabled=false --format json
pscale insights agent schedules <database> <branch> --org <org> --format json
```

Always use `--enabled=true` or `--enabled=false` with `=`. With all three required positionals supplied, `--enabled false` sets enabled to **true** and leaves `false` as an extra positional argument; the CLI accepts and ignores that extra argument, so this form can enable recurring work instead of disabling it.

Schedule update requires at least one setting; omitted settings keep their current value. `--enabled=false` is an explicit write, not the effect of omission. Frequencies are `day`, `week`, `month`; weekly day is 0 (Sunday)–6, monthly day 1–31 (shorter months use their last day). Disabling a schedule is distinct from cancelling an active run. Read back the schedule and `next_run_at`; do not infer server defaults for a new schedule.

Use JSON for full objects: runs/schedules list returns an array, run create/show/cancel returns one run object, and schedule update returns one schedule object. Human run show includes targets, stages, summary and pull request; run creation/cancellation print status text. Human/CSV list output is a summary. Schedule update's human/CSV output is a **one-row list**, not a JSON array. See [agent command reference](references/agent-commands.md) for exact options, filters, compatibility, source, and complete help. A not-found result can also mean Insights Agent is not enabled for the organization; verify scope and availability without enabling it automatically. Treat SQL, run summaries, and repository details as potentially sensitive.

## Related skills

- **pscale-inspect** — point-in-time, read-only diagnostics against one database connection target
- **pscale-sql** — deliberate one-off SQL queries with role and destructive-query safeguards
- **pscale-deploy-request** — reviewed Vitess/MySQL schema deployment workflow

## References

See [references/commands.md](references/commands.md) for the verified command synopsis and flags.
