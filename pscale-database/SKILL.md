---
name: pscale-database
description: Create, list, show, update, delete, dump, and manage PlanetScale databases, settings, and PostgreSQL IP restrictions. Use when creating databases, inspecting or changing database settings, managing Postgres CIDR allowlists, opening database shells, managing Vitess read-only regions, or dumping Vitess data from a primary, replica, rdonly tablet, or separate read-only region. Triggers on database, create database, database settings, IP restriction, CIDR, database dump, read-only region, database shell, pscale shell.
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

# Update one setting; boolean flags require an explicit value
pscale database update <database> --require-approval-for-deploy=true

# Inspect PostgreSQL IP restrictions
pscale database ip-restriction list <database> --format json

# Delete database
pscale database delete <database>

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

### Manage Vitess read-only regions

Use `pscale region list` to discover available region slugs, and `pscale size cluster list` to discover valid cluster sizes. Add/update require at least one sizing flag supported by the API. Removing a region can disrupt region-scoped readers, dumps, and passwords: inventory those dependencies, confirm the exact keyspace and region, obtain approval, run the removal, and verify the remaining list.

```bash
pscale keyspace read-only-regions add <database> <branch> <keyspace> <region> \
  --org <org> --cluster-size <size> --replicas <count> --format json
pscale keyspace read-only-regions update <database> <branch> <keyspace> <region> \
  --org <org> --replicas <count> --format json
pscale keyspace read-only-regions remove <database> <branch> <keyspace> <region> \
  --org <org>
pscale keyspace read-only-regions <database> <branch> <keyspace> \
  --org <org> --format json
```

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
