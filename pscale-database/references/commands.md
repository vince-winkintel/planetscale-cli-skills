> All help fences below are exact output from the official, checksum-verified PlanetScale CLI v0.324.0 macOS arm64 release binary after normalizing only trailing whitespace.

## pscale database

```text
Create, read, update, delete, and dump/restore databases

Usage:
  pscale database [command]

Aliases:
  database, db

Available Commands:
  aggressive-cutover Show or change aggressive cutover for a database
  create             Create a database instance
  delete             Delete a database instance
  dump               Backup and dump your database (Vitess databases only)
  ip-restriction     Manage Postgres IP restrictions
  list               List databases
  restore-dump       Restore your database from a local dump directory (Vitess databases only)
  show               Retrieve information about a database, including settings
  throttler          Show or update database throttler configuration
  update             Update a database's settings

Flags:
  -h, --help         help for database
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

Use "pscale database [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale database aggressive-cutover

```text
Show, enable, or disable aggressive cutover for a Vitess database.

When enabled, future deploy requests on this database cut over more
aggressively when waiting on table locks. This is a database-level setting,
not the same as forcing cutover on a single deploy request
(pscale deploy-request force-cutover).

See https://planetscale.com/docs/vitess/schema-changes/aggressive-cutover

Usage:
  pscale database aggressive-cutover [command]

Available Commands:
  disable     Disable aggressive cutover for a database
  enable      Enable aggressive cutover for a database
  show        Show whether aggressive cutover is enabled

Flags:
  -h, --help   help for aggressive-cutover

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

Use "pscale database aggressive-cutover [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale database aggressive-cutover show

```text
Show whether aggressive cutover is enabled

Usage:
  pscale database aggressive-cutover show <database> [flags]

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

## pscale database aggressive-cutover enable

```text
Enable aggressive cutover for a database

Usage:
  pscale database aggressive-cutover enable <database> [flags]

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

## pscale database aggressive-cutover disable

```text
Disable aggressive cutover for a database

Usage:
  pscale database aggressive-cutover disable <database> [flags]

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

## pscale database throttler

```text
Show or update database-level Vitess migration throttler configuration.

This sets the default throttler for future deploy requests on the database.
It is not the per-deploy-request throttler (pscale deploy-request throttler)
and not the tablet/vtctld throttler (pscale branch vtctld throttler).

Usage:
  pscale database throttler [command]

Available Commands:
  show        Show database throttler configuration
  update      Update database throttler configuration

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

Use "pscale database throttler [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale database throttler show

```text
Show database throttler configuration

Usage:
  pscale database throttler show <database> [flags]

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

## pscale database throttler update

```text
Update database-level Vitess migration throttler configuration.

Use --ratio to apply one ratio (0-95) to all eligible keyspaces.
Use --configuration keyspace=ratio (repeatable) for per-keyspace ratios.
Pass exactly one of these modes. 0 effectively disables throttling; 95 slows migrations the most.

This is the database default for future deploy requests, not a single deploy request.

Usage:
  pscale database throttler update <database> [flags]

Flags:
      --configuration stringArray   Per-keyspace ratio as keyspace=ratio (repeatable)
  -h, --help                        help for update
      --ratio int                   Throttler ratio 0-95 applied to all eligible keyspaces

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

## pscale keyspace read-only-regions

```text
List read-only regions configured for a Vitess keyspace.

This command is only supported for Vitess databases.

Usage:
  pscale keyspace read-only-regions <database> <branch> <keyspace> [flags]
  pscale keyspace read-only-regions [command]

Available Commands:
  add         Add a read-only region to a keyspace
  remove      Remove a read-only region from a keyspace
  update      Update a keyspace's read-only region

Flags:
  -h, --help   help for read-only-regions

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

Use "pscale keyspace read-only-regions [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

JSON output includes each region's identifying fields plus cluster size and replica count. Use a ready region's slug, display name, or ID with `database dump --read-only-region`.

## pscale database dump

```text
Backup and dump your database.

This command is only supported for Vitess databases. For Postgres databases, use standard PostgreSQL tools like pg_dump. See: https://planetscale.com/docs/postgres/imports/postgres-migrate-dumprestore

Usage:
  pscale database dump <database> <branch> [options] [flags]

