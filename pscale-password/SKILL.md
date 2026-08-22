---
name: pscale-password
description: Create, list, show, update, renew, and delete branch connection passwords, and inspect Postgres roles and their connection targets. Use when creating connection strings for applications, managing database credentials, generating passwords for local development, routing reads to a Vitess read-only region, retrieving Postgres role details for a branch replica, regional read-only replica, or PgBouncer, rotating credentials, updating password names or CIDR restrictions, or finding credentials by name, status, or expiration. Triggers on password, connection string, database credentials, create password, show password, update password, CIDR, read-only region password, password status, Postgres role, role get, role status, role expiration, default Postgres role, read-only replica, PgBouncer connection.
---

# pscale password

Create, list, filter, renew, and delete branch passwords for database connections. The `pscale password` command group is for Vitess databases; use `pscale role` for Postgres branch credentials.

## Common Commands

```bash
# Create password
pscale password create <database> <branch> <password-name>

# Create a reader password scoped to one separate Vitess read-only region
pscale keyspace read-only-regions <database> <branch> <keyspace> --format json
pscale password create <database> <branch> <password-name> \
  --read-only-region <region> \
  --format json

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

# Show password metadata by ID or exact name
pscale password show <database> <branch> <password-id> --format json
pscale password show <database> <branch> --name production-app --format json

# Update password metadata or CIDR restrictions without rotating the secret
pscale password update <database> <branch> <password-id> --new-name production-app-v2 --format json
pscale password update <database> <branch> --name production-app --cidrs 10.0.0.0/8,192.168.1.1/32 --format json

# Delete password
pscale password delete <database> <branch> <password-id>
```

`--name` performs a substring match. Password status values are `active`, `renewable`, and `expired`. List output is limited to one page by default; request subsequent pages with `--page` when needed.

When `--read-only-region` is present, the default role is `reader`, the created password is labeled as a read-only-region credential, and `--replica` is rejected. Use the region slug, display name, or ID returned by `pscale keyspace read-only-regions`. The plaintext secret is shown only at creation time: capture it directly into an approved secret manager and never print it in logs or commit it.

### Show or update Vitess password metadata

`pscale password show` returns metadata only. The secret cannot be retrieved after create or renew. `show`, `update`, and `delete` can identify a password by ID or by `--name`; use IDs when names are ambiguous.

```bash
# Inspect metadata before changing it
pscale password show <database> <branch> <password-id> --org <org> --format json
pscale password show <database> <branch> --org <org> --name <password-name> --format json

# Change the display name without rotating the password
pscale password update <database> <branch> <password-id> --org <org> \
  --new-name <new-name> \
  --format json

# Replace CIDR restrictions; pass an empty value to clear all restrictions
pscale password update <database> <branch> --org <org> \
  --name <password-name> \
  --cidrs 10.0.0.0/8,192.168.1.1/32 \
  --format json
pscale password update <database> <branch> --org <org> \
  --name <password-name> \
  --cidrs "" \
  --format json

# Verify the metadata after the write
pscale password show <database> <branch> <password-id> --org <org> --format json
```

Updating a name or CIDR allowlist does not rotate the secret. Treat updates as credential-access writes: show the target password metadata, exact new name/CIDRs, and clearing behavior before asking for approval, then verify with `show` or `list`. Use create/delete or `renew` only when the user needs a new secret.

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

### Region-scoped read access

```bash
# Discover configured regions and confirm the intended target is ready
pscale keyspace read-only-regions <database> <branch> <keyspace> \
  --org <org> --format json

# Create a temporary, reader-only credential for that region
pscale password create <database> <branch> reporting-reader \
  --org <org> \
  --read-only-region <region> \
  --role reader \
  --ttl 24h \
  --format json
```

Use `--read-only-region` when reads must stay in one separate region. Use `--replica` instead when reads may route to the primary region's replicas and all read-only regions. The two routing modes are mutually exclusive.

### Postgres role lookup and filtering

Postgres databases use roles instead of Vitess branch passwords. `pscale role default` is a read-only lookup for the default `postgres` role and does not rotate credentials. Use `pscale role reset-default` only when the user explicitly asks to reset default-role credentials and approves the connection impact. Role list/get/default output includes `status` and `expires_at`; listing supports pagination and name filtering plus status filters for `active`, `renewable`, `disabled`, and `expired`.

This workflow intentionally lives here because no dedicated `pscale-role` skill exists, and both command groups manage branch credentials.

```bash
pscale role list <database> <branch> \
  --name production \
  --status active \
  --page 1 \
  --per-page 100 \
  --format json
pscale role default <database> <branch> --format json

# Retrieve the same role for exactly one alternate connection target
pscale role get <database> <branch> <role-id> --org <org> --format json --replica
pscale role get <database> <branch> <role-id> --org <org> --format json --read-only-replica <region-slug>
pscale role get <database> <branch> <role-id> --org <org> --format json --bouncer <bouncer-name>
```

`--replica`, `--read-only-replica`, and `--bouncer` are mutually exclusive. A targeted response keeps the normal role shape but can change `username`, `access_host_url`, and `database_url`; PgBouncer URLs use port `6432`. A target-specific `NOT_FOUND` can mean either the role or the requested replica/PgBouncer was not found, so verify both identifiers before retrying. Treat any returned password or connection URL as a secret: capture it directly into an approved secret manager and never print it in logs or commit it.

## Troubleshooting

### Password not working

**Solution:** Inspect status and metadata first. For ordinary name or CIDR allowlist changes, use `password update`; delete/recreate or renew only when the secret itself has expired or must rotate.

```bash
pscale password list <database> <branch> --format json
pscale password show <database> <branch> <password-id> --format json
# After explicit approval; --cidrs replaces the entire allowlist
pscale password update <database> <branch> <password-id> --cidrs <cidr-allowlist> --format json
```

## Related Skills

- **pscale-service-token** - For CI/CD authentication (preferred over passwords)
- **pscale-database** - Database management

## References

See `references/commands.md` for complete command reference.
