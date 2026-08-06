Create, read, delete, and dump/restore databases

Usage:
  pscale database [command]

Aliases:
  database, db

Available Commands:
  create       Create a database instance
  delete       Delete a database instance
  dump         Backup and dump your database (Vitess databases only)
  list         List databases
  restore-dump Restore your database from a local dump directory (Vitess databases only)
  show         Retrieve information about a database

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

## pscale keyspace read-only-regions

```text
List read-only regions configured for a Vitess keyspace.

This command is only supported for Vitess databases.

Usage:
  pscale keyspace read-only-regions <database> <branch> <keyspace> [flags]
```

JSON output includes each region's identifying fields plus cluster size and replica count. Use a ready region's slug, display name, or ID with `database dump --read-only-region`.

## pscale database dump

```text
Backup and dump your database.

This command is only supported for Vitess databases. For Postgres databases,
use standard PostgreSQL tools like pg_dump.

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
      --wheres string               Comma separated string of WHERE clauses to filter the tables to dump. Only used when you specify tables to dump.
```

`--read-only-region` cannot be combined with `--rdonly` or `--replica`. The command rejects regions that are not ready and creates a short-lived reader credential scoped to the selected region; it does not fall back to the primary region.
