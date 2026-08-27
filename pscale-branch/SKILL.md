---
name: pscale-branch
description: Create, rename, protect, delete, promote, diff, switchover, restore, inspect query patterns, and manage PlanetScale database branches, Postgres maintenance/extensions/parameters, Vitess VTGate capacity, tablet throttling, keyspace routing rules, and Vitess workflows. Use when creating development branches for schema changes, restoring a PostgreSQL branch to a point in time, renaming branches, changing deletion protection, switching a Postgres primary to a replica, running Postgres branch maintenance, listing available Postgres extensions, viewing schema diffs, changing Postgres branch size, inspecting or resizing VTGates, inspecting or replacing live keyspace routing rules, changing tablet throttler rules, promoting branches, or creating vtctld MoveTables workflows. Essential for schema migration workflows and branch-level query analysis. Triggers on branch, create branch, restore point, point-in-time recovery, PITR, rename branch, deletion protection, branch switchover, primary switchover, branch maintenance, Postgres maintenance, extensions, schema diff, query patterns, resize branch, Postgres parameters, VTGate, tablet throttler, keyspace routing rules, routing rules, vtctld, promote branch, MoveTables, global keyspace.
---

# pscale branch

Create, delete, diff, and manage database branches.

## Common Commands

```bash
# Create branch from main
pscale branch create <database> <branch-name>

# Create branch from specific source
pscale branch create <database> <branch-name> --from <source-branch>

# Restore a new Postgres branch to a point in time (write; inspect and approve first)
pscale branch create <database> <branch-name> \
  --from <source-branch> \
  --restore-point <RFC3339-timestamp> \
  --cluster-size <postgres-cluster-size> \
  --wait \
  --format json

# List the default page (up to 100 branches)
pscale branch list <database>

# Page through larger branch sets
pscale branch list <database> --page 2 --per-page 100 --format json

# Show branch details
pscale branch show <database> <branch-name>

# Rename a branch or change deletion protection (write; inspect and approve first)
pscale branch update <database> <branch-name> --new-name <new-name> --format json
pscale branch update <database> <branch-name> --deletion-protected=true --format json

# Inspect branch infrastructure/pods (supports Postgres and Vitess)
pscale branch infra <database> <branch-name> --format json

# List available extensions on a Postgres branch cluster image
pscale branch extensions list <database> <branch-name> --format json

# Start Postgres branch image maintenance (operational write; inspect and approve first)
pscale branch maintenance run <database> <branch-name> --format json

# Start a Postgres primary switchover (operational write; inspect and approve first)
pscale branch switchover <database> <branch-name> --candidate <replica-name> --format json
pscale branch switchover list <database> <branch-name> --format json
pscale branch switchover show <database> <branch-name> <switchover-id> --format json

# View schema diff
pscale branch diff <database> <branch-name>

# View schema
pscale branch schema <database> <branch-name>

# Inspect configurable Postgres parameters before changing them
pscale branch parameters list <database> <branch-name> --format json

# Queue one Postgres branch change request for size, replicas, and/or parameters
pscale branch resize <database> <branch-name> \
  --cluster-size PS_10_GCP_X86 \
  --replicas 2 \
  --parameters pgconf.max_connections=500 \
  --wait

# Inspect or cancel the latest queued change request
pscale branch resize status <database> <branch-name> --format json
pscale branch resize cancel <database> <branch-name> --format json

# Inspect and resize VTGates on a Vitess production branch
pscale branch vtgate show <database> <branch-name> --format json
pscale branch vtgate resize <database> <branch-name> \
  --vtgate-size VTG_320 \
  --vtgate-autoscaling \
  --vtgate-count 2 \
  --vtgate-max-count 8 \
  --vtgate-target-cpu-utilization 50 \
  --format json
pscale branch vtgate resize status <database> <branch-name> --format json

# Inspect live branch connections (Postgres and Vitess)
pscale branch connections show <database> <branch-name> --format json
pscale branch connections top <database> <branch-name>

# Download a branch query patterns CSV report
pscale branch query-patterns download <database> <branch-name> --output query-patterns.csv

# List/show generated branch query pattern reports
pscale branch query-patterns list <database> <branch-name> --format json
pscale branch query-patterns show <database> <branch-name> <report-id> --format json

# Delete a stale query pattern report only after explicit approval
pscale branch query-patterns delete <database> <branch-name> <report-id> --format json

# Stream the CSV to stdout for pipelines
pscale branch query-patterns download <database> <branch-name> --output - > query-patterns.csv

# Inspect Vitess routing rules and tablet state
pscale branch routing-rules get <database> <branch-name>
pscale branch vtctld get-routing-rules <database> <branch-name>
pscale branch vtctld get-keyspace-routing-rules <database> <branch-name> --format json
pscale branch vtctld get-shard <database> <branch-name> --keyspace <keyspace> --shard <shard>
pscale branch vtctld list-tablets <database> <branch-name> --format json

# Inspect one tablet's throttler state before proposing a change
pscale branch vtctld throttler status <database> <branch-name> \
  --tablet-alias <zone-tablet-alias> --format json

# Create a Vitess MoveTables workflow whose generated sequence tables live in a global keyspace
pscale branch vtctld move-tables create <database> <branch-name> \
  --workflow <workflow> \
  --source-keyspace <source-keyspace> \
  --target-keyspace <target-keyspace> \
  --all-tables \
  --sharded-auto-increment-handling REPLACE \
  --global-keyspace <unsharded-global-keyspace>

# Delete branch
pscale branch delete <database> <branch-name>

# Promote to production
pscale branch promote <database> <branch-name>
```

