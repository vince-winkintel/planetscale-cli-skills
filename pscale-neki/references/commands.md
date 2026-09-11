Exact help output below was captured from the official, checksum-verified PlanetScale CLI v0.332.0 macOS arm64 release binary with `NO_COLOR=1` (archive SHA-256 `61eadf71c9d5e6423587fbf01fd698800d8a944775a06519a1c2ac38fcb89287`) after normalizing only trailing whitespace.

## pscale logs

```text
Query recent logs for a PostgreSQL or Neki branch.

The command obtains a signed logs URL from the PlanetScale API, builds a LogsQL
query, and prints parsed log entries. By default it returns up to 100 logs from
the primary server over the last hour, newest first.

Usage:
  pscale logs <database> <branch> [flags]

Examples:
  # Recent primary logs
  pscale logs <database> <branch> --org <org> --format json

  # Errors from a selected pod over the last six hours
  pscale logs <database> <branch> --org <org> --format json --period 6h --level ERROR --server <pod>

  # Logs from a custom ISO 8601 time range
  pscale logs <database> <branch> --org <org> --format json \
    --from 2026-08-20T16:00:00Z --to 2026-08-20T18:00:00Z

  # Search and filter with LogsQL syntax
  pscale logs <database> <branch> --org <org> --format json --query 'connection refused'

Flags:
      --from string      Start of a custom time range as an ISO 8601 timestamp
  -h, --help             help for logs
      --level strings    Log levels to include (comma-separated or repeatable): DEBUG, INFO, WARNING, ERROR
      --limit int        Maximum number of logs to return (default 100)
      --org string       The organization for the current user
      --page int         Page number to fetch (default 1)
      --period string    Time period to query: 15m, 1h, 3h, 6h, 12h, 1d, 7d, or 8d (default "1h")
      --query string     Text or LogsQL expression to search for
      --server strings   Servers to include (comma-separated or repeatable); primary selects the primary role, other values select pod names (default [primary])
      --shard strings    Neki shards to include (comma-separated or repeatable)
      --to string        End of a custom time range as an ISO 8601 timestamp

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch

```text
Create, delete, diff, and manage branches

Usage:
  pscale branch [command]

MySQL, Postgres, and Neki branch commands:
  create          Create a new branch from a database
  delete          Delete a branch from a database
  demote          Demote a production branch to development
  list            List all branches of a database
  promote         Promote a new branch from a database
  schema          Show the schema of a branch
  show            Show a specific branch of a database
  switch          Switches the current project to use the specified branch
  update          Update a branch's name or deletion protection

MySQL and Postgres:
  connections     Show and kill MySQL or Postgres branch connections

Vitess/MySQL-specific:
  diff            Show the schema diff of a MySQL branch
  lint            Lint the schema of a MySQL branch
  query-patterns  List, show, delete, and download query pattern reports for a MySQL branch
  refresh-schema  Refresh the schema for a MySQL branch
  routing-rules   Fetch or update keyspace routing rules for a MySQL branch
  safe-migrations Enable or disable safe migrations on a MySQL branch
  vtgate          Manage VTGate size for a Vitess branch

Postgres-specific:
  extensions      List extensions available on a Postgres branch
  parameters      List the configuration parameters of a Postgres branch
  resize          Change a Postgres branch's cluster size, replicas, or parameters
  switchover      Switch over the primary of a Postgres branch (Postgres only)

Postgres and Neki:
  maintenance     Run maintenance for a Postgres or Neki branch

Neki-specific:
  admin           Manage the admin config for a Neki database branch
  config-profile  Manage configuration profiles for a Neki database branch
  data-topology   Fetch or update the data topology of a Neki branch
  router          Manage routers for a Neki database branch
  shard           Manage shards for a Neki database branch
  sidecar         Manage sidecars for a Neki database branch

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

## pscale branch data-topology

```text
Fetch or update the data topology of a Neki branch

Usage:
  pscale branch data-topology [command]

Available Commands:
  get         Show the data topology of a Neki branch
  ls          Show the relationships in a Neki branch's data topology
  update      Update the data topology of a Neki branch from standard input

Flags:
  -h, --help   help for data-topology

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

Use "pscale branch data-topology [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch data-topology get

```text
Show the data topology of a Neki branch

Usage:
  pscale branch data-topology get <database> <branch> [flags]

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

