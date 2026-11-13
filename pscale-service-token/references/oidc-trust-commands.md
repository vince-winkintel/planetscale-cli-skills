# OIDC trust policy

## Compatibility and provenance

Minimum CLI: **v0.351.0** for the `oidc-trust` parent and its six direct children (`providers`, `list`, `show`, `create`, `update`, `delete`), including update empty-list clearing and non-interactive deletion requiring `--force`. **v0.352.0** adds `providers list` (alias `providers ls`) and `providers show <name>`, plus structured provider claim descriptions. Bare `providers` still lists providers for compatibility. These commands are registered at the root; they are not service-token subcommands. CLI support does not establish organization feature enablement or permissions. Check `pscale version` and stop on unsupported commands or permission failures.

Source contract: official `planetscale/cli` commit `e6449dc17ee2af30aed4a1a07aa5112bf6b7d8ca`, [root registration](https://github.com/planetscale/cli/blob/e6449dc17ee2af30aed4a1a07aa5112bf6b7d8ca/internal/cmd/root.go), [command implementations](https://github.com/planetscale/cli/tree/e6449dc17ee2af30aed4a1a07aa5112bf6b7d8ca/internal/cmd/oidctrust), and [API models](https://github.com/planetscale/cli/blob/e6449dc17ee2af30aed4a1a07aa5112bf6b7d8ca/internal/planetscale/oidc_trusts.go). This section describes reviewed source behavior, not captured binary help or live API output.

Provider discovery contract: official commit `d4dd5a80ef64eb48ee8148d571fe10e4ffb1efd1`, [provider commands](https://github.com/planetscale/cli/blob/d4dd5a80ef64eb48ee8148d571fe10e4ffb1efd1/internal/cmd/oidctrust/providers.go) and [provider/claim models](https://github.com/planetscale/cli/blob/d4dd5a80ef64eb48ee8148d571fe10e4ffb1efd1/internal/planetscale/oidc_trusts.go). The complete help fences below come from the checksum-verified official macOS arm64 release in a credential-free environment with network denied; only trailing terminal padding is normalized. Behavioral/output descriptions are source-backed, not observed live API output.

## Inspect before proposing policy

All commands require authentication and an explicit `--org`. Use the existing approved authentication path; do not fetch, decode, log, paste, or persist OIDC assertions, exchanged access tokens, or service-token secrets. Do not enable debug logging for credential-bearing operations. Trust metadata is not a credential, but redact organization/repository identifiers when reporting it outside the approved context.

```bash
# v0.351.0: bare providers is the compatible inspection command
pscale oidc-trust providers --org <org> --format json

# v0.352.0+: explicit list/show and structured claim descriptions
pscale oidc-trust providers list --org <org> --format json
pscale oidc-trust providers show <provider-name> --org <org> --format json

# Both versions support trust list/show
pscale oidc-trust list --org <org> --format json
pscale oidc-trust show <trust-id> --org <org> --format json
```

On v0.351.0, bare `providers` returns provider JSON with `required_claims` but no `claims` descriptions; select the exact provider by its returned `name` and review every required claim. Do not run `providers list` or `providers show` on that version. If required policy detail is unavailable, stop and obtain authoritative provider policy or an approved upgrade rather than inventing claims.

Use provider `name`, `issuer`, and the JSON `required_claims` array to review the intended issuer and every required claim. Provider list JSON is an array; provider show JSON is one object, retaining the `claims` array (or null when absent), whose entries contain `name`, boolean `required`, and `description`. Do not convert missing/null claim detail into proof that no restrictions are required. Human show output appends a claim table only when claims exist; human/CSV provider summaries join required claims into text, and CSV show emits the provider summary only, not the claim-detail table. Use JSON for policy review. `show` selects an exact provider name from the organization-scoped provider list, not a trust ID; it fails if that provider is unavailable. Never fall back to a different provider or broaden policy after that failure.

Do not invent provider names, supported permissions, TTL bounds, wildcard matching, or claim semantics from an example. Confirm them with the organization owner and current provider/API policy. Restrict the approved workload/repository/ref/environment as supported; missing or empty conditions are not a safe default.

Trust JSON preserves structured `conditions`, `accesses`, and `bulk_database_accesses`, plus `id`, `display_name`, `provider`, `audience`, `max_ttl_seconds`, `created_at`, and `updated_at`. Human/CSV tables flatten claims and accesses; all-database grants render with `*:`. Use JSON for readback. `list` returns a JSON array (empty `[]` for no trusts); the human empty-state message is not an error. A not-found response from `list`/`providers` can mean missing organization or OIDC not enabled; do not interpret it as an empty inventory. The list command exposes no pagination flags and the API client uses its default list options; do not assume one response proves an exhaustive inventory in a large organization.

## Approve and create

Obtain explicit user approval for the exact organization, display name, provider/issuer, all claim restrictions, maximum token lifetime, and every permission/resource. Select the shortest suitable approved TTL in seconds and the narrowest access scope. Organization accesses and `--all-databases-access` are broader than a named database grant and require an explicit scope justification. These commands manage trust policy only; no token-exchange command is provided here.

After replacing placeholders with reviewed values, the following is an example of a proposed create, not authorization to execute it. Repeat `--condition` for every required restriction and `--database-access` for each approved grant; repeatable flags take separate values, not a comma-separated policy.

```bash
pscale oidc-trust create --org <org> --name <trust-name> \
  --provider <provider-name> --max-ttl <approved-seconds> \
  --condition <claim>=<approved-value> \
  --database-access <database>:<approved-access> --format json
```

`--name`, `--provider`, and `--max-ttl` are required. `--condition` uses `claim=value`; database access uses `database:access`; `--org-access` and `--all-databases-access` take access names. Review API validation rather than treating CLI parsing as policy validation. Read back the exact returned trust ID with `show --org ... --format json`, verify provider, audience, TTL, conditions, and all access scopes before declaring success. On an ambiguous create response, inspect first to avoid duplicate trusts.

## Update replacement and clearing rules

Read fresh `show` output, prepare the complete before/after policy, check dependent workloads and recovery, and obtain explicit approval before one update. The provider and audience have no update flags. At least one supported update flag is required.

| Supplied update flags | Effect |
| --- | --- |
| `--name`, `--max-ttl` | Replace only the supplied scalar fields; omitted fields remain unchanged. |
| `--condition` (repeatable) | Replaces **all conditions** with the supplied list. |
| Either `--org-access` or `--database-access` (repeatable) | Replaces the **combined org and database access list**. Include every approved grant to retain from both scopes, even if only one scope changes. |
| `--all-databases-access` (repeatable) | Replaces the separate all-database access list. |
| A list flag supplied as `--condition=`, `--org-access=`, `--database-access=`, or `--all-databases-access=` | Blank values are removed. With no remaining values, the corresponding list is sent as `[]`, clearing it. Either access flag can clear the combined list; a nonempty sibling access flag supplies the replacement entries. |
| List flags omitted entirely | Corresponding list is not sent and remains unchanged. |

Never let an unset shell variable silently become an empty list flag. Clearing conditions can broaden who qualifies; clearing permissions can interrupt workloads. Both need separate, explicit approval of that outcome, fresh dependency checks, and a verified recovery plan. An API refusal is a stop signal, not a reason to remove conditions or expand permissions.

For a scalar-only change, retain all lists by omitting their flags:

```bash
pscale oidc-trust update <trust-id> --org <org> \
  --max-ttl <approved-seconds> --format json
pscale oidc-trust show <trust-id> --org <org> --format json
```

Compare readback with the entire approved policy, including unchanged fields; investigate concurrent changes or ambiguous responses rather than automatically retrying.

## Delete safeguards

Before deletion, obtain approval for the exact organization and trust ID, identify dependent CI/workloads and availability impact, and verify a recovery/replacement procedure with an owner that survives loss of this trust. Preserve only approved non-secret policy metadata. Do not assume deletion revokes already-issued tokens; confirm the provider/API revocation and TTL behavior separately. Never delete to repair an update refusal.

```bash
# Only after exact-target approval, dependency checks, and verified recovery
pscale oidc-trust delete <trust-id> --org <org>
```

Interactive deletion confirms the trust ID. Non-interactive deletion and JSON/CSV output (even with a terminal) require `--force`; obtain separate explicit approval for that flag before any attempt. Never add force after a refusal. Read back the exact target and verify dependent workload health or the approved replacement path. Only an expected not-found response under verified organization/authentication scope supports absence; network/authentication failures do not. No live trust operations are part of this reference's verification.

## Complete provider help

Captured from official v0.352.0; archive SHA-256 `8ac6b09f8df40d94dc16468a7db7e5df5e099e04401e6d5ee0a92cd73bd930fd`. The `providers ls --help` alias was separately captured and matches canonical `providers list --help` line-for-line after trailing-padding normalization. Other unchanged help retains its earlier provenance. The CLI's displayed credential flags are interface documentation, not permission to pass secrets on the command line.

### providers

```text
List and show OIDC trust providers

Usage:
  pscale oidc-trust providers <command> [flags]
  pscale oidc-trust providers [command]

Available Commands:
  list        List OIDC trust providers
  show        Show an OIDC trust provider and the claims in its tokens

Flags:
  -h, --help   help for providers

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

Use "pscale oidc-trust providers [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

### providers list

```text
List OIDC trust providers

Usage:
  pscale oidc-trust providers list [flags]

Aliases:
  list, ls

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

### providers show

```text
Show an OIDC trust provider and the claims in its tokens

Usage:
  pscale oidc-trust providers show <name> [flags]

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