## Workflows

### Paginate branch inventory

`pscale branch list` returns one page with up to 100 branches by default. For databases with larger branch inventories, request subsequent pages explicitly with `--page`; use `--format json` for automation and stop when a page is empty.

```bash
pscale branch list <database> --page 1 --per-page 100 --format json
pscale branch list <database> --page 2 --per-page 100 --format json
```

### Schema Migration Workflow (Standard)

```bash
# 1. Create development branch
pscale branch create my-database feature-migration --from main

# 2. Make schema changes (via shell, ORM, or direct SQL)
pscale shell my-database feature-migration
# ... run ALTER TABLE, CREATE TABLE, etc.

# 3. View changes
pscale branch diff my-database feature-migration

# 4. Create deploy request (safer than direct promotion)
pscale deploy-request create my-database feature-migration

# 5. Deploy via deploy request (see pscale-deploy-request)
```

### Quick Branch for MR/PR

```bash
# Match PlanetScale branch to your MR/PR branch
BRANCH_NAME="feature-add-user-preferences"
pscale branch create my-database $BRANCH_NAME --from main
```

See `scripts/create-branch-for-mr.sh` for automation.

### Restore a Postgres branch to a point in time

`pscale branch create --restore-point` creates a new PostgreSQL branch from a point-in-time recovery timestamp. This is a write that can allocate billable resources. Confirm the organization, database, source branch, timestamp, target branch name, cluster size, and retention/recovery objective with the user before running it.

If `--cluster-size` is omitted, a restore-point branch defaults to `PS-10`, a billable non-development size, rather than `PS_DEV`; always pass an explicit size. `--from` may be omitted only when `--restore <backup-id>` is supplied; with `--restore-point` and no `--restore`, the CLI requires `--from` and resolves the covering backup from that parent branch and timestamp. Prefer passing the source branch explicitly in automation.

```bash
# Inspect the intended source branch and its current state first
pscale branch show <database> <source-branch> --org <org> --format json

# After explicit approval, create and wait for the recovered branch
pscale branch create <database> <new-branch> --org <org> \
  --from <source-branch> \
  --restore-point <RFC3339-timestamp> \
  --cluster-size <postgres-cluster-size> \
  --wait \
  --format json

# Verify the resulting branch rather than relying only on the create exit code
pscale branch show <database> <new-branch> --org <org> --format json
```

Use an absolute RFC 3339 timestamp such as `2026-08-25T13:30:00Z`; do not infer a timezone or silently round the requested recovery point. The flag is PostgreSQL-only. The CLI permits `--restore <backup-id>` with `--restore-point` even when `--from` is omitted; in that mode, the recovery source is the supplied backup. Without `--restore`, the CLI resolves the backup needed by the API from the required parent branch and timestamp. If the user supplied a specific backup ID, read back both the backup and timestamp before creating the branch. The CLI still rejects combining `--restore-point` with `--seed-data`. If creation fails or times out, treat the outcome as unconfirmed and inspect the target branch before retrying.

### Schema Comparison

```bash
# Compare branch schema with main
pscale branch diff <database> <branch-name>

# View full branch schema
pscale branch schema <database> <branch-name>

# Export schema to file
pscale branch schema <database> <branch-name> > schema.sql
```

### Branch infrastructure

