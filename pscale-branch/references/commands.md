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
  lint            Lints the schema for a branch
  list            List all branches of a database
  parameters      List the configuration parameters of a Postgres branch
  promote         Promote a new branch from a database
  query-patterns  Download query pattern reports for a branch
  refresh-schema  Refresh the schema for a database branch
  resize          Change a Postgres branch's cluster size, replicas, or parameters
  routing-rules   Fetch or update your keyspace routing rules
  safe-migrations Enable or disable safe migrations on a branch
  schema          Show the schema of a branch
  show            Show a specific branch of a database
  switch          Switches the current project to use the specified branch

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
```

At least one change flag is required. Parameter changes are validated against the catalog; unknown and immutable parameters fail. Values marked `restart` restart the database when applied. Without `--wait`, poll `resize status`; `queued`, `pending`, and `resizing` are non-terminal, while `completed` and `canceled` are terminal.

## pscale branch resize status

```text
Show the latest change request for a Postgres branch

Usage:
  pscale branch resize status <database> <branch> [flags]
```

## pscale branch resize cancel

```text
Cancel the queued change request for a Postgres branch

Usage:
  pscale branch resize cancel <database> <branch> [flags]
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
```

## pscale branch query-patterns

```text
Download query pattern reports for a branch

Usage:
  pscale branch query-patterns [command]

Available Commands:
  download    Download a CSV report of the query patterns for a branch

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

```

## pscale branch vtctld

```text
Run vtctld commands against a branch. This command is only supported for Vitess databases.

Usage:
  pscale branch vtctld [command]

Available Commands:
  get-shard              Get a shard record for a branch
  get-routing-rules      Get live routing rules for a branch
  list-keyspaces         List vtctld keyspaces for a branch
  list-tablets           List tablets for a branch, grouped by keyspace and shard
  list-workflows         List vtctld workflows for a branch
  lookup-vindex          Manage Lookup Vindex operations
  materialize            Manage Materialize workflows
  move-tables            Manage MoveTables workflows
  planned-reparent-shard Reparent a shard to a new primary
  start-workflow         Start a workflow on a branch
  stop-workflow          Stop a workflow on a branch
  throttler              Inspect and configure the tablet throttler
  vdiff                  Manage VDiff operations

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

```

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
```

## pscale branch vtctld get-shard

```text
Get a live shard record from the cluster via vtctld, including tablet controls and denied tables.

Usage:
  pscale branch vtctld get-shard <database> <branch> [flags]

Flags:
  -h, --help              help for get-shard
      --keyspace string   Keyspace name
      --shard string      Shard name (e.g. "-" for unsharded)

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

```
