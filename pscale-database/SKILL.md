---
name: pscale-database
description: Create, list, show, delete, dump, and manage PlanetScale databases. Use when creating new databases, listing available databases, viewing database details, deleting databases, opening database shells, discovering Vitess read-only regions, or dumping Vitess data from a primary, replica, rdonly tablet, or separate read-only region. Triggers on database, create database, list databases, database dump, read-only region, database shell, pscale shell.
---

# pscale database

Create, read, delete, and manage databases.

## Common Commands

```bash
# List all databases
pscale database list --org <org>

# Create database
pscale database create <database> --org <org>

# Show database details
pscale database show <database>

# Delete database
pscale database delete <database>

# Open database shell
pscale shell <database> <branch>

# List configured Vitess read-only regions for a keyspace
pscale keyspace read-only-regions <database> <branch> <keyspace> --format json

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