`pscale branch infra` shows branch infrastructure/pod state for Postgres and Vitess branches. Prefer JSON output when an agent needs to inspect or compare infrastructure state.

```bash
pscale branch infra <database> <branch-name> --org <org> --format json
```

Use this for read-only diagnostics. Do not infer that a schema/deploy operation is safe solely from infra output; combine it with branch status, schema diff, and deploy-request checks.

### Postgres branch extensions

`pscale branch extensions list` is read-only and returns the extensions available on the branch's current cluster image. It is not an inventory of installed `CREATE EXTENSION` state inside a database.

```bash
pscale branch extensions list <database> <branch> --org <org> --format json
```

There is no CLI command to enable an extension. Use `pscale sql` for reviewed SQL such as `CREATE EXTENSION`, and use `pscale branch resize --parameters` only for preload-library configuration when the parameter catalog shows that a parameter is available.

### Rename or protect a branch

`pscale branch update` supports both Vitess and Postgres branches. It sends only flags explicitly provided and requires at least one of `--new-name` or `--deletion-protected`. Renames can break connection configuration, deployment jobs, scripts, and branch references; disabling deletion protection increases removal risk.

```bash
# Inspect the current branch first
pscale branch show <database> <branch> --org <org> --format json

# After reviewing downstream references and receiving explicit approval
pscale branch update <database> <branch> --org <org> \
  --new-name <new-name> \
  --deletion-protected=true \
  --format json

# Use an explicit false value to remove protection after approval
pscale branch update <database> <branch> --org <org> \
  --deletion-protected=false --format json

# Verify using the resulting branch name
pscale branch show <database> <resulting-branch-name> --org <org> --format json
```

Before a rename, inventory application connection settings, CI/CD jobs, deploy-request automation, and project `.pscale.yml` references. Show the complete proposed update and obtain explicit approval. If renaming and changing deletion protection together, verify both returned fields rather than assuming an all-or-nothing update.

### Postgres primary switchover

`pscale branch switchover` starts a Postgres-only primary switchover and returns immediately; it does not wait for completion. On a replicated branch, PlanetScale promotes the named `--candidate` from `branch infra`, or selects one when the flag is omitted. A single-instance branch has no replica to promote, so PlanetScale restarts the instance in place and the branch is unavailable while it returns. Writes are briefly interrupted in either case.

```bash
# Inspect instance names, roles, and replica availability
pscale branch infra <database> <branch> --org <org> --format json

# After confirming impact, target, and rollback/incident plan with the user
pscale branch switchover <database> <branch> --org <org> \
  --candidate <replica-name> --format json

# Re-read infra until the primary role and instance health are clear
pscale branch infra <database> <branch> --org <org> --format json

# Inspect switchover history/status if the create result is unclear
pscale branch switchover list <database> <branch> --org <org> --format json
pscale branch switchover show <database> <branch> <switchover-id> --org <org> --format json
```

Only one switchover can run on a branch at a time. If the create response contains a switchover ID, keep it with the incident notes and use `switchover show` for read-only status/detail lookup. Do not pass `--candidate` for a branch without replicas. A failed switchover has an unconfirmed outcome: the primary may still have moved and the CLI does not roll it back. Re-check `branch infra` and switchover history before any retry. Treat this as an availability-impacting operational write that always requires explicit approval.

### Postgres branch maintenance

`pscale branch maintenance run` starts asynchronous Postgres branch image maintenance. PlanetScale applies the image upgrade to replicas first, then switches over from the old primary to an upgraded replica. Expect seconds of unavailability during the switchover, and expect all direct connections to be terminated; applications must rely on retry logic. A single-instance branch has no replica to promote and is unavailable until the instance returns.

```bash
# Inspect instance topology and make sure no resize/change request is in progress
pscale branch infra <database> <branch> --org <org> --format json
pscale branch resize status <database> <branch> --org <org> --format json

# After explicit approval for the target and impact
pscale branch maintenance run <database> <branch> --org <org> --format json

# Optionally include a PostgreSQL minor-version upgrade during maintenance
pscale branch maintenance run <database> <branch> --org <org> \
  --update-postgres-minor-version \
  --format json

# Track async progress through branch infrastructure
pscale branch infra <database> <branch> --org <org> --format json
```

Maintenance cannot start while a `branch resize` change request is in progress. Treat this as an availability-impacting operational write: show the target branch, topology, expected connection termination/unavailability, minor-version choice, and incident/rollback plan before asking for approval.

### Connection inspection and safe termination

