---
name: pscale-database
description: Create, list, show, update, delete, dump, discover regions, and manage PlanetScale databases, keyspaces, settings, PostgreSQL IP restrictions, database-level Vitess migration throttling, and aggressive cutover. Use when creating databases, deleting a Vitess keyspace, inspecting or changing database settings, discovering database regions or read-only regions, managing Postgres CIDR allowlists, setting future deploy-request throttler defaults, enabling or disabling aggressive cutover for future Vitess deploy requests, opening database shells, managing Vitess read-only regions, or dumping Vitess data. Triggers on database, create database, database regions, available regions, read-only regions, keyspace delete, database settings, database throttler, aggressive cutover, migration ratio, IP restriction, CIDR, database dump, read-only region, database shell, pscale shell.
---

# pscale database

Create, read, update, delete, and manage databases.

## Common Commands

```bash
# List all databases
pscale database list --org <org>

# Create database
pscale database create <database> --org <org>

# Show database details
pscale database show <database> --format json

# Inspect database-level defaults for future Vitess deploy requests
pscale database throttler show <database> --org <org> --format json

# Inspect database-level aggressive cutover for future Vitess deploy requests
pscale database aggressive-cutover show <database> --org <org> --format json

# Update one setting; boolean flags require an explicit value
pscale database update <database> --require-approval-for-deploy=true

# Inspect PostgreSQL IP restrictions
pscale database ip-restriction list <database> --format json

# Discover valid branch/read-only region targets for a database
pscale database regions list <database> --org <org> --format json
pscale database read-only-regions list <database> --org <org> --format json

# Delete database
pscale database delete <database>

# Delete a Vitess keyspace (destructive; inspect and approve first)
pscale keyspace delete <database> <branch> <keyspace>

# Open database shell
pscale shell <database> <branch>

# List configured Vitess read-only regions for a keyspace
pscale keyspace read-only-regions <database> <branch> <keyspace> --format json

# Add or resize a Vitess read-only region
pscale keyspace read-only-regions add <database> <branch> <keyspace> <region> \
  --cluster-size <size> --replicas <count>
pscale keyspace read-only-regions update <database> <branch> <keyspace> <region> \
  --cluster-size <size> --replicas <count>

# Dump from one separate Vitess read-only region
pscale database dump <database> <branch> \
  --keyspace <keyspace> \
  --read-only-region <region> \
  --output ./dump
```

## Workflows

### Database Creation

```bash
# Create new database
pscale database create my-new-db --org my-org

# Create main branch (automatic)
# Create development branch
pscale branch create my-new-db development
```

### Database Shell Access

```bash
# Open shell to specific branch
pscale shell my-database main

# Execute SQL directly
pscale shell my-database main --execute "SHOW TABLES"

# Run SQL from file
pscale shell my-database main < schema.sql
```

### Database settings

Inspect the complete current settings before changing anything, then pass only the intended update flags. Boolean flags must use `=true` or `=false`; merely naming a boolean flag is not a safe way to express operator intent.

```bash
pscale database show <database> --org <org> --format json

# Cross-engine examples
pscale database update <database> --org <org> --new-name <new-name>
pscale database update <database> --org <org> --restrict-branch-region=true

# Vitess-only examples
pscale database update <database> --org <org> --require-approval-for-deploy=true
pscale database update <database> --org <org> --insights-raw-queries=false
```

The CLI rejects Vitess-only flags for PostgreSQL databases. `--default-branch`, `--new-name`, `--production-branch-web-console`, and `--restrict-branch-region` work for both engines. Renaming or changing a default branch can affect automation and connection workflows; confirm the database and proposed diff before executing, then re-run `database show` to verify.

### Database-level Vitess migration throttler

This configuration sets the default migration-throttling ratio for future deploy requests on a Vitess database. It is distinct from both `pscale deploy-request throttler` for one deploy request and `pscale branch vtctld throttler` for tablet/keyspace throttler policy.

```bash
# Inspect current database defaults and eligible keyspaces
pscale database throttler show <database> --org <org> --format json

# Apply one ratio to all eligible keyspaces after explicit approval
pscale database throttler update <database> --org <org> \
  --ratio 25 \
  --format json

# Or set reviewed per-keyspace ratios; the flag is repeatable
pscale database throttler update <database> --org <org> \
  --configuration commerce=20 \
  --configuration analytics=10 \
  --format json

# Verify the resulting defaults
pscale database throttler show <database> --org <org> --format json
```

Pass exactly one update mode: `--ratio` or one or more `--configuration keyspace=ratio` values. Ratios range from 0 through 95; 0 effectively disables migration throttling, while 95 slows migrations the most. Because a change affects future schema deployment behavior, show the current configuration and complete proposed values, obtain explicit approval, then verify the returned and re-read configuration. The command rejects PostgreSQL databases.

### Database-level Vitess aggressive cutover

Aggressive cutover is a Vitess database setting for **future** deploy requests. When enabled, those deploy requests cut over more aggressively while waiting on table locks. It is not the same action as `pscale deploy-request force-cutover`, which affects one already-running deployment.

```bash
# Read current state
pscale database aggressive-cutover show <database> --org <org> --format json

# After reviewing lock/transaction impact and obtaining explicit approval
pscale database aggressive-cutover enable <database> --org <org> --format json
# or
pscale database aggressive-cutover disable <database> --org <org> --format json

# Verify persisted state
pscale database aggressive-cutover show <database> --org <org> --format json
```

