# Authentication and API credential behavior

## Compatibility and source

The lazy credential loading, direct-consumer loading, and logout/migration behavior described here require **PlanetScale CLI v0.353.0 or later**. Check the installed CLI before relying on these fixes; older versions can access credential storage during startup or handle unreadable stored tokens differently. This is a behavior minimum, not a minimum for the existence of `auth`, `api`, or service-token flags.

Immutable source: [configuration and storage](https://github.com/planetscale/cli/blob/323c9899fe9072e00bd142ee2f99d76552f0c8fb/internal/config/config.go), [root initialization and flag binding](https://github.com/planetscale/cli/blob/323c9899fe9072e00bd142ee2f99d76552f0c8fb/internal/cmd/root.go), [authentication guard](https://github.com/planetscale/cli/blob/323c9899fe9072e00bd142ee2f99d76552f0c8fb/internal/cmdutil/cmdutil.go), [auth check](https://github.com/planetscale/cli/blob/323c9899fe9072e00bd142ee2f99d76552f0c8fb/internal/cmd/auth/check.go), [logout](https://github.com/planetscale/cli/blob/323c9899fe9072e00bd142ee2f99d76552f0c8fb/internal/cmd/auth/logout.go), [raw API consumer](https://github.com/planetscale/cli/blob/323c9899fe9072e00bd142ee2f99d76552f0c8fb/internal/cmd/api/api.go), [live branch-connections consumer](https://github.com/planetscale/cli/blob/323c9899fe9072e00bd142ee2f99d76552f0c8fb/internal/cmd/branch/connections/client.go), and [storage fixtures](https://github.com/planetscale/cli/blob/323c9899fe9072e00bd142ee2f99d76552f0c8fb/internal/config/config_test.go). These are source-derived behavior statements, not results of executing credential operations.

## When credential storage is accessed

Constructing configuration no longer reads the system credential store. Help, version, and binary-native skill discovery do not need a stored token; their success is not proof of authentication. Protected commands load the token when checking authentication or constructing an API client. `auth check`, `api`, and the live branch-connections client explicitly load before reading the access-token field. A metadata read can therefore still prompt for system credential access or migrate a legacy token. Do not enter a password or operate a keyring dialog on the user's behalf.

For ordinary commands, either nonempty service-token field skips stored-token loading. Authentication requires both `--service-token-id` and `--service-token` (or `PLANETSCALE_SERVICE_TOKEN_ID` and `PLANETSCALE_SERVICE_TOKEN`); a partial pair errors rather than falling back to stored login. A nonempty direct `--api-token` / `PLANETSCALE_API_TOKEN` also avoids a stored-token lookup. Do not print any configured values to diagnose this. Prefer an already authorized secret-manager injection mechanism to command-line secrets.

With neither direct access token nor service-token fields supplied, the stored-token loader runs once per configuration instance, caching success, absence, or failure. Storage errors propagate to protected commands and authentication checks; do not treat an unreadable token as an absent token or blindly start login. In JSON mode, storage failures use the global error envelope, not a successful auth-check result.

Avoid mixing credential methods. The normal API client chooses a complete service-token pair over an access token; `pscale api` instead chooses a nonempty access token before a complete service-token pair. This distinction matters if both are explicitly configured. `api` loads a stored access token when neither method is supplied. Keep the existing redirect protections: cross-host redirects do not forward authentication or caller-supplied headers. Confirm the intended host and operation; `--field` changes the default GET to POST, so do not use it for a read-only probe.

## Migration and logout

When no system credential backend is available, storage uses the legacy `~/.config/planetscale/access-token` file. With a backend, a missing keyring entry triggers legacy-file migration if the file is readable and nonempty. A missing file is treated as no credential; other read errors now propagate. Successful migration stores the token in the keyring and leaves the legacy file in place, with a notice. A successful existing keyring read also leaves the file alone. Do not read token files or manually remove them as an automated troubleshooting step.

Logout deliberately calls the stored-token loader even when service-token credentials are configured. It logs out the stored user session; it does not delete/revoke the configured service token or unset its environment variables. A nonempty explicit API token prevents that stored lookup and becomes the revocation target, so inspect credential configuration by method only and confirm the intended session before approving logout.

- If loading succeeds but the access token is empty, logout reports already logged out and returns without deletion.
- With a nonempty explicit API token (`--api-token`, `PLANETSCALE_API_TOKEN`, or effective user-config `api-token`), stored-token loading returns early. After successful revocation of that explicit token, local stored-login deletion still runs. If the stored session is different, it is not revoked and remains valid server-side; the unreadable-token warning does not appear because there was no read error. Authorize both affected credentials; success or absence of a warning is not proof that the stored session was revoked. If revocation fails, local deletion does not run.
- If the token is readable and nonempty, logout attempts remote revocation first. Revocation failure returns an error before local deletion.
- If reading fails, logout skips revocation and attempts local deletion. On success it warns on stderr that the stored access token was deleted **without revoking it**, then reports logout success. Local cleanup is not proof of server-side revocation; any further account action needs separate authorization.
- Deletion errors fail logout (joined with the read error when applicable); do not claim successful cleanup or retry blindly.
- With a system backend, deletion first removes the legacy token file, then removes the keyring entry; a missing file or missing keyring entry is tolerated. File-removal failure prevents keyring removal. This prevents later re-migration of the legacy credential. The default config file is preserved on this path.
- With no system backend, the fallback removes the legacy token file and then the default config file, tolerating missing files. An error can leave partial cleanup; inspect the reported outcome without opening credential files.

Logout is a credential mutation, not a diagnostic probe. Require explicit authorization for the intended session and explain local deletion versus remote revocation before proceeding. Do not operate system keyring tools or dialogs, inspect secrets, or change auth/runtime scripts to work around a prompt or error. For verification use only an authorized read-only check after the user has completed required credential interactions.

## Service-token creation compatibility

For the standalone auth skill's CI setup example, `service-token create --cidrs` requires **PlanetScale CLI v0.355.0 or later**; existing create name/TTL and authentication commands keep their earlier compatibility. Check installed help and stop if restrictions cannot be expressed; do not silently create an unrestricted token. [Create and integer TTL handling](https://github.com/planetscale/cli/blob/00631d2b78af4f51767815c83dfc3b96d1525442/internal/cmd/token/create.go), [CIDR normalization](https://github.com/planetscale/cli/blob/00631d2b78af4f51767815c83dfc3b96d1525442/internal/cmd/token/update.go), and [effective flag fallback](https://github.com/planetscale/cli/blob/00631d2b78af4f51767815c83dfc3b96d1525442/internal/cmd/root.go#L481-L577) are immutable source contracts. Create trims and drops blank CIDR entries; effective omission or an empty normalized list leaves the token unrestricted and requires explicit approval. Nonempty environment/user-config values can supply omitted name, TTL, or CIDRs, but CIDR user config must be a scalar string such as `cidrs: "192.0.2.0/24,198.51.100.1/32"`; a YAML sequence is silently ignored by `viper.GetString`-based flag presetting. Pass approved restrictions explicitly and verify the exact token; do not dump settings to inspect them. Create TTL is integer seconds, with zero/omission omitted from the request; `never` is not valid. Use human or JSON for creation: CSV output fails after the API call, potentially leaving a created token without a delivered secret. Do not automatically retry; reconcile safe metadata/access and stop on uncertainty. Creation still requires exact-target/scope approval, dependency checks, user-controlled secret delivery and JSON metadata/access read-back under the skill's local gates.

## Capture provenance

Except for the root help fence with its newer adjacent capture note, complete help fences below were captured by the parent from the official checksum-verified PlanetScale CLI v0.353.0 macOS arm64 binary, in a credential-free environment with network denied. Only trailing horizontal terminal padding is removed; no spelling, punctuation, wrapping, or content is rewritten. These help examples are upstream reference text, not authorization to perform mutations.

- Immutable source: [323c9899fe9072e00bd142ee2f99d76552f0c8fb](https://github.com/planetscale/cli/tree/323c9899fe9072e00bd142ee2f99d76552f0c8fb).
- Official release archive SHA-256: `0b7f7c522466d1dd428d8b52372c9534446baf05fe00a5cdb218b11470290411`.
- Extracted binary SHA-256: `1c355a86331ec65256adfbcf8cd82f2be36e86482c644acdc8fbd10d916554b8`.

## pscale --help

Superseded root capture attribution (the following fence is newer):

> Complete help below was captured by the parent from the official checksum-verified PlanetScale CLI v0.354.0 macOS arm64 binary in a fresh credential-free HOME/XDG/config/cwd with network denied. Archive SHA-256: `ef619110dec4d7714b2d858a708d15146027a7455a169b4c9d7dee48d08d5f85`; binary SHA-256: `860140c902d3bc6e5674f42db9242cb98560c3d6809214a738fe6f1e7d1907ab`. Only trailing horizontal terminal padding is removed. Captured examples are reference text, not authorization.

Complete root help below was captured by the parent from the official checksum-verified PlanetScale CLI v0.355.0 macOS arm64 binary in a fresh credential-free HOME/XDG/config/cwd with network denied. Archive SHA-256: `3082dd232de99fa55dfd5621343a6fe9ddb2848a1a7265053c886f5760adf246`; binary SHA-256: `1c957db14d7e18e7201e4cf50ce453f610c732ba838be4e353be4971af48896e`. Only trailing horizontal terminal padding is removed. Captured examples are reference text, not authorization.

```text
pscale is a CLI for communicating with PlanetScale's API.

Agents and automation should start with:

  pscale --skill
  pscale auth check --format json

Usage:
  pscale [flags]
  pscale [command]

MySQL, Postgres, and Neki database commands:
  backup                 Manage branch backups, backup policies, and restores
  branch                 Create, delete, diff, and manage branches
  database               Create, read, update, delete, and dump/restore databases
  insights               Query performance insights and schema recommendations for a database
  inspect                Run read-only diagnostic checks against a database branch
  logs                   Query logs for a PostgreSQL or Neki branch
  metrics                Query historical and current metrics for a database branch
  role                   Manage database roles for a Postgres or Neki database branch
  shell                  Open a shell instance to a database and branch
  sql                    Execute a SQL query without an interactive shell
  webhook                Create, list, and manage webhooks

Vitess/MySQL-specific commands:
  connect                Create a secure connection to a database and branch for a local client
  deploy-request         Create, review, diff, revert, and manage deploy requests
  keyspace               List, show, and manage keyspaces
  maintenance            List and show maintenance schedules for a database
  password               Create, list, update, and delete branch passwords

PostgreSQL-specific commands:
  dedicated-read-replica Manage dedicated read replicas for a Postgres branch
  import                 Import external databases into PlanetScale Postgres
  pgbouncer              Manage dedicated PgBouncers for a Postgres branch
  traffic-control        Manage Database Traffic Control™ for a Postgres database branch

Platform & account management:
  agent-guide            Show guidance for AI agents and automation
  api                    Performs authenticated calls against the PlanetScale API. Useful for scripting.
  audit-log              List audit logs and download authentication-attempt exports
  auth                   Login and logout via the PlanetScale API
  billing                Manage organization billing
  completion             Generate completion script for your shell
  oidc-trust             Manage OIDC trusts
  org                    Manage organizations
  ping                   Ping public PlanetScale database endpoints
  region                 List regions
  service-token          Create, list, and manage access for service tokens
  signup                 Signup for a new PlanetScale account
  size                   Lists the sizes for various components within PlanetScale

Additional Commands:
  help                   Help about any command

Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug[=true|false]        Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
  -h, --help[=true|false]         help for pscale
      --no-color[=true|false]     Disable color output
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.
      --skill[=true|false]        Print the agent skill file and exit
      --version[=true|false]      Show pscale version

Additional help topics:
  pscale agents                 How AI agents and automation should use pscale

Use "pscale [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale auth --help

```text
Manage authentication

Usage:
  pscale auth [command]

Available Commands:
  check       Check if you are authenticated
  login       Authenticate with the PlanetScale API
  logout      Log out of the PlanetScale API

Flags:
  -h, --help   help for auth

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Use "pscale auth [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale auth check --help

```text
Check if you are authenticated

Usage:
  pscale auth check [flags]

Flags:
  -h, --help   help for check

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

## pscale auth login --help

```text
Authenticate with the PlanetScale API

Usage:
  pscale auth login [flags]

Flags:
      --api-url string         The PlanetScale Auth API base URL. (default "https://auth.planetscale.com/")
      --client-id string       The client ID for the PlanetScale CLI application.
      --client-secret string   The client secret for the PlanetScale CLI application.
  -h, --help                   help for login

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale auth logout --help

```text
Log out of the PlanetScale API

Usage:
  pscale auth logout [flags]

Flags:
      --api-url string         The PlanetScale base API URL. (default "https://auth.planetscale.com/")
      --client-id string       The client ID for the PlanetScale CLI application.
      --client-secret string   The client secret for the PlanetScale CLI application.
  -h, --help                   help for logout

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale api --help

```text
Performs authenticated calls against the PlanetScale API and prints the response to stdout.

ENDPOINT

	The endpoint should be a path for the v1 PlanetScale API, not including the "v1" prefix. The placeholder "{org}",
	"{db}" and "{branch}" will be replaced with the currently selected organization, and the project's database and
	branch. If invoked from outside a project, "{db}" and "{branch}" yield an empty string.

	Query parameters, such as for pagination, can be added with the --query/-Q flag, in "key=value" format.
	By default, all HTTP requests use the GET method, unless fields for the body are passed via --field/-F, in which
	case a POST method is used. If another method is required, use the --method/-X flag to specify which one to use.

HEADERS

	Use the --header/-H flag to specify headers manually. Default headers are already included such as "User-Agent",
	"Content-Type", "Accept" and "Authorization".

BODY

	If a body is required for the endpoint you're targeting, the --field/-F flag allows you to specify values at specific
	paths of a JSON document. Repeat the flag to set multiple values. All bodies sent are JSON objects, it isn't possible
	to send non JSON content, or JSON entities of non-object type as the root of the body.

	If you wish to pass the content of a file as body, use the --input/-I flag. If the body should be read from stdin,
	use --input="-".

	Fields specified with --field/-F will be updated in the content of --input/-I if the content is JSON. If not, an error
	will be returned.

Usage:
  pscale api <endpoint> [flags]

Examples:
# get the current user

$ pscale api user

# list an org's databases

$ pscale api organizations/{org}/databases

# create a database

$ pscale api organizations/{org}/databases -F 'name="my-database"'

# get a database

$ pscale api organizations/{org}/databases/my-database

# delete a database

$ pscale api -X DELETE organizations/{org}/databases/my-database

# add a note on a database from the content of a file

$ pscale api -X PATCH organizations/{org}/databases/{db} -F 'notes=@mynotes.txt'

# create a database branch from a file

$ pscale api organizations/{org}/databases/{db}/branches --input=spec.json

# create a database branch from stdin, override the name

$ pscale api organizations/{org}/databases/{db}/branches --input=- -F 'name="my-name"'



Flags:
      --branch string        The branch this project is using
      --database string      The database this project is using
  -F, --field key=value      HTTP body to send with the request, in key=value format where value is a JSON entity, unless value starts with a @ in which case the string after @ represents a file that will be read. Nested types are represented as 'root.depth1.depth2=value'
  -H, --header stringArray   HTTP headers to add to the request
  -h, --help                 help for api
  -I, --input string         HTTP body to send with the request, as a file that will be read and then sent.
  -X, --method string        HTTP method to use for the request.  Defaults to GET for requests without a body, or POST when a body is specified with --field/-F or --input/-I (default "GET")
      --org string           The organization for the current user
  -Q, --query key=value      query to append to the URL path, in key=value format

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