`pscale branch connections` replaced the older MySQL-only process view with a shared Postgres/Vitess connection view. Prefer JSON output for agent workflows so action IDs are explicit and not truncated.

```bash
# Inspect current connections once
pscale branch connections show <database> <branch-name> --format json

# Watch live connection activity
pscale branch connections top <database> <branch-name>

# Cancel a query only after confirming the query_id with the user
pscale branch connections kill <database> <branch-name> <query-id> --query

# Terminate a connection only after explicit user approval
pscale branch connections kill <database> <branch-name> <connection-id>

# Postgres only: terminate a transaction after explicit user approval
pscale branch connections kill-transaction <database> <branch-name> <transaction-id>
```

Treat `kill` and `kill-transaction` as destructive operational actions: show the selected row, explain the effect, get confirmation, run exactly one action, then verify with `connections show`.

### Query pattern reports

`pscale branch query-patterns` manages branch-level query pattern reports for query-shape analysis before tuning indexes, schema, or application query patterns. `list` and `show` are read-only. `download` generates/polls/downloads a CSV report. `delete` removes one generated report and requires explicit approval for the exact report ID.

```bash
# List generated reports, paging by cursor when needed
pscale branch query-patterns list <database> <branch-name> --org <org> --format json
pscale branch query-patterns list <database> <branch-name> --org <org> \
  --starting-after <cursor> \
  --limit 100 \
  --format json

# Inspect one report before downloading or deleting it
pscale branch query-patterns show <database> <branch-name> <report-id> --org <org> --format json

# Download with an explicit output path
pscale branch query-patterns download <database> <branch-name> --org <org> --output query-patterns.csv

# If --output is omitted, pscale writes a timestamped file in the current directory:
# query-patterns-<organization>-<database>-<branch>-<timestamp>.csv
pscale branch query-patterns download <database> <branch-name> --org <org>

# Use --output - to write the CSV to stdout for shell pipelines
pscale branch query-patterns download <database> <branch-name> --org <org> --output - > query-patterns.csv

# Delete only after confirming the exact report ID and target branch
pscale branch query-patterns delete <database> <branch-name> <report-id> --org <org> --format json
```

The command group requires Query Insights to be enabled for the database. A not-found error can mean either the branch/report does not exist or Query Insights is disabled. Prefer an explicit `--output` path in automation so downstream analysis can find the CSV deterministically; use `--output -` when a pipeline should consume the CSV from stdout. For deletion, `--force` only skips the prompt; it is not approval. Re-run `list` or `show` after deletion and verify the report is gone.

### Change a Postgres branch

`pscale branch resize` queues one asynchronous change request that can combine cluster size, replica count, and configuration parameter changes. At least one of `--cluster-size`, `--replicas`, or repeatable `--parameters namespace.name=value` is required. This command rejects MySQL databases; use `pscale keyspace resize` for Vitess keyspaces.

```bash
# Inspect the parameter catalog first. The bare `parameters` form is equivalent.
pscale branch parameters list <database> <branch-name> --org <org> --format json
pscale branch parameters list <database> <branch-name> --org <org> --namespace pgconf --format json

# List valid Postgres cluster sizes
pscale size cluster list --engine postgresql --org <org>

# Combine desired changes into one request and wait up to 20 minutes
pscale branch resize <database> <branch-name> --org <org> --format json \
  --cluster-size PS_10_GCP_X86 \
  --replicas 2 \
  --parameters pgconf.max_connections=500 \
  --wait --wait-timeout 20m

# Without --wait, inspect the latest request before assuming completion
pscale branch resize status <database> <branch-name> --org <org> --format json

# Cancel only while the change request is still queued
pscale branch resize cancel <database> <branch-name> --org <org> --format json
```

Review the parameter catalog's `restart` and `immutable` fields before proposing a change. Surface restart impact and capacity/cost impact to the user, then obtain approval before running `resize`. Request states include `queued`, `pending`, `resizing`, `completed`, and `canceled`; only the last two are terminal. A JSON no-op returns `{"result":"no_change","branch":"<branch>"}` rather than a change request. After completion, verify with both `resize status` and `branch show`.

### Resize Vitess VTGates

`pscale branch vtgate` manages VTGate capacity for Vitess production branches. Development branches cannot be resized. Inspect current capacity first, propose the exact size/count/autoscaling change and cost/capacity impact, and obtain approval before creating or canceling a resize.

