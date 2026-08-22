Create, list, show, update, renew, and delete branch passwords.

All help fences below are exact output from the official, checksum-verified PlanetScale CLI v0.324.0 macOS arm64 release binary after normalizing only trailing whitespace. Role surfaces are included because Postgres branches use roles instead of Vitess passwords.

## pscale password

```text
Create, list, update, and delete branch passwords.

This command is only supported for Vitess databases.

Usage:
  pscale password [command]

Available Commands:
  create      Create password to access a branch's data
  delete      Delete a branch password
  list        List all passwords of a database
  renew       Renew a branch password
  show        Show a branch password
  update      Update a branch password's name or IP restrictions

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

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

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

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale password show

```text
Show a branch password.

Only metadata is returned. The password itself is shown once, when it is
created or renewed, and cannot be retrieved afterwards.

Usage:
  pscale password show <database> <branch> [<password-id>] [flags]

Flags:
  -h, --help          help for show
      --name string   Show password by name instead of ID

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

## pscale password update

```text
Update a branch password's name or IP restrictions.

This does not change the password itself. To rotate a password, create a new
one and delete the old one.

Usage:
  pscale password update <database> <branch> [<password-id>] [flags]

Examples:
  pscale password update mydb main pscale_pw_xxx --new-name reporting
  pscale password update mydb main --name reporting --cidrs 10.0.0.0/8,192.168.1.1/32
  pscale password update mydb main --name reporting --cidrs ""

Flags:
      --cidrs strings     Replace the IP addresses and CIDR ranges allowed to use this password. Pass an empty value to remove all restrictions
  -h, --help              help for update
      --name string       Update password by name instead of ID
      --new-name string   New name for the password

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

## pscale password renew

```text
Renew a branch password

Usage:
  pscale password renew <database> <branch> <password-id> [flags]

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

## pscale password delete

```text
Delete a branch password

Usage:
  pscale password delete <database> <branch> [<password-id>] [flags]

Aliases:
  delete, rm

Flags:
      --force         Delete a password without confirmation
  -h, --help          help for delete
      --name string   Delete password by name instead of ID

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

## pscale role

```text
Manage database roles for a Postgres database branch.

This command is only supported for Postgres databases.

Usage:
  pscale role [command]

Available Commands:
  create        Create a new role for a Postgres database branch
  default       Show the default postgres role
  delete        Delete a role
  get           Retrieve information about a specific role
  list          List all roles for a Postgres database branch
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

## pscale role get

```text
Retrieve information about a specific role

Usage:
  pscale role get <database> <branch> <role-id> [flags]

Flags:
      --bouncer string             Return connection details for a PgBouncer (name).
  -h, --help                       help for get
      --read-only-replica string   Return connection details for a regional read-only replica (region slug).
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

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```
