---
name: pscale-pgbouncer
description: Manage dedicated PostgreSQL PgBouncers with PlanetScale CLI. Use when listing or inspecting dedicated poolers, creating primary or replica poolers, changing PgBouncer size, replicas, traffic target, or parameters, monitoring/canceling asynchronous resize requests, or deleting a dedicated PgBouncer. Triggers on pscale pgbouncer, dedicated PgBouncer, Postgres pooler, bouncer resize, replica pooler, PGB SKU.
---

# pscale pgbouncer

Manage dedicated PgBouncers for PlanetScale PostgreSQL branches. These are separate pooler services, not the local PgBouncer on port 6432 and not the `pgbouncer.*` parameters managed by `pscale branch resize`.

## Inspect before changing

```bash
pscale pgbouncer list <database> <branch> --org <org> --format json
pscale pgbouncer show <database> <branch> <name> --org <org> --format json
```

This command group rejects Vitess databases. Use JSON output to preserve the exact name, target, SKU, replica count, parameters, and lifecycle metadata.

## Create a dedicated PgBouncer

`--target` is required and accepts `primary`, `replica`, or `replica_az_affinity`. `--name` is optional and auto-generated when omitted; explicit names are at most 12 characters, and `primary` and `replica` are reserved. If `--size` is omitted, the API selects a default SKU.

The command help documents the explicit-name limit and reserved names.

```bash
pscale pgbouncer create <database> <branch> \
  --org <org> \
  --name read-pool \
  --target replica \
  --size PGB_10 \
  --replicas-per-cell 2 \
  --format json
```

Creation changes capacity and cost. Inspect the branch and existing poolers, propose the exact target/size/replica values, and obtain approval before creating one. Verify afterward with `show`.

## Resize or reconfigure

`resize` can combine size, replicas per cell, traffic target, and repeatable `namespace.name=value` parameters in one asynchronous request.

```bash
pscale pgbouncer resize <database> <branch> <name> \
  --org <org> \
  --size PGB_10 \
  --replicas-per-cell 2 \
  --target replica \
  --parameters pgbouncer.default_pool_size=100 \
  --wait --wait-timeout 20m \
  --format json
```

Inspect `show` first and surface capacity, cost, routing, restart, and connection impact. Pass only intended changes. Without `--wait`, poll the latest request:

```bash
pscale pgbouncer resize status <database> <branch> <name> \
  --org <org> --format json
```

`pending` and `resizing` are non-terminal; `completed` and `canceled` are terminal. A request that already matches the current configuration returns a `no_change` result rather than a resize ID. After completion, verify both `resize status` and `show`.

## Cancel an unfinished resize

```bash
pscale pgbouncer resize cancel <database> <branch> <name> \
  --org <org> --format json
```

Cancellation is an operational write. Confirm the latest request is unfinished, obtain approval, cancel exactly the intended pooler, then re-run `status` and `show`.

## Delete a dedicated PgBouncer

Deletion removes a connection endpoint and can break clients. Show the pooler, confirm no clients depend on it, present the exact database/branch/name, and get explicit approval. Prefer the interactive confirmation; reserve `--force` for already-approved non-interactive automation.

```bash
pscale pgbouncer show <database> <branch> <name> --org <org> --format json
pscale pgbouncer delete <database> <branch> <name> --org <org>

# Non-interactive only after explicit approval
pscale pgbouncer delete <database> <branch> <name> --org <org> --force
```

Verify deletion by listing the branch's remaining PgBouncers.

See [references/commands.md](references/commands.md) for captured command help.
