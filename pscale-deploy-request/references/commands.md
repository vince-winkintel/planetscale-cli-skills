Create, review, diff, inspect, throttle, revert, and manage deploy requests.

The help blocks below are exact output from the official, checksum-verified PlanetScale CLI v0.321.0 macOS arm64 release binary. Terminal padding and trailing whitespace are not material.

## pscale deploy-request

```text
Create, review, diff, revert, and manage deploy requests.

This command is only supported for Vitess databases.

Usage:
  pscale deploy-request [command]

Aliases:
  deploy-request, dr

Available Commands:
  apply         Apply changes to a gated deploy request
  cancel        Cancel a deploy request
  close         Close a deploy request
  create        Create a deploy request from a branch
  deploy        Deploy a specific deploy request
  deployment    Show the deployment for a deploy request
  diff          Show the diff of a deploy request
  edit          Edit a deploy request
  force-cutover Force cutover when a migration is delayed by a table lock
  list          List all deploy requests for a database
  operations    List deploy operations for a deploy request
  queue         Show the deploy queue for a database
  revert        Revert a deployed deploy request
  review        Review a deploy request (approve, comment, etc...)
  reviews       List reviews for a deploy request
  show          Show a specific deploy request
  skip-revert   Skip and close a pending deploy request revert
  storage-check Check storage readiness for a deploy request
  throttler     Show or update deploy request throttler configuration

Flags:
  -h, --help         help for deploy-request
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

Use "pscale deploy-request [command] --help" for more information about a command.

Agents: run "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale deploy-request deploy

```text
Deploy a specific deploy request

Usage:
  pscale deploy-request deploy <database> <number|branch> [flags]

Flags:
  -h, --help              help for deploy
      --instant           If enabled, the schema migrations from this deploy request will be applied using MySQL’s built-in ALGORITHM=INSTANT option. Deployment will be faster, but cannot be reverted.
      --strategy string   Deployment strategy: "serial" (default) or "parallel".
      --wait              wait until the branch is deployed

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

Agents: run "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale deploy-request force-cutover

```text
Force cutover when a deploy request is delayed waiting for a table lock.

The final step of a migration requires a brief table lock. Long-running
transactions can block that lock and delay completion. PlanetScale keeps
retrying for up to 1 hour, then forces cutover automatically.

Use this command to skip the wait: force cutover kills long-running
transactions that are blocking the table lock so the migration can finish.

Only allowed when the deployment state is in_progress_cutover.

Usage:
  pscale deploy-request force-cutover <database> <number> [flags]

Flags:
      --force   Skip the confirmation prompt and force cutover now.
  -h, --help    help for force-cutover

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

Agents: run "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale deploy-request queue

```text
Show the deploy queue for a database

Usage:
  pscale deploy-request queue <database> [flags]

Flags:
  -h, --help   help for queue

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

Agents: run "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale deploy-request deployment

```text
Show the deployment for a deploy request

Usage:
  pscale deploy-request deployment <database> <number> [flags]

Flags:
  -h, --help   help for deployment

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

Agents: run "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale deploy-request operations

```text
List deploy operations for a deploy request

Usage:
  pscale deploy-request operations <database> <number> [flags]

Flags:
  -h, --help   help for operations

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

Agents: run "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale deploy-request reviews

```text
List reviews for a deploy request

Usage:
  pscale deploy-request reviews <database> <number> [flags]

Flags:
  -h, --help   help for reviews

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

Agents: run "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale deploy-request storage-check

```text
Check storage readiness for a deploy request

Usage:
  pscale deploy-request storage-check <database> <number> [flags]

Flags:
  -h, --help   help for storage-check

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

Agents: run "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale deploy-request throttler

```text
Show or update deploy request throttler configuration.

This is per deploy request, not the database-level throttler.

Usage:
  pscale deploy-request throttler [command]

Available Commands:
  show        Show throttler configuration for a deploy request
  update      Update throttler configuration for a deploy request

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

Use "pscale deploy-request throttler [command] --help" for more information about a command.

Agents: run "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale deploy-request throttler show

```text
Show throttler configuration for a deploy request

Usage:
  pscale deploy-request throttler show <database> <number> [flags]

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

Agents: run "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale deploy-request throttler update

```text
Update throttler configuration for a deploy request.

Use --ratio to apply one ratio (0-95) to all eligible keyspaces.
Use --configuration keyspace=ratio (repeatable) for per-keyspace ratios.
Pass exactly one of these modes. 0 effectively disables throttling; 95 slows migrations the most.

Usage:
  pscale deploy-request throttler update <database> <number> [flags]

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

Agents: run "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```
