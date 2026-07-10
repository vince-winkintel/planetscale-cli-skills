---
name: pscale-import-d1
description: Import Cloudflare D1 SQLite exports into PlanetScale Postgres with pscale import d1. Use when migrating from Cloudflare D1, linting D1 exports, converting SQLite schema to PostgreSQL DDL, starting/resuming D1 imports, verifying row counts/content, or completing local migration state. Triggers on pscale import d1, Cloudflare D1 migration, D1 export, SQLite to Postgres import, pgloader, D1 verify.
---

# pscale import d1

Import a Cloudflare D1 database export into PlanetScale Postgres using `pscale import d1`.

## Capabilities

The `pscale import d1` command group supports offline Cloudflare D1 migrations. It lints a D1 SQL export, converts SQLite DDL to PostgreSQL DDL, loads data into a PlanetScale Postgres branch, stores local migration state, and verifies the import.

All commands support `--format json` through the global pscale flag; use JSON for agent automation.

## Prerequisites

```bash
# Export D1 using Wrangler first
wrangler d1 export <d1-database-name> --remote --output ./d1-export.sql

# Verify local import prerequisites such as pgloader
pscale import d1 doctor --format json
```

`start` requires `pgloader` on `PATH`. For small databases, `--method psql` uses `psql` for schema and `pgloader` for data; for larger exports, use `--method pgloader`.

### SQLite configuration isolation

pscale isolates its internal `sqlite3` calls from `~/.sqliterc` and forces batch, no-header output. User settings such as `.headers on` or `.mode column` therefore do not corrupt D1 import row-count and verification parsing. Integer parsing is strict, stderr stays separate from parsed output, and unusual SQLite identifiers are quoted correctly.

If a D1 import or verification fails with unexpected SQLite output, upgrade pscale to the current release and rerun the same migration step. Treat an `unexpected output` error on a current release as a real parsing/data problem, and preserve the reported output and stderr when troubleshooting.

## Recommended migration workflow

```bash
# 1. Lint the D1 export before touching PlanetScale
pscale import d1 lint --input ./d1-export.sql --format json

# 2. Preview the import plan and save a migration ID without loading data
pscale import d1 start <database> <branch> \
  --input ./d1-export.sql \
  --dry-run \
  --format json

# 3. Review lint output and generated migration ID from the dry-run
MIGRATION_ID=<migration-id-from-json>

# 4. Run the import after the user confirms the target database/branch
pscale import d1 start <database> <branch> \
  --input ./d1-export.sql \
  --migration-id "$MIGRATION_ID" \
  --method pgloader \
  --format json

# 5. Verify source/target counts, sequences, coercions, and content checks
pscale import d1 verify <database> <branch> \
  --migration-id "$MIGRATION_ID" \
  --input ./d1-export.sql \
  --format json

# 6. Mark local migration state complete when verification passes
pscale import d1 complete <database> <branch> --migration-id "$MIGRATION_ID" --format json
```

If `<branch>` is omitted, pscale uses the default branch. Prefer passing the branch explicitly in automation to avoid importing into the wrong target.

## Command map

| Command | Purpose | Typical use |
|---------|---------|-------------|
| `pscale import d1 doctor` | Check local prerequisites | Run before migration to confirm `pgloader` and toolchain availability |
| `pscale import d1 lint --input FILE` | Analyze D1 SQL export | Catch SQLite/D1 features that need manual handling |
| `pscale import d1 convert-schema --input FILE --output schema.sql` | Convert SQLite DDL to PostgreSQL DDL | Review generated schema before loading |
| `pscale import d1 start <database> [branch] --input FILE` | Lint, plan, and load data | Use `--dry-run` first; reuse `--migration-id` for the real run |
| `pscale import d1 status <database> [branch] --migration-id ID` | Show local migration state | Resume or inspect in-progress migration state |
| `pscale import d1 verify <database> [branch] --migration-id ID` | Verify row counts/content | Required before declaring migration complete |
| `pscale import d1 complete <database> [branch] --migration-id ID` | Mark local migration complete | Use only after successful verification |

## Safety rules for agents

1. Treat D1 import as a data migration: identify org, database, branch, export path, and method before running non-dry-run commands.
2. Always run `lint` and `start --dry-run` first; summarize warnings/errors and migration ID.
3. Do not run non-dry-run `start` or `complete` without explicit user confirmation of the target and source export.
4. Prefer `--format json` and preserve the JSON output path/summary for auditability.
5. Use an explicit branch argument and `--dbname` when the destination PostgreSQL database name is not `postgres`.
6. Verify after loading; do not call the migration complete until `verify` succeeds.

## Troubleshooting

### `pgloader` missing

Run:

```bash
pscale import d1 doctor
```

Install `pgloader`, then rerun `doctor`. Do not bypass this by starting a real import.

### Lint errors block import

Review the lint JSON. Common blockers include unsupported SQLite constructs, non-simple indexes, views, triggers, or type coercions that need manual review. Fix or consciously accept the migration plan before running `start`.

### Resume an interrupted migration

```bash
pscale import d1 status <database> <branch> --migration-id <existing-migration-id> --format json
pscale import d1 start <database> <branch> \
  --input ./d1-export.sql \
  --migration-id <existing-migration-id> \
  --format json
```

Use the same export file and target branch unless intentionally restarting the migration.

## References

See `references/commands.md` for the current `pscale import d1` command reference.
