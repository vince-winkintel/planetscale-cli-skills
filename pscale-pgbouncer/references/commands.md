# pscale pgbouncer command reference

> Help captured from the checksum-verified PlanetScale CLI v0.314.0 macOS arm64 release binary.

## pscale pgbouncer

```text
Manage dedicated PgBouncers for a PostgreSQL database branch.

Dedicated PgBouncers run separately from the database nodes and provide
connection pooling for primary or replica traffic. This is distinct from the
local PgBouncer on port 6432 and from pgbouncer.* parameters on
'pscale branch resize'.

This command is only available for PostgreSQL databases.

Usage:
  pscale pgbouncer [command]

Available Commands:
  create      Create a dedicated PgBouncer
  delete      Delete a dedicated PgBouncer
  list        List dedicated PgBouncers for a Postgres branch
  resize      Change a dedicated PgBouncer's size, replicas, target, or parameters
  show        Show a dedicated PgBouncer
```

## list and show

```text
pscale pgbouncer list <database> <branch> [flags]
pscale pgbouncer show <database> <branch> <name> [flags]
```

`list` has alias `ls`. Both accept root global flags, including `--org` and `--format human|json|csv`.

## create

```text
Usage:
  pscale pgbouncer create <database> <branch> [flags]

Flags:
      --name string             Name for the PgBouncer (optional; auto-generated if omitted)
      --replicas-per-cell int   Number of replica servers per cell (default 1)
      --size string             PgBouncer size SKU (e.g. PGB_10)
      --target string           Traffic target: primary, replica, or replica_az_affinity (required)
```

## resize

```text
Usage:
  pscale pgbouncer resize <database> <branch> <name> [flags]
  pscale pgbouncer resize [command]

Available Commands:
  cancel      Cancel unfinished resize requests for a dedicated PgBouncer
  status      Show the latest resize request for a dedicated PgBouncer

Flags:
      --parameters stringArray   Set a PgBouncer parameter as namespace.name=value (e.g. pgbouncer.default_pool_size=100). Repeatable.
      --replicas-per-cell int    Number of PgBouncer replica servers per cell (default 1)
      --size string              PgBouncer size SKU (e.g. PGB_10)
      --target string            Traffic target: primary, replica, or replica_az_affinity
      --wait                     Wait for the resize request to complete before returning
      --wait-timeout duration    Maximum time to wait for the resize request to complete with --wait (default 10m0s)
```

## resize status and cancel

```text
pscale pgbouncer resize status <database> <branch> <name> [flags]
pscale pgbouncer resize cancel <database> <branch> <name> [flags]
```

## delete

```text
Usage:
  pscale pgbouncer delete <database> <branch> <name> [flags]

Aliases:
  delete, rm

Flags:
      --force   Delete a PgBouncer without confirmation
```

All subcommands accept root global flags: `--api-token`, `--api-url`, `--config`, `--debug`, `--format`, `--no-color`, `--org`, `--service-token`, and `--service-token-id`.
