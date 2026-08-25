Unless noted otherwise, help fences below are exact output from the official, checksum-verified PlanetScale CLI v0.324.0 macOS arm64 release binary after normalizing only trailing whitespace. The `pscale branch` and `pscale branch create` surfaces were recaptured from the checksum-verified v0.325.0 binary; the parent output is unchanged from v0.324.0.

## pscale branch

```text
Create, delete, diff, and manage branches

Usage:
  pscale branch [command]

Available Commands:
  connections     Show and kill branch connections
  create          Create a new branch from a database
  delete          Delete a branch from a database
  demote          Demote a production branch to development
  diff            Show the diff of a branch
  extensions      List extensions available on a Postgres branch
  lint            Lints the schema for a branch
  list            List all branches of a database
  maintenance     Run maintenance for a Postgres branch
  parameters      List the configuration parameters of a Postgres branch
  promote         Promote a new branch from a database
  query-patterns  List, show, delete, and download query pattern reports for a branch
  refresh-schema  Refresh the schema for a database branch
  resize          Change a Postgres branch's cluster size, replicas, or parameters
  routing-rules   Fetch or update your keyspace routing rules
  safe-migrations Enable or disable safe migrations on a branch
  schema          Show the schema of a branch
  show            Show a specific branch of a database
  switch          Switches the current project to use the specified branch
  switchover      Switch over the primary of a Postgres branch (Postgres only)
  update          Update a branch's name or deletion protection
  vtgate          Manage VTGate size for a Vitess branch

Flags:
  -h, --help         help for branch
      --org string   The organization for the current user

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Use "pscale branch [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch create

```text
Create a new branch from a database

Usage:
  pscale branch create <source-database> <branch> [options] [flags]

Aliases:
  create, b

Flags:
      --cluster-size string    Cluster size for the branch. Defaults to PS_DEV for regular branches, or PS-10 for branches created from a backup or with seed-data. Use 'pscale size cluster list' to see the valid sizes.
      --from string            Parent branch to create the new branch from. Cannot be used with --restore
  -h, --help                   help for create
      --major-version string   For PostgreSQL databases, the PostgreSQL major version to use for the branch. Defaults to the major version of the parent branch if it exists or the database's default branch major version. Ignored for branches restored from backups.
      --max-storage int        Maximum storage size in bytes for autoscaling
      --min-storage int        Minimum storage size in bytes
      --region string          Region for the branch to be created in.
      --restore string         ID of Backup to restore into branch.
      --restore-point string   For PostgreSQL databases, restore from a point-in-time recovery timestamp (e.g. 2023-01-01T00:00:00Z).
      --seed-data              Add seed data using the Data Branching™ feature. This branch will be created with the same resources as the base branch.
      --wait                   Wait until the branch is ready

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch update

```text
Update a branch's name or deletion protection.

Only the flags you pass are sent. At least one flag is required.

Usage:
  pscale branch update <database> <branch> [flags]

Examples:
  pscale branch update mydb main --new-name trunk
  pscale branch update mydb main --deletion-protected
  pscale branch update mydb main --deletion-protected=false

Flags:
      --deletion-protected   Protect the branch from deletion (use --deletion-protected=false to disable)
  -h, --help                 help for update
      --new-name string      Rename the branch

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch switchover

```text
Switch over the primary of a Postgres branch. Postgres only.

On a branch with replicas the primary steps down and a replica is promoted in
its place; use --candidate to pick the replica, otherwise one is selected
automatically. A branch running a single instance has nothing to promote, so
that instance is restarted in place and the branch is unreachable while it
comes back. Writes are briefly interrupted while the switch completes.

Usage:
  pscale branch switchover <database> <branch> [flags]

Flags:
      --candidate string   Name of the replica to promote, as returned by 'branch infra'. Omit to select automatically. Only applies to branches with replicas
  -h, --help               help for switchover

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch maintenance

```text
Manage maintenance for a Postgres branch.

PlanetScale upgrades a branch's image in emergencies, such as patching security
issues, or when you initiate the upgrade yourself. 'maintenance run' initiates
one.

See https://planetscale.com/docs/postgres/operations-philosophy

Usage:
  pscale branch maintenance [command]

Available Commands:
  run         Run maintenance for a Postgres branch now (Postgres only)

Flags:
  -h, --help   help for maintenance

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Use "pscale branch maintenance [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch maintenance run

```text
Run maintenance for a Postgres branch, updating it to the latest available
image. Postgres only.

