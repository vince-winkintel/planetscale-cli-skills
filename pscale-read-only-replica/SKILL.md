---
name: pscale-read-only-replica
description: Manage dedicated PostgreSQL read-only replicas with PlanetScale CLI. Use when listing, inspecting, creating, resizing, configuring, or deleting Postgres read-only replicas, choosing replica regions, or changing replica parameters. Triggers on pscale read-only-replica, Postgres read replica, analytics replica, read capacity, replica region, replica parameters.
---

# pscale read-only-replica

Manage dedicated read-only capacity for a PlanetScale PostgreSQL branch. These named resources are separate from the primary branch cluster's replicas and from Vitess/MySQL read-only regions.

## Read before writing

```bash
# Inventory the branch when the replica name is unknown
pscale read-only-replica list <database> <branch> --org <org> --format json

# Or inspect one exact target when its name is already known; do not run both
pscale read-only-replica show <database> <branch> <name> --org <org> --format json
```

The command group checks the database kind itself and rejects Vitess databases, so a separate `database show` preflight is unnecessary. Use `pscale region list --org <org> --format json` to discover region slugs. Inspect the primary branch before choosing capacity; omitting `--cluster-size` inherits its size, which is usually the safest and least wasteful starting point. When an explicit override is intentional, use `pscale size cluster list --org <org> --engine postgresql --format json` and choose a fully qualified SKU matching the branch's provider and architecture.

List/show JSON serializes the underlying API model rather than the normalized human/CSV fields. Expect API-native nested objects and names, probe a representative response before automating, and use defensive access such as `.region.slug // .region.name // empty` and `.cluster_display_name // .cluster_name // empty` rather than assuming a fixed flattened schema.

To validate branch-level replica routing after provisioning, run a read-only query with the actual replica flag:

```bash
pscale sql <database> <branch> --org <org> --format json \
  --replica --query "SELECT 1"
```

`pscale sql --replica` and `pscale shell --replica` route reads across the branch's primary replicas and all read-only regions; they cannot pin a query to one named read-only replica. Validate a specific named/region target through the same application connection path or region-aware endpoint that production will use.

## Create

```bash
# Inspect primary sizing before deciding whether to override it
pscale branch show <database> <branch> --org <org> --format json

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

# Before deletion, send representative production reads through the exact
# application connection path/region that will remain and verify success,
# latency, and capacity there; --replica alone cannot prove a named target.

# Interactive confirmation (preferred when a TTY is available)
pscale read-only-replica delete <database> <branch> <name> --org <org>

# OR: non-interactive/JSON only after explicit approval
pscale read-only-replica delete <database> <branch> <name> --org <org> --format json --force
pscale read-only-replica list <database> <branch> --org <org> --format json
```

Never add `--force` merely to bypass an interactive prompt. JSON/CSV and other non-human execution cannot present the confirmation and fails without `--force`, which is why the headless example includes it. Run exactly one deletion form, then verify absence from the final list and confirm remaining read capacity.

## Related skills

- `pscale-password` — obtain connection details for named PostgreSQL replica targets
- `pscale-branch` — manage primary branch size, replicas, and parameters
- `pscale-database` — manage Vitess/MySQL read-only regions instead

## Reference

See `references/commands.md` for checksum-verified command help surfaces.
