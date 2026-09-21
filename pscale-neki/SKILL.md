---
name: pscale-neki
description: Manage PlanetScale Neki branch resources with pscale. Use for Neki data topology, shards, branch-wide change requests, configuration profiles and extension sets, routers, sidecars, admin config, Neki profile maintenance, restore sizing overrides, target-specific inspection, inherited roles, and router/shard access context. Triggers on Neki, branch data-topology, branch shard, branch changes, Neki changes, branch config-profile, config-profile extensions, branch router, branch sidecar, branch admin, Neki restore, Neki profile maintenance, Neki inspect, Neki role, --router, or --shard.
---

# pscale-neki

Use this skill for Neki-specific PlanetScale CLI operations. Prefer `--format json`, pass explicit `--org`, inspect current state before writes, and verify by reading the target back after every mutation.

For exact command surfaces, read [references/commands.md](references/commands.md). Its help fences are captured from the verified binary; do not infer flags from older Postgres or Vitess commands.

## Safety model

- Creating Neki databases, branches, shards, config profiles, routers, and capacity changes can incur cost.
- Treat data-topology replacement, shard assignment, shard deletion, default-profile changes, admin/router/profile/sidecar updates, maintenance, and cancellation of pending changes as writes that require explicit user approval for the exact org, database, branch, and target.
- Use `--format json` for reads and writes, then poll or re-read the resource. Async profile/router/sidecar/admin changes must be checked through their `changes` commands until terminal.
- Never log or commit secrets, connection strings, role passwords, or SQL that contains sensitive data.
- JSON input for `branch data-topology update` must be a JSON object. `--format json` only controls output; it does not make stdin JSON.
- Sidecars and admins are managed as branch-owned components; use the CLI's show/list/update surfaces and do not assume they can be created or deleted independently.

## Branch-wide change requests

Use `branch changes` for one inventory across Neki admin, cluster, configuration-profile, router, and sidecar requests. Per-resource `changes` commands remain useful when the target component is already known.

```bash
# Inventory the branch, then narrow by target when needed
pscale branch changes list <database> <branch> --org <org> --format json
pscale branch changes list <database> <branch> --org <org> --format json \
  --target-type config-profile --page 1 --per-page 100

# Inspect the exact request before taking action
pscale branch changes show <database> <branch> <change-id> --org <org> --format json

# Operational write: run only after approval for this pending request
pscale branch changes cancel <database> <branch> <change-id> --org <org> --format json
```

`--target-type` accepts `admin`, `cluster`, `config-profile`, `router`, or `sidecar`; `--target-id` requires a target type and takes the API `target_id` from JSON output, not the resource name shown in human tables. List filters also include `--state`, `--completed-at`, `--page`, and `--per-page`. Do not use a state filter for a pre-maintenance gate: page through the unfiltered JSON inventory until a page is empty and treat every entry with `completed_at: null` as in flight. The CLI exposes page selection but does not auto-paginate `changes list`, so do not rely on one default page or a hard-coded state vocabulary.

JSON preserves the API change objects rather than reducing them to the human table. Cancellation is not a generic rollback: `show` the exact change immediately before canceling and require both `state: "pending"` and `can_delete: true`. Pending alone is insufficient, and non-pending, maintenance-driven, or otherwise uncancellable changes must not be canceled. Identify the target and impact, obtain explicit approval for that change ID, then re-run `show` and read back the affected component.

## Discovery

Start by confirming engine and branch readiness:

```bash
pscale database show <database> --org <org> --format json
pscale branch show <database> <branch> --org <org> --format json
```

For size choices, use Neki-scoped discovery rather than Postgres or MySQL defaults:

```bash
pscale size cluster list --org <org> --engine neki --format json
pscale branch config-profile parameters <database> <branch> <profile> --org <org> --format json
pscale branch router sizes <database> <branch> --org <org> --format json
pscale branch admin sizes <database> <branch> --org <org> --format json
```

## Creation And Access

Create Neki databases through `pscale-database`; that skill owns the complete command and operational workflow. Before handing off, confirm region, cluster size, replica count, storage bounds, and cost impact. The help documents `0` for single-node Postgres, not Neki, so confirm the supported Neki replica count and use `2` or more for high availability. Treat a timeout or interruption as an unconfirmed provisioning outcome and inspect `database show` before retrying.

Neki uses Postgres-style shell, SQL, and roles. `pscale sql` defaults to the reader role; use write-capable roles only after approval. Ephemeral Neki roles can take time to become connectable, and the CLI waits up to one minute before connecting. Role creation, reset, deletion, renewal, update, reassignment, inherited-role pairings, and persistent connection details follow `pscale-password`.