The command rejects PostgreSQL databases. Enabling it can shorten cutover waits but may increase the chance that blocking application transactions are interrupted. Confirm the database, current setting, expected migration workload, application tolerance, and rollback choice before changing it. JSON output exposes the resulting `enabled` boolean; verify that field after the write.

### PostgreSQL IP restrictions

IP restrictions apply at the database level across all branches. List and inspect existing entries first, use IPv4 CIDRs (a single address is `/32`), and omit `--schema` or `--role` to apply the rule to all schemas or roles.

```bash
pscale database ip-restriction list <database> --org <org> --format json

pscale database ip-restriction create <database> --org <org> \
  --cidrs 203.0.113.10/32,198.51.100.0/24 \
  --schema public --role app_reader \
  --description "approved application networks"

pscale database ip-restriction show <database> <entry-id> --org <org> --format json
pscale database ip-restriction update <database> <entry-id> --org <org> \
  --cidrs 203.0.113.10/32
```

On update, only supplied flags change; an empty description clears it, while empty schema/role broadens the entry to all schemas/roles. Before `delete`, verify the entry ID and replacement access path, obtain approval, avoid `--force` unless explicitly authorized, and list the rules again afterward. Removing or narrowing the wrong rule can block database access; broadening one can expose it.

### Dump from a Vitess read-only region

Read-only regions are separate from `rdonly` or replica tablets in the primary region. Discover the configured regions for the target keyspace, select a ready region by slug, display name, or ID, and pass it explicitly to the dump command.

```bash
# Inspect region, cluster size, and replica count first
pscale keyspace read-only-regions <database> <branch> <keyspace> \
  --org <org> --format json

# Dump through a short-lived reader credential scoped to that region
pscale database dump <database> <branch> \
  --org <org> \
  --keyspace <keyspace> \
  --read-only-region <region> \
  --output ./pscale-dump
```

This workflow is Vitess-only. `--read-only-region` cannot be combined with `--replica` or `--rdonly`; those flags target tablet types in the primary region. Confirm the output path does not already exist and that local disk has sufficient space before starting a dump. If the selected region is not ready, wait rather than silently falling back to the primary region.

Current dump behavior propagates cursor-close and worker errors as a non-zero exit instead of logging and continuing. Treat any failed dump as incomplete even if some files exist; do not restore or publish partial output, and rerun into a fresh directory after resolving the underlying error.

### Manage Vitess read-only regions

Use `pscale database regions list <database>` to discover regions currently available to a database, `pscale database read-only-regions list <database>` to discover configured read-only regions, and `pscale size cluster list` to discover valid cluster sizes. The database-scoped read-only-region command is Vitess-only; for PostgreSQL databases the CLI fetches the database to determine its engine and rejects it before calling the read-only-regions endpoint. Add/update require at least one sizing flag supported by the API. Removing a region can disrupt region-scoped readers, dumps, and passwords: inventory those dependencies, confirm the exact keyspace and region, obtain approval, run the removal, and verify the remaining list.

```bash
pscale database regions list <database> --org <org> --format json
pscale database read-only-regions list <database> --org <org> --format json
pscale keyspace read-only-regions add <database> <branch> <keyspace> <region> \
  --org <org> --cluster-size <size> --replicas <count> --format json
pscale keyspace read-only-regions update <database> <branch> <keyspace> <region> \
  --org <org> --replicas <count> --format json
pscale keyspace read-only-regions remove <database> <branch> <keyspace> <region> \
  --org <org>
pscale keyspace read-only-regions <database> <branch> <keyspace> \
  --org <org> --format json
```

### Delete a Vitess keyspace

Keyspace deletion is destructive. Confirm the organization, database, branch, exact keyspace, routing/workflow dependencies, and recovery plan before asking for approval.

```bash
# Inspect the target and related branch state first
pscale keyspace show <database> <branch> <keyspace> --org <org> --format json
pscale branch vtctld get-keyspace-routing-rules <database> <branch> --org <org> --format json
pscale branch vtctld list-workflows <database> <branch> --org <org> \
  --keyspace <keyspace> --format json

# Interactive deletion requires typing database/branch/keyspace exactly
pscale keyspace delete <database> <branch> <keyspace> --org <org>

# Non-interactive deletion only after explicit approval
pscale keyspace delete <database> <branch> <keyspace> --org <org> --force --format json

# Verify absence and inspect remaining keyspaces
pscale keyspace list <database> <branch> --org <org> --format json
```

Without `--force`, the CLI first verifies the keyspace exists and requires a TTY confirmation of `<database>/<branch>/<keyspace>`. JSON/CSV or headless execution requires `--force`; never add it simply to bypass the safety prompt.

## Troubleshooting

### Cannot create database

**Error:** "Organization limit reached"

**Solution:** Upgrade plan or delete unused databases

### Shell connection fails

**Error:** "Authentication failed"

**Solution:**
```bash
# Re-authenticate
pscale auth logout && pscale auth login

# Verify branch exists
pscale branch list <database>
```

## Related Skills

- **pscale-branch** - Manage database branches
- **pscale-password** - Create connection passwords for databases

## References

See `references/commands.md` for complete command reference.