This is how regular version bumps, bugfixes, and quality-of-life improvements
reach a branch. PlanetScale otherwise upgrades images only in emergencies, such
as patching security issues.

The upgrade is applied to the replicas first, followed by a switchover from the
old primary to an upgraded replica. That failover leads to a short period of
database unavailability (seconds), and all direct connections are terminated, so
your application should have retry logic. A branch running a single instance has
no replica to switch over to and is unavailable until it comes back.

Pass --update-postgres-minor-version to also upgrade the branch to the latest
PostgreSQL minor version during the run.

Maintenance cannot start while a change request (see 'branch resize') is still
in progress.

See https://planetscale.com/docs/postgres/operations-philosophy

Usage:
  pscale branch maintenance run <database> <branch> [flags]

Flags:
  -h, --help                            help for run
      --update-postgres-minor-version   Upgrade the branch to the latest PostgreSQL minor version during maintenance

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch extensions

```text
List extensions available on a Postgres branch's cluster image.

This is the catalog of extensions the image can load, not the result of
CREATE EXTENSION. There is no CLI command to enable an extension; preload
libraries are configured with 'pscale branch resize --parameters'.

Usage:
  pscale branch extensions <database> <branch> [flags]
  pscale branch extensions [command]

Available Commands:
  list        List extensions available on a Postgres branch

Flags:
  -h, --help   help for extensions

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Use "pscale branch extensions [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

`pscale branch extensions <database> <branch>` accepts the same flags and is equivalent to `extensions list`. This is a read-only cluster-image catalog, not installed extension state.

## pscale branch extensions list

```text
List extensions available on a Postgres branch's cluster image.

This is the catalog of extensions the image can load, not the result of
CREATE EXTENSION. There is no CLI command to enable an extension; preload
libraries are configured with 'pscale branch resize --parameters'.

Usage:
  pscale branch extensions list <database> <branch> [flags]

Aliases:
  list, ls

Flags:
  -h, --help   help for list

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

Unless a command-specific help block repeats them inline, every `pscale branch`
subcommand accepts these global flags:

```text
Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.
```

## pscale branch list

```text
List all branches of a database

Usage:
  pscale branch list <database> [flags]

Aliases:
  list, ls

Flags:
  -h, --help           help for list
      --page int       Page number to fetch
      --per-page int   Number of results per page (default 100)
  -w, --web            List branches in your web browser.

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch parameters

```text
List the configuration parameters of a Postgres branch, including their
current and default values. Values from a queued change request are reflected.

To change parameters, use 'pscale branch resize <database> <branch> --parameters namespace.name=value'.

Usage:
  pscale branch parameters <database> <branch> [flags]
  pscale branch parameters [command]

Aliases:
  parameters, params

Available Commands:
  list        List the configuration parameters of a Postgres branch

Flags:
      --extension          Only show parameters that configure an extension (--extension=false hides them).
  -h, --help               help for parameters
      --internal           Only show internal (immutable) parameters (--internal=false hides them).
      --namespace string   Only show parameters in this namespace (e.g. pgconf, pgbouncer, patroni).

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Use "pscale branch parameters [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

`pscale branch parameters list <database> <branch>` accepts the same flags. The bare `parameters <database> <branch>` form is an alias for `parameters list`. Prefer `--format json` before a change so `restart`, `immutable`, current, and default values remain explicit.

## pscale branch resize