```bash
# Read the applied configuration
pscale branch vtgate show <database> <branch> --org <org> --format json

# Fixed capacity: two VTGates per availability zone
pscale branch vtgate resize <database> <branch> --org <org> --format json \
  --vtgate-size VTG_320 \
  --vtgate-count 2 \
  --vtgate-autoscaling=false

# Autoscaling: minimum two and maximum eight VTGates per availability zone
pscale branch vtgate resize <database> <branch> --org <org> --format json \
  --vtgate-size VTG_320 \
  --vtgate-autoscaling \
  --vtgate-count 2 \
  --vtgate-max-count 8 \
  --vtgate-target-cpu-utilization 50

# Track the latest request; cancel only while it is still queued
pscale branch vtgate resize status <database> <branch> --org <org> --format json
pscale branch vtgate resize cancel <database> <branch> --org <org> --format json
```

At least one resize flag is required. Omitted flags preserve their current values; pass `--vtgate-autoscaling=false` explicitly to disable autoscaling. `--vtgate-count` is the per-availability-zone fixed count, or the minimum when autoscaling is enabled. After the request completes, verify both `resize status` and `vtgate show`; do not treat the requested values as applied while status is non-terminal.

### Routing rules

```bash
# Read routing rules from the branch schema snapshot
pscale branch routing-rules get <database> <branch-name>

# Vitess only: read live routing rules from vtctld/current cluster state
pscale branch vtctld get-routing-rules <database> <branch-name>

# Vitess only: read live keyspace-to-keyspace routing rules
pscale branch vtctld get-keyspace-routing-rules <database> <branch-name> --format json

# Update routing rules from a file
pscale branch routing-rules update <database> <branch-name> --routing-rules routing-rules.json

# Replace live keyspace routing rules (approved write)
pscale branch vtctld apply-keyspace-routing-rules <database> <branch-name> \
  --rules-file keyspace-routing-rules.json --format json
```

Use `vtctld get-routing-rules` when debugging propagation/live cluster state; use `routing-rules get` when you need the schema snapshot contract.

Keyspace routing rules are a separate live map of `from_keyspace` to `to_keyspace`. Before replacing them, save `get-keyspace-routing-rules` output, validate every entry includes both fields, show the complete proposed replacement, and obtain explicit approval. `apply-keyspace-routing-rules` requires exactly one of `--rules` or `--rules-file`; an empty `rules` array clears all live keyspace routing rules. By default the command rebuilds SrvVSchema objects; use `--cells` only to scope that rebuild deliberately, and use `--skip-rebuild` only with an explicit propagation plan. Re-run `get-keyspace-routing-rules` after the write and compare the full returned set.

### Vitess shard inspection

`pscale branch vtctld get-shard` reads a live shard record from vtctld, including tablet controls and denied tables. It is Vitess-only and requires both `--keyspace` and `--shard`.

```bash
# Inspect an unsharded keyspace
pscale branch vtctld get-shard <database> <branch-name> \
  --keyspace main \
  --shard '-'

# Inspect a sharded keyspace shard
pscale branch vtctld get-shard <database> <branch-name> \
  --keyspace commerce \
  --shard '-80'
```

### Vitess tablet throttler configuration

`pscale branch vtctld throttler update-config` mutates a Vitess keyspace's tablet-throttler policy. Inspect tablet aliases and current state first, show the exact keyspace/app/metrics/rule to the user, and obtain explicit approval before changing it.

```bash
# Discover tablets and inspect current throttler state
pscale branch vtctld list-tablets <database> <branch> --org <org> --format json
pscale branch vtctld throttler status <database> <branch> --org <org> \
  --tablet-alias <zone-tablet-alias> --format json

# Temporarily throttle an app at 50% for 30 minutes
pscale branch vtctld throttler update-config <database> <branch> --org <org> \
  --keyspace <keyspace> \
  --throttle-app rowstreamer \
  --throttle-app-ratio 0.5 \
  --throttle-app-duration 30m \
  --format json

# Remove one app throttle rule
pscale branch vtctld throttler update-config <database> <branch> --org <org> \
  --keyspace <keyspace> --unthrottle-app rowstreamer --format json

# Assign the metrics checked for one app
pscale branch vtctld throttler update-config <database> <branch> --org <org> \
  --keyspace <keyspace> --app-name vreplication \
  --app-metrics lag,loadavg --format json

# Change the keyspace's overall enable state explicitly
pscale branch vtctld throttler update-config <database> <branch> --org <org> \
  --keyspace <keyspace> --enabled=false --format json
```

Rules:

