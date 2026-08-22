Manage branch backups and backup policies

Usage:
  pscale backup [command]

Available Commands:
  create      Backup a branch's data and schema
  delete      Delete a branch backup
  list        List all backups of a branch
  policy      Create, list, show, update, and delete backup policies
  restore     Restore a backup to a new branch
  show        Show a specific backup of a branch

Flags:
  -h, --help         help for backup
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

Use "pscale backup [command] --help" for more information about a command.

## pscale backup policy

All help fences below are exact output from the official, checksum-verified PlanetScale CLI v0.324.0 macOS arm64 release binary after normalizing only trailing whitespace.

```text
Manage scheduled backup policies for a database.

Backup policies define automatic backup frequency, schedule, and retention for
production or development branches. This is separate from one-off branch
backups created with 'pscale backup create'.

Usage:
  pscale backup policy [command]

Available Commands:
  create      Create a backup policy
  delete      Delete a backup policy
  list        List backup policies for a database
  show        Show a backup policy
  update      Update a backup policy

Flags:
  -h, --help   help for policy

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

Use "pscale backup policy [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

### pscale backup policy create

```text
Create a scheduled backup policy for production or development branches.

Custom schedules beyond the included defaults may incur additional backup storage charges.

Usage:
  pscale backup policy create <database> [flags]

Flags:
      --frequency-unit string   Frequency unit: hour, day, week, or month (required) (required)
      --frequency-value int     Frequency value (required) (required)
  -h, --help                    help for create
      --name string             Optional name for the backup policy
      --retention-unit string   Retention unit: hour, day, week, month, or year (required) (required)
      --retention-value int     Retention period value (required) (required)
      --schedule-day int        Day of week (0=Sunday … 6=Saturday); used for weekly/monthly schedules
      --schedule-time string    Schedule time of day in HH:MM format (required) (required)
      --schedule-week int       Week of month (0=first … 3=fourth); used for monthly schedules
      --target string           Branch target: production or development (required) (required)

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

### pscale backup policy update

```text
Update a backup policy.

Only flags you pass are sent to the API. Required system policies may reject
some changes.

Usage:
  pscale backup policy update <database> <policy-id> [flags]

Flags:
      --frequency-unit string   Frequency unit: hour, day, week, or month
      --frequency-value int     Frequency value
  -h, --help                    help for update
      --name string             Name for the backup policy
      --retention-unit string   Retention unit: hour, day, week, month, or year
      --retention-value int     Retention period value
      --schedule-day int        Day of week (0=Sunday … 6=Saturday)
      --schedule-time string    Schedule time of day in HH:MM format
      --schedule-week int       Week of month (0=first … 3=fourth)
      --target string           Branch target: production or development

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

### pscale backup policy delete

```text
Delete a custom backup policy. Required default system policies cannot be deleted.

Usage:
  pscale backup policy delete <database> <policy-id> [flags]

Aliases:
  delete, rm

Flags:
      --force   Delete a backup policy without confirmation
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

Create usage is `pscale backup policy create <database>` and requires target, frequency value/unit, schedule time, and retention value/unit. Update usage is `pscale backup policy update <database> <policy-id>` and sends only supplied flags. Delete usage is `pscale backup policy delete <database> <policy-id>`; `--force` skips confirmation, and required default system policies cannot be deleted.