```text
Change a Postgres branch's cluster size, replica count, and/or configuration
parameters. All requested changes are combined into a single change request
that is applied asynchronously. Use "pscale branch resize status" to track it
and "pscale branch resize cancel" to cancel it while queued.

Usage:
  pscale branch resize <database> <branch> [flags]
  pscale branch resize [command]

Examples:
  pscale branch resize mydb main --cluster-size PS_10_GCP_X86
  pscale branch resize mydb main --parameters pgconf.max_connections=200
  pscale branch resize mydb main --cluster-size PS_20_GCP_X86 --replicas 2 --parameters pgconf.max_connections=500 --wait

Available Commands:
  cancel      Cancel the queued change request for a Postgres branch
  status      Show the latest change request for a Postgres branch

Flags:
      --cluster-size string      New cluster size for the branch (a fully-qualified SKU name, e.g. PS_10_GCP_X86). Use 'pscale size cluster list --engine postgresql' to see the valid sizes.
  -h, --help                     help for resize
      --parameters stringArray   Set a configuration parameter as namespace.name=value (e.g. pgconf.max_connections=200). Repeatable. Use 'pscale branch parameters list' to see available parameters.
      --replicas int             Desired number of replicas for the branch.
      --wait                     Wait for the change request to complete before returning.
      --wait-timeout duration    Maximum time to wait for the change request to complete with --wait. (default 10m0s)

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Use "pscale branch resize [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

At least one change flag is required. Parameter changes are validated against the catalog; unknown and immutable parameters fail. Values marked `restart` restart the database when applied. Without `--wait`, poll `resize status`; `queued`, `pending`, and `resizing` are non-terminal, while `completed` and `canceled` are terminal.

## pscale branch resize status

```text
Show the latest change request for a Postgres branch

Usage:
  pscale branch resize status <database> <branch> [flags]

Flags:
  -h, --help   help for status

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch resize cancel

```text
Cancel the queued change request for a Postgres branch

Usage:
  pscale branch resize cancel <database> <branch> [flags]

Flags:
  -h, --help   help for cancel

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

Cancel is an operational write. Confirm the target and latest request state before running it, then re-run `resize status` to verify the result.

## pscale branch connections

```text
Show and kill branch connections.

Agent workflow:
  1. Run: pscale branch connections show <database> <branch> --format json
  2. Inspect query_id, transaction_id, and connection_id from the selected row.
  3. Explain the proposed action and wait for user approval before running it.
  4. Run exactly one action command with the matching ID.
  5. Run show again to verify the result.

Action semantics:
  kill <database> <branch> <query-id> --query        Cancels the listed query_id.
  kill-transaction <database> <branch> <transaction-id>
                                                     Postgres only. destructive. Terminates the listed transaction_id if it still matches server state.
  kill <database> <branch> <connection-id>           destructive. Terminates the listed connection_id.

Use --format json when an agent or script needs to inspect query_id,
transaction_id, and connection_id fields. Human output uses vertical records so
query text and action IDs are not truncated.

Usage:
  pscale branch connections [command]

Available Commands:
  kill             Kill a branch connection or query
  kill-transaction Kill a Postgres branch transaction
  show             Show branch connections once
  top              Show live branch connection activity

Flags:
  -h, --help   help for connections

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Use "pscale branch connections [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch connections show

```text
Show branch connections once.

Use --format json when an agent or script needs to inspect query_id,
transaction_id, and connection_id fields. Human output uses vertical records so
query text and action IDs are not truncated.

Usage:
  pscale branch connections show <database> <branch> [flags]

Flags:
  -h, --help              help for show
      --instance string   Postgres instance to target
      --keyspace string   Vitess keyspace to target
      --role string       Postgres instance role to target: primary or replica
      --shard string      Vitess shard to target

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch connections top

```text
Show live branch connection activity.

Run interactively in a terminal to launch the TUI. Pipe or redirect output to
run headlessly with --capture; --duration bounds either mode and without
--duration the command runs until interrupted. Pass --replay FILE to render a
previously captured trace in the TUI — actions are rejected in replay mode.

For Postgres, connections top shows session activity across instances. For
Vitess, pass --keyspace and --shard or run interactively to select them when
the server reports available targets.

Usage:
  pscale branch connections top [database] [branch] [flags]

Flags:
      --capture string      Write captured samples to a trace file. Required in headless mode.
      --duration duration   Run for this duration. Default is to run until interrupted.
  -h, --help                help for top
      --instance string     Filter the live view to a single instance (by id from the list response).
      --interval duration   Refresh interval. (default 1s)
      --keyspace string     Vitess keyspace to target.
      --replay string       Replay a previously captured trace file in the TUI. Mutually exclusive with --capture.
      --role string         Filter the live view to rows whose instance role is primary or replica.
      --shard string        Vitess shard to target.

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch connections kill

```text
Kill a branch connection or query.

This is destructive. Pass a connection_id from connections show to terminate a
connection, or pass --query with a query_id from connections show to cancel only
the current query.

Usage:
  pscale branch connections kill <database> <branch> <id> [flags]

Flags:
  -h, --help              help for kill
      --keyspace string   Vitess keyspace to target
      --query             Cancel the query_id instead of terminating the connection_id
      --shard string      Vitess shard to target

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch connections kill-transaction

```text
Kill a Postgres branch transaction.