## pscale branch data-topology ls

```text
Show the relationships in a Neki branch's data topology

Usage:
  pscale branch data-topology ls <database> <branch> [flags]

Examples:
  pscale branch data-topology ls mydb main --org my-org --format json
  pscale branch data-topology ls mydb main --org my-org --shards --format json

Flags:
  -h, --help     help for ls
      --shards   Group data by the physical shards that host it

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

## pscale branch data-topology update

```text
Update the data topology of a Neki branch from standard input

Usage:
  pscale branch data-topology update <database> <branch> [flags]

Examples:
  pscale branch data-topology update mydb main --org my-org --format json < data-topology.json

Flags:
  -h, --help   help for update

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

## pscale branch shard

```text
Manage shards for a Neki database branch.

This command is only supported for Neki databases.

Usage:
  pscale branch shard [command]

Available Commands:
  assign      Assign shards to a Neki configuration profile
  create      Create shards in a Neki configuration profile
  delete      Delete a shard from a Neki database branch
  list        List shards for a Neki database branch
  show        Show a shard for a Neki database branch
  update      Update a Neki shard's display name

Flags:
  -h, --help   help for shard

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

Use "pscale branch shard [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch shard list

```text
List shards for a Neki database branch

Usage:
  pscale branch shard list <database> <branch> [flags]

Aliases:
  list, ls

Flags:
      --config-profile string           List shards assigned to this configuration profile
      --exclude-config-profile string   Exclude shards assigned to this configuration profile
  -h, --help                            help for list
      --page int                        Page number to fetch
      --per-page int                    Number of results per page (default 100)
  -q, --query string                    Search by shard name, display name, or configuration profile

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

## pscale branch shard show

```text
Show a shard for a Neki database branch

Usage:
  pscale branch shard show <database> <branch> <shard-id> [flags]

Aliases:
  show, get

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

## pscale branch shard create

```text
Create shards in a Neki configuration profile

Usage:
  pscale branch shard create <database> <branch> [flags]

Flags:
      --config-profile string   Configuration profile that will host the new shards (required)
      --count int               Number of shards to create (default 1)
  -h, --help                    help for create

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

## pscale branch shard assign

```text
Assign shards to a Neki configuration profile

Usage:
  pscale branch shard assign <database> <branch> <shard-id>... [flags]

Flags:
      --config-profile string   Configuration profile to assign the shards to (required)
  -h, --help                    help for assign

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

## pscale branch shard update

```text
Update a Neki shard's display name

Usage:
  pscale branch shard update <database> <branch> <shard-id> [flags]

Flags:
      --display-name string   New display name; pass an empty string to clear it (required)
  -h, --help                  help for update

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

## pscale branch shard delete

```text
Delete a shard from a Neki database branch

Usage:
  pscale branch shard delete <database> <branch> <shard-id> [flags]

Aliases:
  delete, rm

Flags:
      --force   Delete the shard without confirmation
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

## pscale branch config-profile

```text
Manage configuration profiles for a Neki database branch.

This command is only supported for Neki databases.

Usage:
  pscale branch config-profile [command]

Available Commands:
  changes     Manage changes to a Neki configuration profile
  create      Create a Neki configuration profile
  default     Show the default Neki configuration profile
  delete      Delete a Neki configuration profile
  extensions  List extensions for a Neki configuration profile
  list        List configuration profiles for a Neki branch
  maintenance Run maintenance for one or more Neki configuration profiles
  parameters  List parameters for a Neki configuration profile
  set-default Set the default Neki configuration profile
  show        Show a Neki configuration profile
  update      Update a Neki configuration profile

Flags:
  -h, --help   help for config-profile

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

Use "pscale branch config-profile [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch config-profile list

```text
List configuration profiles for a Neki branch

Usage:
  pscale branch config-profile list <database> <branch> [flags]

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

## pscale branch config-profile show

```text
Show a Neki configuration profile

Usage:
  pscale branch config-profile show <database> <branch> <name> [flags]

Aliases:
  show, get

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

## pscale branch config-profile create

