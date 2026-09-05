---
name: pscale-read-only-replica
description: Manage dedicated PostgreSQL read-only replicas with PlanetScale CLI. Use when listing, inspecting, creating, resizing, configuring, or deleting Postgres read-only replicas, choosing replica regions, or changing replica parameters. Triggers on pscale read-only-replica, Postgres read replica, analytics replica, read capacity, replica region, replica parameters.
---

# pscale read-only-replica

Manage dedicated read-only capacity for a PlanetScale PostgreSQL branch. These named resources are separate from the primary branch cluster's replicas and from Vitess/MySQL read-only regions.

## Read before writing

```bash
pscale database show <database> --org <org> --format json
pscale branch show <database> <branch> --org <org> --format json
pscale read-only-replica list <database> <branch> --org <org> --format json
pscale read-only-replica show <database> <branch> <name> --org <org> --format json
```

Confirm the database is PostgreSQL and the target branch is ready. Use `pscale region list --org <org> --format json` to discover region slugs and `pscale size cluster list --org <org> --format json` to discover supported cluster sizes.

## Create

```bash
# The API defaults to one instance and the primary cluster size
pscale read-only-replica create <database> <branch> <name> \
  --region <region> --org <org> --format json

# Select capacity explicitly
pscale read-only-replica create <database> <branch> <name> \
  --region <region> \
  --replicas 2 \
  --cluster-size PS_10_GCP_X86 \
  --org <org> --format json
```

Confirm the organization, database, branch, unique name, region, cluster size, instance count, and expected cost before creating capacity. Creation is asynchronous: inspect `state` and `ready` in the returned object, then poll `list` or `show` until ready rather than assuming the resource can serve reads immediately.

## Update

```bash
# Inspect current state first
pscale read-only-replica show <database> <branch> <name> --org <org> --format json

# Change one or more supported dimensions
pscale read-only-replica update <database> <branch> <name> \
  --replicas 3 \
  --cluster-size PS_20_GCP_X86 \
  --parameters pgconf.max_connections=300 \
  --org <org> --format json

# Verify the asynchronous result
pscale read-only-replica show <database> <branch> <name> --org <org> --format json
```

At least one of `--replicas`, `--cluster-size`, or repeatable `--parameters namespace.name=value` is required. Parameter values must be greater than or equal to the primary branch's corresponding values. Review restart, connection, capacity, and cost impact before approval; then poll until the returned state is terminal and ready.

## Delete

Deletion removes dedicated read capacity and can break clients routed to the named replica. Inventory those clients, confirm replacement capacity and the exact target, obtain explicit approval, and verify the resource before using `--force` in headless/JSON execution.

```bash
pscale read-only-replica show <database> <branch> <name> --org <org> --format json
pscale read-only-replica delete <database> <branch> <name> --org <org> --format json --force
pscale read-only-replica list <database> <branch> --org <org> --format json
```

Never add `--force` merely to bypass an interactive prompt. Verify absence from the final list and confirm remaining read capacity.

## Related skills

- `pscale-password` — obtain connection details for named PostgreSQL replica targets
- `pscale-branch` — manage primary branch size, replicas, and parameters
- `pscale-database` — manage Vitess/MySQL read-only regions instead

## Reference

See `references/commands.md` for checksum-verified command help surfaces.
