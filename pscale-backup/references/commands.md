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

```text
Usage:
  pscale backup policy [command]

Available Commands:
  create      Create a backup policy
  delete      Delete a backup policy
  list        List backup policies for a database
  show        Show a backup policy
  update      Update a backup policy
```

Create usage is `pscale backup policy create <database>` and requires target, frequency value/unit, schedule time, and retention value/unit. Update usage is `pscale backup policy update <database> <policy-id>` and sends only supplied flags. Delete usage is `pscale backup policy delete <database> <policy-id>`; `--force` skips confirmation, and required default system policies cannot be deleted.