```text
Create a Neki configuration profile

Usage:
  pscale branch config-profile create <database> <branch> <name> [flags]

Flags:
      --cluster-size string             Cluster size for shards in the profile
  -h, --help                            help for create
      --max-storage int                 Maximum storage size in bytes for autoscaling
      --min-storage int                 Minimum storage size in bytes
      --postgres-major-version string   PostgreSQL major version
      --postgres-minor-version string   PostgreSQL minor version
      --replicas int                    Number of replicas for shards in the profile
      --storage-autoscaling             Enable storage autoscaling
      --storage-iops int                Storage IOPS
      --storage-throughput int          Storage throughput in MiB/s

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

## pscale branch config-profile update

```text
Update a Neki configuration profile

Usage:
  pscale branch config-profile update <database> <branch> <name> [flags]

Flags:
      --cluster-size string             New cluster size for shards in the profile
  -h, --help                            help for update
      --max-storage int                 Maximum storage size in bytes for autoscaling
      --min-storage int                 Minimum storage size in bytes
      --name string                     New name for the configuration profile
      --parameters stringArray          Set a parameter as namespace.name=value; repeatable
      --postgres-major-version string   PostgreSQL major version
      --postgres-minor-version string   PostgreSQL minor version
      --replicas int                    New number of replicas for shards in the profile
      --storage-autoscaling             Enable storage autoscaling
      --storage-iops int                Storage IOPS
      --storage-throughput int          Storage throughput in MiB/s

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

## pscale branch config-profile delete

```text
Delete a Neki configuration profile

Usage:
  pscale branch config-profile delete <database> <branch> <name> [flags]

Aliases:
  delete, rm

Flags:
      --force   Delete the configuration profile without confirmation
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

## pscale branch config-profile default

```text
Show the default Neki configuration profile

Usage:
  pscale branch config-profile default <database> <branch> [flags]

Flags:
  -h, --help   help for default

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

## pscale branch config-profile set-default

```text
Set the default Neki configuration profile

Usage:
  pscale branch config-profile set-default <database> <branch> <name> [flags]

Flags:
  -h, --help   help for set-default

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

## pscale branch config-profile parameters

```text
List parameters for a Neki configuration profile

Usage:
  pscale branch config-profile parameters <database> <branch> <name> [flags]

Aliases:
  parameters, params

Flags:
      --extension          Only show extension parameters
  -h, --help               help for parameters
      --internal           Only show internal parameters
      --namespace string   Only show parameters in this namespace

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

## pscale branch config-profile maintenance

```text
Run maintenance for one or more Neki configuration profiles, updating them
to the latest available image.

The upgrade is applied to the replicas first, followed by a switchover from the
old primary to an upgraded replica. That failover leads to a short period of
database unavailability (seconds), and all direct connections to those shards
are terminated.

Use 'pscale branch maintenance run' to maintain every profile on the branch.

Usage:
  pscale branch config-profile maintenance <database> <branch> <name>... [flags]

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

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch config-profile extensions

```text
List extensions for a Neki configuration profile

Usage:
  pscale branch config-profile extensions <database> <branch> <name> [flags]
  pscale branch config-profile extensions [command]

Available Commands:
  disable     Disable an extension for a Neki configuration profile
  enable      Enable an extension for a Neki configuration profile

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

Use "pscale branch config-profile extensions [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch config-profile extensions enable

```text
Enable an extension for a Neki configuration profile

Usage:
  pscale branch config-profile extensions enable <database> <branch> <name> <extension> [flags]

Flags:
  -h, --help   help for enable

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

## pscale branch config-profile extensions disable

```text
Disable an extension for a Neki configuration profile

Usage:
  pscale branch config-profile extensions disable <database> <branch> <name> <extension> [flags]

Flags:
  -h, --help   help for disable

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

## pscale branch config-profile changes

```text
Manage changes to a Neki configuration profile

Usage:
  pscale branch config-profile changes [command]

Available Commands:
  cancel      Cancel a pending change to a Neki configuration profile
  list        List changes for a Neki configuration profile
  show        Show a change to a Neki configuration profile

Flags:
  -h, --help   help for changes

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

Use "pscale branch config-profile changes [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch config-profile changes list

```text
List changes for a Neki configuration profile

Usage:
  pscale branch config-profile changes list <database> <branch> <name> [flags]

Aliases:
  list, ls

Flags:
      --completed-at string   Only show changes completed at this time
  -h, --help                  help for list
      --page int              Page number to fetch
      --per-page int          Number of results per page (default 100)
      --period string         Only show changes from this period

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

## pscale branch config-profile changes show

