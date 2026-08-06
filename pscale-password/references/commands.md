Create, list, and delete branch passwords.

This command is only supported for Vitess databases.

Usage:
  pscale password [command]

Available Commands:
  create      Create password to access a branch's data
  delete      Delete a branch password
  list        List all passwords of a database
  renew       Renew a branch password

Flags:
  -h, --help         help for password
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

Use "pscale password [command] --help" for more information about a command.

## pscale password create

```text
Create password to access a branch's data

Usage:
  pscale password create <database> <branch> <name> [flags]

Aliases:
  create, p

Flags:
  -h, --help                      help for create
      --read-only-region string   Create a password scoped to a Vitess read-only region (region slug, display name, or id). List regions with: pscale keyspace read-only-regions <database> <branch> <keyspace>.
      --replica                   When enabled, the password will route all reads to the branch's primary replicas and all read-only regions.
      --role string               Role defines the access level, allowed values are: reader, writer, readwriter, admin. Defaults to 'reader' for replica and read-only region passwords, otherwise defaults to 'admin'.
      --ttl duration              TTL defines the time to live for the password. Durations such as "30m", "24h", or bare integers such as "3600" (seconds) are accepted. The default TTL is 0s, which means the password will never expire. (default 0s)
```

`--read-only-region` and `--replica` are mutually exclusive. A region-scoped password defaults to `reader`, requires the selected region to be ready, and is labeled as a read-only-region credential in create output.

## pscale password list

```text
List all passwords of a database

Usage:
  pscale password list <database> [branch] [flags]

Aliases:
  list, ls

Flags:
  -h, --help            help for list
      --name string     Filter passwords by name using a substring match
      --page int        Page number to fetch
      --per-page int    Number of results per page (default 100)
      --status string   Filter passwords by status (active, renewable, or expired)
  -w, --web             List passwords in your web browser.

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

## pscale role list (Postgres equivalent)

```text
List all roles for a Postgres database branch

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
```
