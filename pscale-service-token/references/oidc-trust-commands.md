# OIDC trust policy

## Compatibility and provenance

Minimum CLI: **v0.351.0** for the `oidc-trust` parent and all six children (`providers`, `list`, `show`, `create`, `update`, `delete`), including update empty-list clearing and non-interactive deletion requiring `--force`. These commands are registered at the root; they are not service-token subcommands. No aliases are declared for this family. CLI support does not establish organization feature enablement or permissions. Check `pscale version` and stop on unsupported commands or permission failures.

Source contract: official `planetscale/cli` commit `e6449dc17ee2af30aed4a1a07aa5112bf6b7d8ca`, [root registration](https://github.com/planetscale/cli/blob/e6449dc17ee2af30aed4a1a07aa5112bf6b7d8ca/internal/cmd/root.go), [command implementations](https://github.com/planetscale/cli/tree/e6449dc17ee2af30aed4a1a07aa5112bf6b7d8ca/internal/cmd/oidctrust), and [API models](https://github.com/planetscale/cli/blob/e6449dc17ee2af30aed4a1a07aa5112bf6b7d8ca/internal/planetscale/oidc_trusts.go). This section describes reviewed source behavior, not captured binary help or live API output.

## Inspect before proposing policy

All commands require authentication and an explicit `--org`. Use the existing approved authentication path; do not fetch, decode, log, paste, or persist OIDC assertions, exchanged access tokens, or service-token secrets. Do not enable debug logging for credential-bearing operations. Trust metadata is not a credential, but redact organization/repository identifiers when reporting it outside the approved context.

```bash
pscale oidc-trust providers --org <org> --format json
pscale oidc-trust list --org <org> --format json
pscale oidc-trust show <trust-id> --org <org> --format json
```

Use provider `name`, `issuer`, and the JSON `required_claims` array to review the intended issuer and every required claim. Human/CSV providers output joins claims into text. Do not invent provider names, supported permissions, TTL bounds, wildcard matching, or claim semantics from an example. Confirm them with the organization owner and current provider/API policy. Restrict the approved workload/repository/ref/environment as supported; missing or empty conditions are not a safe default.

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