```text
Show a change to a Neki configuration profile

Usage:
  pscale branch config-profile changes show <database> <branch> <name> <change-id> [flags]

Aliases:
  show, get

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

## pscale branch config-profile changes cancel

```text
Cancel a pending change to a Neki configuration profile

Usage:
  pscale branch config-profile changes cancel <database> <branch> <name> <change-id> [flags]

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

## pscale branch router

```text
Manage routers for a Neki database branch.

This command is only supported for Neki databases.

Usage:
  pscale branch router [command]

Available Commands:
  changes     Manage changes to a Neki router
  create      Create a router for a Neki database branch
  delete      Delete a router from a Neki database branch
  list        List routers for a Neki database branch
  show        Show a router for a Neki database branch
  sizes       List available router sizes for a Neki database branch
  update      Update a router for a Neki database branch

Flags:
  -h, --help   help for router

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

Use "pscale branch router [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch router list

```text
List routers for a Neki database branch

Usage:
  pscale branch router list <database> <branch> [flags]

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

## pscale branch router show

```text
Show a router for a Neki database branch

Usage:
  pscale branch router show <database> <branch> <name> [flags]

Aliases:
  show, get

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

## pscale branch router create

```text
Create a router for a Neki database branch

Usage:
  pscale branch router create <database> <branch> <name> [flags]

Flags:
  -h, --help                    help for create
      --replicas-per-cell int   Number of replicas in each cell
      --size string             Router size SKU (e.g. NKR-5); the API picks a default if omitted

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

## pscale branch router update

```text
Update a router for a Neki database branch.

Changes are requested and applied asynchronously; the router state shows progress.

Usage:
  pscale branch router update <database> <branch> <name> [flags]

Flags:
      --autoscaling                  Whether the router scales horizontally within each cell
  -h, --help                         help for update
      --max-replicas-per-cell int    Maximum number of replicas in each cell when autoscaling
      --parameters stringArray       Set a parameter as namespace.name=value; repeatable
      --replicas-per-cell int        New number of replicas in each cell
      --size string                  New router size SKU (e.g. NKR-5)
      --target-cpu-utilization int   Target average CPU utilization percentage when autoscaling

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

## pscale branch router delete

```text
Delete a router from a Neki database branch

Usage:
  pscale branch router delete <database> <branch> <name> [flags]

Aliases:
  delete, rm

Flags:
      --force   Delete the router without confirmation
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

## pscale branch router sizes

```text
List available router sizes for a Neki database branch

Usage:
  pscale branch router sizes <database> <branch> [flags]

Aliases:
  sizes, size-skus

Flags:
  -h, --help   help for sizes

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

## pscale branch router changes

```text
Manage changes to a Neki router

Usage:
  pscale branch router changes [command]

Available Commands:
  cancel      Cancel a pending change to a Neki router
  list        List changes for a Neki router
  show        Show a change to a Neki router

Flags:
  -h, --help   help for changes

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

Use "pscale branch router changes [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch router changes list

```text
List changes for a Neki router

Usage:
  pscale branch router changes list <database> <branch> <router> [flags]

Aliases:
  list, ls

Flags:
      --completed-at string   Only show changes completed at this time
  -h, --help                  help for list
      --page int              Page number to fetch
      --per-page int          Number of results per page (default 100)
      --period string         Only show changes from this period

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

## pscale branch router changes show

```text
Show a change to a Neki router

Usage:
  pscale branch router changes show <database> <branch> <router> <change-id> [flags]

Aliases:
  show, get

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

## pscale branch router changes cancel

```text
Cancel a pending change to a Neki router

Usage:
  pscale branch router changes cancel <database> <branch> <router> <change-id> [flags]

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

## pscale branch sidecar

```text
Manage sidecars for a Neki database branch.

Each configuration profile has one sidecar. Sidecars are created and deleted with their profile. This command is only supported for Neki databases.

Usage:
  pscale branch sidecar [command]

Available Commands:
  changes     Manage changes to a Neki sidecar
  list        List sidecars for a Neki database branch
  parameters  List parameters for a Neki sidecar
  show        Show a sidecar for a Neki database branch
  update      Update a sidecar for a Neki database branch

Flags:
  -h, --help   help for sidecar

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

Use "pscale branch sidecar [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch sidecar list