Flags:
      --columns stringArray         Columns to include for specific tables (format: 'table:col1,col2'). Can be specified multiple times for different tables.
  -h, --help                        help for dump
      --keyspace string             Optionally target a specific keyspace to be dumped. Useful for sharded databases.
      --local-addr string           Local address to bind and listen for connections. By default the proxy binds to 127.0.0.1 with a random port.
      --output string               Output directory of the dump. By default the dump is saved to a folder in the current directory.
      --output-format string        Output format for data: sql (for MySQL, default), json, or csv. (default "sql")
      --rdonly                      Dump from a rdonly tablet in the primary region (if available; will fail if not). Not for separate read-only regions — use --read-only-region instead.
      --read-only-region string     Dump from a Vitess read-only region (region slug, display name, or id). List regions with: pscale keyspace read-only-regions <database> <branch> <keyspace>.
      --remote-addr hostname:port   PlanetScale Database remote network address. By default the remote address is populated automatically from the PlanetScale API. (format: hostname:port)
      --replica                     Dump from a replica tablet in the primary region (if available; will fail if not).
      --schema-only                 Only dump schema, skip table data.
      --shard string                Optional shard to target, must be used with keyspace
      --tables string               Comma separated string of tables to dump. By default all tables are dumped.
      --threads int                 Number of concurrent threads to use to dump the database. (default 16)
      --wheres string               Comma separated string of WHERE clauses to filter the tables to dump. Only used when you specify tables to dump. Default is not to filter dumped tables.

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

`--read-only-region` cannot be combined with `--rdonly` or `--replica`. The command rejects regions that are not ready and creates a short-lived reader credential scoped to the selected region; it does not fall back to the primary region.

## pscale database update

```text
Update a database's settings.

Only flags you pass are sent to the API. Boolean flags must be set explicitly,
for example --insights-raw-queries=true or --insights-raw-queries=false.

Flags marked "Vitess only" are rejected for PostgreSQL databases.

Usage:
  pscale database update <database> [flags]

Flags:
      --allow-data-branching            Allow seeding branches with data (Vitess only)
      --allow-foreign-key-constraints   Allow foreign key constraints (Vitess only)
      --automatic-migrations            Copy migration data to new branches and deploy requests (Vitess only)
      --default-branch string           The default branch of the database (PostgreSQL and Vitess)
  -h, --help                            help for update
      --insights-raw-queries            Collect full SQL queries for Insights (Vitess only; PostgreSQL uses pgconf.pginsights.raw_queries)
      --migration-framework string      Migration framework for the database (Vitess only)
      --migration-table-name string     Migration table name for the database (Vitess only)
      --new-name string                 Rename the database (PostgreSQL and Vitess)
      --production-branch-web-console   Allow the web console on the production branch (PostgreSQL and Vitess)
      --require-approval-for-deploy     Require admin approval for deploy requests (Vitess only)
      --restrict-branch-region          Limit branch creation to the database region (PostgreSQL and Vitess)

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

Only supplied flags are sent. Set booleans explicitly, for example `--require-approval-for-deploy=true` or `=false`.

## pscale database ip-restriction

```text
Manage IP restrictions for a PostgreSQL database.

IP restrictions limit which IPv4 addresses or ranges can connect. Rules can
optionally be scoped to a specific Postgres schema and/or role. This command
is only available for PostgreSQL databases.

Usage:
  pscale database ip-restriction [command]

Aliases:
  ip-restriction, cidr, cidrs

Available Commands:
  create      Create an IP restriction entry
  delete      Delete an IP restriction entry
  list        List IP restriction entries for a Postgres database
  show        Show an IP restriction entry
  update      Update an IP restriction entry

Flags:
  -h, --help   help for ip-restriction

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

Use "pscale database ip-restriction [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

Create requires `--cidrs` with repeatable or comma-separated IPv4 CIDRs; optional `--schema`, `--role`, and `--description` scope the entry. Update replaces only supplied fields. Delete accepts `--force` but should be treated as destructive because entries apply across all database branches.

## pscale keyspace read-only-regions add

```text
Add a read-only region to a Vitess keyspace.

<region> is a PlanetScale region slug. List available slugs with: pscale region list.

Usage:
  pscale keyspace read-only-regions add <database> <branch> <keyspace> <region> [flags]

Flags:
      --cluster-size pscale size cluster list   cluster size for the keyspace in this read-only region. Use pscale size cluster list to get a list of valid sizes.
  -h, --help                                    help for add
      --replicas int                            number of replicas per shard in this read-only region

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

## pscale keyspace read-only-regions update

```text
Update cluster size or replicas for a keyspace's read-only region.

