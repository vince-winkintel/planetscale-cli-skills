---
name: pscale-password
description: Create, list, filter, renew, and delete branch connection passwords. Use when creating connection strings for applications, managing database credentials, generating passwords for local development, rotating credentials, or finding credentials by name or status. Triggers on password, connection string, database credentials, create password, password status, Postgres role.
---

# pscale password

Create, list, filter, renew, and delete branch passwords for database connections. The `pscale password` command group is for Vitess databases; use `pscale role` for Postgres branch credentials.

## Common Commands

```bash
# Create password
pscale password create <database> <branch> <password-name>

# List the default page (up to 100 passwords); omit branch to audit all branches
pscale password list <database> [branch]

# Audit renewable passwords across all branches
pscale password list <database> --status renewable --format json

# Filter and paginate passwords
pscale password list <database> <branch> \
  --name production \
  --status active \
  --page 1 \
  --per-page 100 \
  --format json

# Renew password
pscale password renew <database> <branch> <password-id>

# Delete password
pscale password delete <database> <branch> <password-id>
```

`--name` performs a substring match. Password status values are `active`, `renewable`, and `expired`. List output is limited to one page by default; request subsequent pages with `--page` when needed.

## Workflows

### Application Connection

```bash
# Create password for production app
pscale password create my-database main production-app

# Returns connection string:
# mysql://username:password@host/database

# Use in application environment variables
export DATABASE_URL="mysql://..."
```

### Local Development

```bash
# Create temporary password for local dev
pscale password create my-db main local-dev

# Delete when done
pscale password delete my-db main <password-id>
```

### Postgres role filtering

Postgres databases use roles instead of Vitess branch passwords. Role listing supports the same pagination and name filtering, with statuses `active`, `renewable`, `disabled`, and `expired`.

This workflow intentionally lives here because no dedicated `pscale-role` skill exists, and both command groups manage branch credentials.

```bash
pscale role list <database> <branch> \
  --name production \
  --status active \
  --page 1 \
  --per-page 100 \
  --format json
```

## Troubleshooting

### Password not working

**Solution:** Delete and recreate password (may have expired)

```bash
pscale password list <database> <branch>
pscale password delete <database> <branch> <old-id>
pscale password create <database> <branch> new-name
```

## Related Skills

- **pscale-service-token** - For CI/CD authentication (preferred over passwords)
- **pscale-database** - Database management

## References

See `references/commands.md` for complete command reference.