```text
List sidecars for a Neki database branch

Usage:
  pscale branch sidecar list <database> <branch> [flags]

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

## pscale branch sidecar show

```text
Show a sidecar for a Neki database branch.

<sidecar> is the sidecar ID from `sidecar list`, or the configuration profile name.

Usage:
  pscale branch sidecar show <database> <branch> <sidecar> [flags]

Aliases:
  show, get

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

## pscale branch sidecar update

```text
Update a sidecar for a Neki database branch.

<sidecar> is the sidecar ID from `sidecar list`, or the configuration profile name.
Changes are requested and applied asynchronously; the sidecar state shows progress.

Usage:
  pscale branch sidecar update <database> <branch> <sidecar> [flags]

Flags:
  -h, --help                     help for update
      --parameters stringArray   Set a parameter as namespace.name=value; repeatable

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

## pscale branch sidecar parameters

```text
List parameters for a Neki sidecar.

<sidecar> is the sidecar ID from `sidecar list`, or the configuration profile name.

Usage:
  pscale branch sidecar parameters <database> <branch> <sidecar> [flags]

Aliases:
  parameters, params

Flags:
  -h, --help   help for parameters

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

## pscale branch sidecar changes

```text
Manage changes to a Neki sidecar

Usage:
  pscale branch sidecar changes [command]

Available Commands:
  cancel      Cancel a pending change to a Neki sidecar
  list        List changes for a Neki sidecar
  show        Show a change to a Neki sidecar

Flags:
  -h, --help   help for changes

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

Use "pscale branch sidecar changes [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch sidecar changes list

```text
List changes for a Neki sidecar

Usage:
  pscale branch sidecar changes list <database> <branch> <sidecar> [flags]

Aliases:
  list, ls

Flags:
      --completed-at string   Only show changes completed at this time
  -h, --help                  help for list
      --page int              Page number to fetch
      --per-page int          Number of results per page (default 100)
      --period string         Only show changes from this period

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

## pscale branch sidecar changes show

```text
Show a change to a Neki sidecar

Usage:
  pscale branch sidecar changes show <database> <branch> <sidecar> <change-id> [flags]

Aliases:
  show, get

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

## pscale branch sidecar changes cancel

```text
Cancel a pending change to a Neki sidecar

Usage:
  pscale branch sidecar changes cancel <database> <branch> <sidecar> <change-id> [flags]

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

## pscale branch admin

```text
Manage the admin config for a Neki database branch.

Each cluster has one admin. The admin is created and deleted with the cluster. This command is only supported for Neki databases.

Usage:
  pscale branch admin [command]

Available Commands:
  changes     Manage changes to a Neki admin
  parameters  List parameters for a Neki admin
  show        Show the admin for a Neki database branch
  sizes       List available admin sizes for a Neki database branch
  update      Update the admin for a Neki database branch

Flags:
  -h, --help   help for admin

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

Use "pscale branch admin [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch admin show

```text
Show the admin for a Neki database branch.

Each cluster has one admin.

Usage:
  pscale branch admin show <database> <branch> [flags]

Aliases:
  show, get

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

## pscale branch admin update

```text
Update the admin for a Neki database branch.

Changes are requested and applied asynchronously; the admin state shows progress.

Usage:
  pscale branch admin update <database> <branch> [flags]

Flags:
  -h, --help                     help for update
      --parameters stringArray   Set a parameter as namespace.name=value; repeatable
      --size string              New admin size SKU (e.g. NKA-0)

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

## pscale branch admin parameters

```text
List parameters for a Neki admin.

Each cluster has one admin.

Usage:
  pscale branch admin parameters <database> <branch> [flags]

Aliases:
  parameters, params

Flags:
  -h, --help   help for parameters

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

## pscale branch admin sizes

```text
List available admin sizes for a Neki database branch

Usage:
  pscale branch admin sizes <database> <branch> [flags]

Aliases:
  sizes, size-skus

Flags:
  -h, --help   help for sizes

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

## pscale branch admin changes

```text
Manage changes to a Neki admin

Usage:
  pscale branch admin changes [command]

Available Commands:
  cancel      Cancel a pending change to a Neki admin
  list        List changes for a Neki admin
  show        Show a change to a Neki admin

Flags:
  -h, --help   help for changes

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

Use "pscale branch admin changes [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch admin changes list