<region> is a PlanetScale region slug already configured on the keyspace. List configured regions with: pscale keyspace read-only-regions <database> <branch> <keyspace>.

Usage:
  pscale keyspace read-only-regions update <database> <branch> <keyspace> <region> [flags]

Flags:
      --cluster-size pscale size cluster list   cluster size for the keyspace in this read-only region. Use pscale size cluster list to get a list of valid sizes.
  -h, --help                                    help for update
      --replicas int                            number of replicas per shard in this read-only region

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

## pscale keyspace read-only-regions remove

```text
Remove a read-only region from a Vitess keyspace.

<region> is a PlanetScale region slug already configured on the keyspace. List configured regions with: pscale keyspace read-only-regions <database> <branch> <keyspace>.

Usage:
  pscale keyspace read-only-regions remove <database> <branch> <keyspace> <region> [flags]

Flags:
  -h, --help   help for remove

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

These commands are Vitess-only. `add` uses a slug from `pscale region list`; update/remove require a region already configured on the keyspace. Verify the resulting list after every write.

## pscale keyspace

The keyspace parent, list, show, and delete help blocks below are exact output from the official, checksum-verified PlanetScale CLI v0.324.0 macOS arm64 release binary after normalizing only trailing whitespace.

```text
List, show, and manage keyspaces.

This command is only supported for Vitess databases.

Usage:
  pscale keyspace [command]

Available Commands:
  create            Create a new keyspace within a branch
  delete            Delete a keyspace from a branch
  list              List all keyspaces within a branch
  read-only-regions List read-only regions for a keyspace
  resize            Resize a keyspace within a branch
  rollout-status    Show keyspace rollout status per shard
  settings          Show the settings for a keyspace
  show              Show a keyspace within a branch
  update-settings   Update the settings for a keyspace
  vschema           Update or show the VSchema of a branch

Flags:
  -h, --help         help for keyspace
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

Use "pscale keyspace [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale keyspace list

```text
List all keyspaces within a branch

Usage:
  pscale keyspace list <database> <branch> [flags]

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

## pscale keyspace show

```text
Show a keyspace within a branch

Usage:
  pscale keyspace show <database> <branch> <keyspace> [flags]

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

## pscale keyspace delete

```text
Delete a keyspace from a branch

Usage:
  pscale keyspace delete <database> <branch> <keyspace> [flags]

Aliases:
  delete, rm

Flags:
      --force   Delete a keyspace without confirmation
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

## pscale database parent with region discovery

All help fences in this section are exact output from the official, checksum-verified PlanetScale CLI v0.327.0 macOS arm64 release binary after normalizing only trailing whitespace.

```text
Create, read, update, delete, and dump/restore databases

Usage:
  pscale database [command]

Aliases:
  database, db

Available Commands:
  aggressive-cutover Show or change aggressive cutover for a database
  create             Create a database instance
  delete             Delete a database instance
  dump               Backup and dump your database (Vitess databases only)
  ip-restriction     Manage Postgres IP restrictions
  list               List databases
  read-only-regions  List read-only regions for a database
  regions            List regions available to a database
  restore-dump       Restore your database from a local dump directory (Vitess databases only)
  show               Retrieve information about a database, including settings
  throttler          Show or update database throttler configuration
  update             Update a database's settings

Flags:
  -h, --help         help for database
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

Use "pscale database [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale database regions

All help fences in this section are exact output from the official, checksum-verified PlanetScale CLI v0.327.0 macOS arm64 release binary after normalizing only trailing whitespace.

```text
List regions available to a database

Usage:
  pscale database regions [command]

Available Commands:
  list        List regions available to a database

Flags:
  -h, --help   help for regions

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

Use "pscale database regions [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale database read-only-regions

All help fences in this section are exact output from the official, checksum-verified PlanetScale CLI v0.327.0 macOS arm64 release binary after normalizing only trailing whitespace.

```text
List read-only regions for a database's default branch.

This command is only supported for Vitess databases.

Usage:
  pscale database read-only-regions [command]

Available Commands:
  list        List read-only regions for a database

Flags:
  -h, --help   help for read-only-regions

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

Use "pscale database read-only-regions [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```
