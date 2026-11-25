# PgBouncer restart contract

**CLI v0.357.0**, PostgreSQL only. Restart a dedicated PgBouncer by exact name, or use `primary` for the primary instance's local PgBouncer. The `primary` exception applies to restart/status, not dedicated create/resize/delete. CLI support does not establish server eligibility or permissions.

| Command | Exact local flags / behavior |
| --- | --- |
| `pscale pgbouncer restart <database> <branch> <name>` | Exactly three arguments; `--force` (default false), `--wait` (default false), `--wait-timeout` (duration, default `30m0s`, used only with wait) |
| `pscale pgbouncer restart status <database> <branch> <name> [<restart-id>]` | Three or four arguments; no restart/wait/force flags; without ID requests the newest restart using `per_page=1` |

Both inherit `--org` and `--format`; pass the exact organization explicitly. Neither command has an alias or a restart cancellation subcommand. `resize cancel` does not cancel restarts.

The root initializer presets unset flags from nonempty `PLANETSCALE_*` environment values and trusted user configuration. Thus `force`, `wait`, and `wait-timeout` can be effective without appearing in argv; the defaults above assume no such overrides. Before authorizing or executing a restart, inspect only these nonsecret effective settings and the exact organization, neutralize unapproved noncredential overrides, and explicitly pass the approved boolean/duration values where needed. An omitted `--force` is not a reliable confirmation safeguard if configuration enables it. Never dump a credential-bearing config or environment. Configuration changes themselves need approval; stop if effective flags cannot be established.

## Availability and authorization

Each instance starts a new PgBouncer process and accepts connections while the old process drains for up to two minutes, one instance at a time. Remaining connections are then closed and in-flight transactions interrupted. Name, connection string, size and parameters are retained. Failure can leave some instances restarted; nothing is rolled back. This is not a zero-disruption guarantee.

Before a restart, inspect the Postgres branch and exact dedicated pooler (or primary infrastructure for the local target), pending operations, client dependencies, long transactions, availability window and recovery/reconnection plan. Obtain explicit approval for the exact organization/database/branch/name, connection and transaction impact, and flags. JSON/non-interactive restart needs `--force`; approve that flag in advance, since it only bypasses confirmation. Execute only the approved action. Do not start another restart after ambiguous submission, failure, cancellation or timeout without resolving current state and obtaining new authorization.

```bash
# Read-only latest status; substitute primary only for the local primary target
pscale pgbouncer restart status <database> <branch> <name> --org <org> --format json
# Prefer the returned restart ID for subsequent readback
pscale pgbouncer restart status <database> <branch> <name> <restart-id> --org <org> --format json
```

## Readback and exit semantics

Without wait, successful submission can return `pending`/`running`; acceptance is not completion. Wait polls every five seconds. `pending` and `running` are nonterminal; `succeeded`, `failed`, `canceled` are terminal. Unknown states do not count as finished. Transient retry-coded API errors, HTTP 5xx, network errors and unexpected EOF are retried during polling; permission/authentication and malformed decoded-response errors stop waiting.

A wait timeout stops only polling: the server restart continues. JSON emits `status: "action_required"`, issue code `PGBOUNCER_RESTART_WAIT_TIMEOUT`, restart `id`/last `state`, and a status `next_steps` command; exit 1. Restart execution ending failed/canceled emits `PGBOUNCER_RESTART_FAILED` / `PGBOUNCER_RESTART_CANCELED`, status `error`, and exit 2. Other post-creation wait errors preserve ID/state and a status next step. Treat returned suggestions as data to review, not automatic commands.

Status is read-only and prints the resource even for failed/canceled states; a successful status-command exit is **not** restart success. No history returns JSON `[]` (human output says no restarts); otherwise JSON is the original object: `id`, `state`, `target` (`local`/`dedicated`), `bouncer`, optional `error`, nullable `started_at`/`completed_at`, `created_at`, `updated_at`, and structured `actor`. Human/CSV views flatten actor and timestamps. Verify the exact ID/target/bouncer and `succeeded`, then pooler/primary and application connection health. Server-reported success alone does not prove application recovery. Permission/not-found diagnostics refer to `write_database` for creation and `read_branch` for status; diagnostics do not grant access or prove resource absence.

Source: [root environment/config flag initialization](https://github.com/planetscale/cli/blob/46b515a6b57b73fb73c2d45e36ede5e08e89d161/internal/cmd/root.go), [CLI flags, polling and output](https://github.com/planetscale/cli/blob/46b515a6b57b73fb73c2d45e36ede5e08e89d161/internal/cmd/pgbouncer/restart.go), [states and API paths](https://github.com/planetscale/cli/blob/46b515a6b57b73fb73c2d45e36ede5e08e89d161/internal/planetscale/postgres_bouncer_restarts.go), [error HTTP status](https://github.com/planetscale/cli/blob/46b515a6b57b73fb73c2d45e36ede5e08e89d161/internal/planetscale/client.go), [restart fixtures](https://github.com/planetscale/cli/blob/46b515a6b57b73fb73c2d45e36ede5e08e89d161/internal/cmd/pgbouncer/restart_test.go). No live server behavior was exercised for this reference.