```text
List changes for a Neki admin

Usage:
  pscale branch admin changes list <database> <branch> [flags]

Aliases:
  list, ls

Flags:
      --completed-at string   Only show changes completed at this time
  -h, --help                  help for list
      --page int              Page number to fetch
      --per-page int          Number of results per page (default 100)
      --period string         Only show changes from this period

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

## pscale branch admin changes show

```text
Show a change to a Neki admin

Usage:
  pscale branch admin changes show <database> <branch> <change-id> [flags]

Aliases:
  show, get

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

## pscale branch admin changes cancel

```text
Cancel a pending change to a Neki admin

Usage:
  pscale branch admin changes cancel <database> <branch> <change-id> [flags]

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

## pscale size cluster list

```text
List the sizes that are available for a PlanetScale database. By default, shows all clusters for all engines. Use --engine to filter by a specific engine type.

Usage:
  pscale size cluster list [flags]

Aliases:
  list, ls

Flags:
      --engine string   Filter cluster sizes by database engine. Supported values: mysql, postgresql, neki. If not specified, shows all clusters for all engines.
  -h, --help            help for list
      --metal           view cluster sizes and rates for clusters with metal storage
      --region string   view cluster sizes and rates for a specific region

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

## pscale database create

```text
Create a database instance

Usage:
  pscale database create <database> [flags]

Flags:
      --cluster-size pscale size cluster list   cluster size for Scaler Pro databases. Use pscale size cluster list to see the valid sizes.
      --engine string                           The database engine for the database. Supported values: mysql, postgresql, neki. Defaults to mysql. (default "mysql")
  -h, --help                                    help for create
      --major-version string                    For Postgres or Neki databases, the Postgres major version to use. Defaults to the latest available major version.
      --max-storage int                         Maximum storage size in bytes for autoscaling
      --min-storage int                         Minimum storage size in bytes
      --region string                           region for the database
      --replicas int                            number of replicas for Postgres or Neki databases. Use 0 for single-node Postgres or 2 or more for HA.
      --wait                                    Wait until the database is ready

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
Manage maintenance for a Postgres or Neki branch.

PlanetScale upgrades a branch's image in emergencies, such as patching security
issues, or when you initiate the upgrade yourself. 'maintenance run' initiates
one.

See https://planetscale.com/docs/postgres/operations-philosophy

Usage:
  pscale branch maintenance [command]

Available Commands:
  run         Run maintenance for a Postgres or Neki branch now

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
Run maintenance for a Postgres or Neki branch, updating it to the latest
available image. Vitess (MySQL) databases are not supported.

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

## pscale backup restore

```text
Restore a backup to a new branch.

<new-branch> is the name of the branch to create. It must not already exist.
The backup is identified by id; the source branch is not a restore argument.
Preview Neki restore sizes from the source branch with:

  pscale backup restore show <database> <source-branch> <backup>

Usage:
  pscale backup restore <database> <new-branch> <backup> [flags]
  pscale backup restore [command]

Available Commands:
  show        Show the sizes a Neki backup restore will use if you do not override them

Flags:
      --cluster-size pscale size cluster list   Cluster size for restored backup branch. For Neki, omitted unless set so the source default profile size is used. Use pscale size cluster list to see the valid sizes. (default "PS-10")
      --config-profile stringArray              For Neki backup restores, size and replica count for one configuration profile as name=<profile>[,cluster-size=<size>][,replicas=<n>]. Repeatable. Omitted profiles inherit the source. List names with 'pscale branch config-profile list' on the source branch.
  -h, --help                                    help for restore
      --replicas int                            Number of additional replicas for a PostgreSQL restore. 0 creates a single-node branch; omit to use the target cluster size default.
      --router stringArray                      For Neki backup restores, size and replica count for one router as name=<router>[,size=<sku>][,replicas-per-cell=<n>]. Repeatable. Omitted routers inherit the source. List names with 'pscale branch router list' on the source branch.

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

Use "pscale backup restore [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale backup restore show

```text
Show the configuration profile and router sizes a Neki backup restore will use.

These values come from the live source branch, the same source the dashboard
pickers use. They are not stored on the backup. If the source branch was resized
after the backup, this command shows the current sizes.

<branch> is the source branch the backup belongs to, same as backup show.

Usage:
  pscale backup restore show <database> <branch> <backup> [flags]

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

## pscale shell

```text
Open a shell instance to a database and branch