```bash
pscale role list <database> <branch> --org <org> --format json
pscale sql <database> <branch> --org <org> --format json --query "SELECT 1"
pscale shell <database> <branch> --org <org> --router <router-name>
pscale role get <database> <branch> <role-id> --org <org> --format json \
  --shard <shard-name> --router <router-name> --replica
```

For `role get`, the shard selector is the shard **name** returned by `branch shard list`; it is distinct from the shard ID accepted by `pscale inspect --shard`. Neki can combine `--shard`, `--router`, and `--replica`: router selection suffixes the username, while shard/replica selection is returned in libpq `options` and encoded into `database_url`. Do not expose returned role credentials, options, or database URLs in logs.

## Targeted Inspection

Use `pscale-inspect` for live, read-only checks pinned to one Neki connection target. Inventory the target first; inspect does not fan out across shards.

```bash
pscale branch shard list <database> <branch> --org <org> --format json
pscale branch router list <database> <branch> --org <org> --format json
# Primary-path evidence is the default
pscale inspect all <database> <branch> --org <org> \
  --shard <shard-id> --format json
# Select a router and/or replica only when that target path is intentional
pscale inspect all <database> <branch> --org <org> \
  --shard <shard-id> --router <router-name> --replica --format json
```

Unlike `role get`, `pscale inspect --shard` accepts the shard **ID**. `--shard` and `--router` are Neki-only, and Neki internal `__neki` relations are excluded from customer-facing diagnostic results.

## Branch Logs

`pscale logs` is owned by `pscale-branch` for both PostgreSQL and Neki branches. Use that skill for the exact help and safety guidance; Neki-specific filters include `--shard` and pod/server selection.


## Data Topology And Shards

Read the topology and shard inventory before proposing any change:

```bash
pscale branch data-topology get <database> <branch> --org <org> --format json
pscale branch data-topology ls <database> <branch> --org <org> --format json
pscale branch data-topology ls <database> <branch> --org <org> --shards --format json
pscale branch shard list <database> <branch> --org <org> --format json
```

`data-topology get` returns the cached topology and `synced_at`; a stale read can schedule an asynchronous refresh and briefly return the previous topology. `data-topology ls` renders relationships among databases, tables, shard groups, indexes, key ranges, and shards. `--shards` reverses that view to physical shard placement.

Topology replacement is high-impact. Review the complete JSON object, affected shards/profiles, routing impact, and recovery plan before applying it. Empty input, arrays, scalars, and malformed JSON are rejected.

```bash
pscale branch data-topology update <database> <branch> --org <org> --format json < topology.json
pscale branch data-topology get <database> <branch> --org <org> --format json
```

Shard creation, assignment, updates, and deletion are operational writes:

```bash
pscale branch shard show <database> <branch> <shard-id> --org <org> --format json
pscale branch shard create <database> <branch> --org <org> \
  --config-profile <profile> --count 2 --format json
pscale branch shard assign <database> <branch> <shard-id>... --org <org> \
  --config-profile <profile> --format json
pscale branch shard update <database> <branch> <shard-id> --org <org> \
  --display-name <name> --format json
pscale branch shard delete <database> <branch> <shard-id> --org <org> \
  --force --format json
```

`list` and `show` identify whether each shard is authoritative. Assignment can return a mixed result with `assigned`, `unchanged`, and `failed` entries, so inspect every result instead of treating command success as all-or-nothing. Show current shard/profile state, obtain approval for exactly one intended mutation, and verify with `list` or `show`. Add `--force` to deletion only after approval for that exact shard.

## Configuration Profiles

Profiles define infrastructure shared by groups of Neki shards. Inspect the current profile, default, parameter catalog, and extension catalog before changing capacity or behavior.

```bash
pscale branch config-profile list <database> <branch> --org <org> --format json
pscale branch config-profile show <database> <branch> <profile> --org <org> --format json
pscale branch config-profile default <database> <branch> --org <org> --format json
pscale branch config-profile parameters <database> <branch> <profile> --org <org> --format json
pscale branch config-profile extensions <database> <branch> <profile> --org <org> --format json

# Examples of approved writes
pscale branch config-profile create <database> <branch> <profile> --org <org> \
  --cluster-size <size> --replicas 2 --format json
pscale branch config-profile update <database> <branch> <profile> --org <org> \
  --parameters pgconf.max_connections=200 --format json
pscale branch config-profile update <database> <branch> <profile> --org <org> \
  --extensions hll,pg_stat_statements --format json
pscale branch config-profile set-default <database> <branch> <profile> --org <org> --format json
```