- Omit `--enabled` to preserve the current enable state; use `--enabled=true` or `--enabled=false` only for an approved state change.
- `--throttle-app` and `--unthrottle-app` are mutually exclusive.
- `--app-name` and `--app-metrics` must be passed together; `--app-name` cannot be empty.
- `--throttle-app-ratio` is between `0.00` and `1.00` and defaults to `1`; `--throttle-app-duration` defaults to one hour.
- `--threshold` changes the replication-lag threshold (in seconds) for the keyspace's default check; treat it as a keyspace-wide mutation that needs the same explicit approval as an app rule change.
- After a write, re-run `throttler status` on the relevant tablets and verify the returned policy. Do not assume one tablet proves cluster-wide propagation when the branch has multiple tablets.

### Vitess MoveTables and global sequences

`pscale branch vtctld move-tables create` supports `--global-keyspace`. Use it with `--sharded-auto-increment-handling REPLACE` when backing sequence tables for sharded auto-increment columns must be created in a specific unsharded keyspace.

```bash
pscale branch vtctld move-tables create <database> <branch-name> \
  --workflow move-commerce \
  --source-keyspace source \
  --target-keyspace commerce \
  --tables orders,order_items \
  --sharded-auto-increment-handling REPLACE \
  --global-keyspace global \
  --stop-after-copy
```

This command creates a data-movement workflow and starts it automatically unless `--auto-start=false` is supplied. Before running it, confirm the database, branch, source and target keyspaces, table selection, workflow name, and global keyspace with the user. Prefer `--stop-after-copy` or `--auto-start=false` when the workflow requires review before traffic switching.

### Branch Cleanup

```bash
# List all branches
pscale branch list <database>

# Delete merged/stale branches
pscale branch delete <database> <old-branch-name>
```

## Decision Trees

### Should I promote directly or use deploy request?

```
What's your environment?
├─ Production database → ALWAYS use deploy request (safe, reviewable)
├─ Pre-production database with team → Use deploy request (review workflow)
├─ Personal dev database → Direct promotion OK (but deploy request still safer)
└─ Experimental changes → Keep as branch, don't promote
```

### When to create a new branch?

```
What's your goal?
├─ Schema migration for feature → Create branch (from main)
├─ Testing schema changes → Create branch (isolated)
├─ Hotfix schema change → Create branch (from production)
├─ Experiment / spike → Create branch (delete after)
└─ Working on existing schema → Use existing branch
```

## Troubleshooting

### "Branch already exists"

**Solution:**
```bash
# Check existing branches
pscale branch list <database>

# Use different name or delete existing
pscale branch delete <database> <existing-branch>
```

### Schema diff shows no changes

**Causes:**
- No schema changes made yet
- Changes not committed in database session
- Comparing branch to itself

**Solution:**
```bash
# Verify schema was modified
pscale branch schema <database> <branch-name>

# Ensure you're in the right branch when making changes
pscale shell <database> <branch-name>
```

### Cannot delete branch

**Error:** "Branch is protected" or "Branch is a production branch"

**Solution:**
```bash
# Demote production branch first
pscale branch demote <database> <branch-name>

# Then delete
pscale branch delete <database> <branch-name>
```

### Branch creation fails

**Common causes:**
- Invalid branch name (spaces, special chars)
- Source branch doesn't exist
- Insufficient permissions

**Solution:**
```bash
# Use valid branch name (alphanumeric, hyphens, underscores)
pscale branch create <database> my-feature-branch --from main

# Verify source branch exists
pscale branch list <database> | grep main
```

## Related Skills

- **pscale-deploy-request** - Create deploy requests from branches (safer than direct promotion)
- **pscale-database** - Database management
- **drizzle-kit** - ORM-based schema migrations (generates SQL for pscale shell)
- **gitlab-cli-skills** - MR/PR integration (match branch names across tools)

## References

See `references/commands.md` for complete `pscale branch` command reference.

## Branch Lifecycle

```
main (production)
  │
  ├─ Create branch ──> feature-branch (development)
  │                         │
  │                         ├─ Make schema changes
  │                         ├─ Test changes
  │                         └─ Create deploy request
  │                               │
  └─ Deploy ←──────────────────────┘
```

## Best Practices

1. **Always create branches from main** for schema changes
2. **Use descriptive branch names** matching MR/PR numbers when applicable
3. **Run diff before deploy request** to review changes
4. **Delete merged branches** to keep branch list clean
5. **Use deploy requests** instead of direct promotion (reviewable, revertable)
6. **Test schema changes** in branch before deploying
