# Workflow listing and source-cell selection

## Compatibility and provenance

Minimum CLI: **v0.351.0** for asynchronous `branch vtctl list-workflows`, asynchronous multi-keyspace `branch vtctl move-tables list`/`ls` with the final `workflows` object, and `move-tables create --all-cells` with omitted-`--cells` selecting all source cells. The existing canonical `vtctl` spelling and `vtctld` alias predate this minimum; this is a minimum for the behavior described here, not for initial command availability. Older clients must not assume these defaults or output contracts.

Reviewed official `planetscale/cli` commit `e6449dc17ee2af30aed4a1a07aa5112bf6b7d8ca`: [MoveTables commands and operation waiter](https://github.com/planetscale/cli/blob/e6449dc17ee2af30aed4a1a07aa5112bf6b7d8ca/internal/cmd/branch/vtctld/move_tables.go), [general listing](https://github.com/planetscale/cli/blob/e6449dc17ee2af30aed4a1a07aa5112bf6b7d8ca/internal/cmd/branch/vtctld/workflows.go), [result enrichment](https://github.com/planetscale/cli/blob/e6449dc17ee2af30aed4a1a07aa5112bf6b7d8ca/internal/cmd/branch/vtctld/workflow_next_steps.go), [MoveTables API](https://github.com/planetscale/cli/blob/e6449dc17ee2af30aed4a1a07aa5112bf6b7d8ca/internal/planetscale/vtctld_move_tables.go), and [general vtctld API](https://github.com/planetscale/cli/blob/e6449dc17ee2af30aed4a1a07aa5112bf6b7d8ca/internal/planetscale/vtctld_general.go). This is source-backed behavior, not a live result or binary help capture. Other stored help retains its explicitly stated capture provenance.

## Listing contract

```bash
pscale branch vtctl move-tables list <database> <branch> --org <org> --format json
pscale branch vtctl move-tables list <database> <branch> --org <org> \
  --target-keyspace <keyspace> --format json
pscale branch vtctl list-workflows <database> <branch> --org <org> \
  --keyspace <keyspace> --include-logs=false --format json
```

These are inspections that submit background API operations via POST, not simple GET requests and not migration authorization. MoveTables submits `move-tables/list-workflows`, receives operation IDs (one per keyspace), waits for each in sequence, and aggregates each result's `workflows` array. The CLI prints a final JSON object with one `workflows` array, including `{"workflows":[]}` when no entries are returned. It no longer preserves an arbitrary raw-array or original top-level wrapper shape. Workflow fields remain intact; an entry with a name and target keyspace gets a status `next_steps` proposal unless it already has `next_steps`. The target may be `target_keyspace` or nested `target.keyspace`. Never execute generated proposals without inspecting their target and applying approval gates.

Omit `--target-keyspace` to request all keyspaces. `ls` aliases `list`; examples use canonical `list`. General `list-workflows` submits `vtctld/list-workflows`, waits for one operation, and prints its raw result rather than the MoveTables aggregation wrapper. It requires `--keyspace`, supports an optional `--workflow` filter, and sends `include_logs` only when `--include-logs` was explicitly set. The help flag default is true; omission leaves the API default in control. Prefer explicit `--include-logs=false` when logs are unnecessary or sensitive.

The waiter checks immediately, then polls every second. Its polling timeout is the server operation timeout in seconds plus 30 seconds when positive, otherwise 10 minutes, subject to earlier context cancellation. This is per operation after its initial lookup, not a single end-to-end deadline for listing all keyspaces. Only `completed: true` with state `completed` is success. Failed, cancelled, unexpected terminal states, request/poll errors, or timeouts fail the command; invalid per-keyspace JSON also fails aggregation. Do not claim a partial list is complete or classify an error as an empty inventory. Preserve the exit status and diagnostics; never hide failure behind a successful JSON pipeline. Do not automatically resubmit jobs or advance/create/delete a workflow to recover from an inspection failure.

## Approve source-cell scope before create

Omitting `--cells` uses all cells for **source tablet selection**. `--all-cells` expresses that same selection by omitting the cells field in the request. `--cells cell1,cell2` limits selection; `--cells` and `--all-cells` are mutually exclusive. `--all-cells=false` does not select no cells: with `--cells` omitted, the same server all-cells default applies.

Before creation, inspect the exact organization/database/branch, source and target keyspaces, eligible cells/tablets, table set, and current workflow inventory. Obtain explicit approval for source-cell scope and cross-cell load/placement impact along with the existing workflow/recovery plan. Keep `--auto-start=false` if stream start needs a later approval; otherwise creation starts automatically. Check status after creation before proposing start, traffic changes, or cleanup. Source-cell selection does not authorize routing changes or destructive completion. Use the existing branch skill's destructive-operation gates for those separate operations.