Create/update sends only explicitly supplied flags. Storage flags use bytes for `--min-storage` and `--max-storage`, MiB/s for `--storage-throughput`, and explicit booleans for `--storage-autoscaling`. Repeat `--parameters namespace.name=value` for multiple settings. `update --extensions` **replaces** the complete enabled extension set: omit it to preserve the set, pass a reviewed comma-separated set to replace it, or pass `--extensions=` to disable all customer-managed extensions. Blank names inside a non-empty list are rejected. Inspect the current extension catalog and enabled set first; only extensions marked enablable can be selected, and extension removal can break dependent objects or parameters. Profile changes may be asynchronous; inspect `changes list/show`, and cancel only an identified cancelable request after approval.

`config-profile maintenance` can target one or multiple profiles and returns before completion. It can cause brief unavailability. Use branch-wide `branch maintenance run` when every profile should be maintained. Profile deletion is destructive and requires exact-target approval before `--force`.

## Routers

Routers are billed Neki routing groups. Discover valid SKUs and current state before creating or resizing one:

```bash
pscale branch router list <database> <branch> --org <org> --format json
pscale branch router show <database> <branch> <router> --org <org> --format json
pscale branch router sizes <database> <branch> --org <org> --format json

pscale branch router create <database> <branch> <router> --org <org> \
  --size <NKR-size> --replicas-per-cell 1 --format json
pscale branch router update <database> <branch> <router> --org <org> \
  --autoscaling --max-replicas-per-cell 4 --target-cpu-utilization 70 --format json
```

SKU names such as `NKR-5` also accept underscores. Router changes are asynchronous; follow them with `router changes list/show`, and re-read the router after completion. Deletion removes a connection target and requires dependency review and explicit approval before `--force`.

## Sidecars And Admin

Each configuration profile has one connection-pool sidecar. Identify it by sidecar ID or profile name. Sidecars cannot be created or deleted independently.

```bash
pscale branch sidecar list <database> <branch> --org <org> --format json
pscale branch sidecar show <database> <branch> <sidecar> --org <org> --format json
pscale branch sidecar parameters <database> <branch> <sidecar> --org <org> --format json
pscale branch sidecar update <database> <branch> <sidecar> --org <org> \
  --parameters pgbouncer.default_pool_size=20 --format json
```

Each Neki cluster also has one failover/recovery admin. It cannot be listed, created, or deleted independently.

```bash
pscale branch admin show <database> <branch> --org <org> --format json
pscale branch admin sizes <database> <branch> --org <org> --format json
pscale branch admin parameters <database> <branch> --org <org> --format json
pscale branch admin update <database> <branch> --org <org> \
  --size <NKA-size> --format json
```

Sidecar update requires one or more `--parameters`; admin update requires `--size` and/or repeatable `--parameters`. Both create asynchronous changes. Use the matching `changes list/show` command, obtain approval before canceling a request, and read back the component after terminal state.

## Maintenance

Branch-wide `pscale branch maintenance run` belongs to `pscale-branch`. Before handing off a Neki branch-wide run, inspect every page of the unfiltered consolidated branch change queue across admin, cluster, configuration-profile, router, and sidecar targets; treat any entry with `completed_at: null` as in flight. Confirm the impact window and recovery plan, and obtain explicit approval for the availability-impacting operation. Keep `pscale branch config-profile maintenance` in this skill for profile-scoped maintenance.

```bash
pscale branch changes list <database> <branch> --org <org> \
  --page 1 --per-page 100 --format json
pscale branch changes list <database> <branch> --org <org> \
  --page 2 --per-page 100 --format json
```

After `pscale-branch` starts branch-wide maintenance, verify completion with Neki-owned reads such as `config-profile list/show`, `router list/show`, `sidecar list/show`, and `admin show`; do not rely on `pscale branch infra` for Neki unless an exact help fence proves support.

## Backup Restore

`pscale backup restore` creates a new branch. For Neki restores, profile and router sizing can be inherited from the live source branch or overridden with repeatable `--config-profile` and `--router` flags. `backup restore show` previews the sizes that will be used when overrides are omitted.

```bash
pscale backup show <database> <source-branch> <backup-id> --org <org> --format json
pscale backup restore show <database> <source-branch> <backup-id> --org <org> --format json

pscale backup restore <database> <new-branch> <backup-id> --org <org> \
  --config-profile name=<profile>,cluster-size=<size>,replicas=<count> \
  --router name=<router>,size=<size>,replicas-per-cell=<count> \
  --format json

pscale branch show <database> <new-branch> --org <org> --format json
```

The restore preview uses the source branch's current profile/router sizes, not values stored on the backup. If the source branch was resized after the backup was taken, inherited sizes follow the current source branch. Configuration profiles and routers are restored, but profile/router parameters, sidecar settings, admin settings, and autoscaling are not. `--cluster-size` is shorthand for overriding the default profile; omit it to inherit that profile's source size. MySQL and PostgreSQL restores reject Neki `--config-profile` and `--router` options. Confirm source branch, backup ID, target branch name, inherited sizes, overrides, and cost before restoring.