Usage:
  pscale shell [database] [branch] [db-name] [flags]

Examples:
The shell subcommand opens a secure shell instance to your database.

For MySQL databases, it uses the MySQL command-line client ("mysql").
For Postgres databases, it uses the Postgres command-line client ("psql").

By default, if no branch names are given and there is only one branch, it
automatically opens a shell to that branch:

  pscale shell mydatabase

If there are multiple branches for the given database, you'll be prompted to
choose one. To open a shell instance to a specific branch, pass the branch as a
second argument:

  pscale shell mydatabase mybranch

For Postgres databases, you can optionally specify the logical database
to connect to using --db-name (or as a third argument):

  pscale shell production main --db-name my_db
  pscale shell production main my_db

Flags:
      --db-name string              Postgres logical database name to connect to (default: postgres). Only supported for Postgres databases.
  -h, --help                        help for shell
      --local-addr string           Local address to bind and listen for connections. By default the proxy binds to 127.0.0.1 with a random port.
      --org string                  The organization for the current user
      --remote-addr hostname:port   PlanetScale Database remote network address. By default the remote address is populated automatically from the PlanetScale API. (format: hostname:port)
      --replica                     When enabled, the password will route all reads to the branch's primary replicas and all read-only regions.
      --role string                 Role defines the access level, allowed values are: reader, writer, readwriter, admin. Defaults to 'reader' for replica passwords, otherwise defaults to 'admin'.
      --router string               Connect through the named router group. Only supported for Neki databases.

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale sql

```text
Execute a single SQL query against a database branch using ephemeral credentials.

Use --format json for machine-readable output. This command is intended for agents and scripts;
for interactive sessions use pscale shell instead.

Access flags match pscale shell: --role (reader, writer, readwriter, admin) and --replica.
Unlike shell, the default role is reader. Pass --role admin (or writer/readwriter) for writes.

Destructive SQL containing DELETE, DROP, or TRUNCATE is blocked unless --force is passed.
Agents must ask the user for approval before using --force.

MySQL (Vitess) databases use the primary keyspace by default (same as pscale shell -D @primary).
Pass --keyspace when targeting a specific keyspace in a multi-keyspace database. A keyspace may
include a shard and tablet type (mykeyspace/-80, mykeyspace/-80@replica) to pin the connection to
one shard; enumerate shards with SHOW VITESS_SHARDS.

Postgres or Neki databases use --dbname (default postgres).

Human output prints rows as a table. Pass --vertical (or end the query with \G,
like the mysql client) to print one column per line, which is easier to read for
wide results such as SHOW REPLICA STATUS.

Place flags after positional arguments (see Usage). --org is required:

  pscale sql <database> <branch> --org <org> --format json --query "SELECT 1"

Usage:
  pscale sql <database> <branch> [flags]

Examples:
  # Read query (default reader role)
  pscale sql <database> <branch> --org <org> --format json --query "SELECT 1"

  # Read from replica
  pscale sql <database> <branch> --org <org> --format json --replica --query "SELECT 1"

  # MySQL — keyspace optional (@primary default)
  pscale sql <database> <branch> --org <org> --format json --keyspace <keyspace> --query "SELECT 1"

  # Vertical output for wide rows (--vertical, or end the query with \G)
  pscale sql <database> <branch> --org <org> --replica --query "SHOW REPLICA STATUS\G"

Flags:
      --dbname string     Postgres or Neki database name (default "postgres")
      --force             Allow destructive SQL (DELETE, DROP, TRUNCATE). Only use after the user explicitly approves.
  -h, --help              help for sql
      --keyspace string   Vitess keyspace, optionally with a shard and tablet type (e.g. mykeyspace, mykeyspace/-80, mykeyspace/-80@replica). List shards with --query "SHOW VITESS_SHARDS". Defaults to @primary, same as pscale shell.
      --org string        The organization for the current user
      --query string      SQL query to execute (required)
      --replica           When enabled, the password will route all reads to the branch's primary replicas and all read-only regions.
      --role string       Role defines the access level, allowed values are: reader, writer, readwriter, admin. Defaults to reader (use --role admin for writes).
      --vertical          Print each row vertically, one column per line. Same as ending the query with \G in the mysql client.

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale role

```text
Manage database roles for a Postgres or Neki database branch.

This command is supported for Postgres or Neki databases.

Usage:
  pscale role [command]

