All help fences below are exact output from the official, checksum-verified PlanetScale CLI v0.329.0 macOS arm64 release binary after normalizing only trailing whitespace. The archive SHA-256 is `2cc70050c1f7397ed1a5c272a5d1bbe1217803966717991466057ffc806c2f7b`.

## `pscale read-only-replica`

```text
Manage read-only replicas for a PostgreSQL database branch.

Read-only replicas provide dedicated capacity for queries that can tolerate
replication lag. They accept read traffic only.

This command is only available for PostgreSQL databases.

Usage:
  pscale read-only-replica [command]

Available Commands:
  create      Create a read-only replica
  delete      Delete a read-only replica
  list        List read-only replicas for a Postgres branch
  show        Show a read-only replica
  update      Update a read-only replica

Flags:
  -h, --help         help for read-only-replica
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

Use "pscale read-only-replica [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## `pscale read-only-replica list`

```text
List read-only replicas for a Postgres branch

Usage:
  pscale read-only-replica list <database> <branch> [flags]

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

## `pscale read-only-replica show`

```text
Show a read-only replica

Usage:
  pscale read-only-replica show <database> <branch> <name> [flags]

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

## `pscale read-only-replica create`

```text
Create a read-only replica for a PostgreSQL database branch.

Region is required. The replica count defaults to 1 and the cluster size
defaults to the primary cluster size when those flags are omitted.

Usage:
  pscale read-only-replica create <database> <branch> <name> [flags]

Flags:
      --cluster-size string   Cluster size SKU; defaults to the primary cluster size
  -h, --help                  help for create
      --region string         Region slug for the read-only replica (required)
      --replicas int          Number of instances serving reads (default 1)

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

## `pscale read-only-replica update`

```text
Update a read-only replica's cluster size, instance count, and/or
PostgreSQL configuration parameters. Parameter values must be greater than or
equal to the primary branch's corresponding values.

Usage:
  pscale read-only-replica update <database> <branch> <name> [flags]

Examples:
  pscale read-only-replica update mydb main analytics --replicas 2
  pscale read-only-replica update mydb main analytics --cluster-size PS_20_GCP_X86
  pscale read-only-replica update mydb main analytics --parameters pgconf.max_connections=300

Flags:
      --cluster-size string      New cluster size SKU
  -h, --help                     help for update
      --parameters stringArray   Set a parameter as namespace.name=value (for example pgconf.max_connections=300); repeatable
      --replicas int             Desired number of instances serving reads

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

## `pscale read-only-replica delete`

```text
Delete a read-only replica

Usage:
  pscale read-only-replica delete <database> <branch> <name> [flags]

Aliases:
  delete, rm

Flags:
      --force   Delete a read-only replica without confirmation
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
