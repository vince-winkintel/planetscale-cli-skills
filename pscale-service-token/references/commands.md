# Service-token commands

## Compatibility and behavior

`service-token duplicate` and `service-token update` require **PlanetScale CLI v0.353.0 or later**. Check installed help before planning either operation; an older CLI has no equivalent update/duplicate command. Do not substitute deletion or recreation without a separately approved plan. Earlier parent/show fences were captured from the official checksum-verified v0.327.0 macOS arm64 binary; the complete current captures below supersede them. That older capture identifies provenance, not a newly asserted minimum for existing commands.

Source: [command registration and output models](https://github.com/planetscale/cli/blob/323c9899fe9072e00bd142ee2f99d76552f0c8fb/internal/cmd/token/token.go), [duplicate](https://github.com/planetscale/cli/blob/323c9899fe9072e00bd142ee2f99d76552f0c8fb/internal/cmd/token/duplicate.go), [update and TTL parsing](https://github.com/planetscale/cli/blob/323c9899fe9072e00bd142ee2f99d76552f0c8fb/internal/cmd/token/update.go), [API request serialization](https://github.com/planetscale/cli/blob/323c9899fe9072e00bd142ee2f99d76552f0c8fb/internal/planetscale/service_tokens.go), and [source fixtures](https://github.com/planetscale/cli/blob/323c9899fe9072e00bd142ee2f99d76552f0c8fb/internal/cmd/token/create_test.go).

## Authorization and secret handling

The entire service-token command family requires authenticated user/API-token access and an organization; it rejects authentication with a complete service-token pair. Do not attempt to manage a token using that same service token, and do not silently switch credentials. Supply an explicit `--org` for the authorized organization.

Before create, duplicate, update, grant changes, or deletion, inspect safe metadata with `show` and access with `show-access` where a source token exists. Obtain explicit approval for the exact organization, token ID, operation, requested name/expiry and complete access scope. Use least privilege and a short approved lifetime. Extending or removing expiry increases exposure; shortening expiry can interrupt dependents. Check affected automation before changing it. Deletion and access removal also require the destructive-operation safety gates in the skill, including verified recovery and read-back. A 404 or authentication error alone is not permission to create, duplicate, or delete another token.

Create and duplicate use the secret-bearing output model: human/CSV include a `token` column and JSON serializes the returned token object including `token`. Never display or store returned token values in chat, logs, evidence, temporary files, or this repository. An approved mutation still needs a user-controlled secret-delivery mechanism that does not expose its response to the agent; stop if none is available. Do not run these commands merely to inspect output. `show` and `update` use the safe details model, which excludes the secret even if the API response contains it; inspect access separately with `show-access`.

## Duplicate

`pscale service-token duplicate <id> --name <approved-name> --org <org>` requires `--name` and sends only the name to `POST /v1/organizations/<org>/service-tokens/<id>/duplicate`. The CLI does not offer TTL or grant-selection flags here, and the client source does not define the server's grant/expiry-copying contract. Do not assume duplication narrows privileges, preserves expiry, revokes the original, or completes rotation. Review source access before approval, then inspect the new ID's metadata and access after the authorized operation. Stop on unexpected scope or expiry; any corrective mutation needs its own approval. Verify dependent automation before considering separately approved retirement of the old token.

## Update

`pscale service-token update <id> --org <org>` requires at least one explicitly supplied `--name` or `--ttl`. It sends a PATCH to the individual service-token endpoint. This changes name or expiry only: **it does not rotate the token secret or change the ID or grants**.

| Input | Request behavior |
| --- | --- |
| Omit `--name` | Omit `name`; leave the name unchanged. |
| Supply `--name` | Send the supplied string, including explicit empty string; the CLI does not validate a nonempty name. |
| Omit `--ttl` | Omit `ttl`; leave expiry unchanged. |
| `--ttl <integer-seconds>` | Parse a decimal integer and send that number. Duration strings such as `1h` are rejected. |
| `--ttl never` | Send JSON `null` to remove expiry; requires explicit approval for a non-expiring credential. |

The CLI does not check positivity: zero and negative integers are sent to the API. Do not infer their server meaning or use zero as a substitute for `never`. By contrast, `create --ttl 0` omits TTL from its request. Propose a positive approved lifetime; inspect the returned `expires_at` and read back the exact token after update. The safe JSON detail fields are `id`, `name`, `created_at`, `last_used_at`, `last_used_ip`, `last_used_asn_organization`, and `expires_at`, with nullable values preserved. Access grants are not part of that response.

## Capture provenance

Complete help fences below were captured by the parent from the official checksum-verified PlanetScale CLI v0.353.0 macOS arm64 binary, in a credential-free environment with network denied. Only trailing horizontal terminal padding is removed; no spelling, punctuation, wrapping, or content is rewritten. These help examples are upstream reference text, not authorization to perform mutations.

- Immutable source: [323c9899fe9072e00bd142ee2f99d76552f0c8fb](https://github.com/planetscale/cli/tree/323c9899fe9072e00bd142ee2f99d76552f0c8fb).
- Official release archive SHA-256: `0b7f7c522466d1dd428d8b52372c9534446baf05fe00a5cdb218b11470290411`.
- Extracted binary SHA-256: `1c355a86331ec65256adfbcf8cd82f2be36e86482c644acdc8fbd10d916554b8`.

## pscale service-token --help

```text
Create, list, and manage access for service tokens

Usage:
  pscale service-token [command]

Available Commands:
  add-access    add access to a service token in the organization
  create        create a service token for the organization
  delete        delete an entire service token in an organization
  delete-access delete access granted to a service token in the organization
  duplicate     duplicate a service token in the organization
  list          list service tokens for the organization
  show          show a service token in the organization
  show-access   fetch a service token and its accesses
  update        update a service token's name or expiry

Flags:
  -h, --help         help for service-token
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

Use "pscale service-token [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale service-token add-access --help

```text
add access to a service token in the organization

Usage:
  pscale service-token add-access <token> <access> <access> ... [flags]

Examples:
The add-access command grants a service token access on a database or organization.

For example, to give a service token the ability to create, read and delete branches on a specific database:

  pscale service-token add-access <token id> read_branch delete_branch create_branch --database <database name>

To give a service token the ability to create and delete databases within the current organization:

  pscale service-token add-access <token id> delete_databases create_databases

For a complete list of the access permissions that can be granted to a token, see: https://api-docs.planetscale.com/reference/service-tokens#access-permissions.

Flags:
      --database string   The database to add access to
  -h, --help              help for add-access

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

## pscale service-token create --help

```text
create a service token for the organization

Usage:
  pscale service-token create [flags]

Flags:
  -h, --help          help for create
      --name string   optional name for the service token
      --ttl int       Time to live (in seconds) for the service token. The token will be invalid when TTL has passed

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

## pscale service-token delete --help

```text
delete an entire service token in an organization

Usage:
  pscale service-token delete <token> [flags]

Flags:
  -h, --help   help for delete

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

## pscale service-token delete-access --help

```text
delete access granted to a service token in the organization

Usage:
  pscale service-token delete-access <token> <access> <access> ... [flags]

Examples:
The delete-access command removes an access grant from a service token.

For example, to remove access for a specific database, include the --database flag:

  pscale service-token delete-access <token id> read_branch --database <database name>

To remove an organization level grant:

  pscale service-token add-access <token id> delete_databases

Flags:
      --database string   The database to remove access to
  -h, --help              help for delete-access

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

## pscale service-token duplicate --help

```text
duplicate a service token in the organization

Usage:
  pscale service-token duplicate <id> [flags]

Flags:
  -h, --help          help for duplicate
      --name string   name for the duplicated service token (required)

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

## pscale service-token list --help

```text
list service tokens for the organization

Usage:
  pscale service-token list [flags]

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

## pscale service-token show --help

```text
show a service token in the organization

Usage:
  pscale service-token show <id> [flags]

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

## pscale service-token show-access --help

```text
fetch a service token and its accesses

Usage:
  pscale service-token show-access <name> [flags]

Flags:
  -h, --help   help for show-access

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

## pscale service-token update --help

```text
Update a service token's name or expiry. This does not rotate the token secret or change its id or grants.

Usage:
  pscale service-token update <id> [flags]

Flags:
  -h, --help          help for update
      --name string   new name for the service token. Omit to leave the name unchanged
      --ttl string    time to live in seconds, or "never" to remove the expiry. Omit to leave the expiry unchanged

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