This is destructive. Pass a transaction_id from connections show to terminate
the matching Postgres connection.

Usage:
  pscale branch connections kill-transaction <database> <branch> <transaction-id> [flags]

Flags:
  -h, --help   help for kill-transaction

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch infra

```text
Show infrastructure (pods) for a branch

Usage:
  pscale branch infra <database> <branch> [flags]

Flags:
  -h, --help   help for infra

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch query-patterns

```text
List, show, delete, and download query pattern reports for a branch

Usage:
  pscale branch query-patterns [command]

Available Commands:
  delete      Delete a query pattern report
  download    Download a CSV report of the query patterns for a branch
  list        List query pattern reports for a branch
  show        Show a query pattern report

Flags:
  -h, --help   help for query-patterns

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Use "pscale branch query-patterns [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch query-patterns list

```text
List query pattern reports for a branch

Usage:
  pscale branch query-patterns list <database> <branch> [flags]

Aliases:
  list, ls

Flags:
  -h, --help                    help for list
      --limit int               Number of results to return (max 100) (default 25)
      --starting-after string   Cursor to fetch the next page of reports

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch query-patterns show

```text
Show a query pattern report

Usage:
  pscale branch query-patterns show <database> <branch> <report-id> [flags]

Flags:
  -h, --help   help for show

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch query-patterns delete

```text
Delete a query pattern report

Usage:
  pscale branch query-patterns delete <database> <branch> <report-id> [flags]

Aliases:
  delete, rm

Flags:
      --force   Delete the report without confirmation
  -h, --help    help for delete

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch query-patterns download

```text
Download a CSV report of the query patterns for a branch

Usage:
  pscale branch query-patterns download <database> <branch> [flags]

Flags:
  -h, --help            help for download
      --output string   Output file name, or - to write to stdout. Defaults to query-patterns-<organization>-<database>-<branch>-<timestamp>.csv.

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch routing-rules

```text
Fetch or update your keyspace routing rules

Usage:
  pscale branch routing-rules [command]

Available Commands:
  get         Show the routing rules of a branch
  update      Update the routing rules of a branch

Flags:
  -h, --help   help for routing-rules

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Use "pscale branch routing-rules [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch routing-rules get

```text
Show the routing rules of a branch

Usage:
  pscale branch routing-rules get <database> <branch> [flags]

Flags:
  -h, --help   help for get

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch routing-rules update

```text
Update the routing rules of a branch

Usage:
  pscale branch routing-rules update <database> <branch> --routing-rules <file> [flags]

Flags:
  -h, --help                   help for update
      --routing-rules string   The routing to set

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch vtgate

```text
Manage VTGate size for a Vitess branch

Usage:
  pscale branch vtgate [command]

Available Commands:
  resize      Resize VTGates for a Vitess production branch
  show        Show the current VTGate configuration for a Vitess branch

Flags:
  -h, --help   help for vtgate

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Use "pscale branch vtgate [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch vtgate show

```text
Show the current VTGate configuration for a Vitess branch

Usage:
  pscale branch vtgate show <database> <branch> [flags]

Examples:
  pscale branch vtgate show mydb main
  pscale branch vtgate show mydb main --format json

Flags:
  -h, --help   help for show

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

Use `--format json` to preserve `vtgate_size`, per-availability-zone `vtgate_count`, `vtgate_autoscaling`, `vtgate_max_count`, and `vtgate_target_cpu_utilization` for agent review.

## pscale branch vtgate resize

```text
Resize the VTGate SKU, count, and/or autoscaling for a Vitess production branch.

Development branches cannot be resized. Use "pscale branch vtgate resize status"
to track a resize and "pscale branch vtgate resize cancel" to cancel one while
queued.

Usage:
  pscale branch vtgate resize <database> <branch> [flags]
  pscale branch vtgate resize [command]

Examples:
  pscale branch vtgate resize mydb main --vtgate-size VTG_320
  pscale branch vtgate resize mydb main --vtgate-size VTG_1280 --vtgate-count 2
  pscale branch vtgate resize mydb main --vtgate-size VTG_320 --vtgate-autoscaling --vtgate-count 2 --vtgate-max-count 8 --vtgate-target-cpu-utilization 50