Available Commands:
  create        Create a new role for a Postgres or Neki database branch
  default       Show the default postgres role
  delete        Delete a role
  get           Retrieve information about a specific role
  list          List all roles for a Postgres or Neki database branch
  reassign      Reassign objects owned by a role to another role
  renew         Renew a role's expiration
  reset         Reset a role's password
  reset-default Reset the credentials for the default `postgres` role
  update        Update a role's name

Flags:
  -h, --help         help for role
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

Use "pscale role [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale role list

```text
List all roles for a Postgres or Neki database branch

Usage:
  pscale role list <database> <branch> [flags]

Aliases:
  list, ls

Flags:
  -h, --help            help for list
      --name string     Filter roles by name using a substring match
      --page int        Page number to fetch
      --per-page int    Number of results per page (default 100)
      --status string   Filter roles by status (active, renewable, disabled, or expired)
  -w, --web             List roles in your web browser.

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

## pscale role get

```text
Retrieve information about a specific role

Usage:
  pscale role get <database> <branch> <role-id> [flags]

Flags:
      --bouncer string             Return connection details for a PgBouncer (name).
  -h, --help                       help for get
      --read-only-replica string   Return connection details for a read-only replica (name).
      --replica                    Return connection details for a branch replica.

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

## pscale role default

```text
Show the default postgres role for a branch.

This does not rotate credentials. Use 'pscale role reset-default' to issue a
new password for the default role.

Usage:
  pscale role default <database> <branch> [flags]

Flags:
  -h, --help   help for default

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

## pscale role reset-default

```text
This command resets the credentials for the default `postgres` role in the database, allowing you to reconfigure access. Any connections using the `postgres` role will need to be updated with the new credentials.

Usage:
  pscale role reset-default <database> <branch> [flags]

Flags:
      --force   Force reset without confirmation
  -h, --help    help for reset-default

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

## pscale role create

```text
Create a new role for a Postgres or Neki database branch

Usage:
  pscale role create <database> <branch> <name> [flags]

Examples:
  # Create a role with admin access
  pscale role create mydb main my-role --inherited-roles postgres

  # Create a role with REPLICATION privilege (requires the postgres inherited role)
  pscale role create mydb main replicator --inherited-roles postgres --with-replication

Flags:
  -h, --help                     help for create
      --inherited-roles string   Comma-separated list of role names to inherit privileges from. Common values are 'pg_read_all_data' for read access, 'pg_write_all_data' for write access, and 'postgres' for admin access.
      --ttl duration             TTL defines the time to live for the role. Durations such as "30m", "24h", or bare integers such as "3600" (seconds) are accepted. The default TTL is 0s, which means the role will never expire. (default 0s)
      --with-replication         When enabled, the role is created with REPLICATION privilege for logical replication. Requires --inherited-roles to include 'postgres'.

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

## pscale role update

```text
Update a role's name

Usage:
  pscale role update <database> <branch> <role-id> [flags]

Flags:
  -h, --help          help for update
      --name string   New name for the role (required)

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

## pscale role renew

```text
Renew a role's expiration

Usage:
  pscale role renew <database> <branch> <role-id> [flags]

Flags:
  -h, --help   help for renew

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

## pscale role reset

```text
Reset a role's password

Usage:
  pscale role reset <database> <branch> <role-id> [flags]

Flags:
      --force   Reset password without confirmation
  -h, --help    help for reset

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

## pscale role delete

```text
Delete a role

Usage:
  pscale role delete <database> <branch> <role-id> [flags]

Aliases:
  delete, rm

Flags:
      --force              Delete a role without confirmation
  -h, --help               help for delete
      --successor string   Role to transfer ownership to before deletion. Usually 'postgres'.

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

## pscale role reassign

```text
Reassign objects owned by a role to another role

Usage:
  pscale role reassign <database> <branch> <role-id> [flags]

Examples:
  # List roles and copy the source role's id value
  pscale role list mydb main --org my-org

  # Reassign objects owned by role tq8hnwl1mlty to successor role pscale_api_stqrbvtoy367
  pscale role reassign mydb main tq8hnwl1mlty --successor pscale_api_stqrbvtoy367 --org my-org

Flags:
      --force              Reassign objects without confirmation
  -h, --help               help for reassign
      --successor string   Successor role to transfer ownership to (required) (required)

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
