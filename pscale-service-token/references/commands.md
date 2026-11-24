# Service-token commands

## Compatibility and behavior

`service-token duplicate` and `service-token update` require **PlanetScale CLI v0.353.0 or later**. The `--cidrs` flags on create/update, CIDR output fields, and duplicate's `--ttl` require **PlanetScale CLI v0.355.0 or later**. These newer minima do not apply to existing create TTL, duplicate without TTL, or update name/TTL. Check installed help before planning an operation; do not substitute deletion/recreation or silently drop restrictions on an older CLI.

Source: [create](https://github.com/planetscale/cli/blob/00631d2b78af4f51767815c83dfc3b96d1525442/internal/cmd/token/create.go), [duplicate and integer TTL](https://github.com/planetscale/cli/blob/00631d2b78af4f51767815c83dfc3b96d1525442/internal/cmd/token/duplicate.go), [update and CIDR normalization](https://github.com/planetscale/cli/blob/00631d2b78af4f51767815c83dfc3b96d1525442/internal/cmd/token/update.go), [output models](https://github.com/planetscale/cli/blob/00631d2b78af4f51767815c83dfc3b96d1525442/internal/cmd/token/token.go), [request serialization](https://github.com/planetscale/cli/blob/00631d2b78af4f51767815c83dfc3b96d1525442/internal/planetscale/service_tokens.go), [duplicate CIDR response expectation](https://github.com/planetscale/cli/blob/00631d2b78af4f51767815c83dfc3b96d1525442/internal/cmd/token/create_test.go).

## Expiry transition

**CLI v0.356.0** adds a warning, not local mandatory-TTL validation. Create and duplicate with effective TTL 0 (including omission) still omit the request field and warn on stderr: `Service tokens will soon require an expiration. Pass --ttl with a number of seconds.` Update warns only when an effectively supplied TTL parses as `never`, then still sends JSON null. Omitted update TTL remains unchanged without this warning; integer zero/negative values are still forwarded. Do not reinterpret a warning as rejection, successful creation, or guaranteed server acceptance.

The upstream change describes server enforcement for create/duplicate when `require_service_token_ttl` is enabled. Do not assume that flag's current organization state, a rollout date, or that update-to-never will be accepted. Prepare a positive explicitly approved lifetime and verify `expires_at` with exact-token `show`, plus CIDRs and `show-access` grants and dependent automation health. Existing expiry extension/removal, secret delivery, and complete-scope authorization gates still apply. Never omit TTL or clear expiry to bypass policy; reconcile ambiguous outcomes without retrying writes. The compatibility minima for existing create TTL, v0.353.0 duplicate/update, and v0.355.0 duplicate TTL/CIDRs remain unchanged.

Immutable source: [create and shared warning](https://github.com/planetscale/cli/blob/431a54b0fa6360d34d2e7f765d58296782b3cb39/internal/cmd/token/create.go), [duplicate](https://github.com/planetscale/cli/blob/431a54b0fa6360d34d2e7f765d58296782b3cb39/internal/cmd/token/duplicate.go), [update](https://github.com/planetscale/cli/blob/431a54b0fa6360d34d2e7f765d58296782b3cb39/internal/cmd/token/update.go), [warning fixtures](https://github.com/planetscale/cli/blob/431a54b0fa6360d34d2e7f765d58296782b3cb39/internal/cmd/token/create_test.go), [enforcement transition rationale](https://github.com/planetscale/cli/commit/4876f1171c23a15c0f519a2a43d8daf345374bfb). Existing v0.355.0 help fences below are historical captures; the warning is runtime behavior, not new help text.

## Authorization and secret handling

The entire service-token command family requires authenticated user/API-token access and an organization; it rejects authentication with a complete service-token pair. Do not attempt to manage a token using that same service token, and do not silently switch credentials. Supply an explicit `--org` for the authorized organization.

Before create, duplicate, update, grant changes, or deletion, inspect safe metadata with `show` and access with `show-access` where a source token exists. Obtain explicit approval for the exact organization, token ID (or new-token name), operation, requested name/expiry, complete access scope, and complete allowed IP/CIDR list. Use least privilege and a short approved lifetime. Extending or removing expiry increases exposure; shortening expiry can interrupt dependents. Check affected automation and its actual egress addresses before changing expiry or restrictions. Widening a range, adding allowed sources, or removing all IP restrictions requires separate explicit approval; never clear restrictions to bypass a refusal. Establish an approved recovery path without assuming automatic rollback is authorized. Deletion and access removal also require the destructive-operation safety gates in the skill, including verified recovery and read-back. A 404 or authentication error alone is not permission to create, duplicate, or delete another token.

Create and duplicate use the secret-bearing output model: human output includes a `token` column and JSON serializes the returned token object including `token`. Use human or JSON, not CSV; CSV printing fails after the API call as detailed below. Never display or store returned token values in chat, logs, evidence, temporary files, or this repository. An approved mutation still needs a user-controlled secret-delivery mechanism that does not expose its response to the agent; stop if none is available. Do not run these commands merely to inspect output. `show` and `update` use the safe details model, which excludes the secret even if the API response contains it; inspect access separately with `show-access`.

## Effective flags and omission

Omission means absent from effective configuration, not just argv. [Root initialization](https://github.com/planetscale/cli/blob/00631d2b78af4f51767815c83dfc3b96d1525442/internal/cmd/root.go#L481-L577) presets unchanged flags from nonempty environment/user-config values using `Flags.Set`, marking them changed. Confirm that `PLANETSCALE_NAME`, `PLANETSCALE_TTL`, `PLANETSCALE_CIDRS` and matching user-config `name`, `ttl`, `cidrs` keys do not supply omitted fields. Explicit CLI flags take precedence; environment values precede user config. Empty inherited strings are not preset and are not a reliable way to override a configured value. Project-scoped `.pscale.yml` only allows org/database/branch, not these keys. Do not print secrets or dump config/environment; stop if effective settings cannot be confirmed safely.

CIDR user config must be a scalar string, for example `cidrs: "192.0.2.0/24,198.51.100.1/32"`. Flag presetting uses `viper.GetString`; a YAML sequence/list cannot be converted and is silently ignored, leaving `cidrs` unset unless another effective source supplies it. Creation can therefore be unrestricted despite a nonempty YAML sequence. Pass approved restrictions explicitly with `--cidrs` and read back the exact token; do not rely on the config key's presence.

For example, `PLANETSCALE_TTL=never` plus a name-only **update** sends `ttl: null`, removing expiry; it is invalid for create/duplicate's integer TTL flags. A nonempty inherited name satisfies duplicate's required `--name`. Nonempty inherited CIDRs turn a name-only update into a restriction replacement; whitespace-only CIDRs can normalize to an empty list and clear restrictions. Inspect the effective normalized list before approval. The omission rows below assume no inherited value.

## Create and IP restrictions

Create accepts optional name, integer TTL, and `--cidrs <approved-ip-or-cidr-list>`. It sends a POST to the organization's service-token endpoint. CIDRs are a comma-separated string slice; repeated flags accumulate entries. Create/update trim surrounding whitespace and drop empty entries. The client does not validate IP syntax, canonicalize networks, deduplicate ranges, or guarantee API acceptance. Blank or whitespace-only entries can therefore yield an empty list; stop if normalization changes the approved intent.

| CIDR input | Create request/meaning | Update request/meaning |
| --- | --- | --- |
| Omit `--cidrs` effectively | Omit `cidrs`; new token is unrestricted. Unrestricted creation needs explicit approval. | Omit `cidrs`; preserve existing restrictions. |
| Supply a nonempty normalized list | Send `cidrs` array; create with approved allowed sources. | Send the complete replacement array, not an additive patch. |
| `--cidrs ""` or a list normalizing to empty | Send `cidrs: []`; unrestricted creation needs explicit approval. | Send `cidrs: []`; remove **all** restrictions, widening access. Separate explicit approval required. |

Omission is not explicit empty: `--cidrs ""` removes all restrictions on update. IP restrictions constrain where a token may be used; they do not grant permissions or replace access-scope review. Confirm all dependent runners' egress and read back the new token's restrictions, expiry, and grants before use.

## Duplicate

`pscale service-token duplicate <id> --name <approved-name> --ttl <approved-positive-seconds> --org <org>` sends the name and nonzero integer TTL to `POST /v1/organizations/<org>/service-tokens/<id>/duplicate`. It has no `--cidrs` or grant-selection flag. The required name flag may be inherited and is not validated for nonempty content; use an explicit approved name.

Create and duplicate use integer TTL flags, **not update's string `never` syntax**. Omitted TTL and explicit zero both omit `ttl` from the request; negative nonzero integers are sent without a client positivity check. Duration strings such as `1h` and `never` are rejected. Do not treat zero/omission as a safe lifetime or infer copied expiry: the server chooses omitted-TTL behavior. Specify a positive approved lifetime and read back `expires_at`.

The upstream duplicate fixture expects the API response to include copied CIDRs. That is a server-side copying expectation, not a client guarantee: the client neither sends CIDRs nor fetches and reapplies the source restrictions. Do not infer copied grants or expiry from this fixture. Review source metadata/access before approval, then inspect the **new ID's** restrictions, expiry, and grants with `show`/`show-access` before enabling dependent automation. Stop on absent or unexpected restrictions, scope, or expiry; any corrective mutation needs its own approval. Duplication does not revoke the original or complete rotation. Verify dependent automation before separately approved retirement of the old token.

## Update

`pscale service-token update <id> --org <org>` requires at least one effectively supplied `--name`, `--ttl`, or `--cidrs`. It sends a PATCH to the individual service-token endpoint. This changes name, expiry, or IP restrictions: **it does not rotate the token secret or change the ID or grants**.

| Input | Request behavior |
| --- | --- |
| Omit `--name` | Omit `name`; leave the name unchanged. |
| Supply `--name` | Send the supplied string, including explicit empty string; the CLI does not validate a nonempty name. |
| Omit `--ttl` | Omit `ttl`; leave expiry unchanged. |
| `--ttl <integer-seconds>` | Parse a decimal integer and send that number. Duration strings such as `1h` are rejected. |
| `--ttl never` | Send JSON `null` to remove expiry; requires explicit approval for a non-expiring credential. |

The CLI does not check positivity: zero and negative integers are sent to the API. Do not infer their server meaning or use zero as a substitute for `never`. By contrast, `create --ttl 0` and `duplicate --ttl 0` omit TTL from their requests. Propose a positive approved lifetime; read back the exact token's `expires_at`, CIDRs, and access after update. Verify dependent automation health; an ambiguous outcome is not permission to repeat a write.

## Output and read-back

Do not use `--format csv` for create, duplicate, show, or update on v0.355.0. The [CSV printer](https://github.com/planetscale/cli/blob/00631d2b78af4f51767815c83dfc3b96d1525442/internal/printer/printer.go#L226-L240) passes their singleton output structs to gocsv, which rejects non-slice/non-array values. Serialization fails after the API call: create/duplicate may already have created a token without delivering its secret, and update may already have applied the change. Use human or JSON and confirm the effective format before the operation. On a printing error, stop and reconcile safe metadata/access; do not retry the mutation automatically or assume rollback. If the new ID or intended state is uncertain, stop for operator investigation; cleanup/replacement is a separately approved mutation. `show --format csv` also fails and cannot verify a write. Prefer JSON for exact-token read-back with `show` and `show-access`.

Human create, duplicate, list, show, and update output has a `cidrs` column, joined with comma-space (blank when empty). CSV works for `list`; its complete header is `ID,Name,CIDRs,LastUsedAt,LastUsedIP,LastUsedOrganization,ExpiresAt,CreatedAt`. In particular, `CIDRs`, `LastUsedIP`, and `LastUsedOrganization` are Go-field names, not the human headers `cidrs`, `last_used_ip`, and `last_used_organization`. Use a CSV parser rather than splitting on commas: multiple CIDRs form one quoted field, and timestamps are raw epoch milliseconds (missing times map to zero). JSON uses a string array: create/duplicate/list serialize the API token model with `cidrs` retained (including null/empty arrays); show/update's details model omits `cidrs` when empty. Missing `cidrs` in safe details is not evidence that restrictions were preserved. Compare fresh read-back with the approved list; if restrictions were expected, stop on missing/empty values. In human mode only, update with effectively supplied CIDRs also prints `IP restrictions: <list>` or `IP restrictions: none` after the table; JSON does not include that extra line.

Safe show/update JSON fields are `id`, `name`, `created_at`, `last_used_at`, `last_used_ip`, `last_used_asn_organization`, `expires_at`, and nonempty `cidrs`; nullable metadata stays nullable. Neither grants nor the secret are included. List JSON serializes the original API model, including its `token` field if returned; do not treat list JSON as a guaranteed secret-filtering view. Prefer `show` for secret-excluding metadata inspection. Protect IP/network metadata in evidence. Successful human/JSON create/duplicate responses are secret-bearing; CSV failure is not a secret-filtering mechanism.

## Capture provenance

Earlier parent/show fences came from the official checksum-verified v0.327.0 macOS arm64 binary; the subsequent full service-token capture was v0.353.0 (archive SHA-256 `0b7f7c522466d1dd428d8b52372c9534446baf05fe00a5cdb218b11470290411`, binary SHA-256 `1c355a86331ec65256adfbcf8cd82f2be36e86482c644acdc8fbd10d916554b8`). These are superseded capture provenance, not compatibility minima.

Complete help fences below were captured by the parent from the official checksum-verified PlanetScale CLI v0.355.0 macOS arm64 binary in a fresh credential-free HOME/XDG/config/cwd with network denied. Only trailing horizontal terminal padding is removed; no spelling, punctuation, wrapping, or content is rewritten. These help examples are upstream reference text, not authorization to perform mutations, unrestricted creation, or restriction removal.

- Immutable source: [00631d2b78af4f51767815c83dfc3b96d1525442](https://github.com/planetscale/cli/tree/00631d2b78af4f51767815c83dfc3b96d1525442).
- Official release archive SHA-256: `3082dd232de99fa55dfd5621343a6fe9ddb2848a1a7265053c886f5760adf246`.
- Extracted binary SHA-256: `1c957db14d7e18e7201e4cf50ce453f610c732ba838be4e353be4971af48896e`.

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
  update        update a service token's name, expiry, or IP restrictions

Flags:
  -h, --help[=true|false]   help for service-token
      --org string          The organization for the current user

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug[=true|false]        Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color[=true|false]     Disable color output
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
      --database string     The database to add access to
  -h, --help[=true|false]   help for add-access

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug[=true|false]        Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color[=true|false]     Disable color output
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

Examples:
  pscale service-token create --name ci --cidrs 10.0.0.0/8,192.168.1.1/32
  pscale service-token create --name ci

Flags:
      --cidrs strings       IP addresses and CIDR ranges allowed to use this service token. Omit to leave the token unrestricted
  -h, --help[=true|false]   help for create
      --name string         optional name for the service token
      --ttl int             Time to live (in seconds) for the service token. The token will be invalid when TTL has passed

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug[=true|false]        Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color[=true|false]     Disable color output
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
  -h, --help[=true|false]   help for delete

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug[=true|false]        Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color[=true|false]     Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale service-token delete-access --help

**Known upstream help typo:** the organization-level removal example inside the verbatim fence incorrectly uses `add-access`, which grants access instead. Do not copy it for removal. The correct approved organization-level removal is `pscale service-token delete-access <token-id> delete_databases --org <org> --database=""`, subject to the local destructive-operation gates and exact grant approval. The explicit empty database prevents `PLANETSCALE_DATABASE`, user configuration, or project `.pscale.yml` from silently selecting database scope; `--org` alone does not clear that inherited scope. Confirm the exact organization-level grant before removal. The capture is intentionally unchanged.

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
      --database string     The database to remove access to
  -h, --help[=true|false]   help for delete-access

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug[=true|false]        Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color[=true|false]     Disable color output
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
  -h, --help[=true|false]   help for duplicate
      --name string         name for the duplicated service token (required)
      --ttl int             Time to live (in seconds) for the duplicated service token. The token will be invalid when TTL has passed

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug[=true|false]        Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color[=true|false]     Disable color output
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
  -h, --help[=true|false]   help for list

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug[=true|false]        Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color[=true|false]     Disable color output
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
  -h, --help[=true|false]   help for show

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug[=true|false]        Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color[=true|false]     Disable color output
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
  -h, --help[=true|false]   help for show-access

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug[=true|false]        Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color[=true|false]     Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale service-token update --help

```text
Update a service token's name, expiry, or IP restrictions. This does not rotate the token secret or change its id or grants.

Usage:
  pscale service-token update <id> [flags]

Examples:
  pscale service-token update <token id> --name ci --ttl 3600
  pscale service-token update <token id> --cidrs 10.0.0.0/8,192.168.1.1/32
  pscale service-token update <token id> --cidrs ""

Flags:
      --cidrs strings       Replace the IP addresses and CIDR ranges allowed to use this service token. Pass an empty value to remove all restrictions
  -h, --help[=true|false]   help for update
      --name string         new name for the service token. Omit to leave the name unchanged
      --ttl string          time to live in seconds, or "never" to remove the expiry. Omit to leave the expiry unchanged

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug[=true|false]        Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color[=true|false]     Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```