Available Commands:
  cancel      Cancel a queued VTGate resize for a Vitess branch
  status      Show the latest VTGate resize for a Vitess branch

Flags:
  -h, --help                                help for resize
      --vtgate-autoscaling                  Enable or disable VTGate autoscaling (use --vtgate-autoscaling=false to disable)
      --vtgate-count int                    Number of VTGates per availability zone (minimum when autoscaling is enabled)
      --vtgate-max-count int                Maximum VTGates per availability zone when autoscaling is enabled
      --vtgate-size string                  VTGate size SKU (e.g. VTG_320, VTG_1280)
      --vtgate-target-cpu-utilization int   Target CPU utilization percent when autoscaling is enabled

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Use "pscale branch vtgate resize [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

At least one resize flag is required. Omitted flags are not sent as changes; boolean disablement therefore requires explicit `--vtgate-autoscaling=false`.

## pscale branch vtgate resize status

```text
Show the latest VTGate resize for a Vitess branch

Usage:
  pscale branch vtgate resize status <database> <branch> [flags]

Flags:
  -h, --help   help for status

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch vtgate resize cancel

```text
Cancel a queued VTGate resize for a Vitess branch

Usage:
  pscale branch vtgate resize cancel <database> <branch> [flags]

Flags:
  -h, --help   help for cancel

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

Cancel is an operational write. Confirm the target and latest request state before running it, then re-run `resize status` and `vtgate show` to verify the result and applied configuration.

## pscale branch vtctld

The parent and keyspace-routing-rule help blocks below are exact output from the official, checksum-verified PlanetScale CLI v0.324.0 macOS arm64 release binary after normalizing only trailing whitespace.

```text
Run vtctld commands against a branch. This command is only supported for Vitess databases.

Usage:
  pscale branch vtctld [command]

Available Commands:
  apply-keyspace-routing-rules Replace live keyspace routing rules for a branch
  get-keyspace-routing-rules   Get live keyspace routing rules for a branch
  get-routing-rules            Get live routing rules for a branch
  get-shard                    Get a shard record for a branch
  list-keyspaces               List vtctld keyspaces for a branch
  list-tablets                 List tablets for a branch, grouped by keyspace and shard
  list-workflows               List vtctld workflows for a branch
  lookup-vindex                Manage Lookup Vindex operations
  materialize                  Manage Materialize workflows
  move-tables                  Manage MoveTables workflows
  planned-reparent-shard       Reparent a shard to a new primary
  refresh-state-by-shard       Reload tablet records for all tablets in a shard
  set-shard-tablet-control     Update shard tablet controls for a branch
  start-workflow               Start a workflow on a branch
  stop-workflow                Stop a workflow on a branch
  throttler                    Inspect and configure the tablet throttler
  vdiff                        Manage VDiff operations

Flags:
  -h, --help   help for vtctld

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Use "pscale branch vtctld [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch vtctld get-keyspace-routing-rules

```text
Get live keyspace routing rules for a branch

Usage:
  pscale branch vtctld get-keyspace-routing-rules <database> <branch> [flags]

Flags:
  -h, --help   help for get-keyspace-routing-rules

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch vtctld apply-keyspace-routing-rules

```text
Replace live keyspace routing rules for a branch

Usage:
  pscale branch vtctld apply-keyspace-routing-rules <database> <branch> [flags]

Flags:
      --cells strings       Limit SrvVSchema rebuilding to these cells
  -h, --help                help for apply-keyspace-routing-rules
      --rules string        Keyspace routing rules as JSON
      --rules-file string   Path to keyspace routing rules JSON
      --skip-rebuild        Skip rebuilding SrvVSchema objects

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch vtctld throttler

```text
Inspect and configure the tablet throttler

Usage:
  pscale branch vtctld throttler [command]

Available Commands:
  check         Issue a throttler check against a single tablet
  status        Get the throttler status for a single tablet
  update-config Update the throttler configuration for a keyspace

Flags:
  -h, --help   help for throttler

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Use "pscale branch vtctld throttler [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch vtctld throttler status

```text
Get the throttler status for a single tablet, identified by its alias. Discover tablet aliases with `pscale branch vtctld list-tablets`.

Usage:
  pscale branch vtctld throttler status <database> <branch> [flags]

Flags:
  -h, --help                  help for status
      --tablet-alias string   Alias of the tablet to probe (e.g. "zone1-0000000100") (required)

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch vtctld throttler check

```text
Issue a throttler check against a single tablet, identified by its alias. Discover tablet aliases with `pscale branch vtctld list-tablets`.

Usage:
  pscale branch vtctld throttler check <database> <branch> [flags]

Flags:
      --app-name string           App to issue the check on behalf of (e.g. "online-ddl"). Defaults to the throttler's default app.
  -h, --help                      help for check
      --ok-if-not-exists          Return OK even if the requested metric does not exist
      --scope string              Scope of the check, either "shard" or "self". Defaults to the throttler's default scope.
      --skip-request-heartbeats   Do not renew the throttler's heartbeat lease while serving this check
      --tablet-alias string       Alias of the tablet to check (e.g. "zone1-0000000100") (required)

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch vtctld throttler update-config

```text
Update the tablet throttler configuration for a keyspace. Omit --enabled to leave the keyspace enable state unchanged. Flag behavior mirrors vtctldclient UpdateThrottlerConfig: --throttle-app and --unthrottle-app are mutually exclusive; --app-name and --app-metrics are required together.

Usage:
  pscale branch vtctld throttler update-config <database> <branch> [flags]

Flags:
      --app-metrics strings              Metrics to check for --app-name (e.g. lag,loadavg)
      --app-name string                  App name for which to assign checked metrics (requires --app-metrics)
      --enabled                          Enable (true) or disable (false) the throttler for the keyspace. Omit to leave unchanged.
  -h, --help                             help for update-config
      --keyspace string                  Keyspace whose throttler config to update (required)
      --threshold float                  Replication lag threshold in seconds for the default check
      --throttle-app string              App name to throttle (e.g. "rowstreamer")
      --throttle-app-duration duration   Duration after which the --throttle-app rule expires (default 1h0m0s)
      --throttle-app-ratio float         Ratio to throttle the app specified by --throttle-app (0.00-1.00) (default 1)
      --unthrottle-app string            App name whose throttled-app rule should be removed

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

`--throttle-app` and `--unthrottle-app` are mutually exclusive. `--app-name` and `--app-metrics` are required together.

## pscale branch vtctld move-tables create

```text
Create a MoveTables workflow

Usage:
  pscale branch vtctld move-tables create <database> <branch> [flags]

Flags:
      --all-tables                               Move all tables from the source keyspace
      --atomic-copy                              Use atomic copy for the workflow
      --auto-start                               Automatically start the workflow after creation (default true)
      --cells strings                            Cells to restrict the workflow to (comma-separated)
      --defer-secondary-keys                     Defer secondary keys during the copy phase (default true)
      --exclude-tables strings                   Tables to exclude from the move (comma-separated)
      --global-keyspace string                   Unsharded keyspace in which to create the backing sequence tables when --sharded-auto-increment-handling is REPLACE
  -h, --help                                     help for create
      --on-ddl string                            DDL handling strategy (IGNORE, STOP, EXEC, EXEC_IGNORE)
      --sharded-auto-increment-handling string   Auto increment handling for sharded keyspaces
      --source-keyspace string                   Source keyspace (required)
      --source-time-zone string                  Source time zone
      --stop-after-copy                          Stop the workflow after the copy phase
      --tables strings                           Tables to move (comma-separated)
      --tablet-types strings                     Tablet types to use for the workflow (comma-separated)
      --target-keyspace string                   Target keyspace (required)
      --tenant-id string                         Tenant ID
      --workflow string                          Name of the workflow (required)

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch vtctld get-shard

```text
Get a live shard record from the cluster via vtctld, including tablet controls and denied tables.

Usage:
  pscale branch vtctld get-shard <database> <branch> [flags]

Flags:
  -h, --help              help for get-shard
      --keyspace string   Keyspace name (required)
      --shard string      Shard name (e.g. "-" for unsharded) (required)

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch vtctld get-routing-rules

```text
Get live routing rules from the cluster via vtctld. This reads the current cluster state, unlike `pscale branch routing-rules get`, which reads from the schema snapshot.

Usage:
  pscale branch vtctld get-routing-rules <database> <branch> [flags]

Flags:
  -h, --help   help for get-routing-rules

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```
