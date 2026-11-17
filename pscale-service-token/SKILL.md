---
name: pscale-service-token
description: Manage PlanetScale service tokens for CI/CD authentication and OIDC trust policy (provider claim discovery, trust create/update/delete). Use when setting up automated deployments, configuring CI/CD pipelines (GitHub Actions, GitLab CI, CircleCI, etc.), creating non-interactive authentication, inspecting service token metadata, duplicating service tokens, updating token names or expiry, rotating CI/CD credentials, or reviewing PlanetScale workload identity policy. Preferred over passwords for production automation. Triggers on PlanetScale OIDC trust, oidc-trust, PlanetScale workload identity, service token, service-token show, CI/CD auth, automation token, pipeline authentication.
---

# pscale service-token

Create, list, and manage service tokens for CI/CD and automation.

## Destructive-operation safety

These gates apply to every destructive example here, including deletion, demotion, protection removal, connection/transaction termination, deploy-request closure/revert, and cleanup. Command examples and CLI confirmation prompts are not authorization.

1. Inspect fresh state and confirm support for the target engine and installed CLI. Obtain explicit approval for the exact organization and, where applicable, database, branch, and resource ID/name, plus the operation and flags; use an explicit `--org` on every operation. Stop on unsupported operations or uncertain identity.
2. Check dependencies and availability: applications, active users, child resources, routing, pending changes, and the maintenance window. Do not infer that a stale, merged, or unused-looking resource is disposable.
3. Require a verified recovery path that survives the operation: confirm backup/export usability and retention, or tested replacement/recreation instructions, ownership, and recovery time. A backup name alone is not verification; stop if recovery cannot be established.
4. Execute only the approved action. Force flags, descendant deletion, demotion, and disabling protection require separate explicit approval; never add them to work around a refusal. For a known headless session, obtain approval for the required force flag up front, before attempting the operation; stop if that approval is absent or any attempt is refused.
5. Perform read-back verification of the exact target and dependent service health. Inspect pending/asynchronous outcomes before claiming completion. Authentication/network errors are not proof of absence; an ambiguous result requires investigation, not an automatic retry.

## Token mutation and credential handling

Service-token management requires approved user/API-token authentication; the command family rejects service-token authentication. Use an explicit `--org`. Before create, duplicate, update, grant changes, or deletion, inspect the exact token's metadata and access where applicable, obtain explicit approval for the organization, token ID, operation, name/expiry and complete access scope, and use least privilege. Check dependent automation before changing expiry or grants. Deletion and access removal also require the safety gates above.

`duplicate <id> --name <approved-name>` returns a new secret-bearing token response. `update <id>` accepts `--name` and/or `--ttl`; it does not rotate the secret or change ID/grants. Effectively omitted fields remain unchanged: before relying on omission, confirm that `PLANETSCALE_NAME` / `PLANETSCALE_TTL` and matching user-config `name` / `ttl` keys do not supply them. Nonempty inherited values count as supplied, including duplicate's required name; `PLANETSCALE_TTL=never` can remove expiry during a name-only argv update. Do not print config files or environment values to check this; stop if effective settings cannot be confirmed safely. TTL is integer seconds or literal `never` to remove expiry. Removing or extending expiry needs explicit approval. Do not infer duplicate grant/expiry behavior or use update as rotation. Read the [command reference](references/commands.md) for compatibility minima, exact request/output semantics, and read-back requirements.

Never display or store returned token values in chat, logs, evidence, temporary files, or this repository. Create/duplicate require a user-controlled secret-delivery mechanism that keeps the response out of agent output; stop if none is available. Examples below describe only previously authorized workflows. Inspect metadata with `show` and grants with `show-access`, and verify the result after an approved mutation without exposing secrets.

## Common Commands

```bash
# Create only through the approved user-controlled secret-delivery mechanism
pscale service-token create --org <org>

# Duplicate only after scope/expiry approval and with secret-safe delivery
pscale service-token duplicate <id> --name <approved-name> --org <org>

# Update only after name/expiry approval and effective-config checks above
# TTL is integer seconds or never; never requires non-expiring-token approval
pscale service-token update <id> --name <approved-name> --ttl <seconds-or-never> --org <org>

# List service tokens
pscale service-token list --org <org>

# Show safe metadata for one service token
pscale service-token show <token-id> --org <org> --format json

# Delete service token
pscale service-token delete <token-id> --org <org>
```

## OIDC trusts for workload identity

Use `pscale oidc-trust providers list --org <org> --format json` and `pscale oidc-trust providers show <provider-name> --org <org> --format json` to inspect the organization-scoped issuer, required claims, and available claim descriptions before proposing trust policy. Check the local [OIDC trust reference](references/oidc-trust-commands.md) first for compatibility minima and the legacy provider-inspection command, JSON versus human/CSV behavior, exact replacement/clearing semantics, and approved examples. This manages trust configuration; it does not perform token exchange or replace the authentication workflow.

Every create, update, or delete needs explicit user approval for the exact organization, trust identity, provider/claims, TTL, and complete access scope. Use least privilege and a short approved TTL; prefer specific database access over organization-wide or all-database grants. Never print or store OIDC assertions, exchanged credentials, or service-token secrets. Read back the trust after writes. Clearing conditions can broaden eligibility; changing either org or database access replaces both lists together. Deletion also requires dependency checks, verified recovery, and separate advance approval for non-interactive `--force` under the safety gates above.

## Workflows

### CI/CD Setup (GitHub Actions)

```bash
# 1. Create only through the approved user-controlled secret-delivery mechanism
pscale service-token create --org my-org

# 2. User provisions the result directly into approved CI secrets
#    through the secret-delivery mechanism agreed before creation.
#    Do not display or capture returned token values in agent output.

# 3. Use in workflow
# .github/workflows/deploy.yml
# env:
#   PLANETSCALE_SERVICE_TOKEN_ID: ${{ secrets.PLANETSCALE_SERVICE_TOKEN_ID }}
#   PLANETSCALE_SERVICE_TOKEN: ${{ secrets.PLANETSCALE_SERVICE_TOKEN }}
# run: |
#   pscale deploy-request deploy my-db my-branch
```

### CI/CD Pipeline Integration

```bash
# 1. Create only through the approved user-controlled secret-delivery mechanism
pscale service-token create --org my-org

# 2. User provisions PLANETSCALE_SERVICE_TOKEN_ID and PLANETSCALE_SERVICE_TOKEN
#    directly into approved CI secrets through that mechanism.
#    Do not display or capture returned token values in agent output.

# 3. Use in your pipeline config (.github/workflows, .gitlab-ci.yml, etc.)
# deploy:
#   script:
#     - pscale deploy-request create $DATABASE $BRANCH_NAME
```

### Token Rotation

```bash
# 1. List existing tokens
pscale service-token list --org my-org

# 2. Create only through the approved user-controlled secret-delivery mechanism
pscale service-token create --org my-org

# 3. User updates CI secrets directly through that mechanism; never capture
#    the returned token in agent output. Verify replacement access first.

# 4. Review cleanup under the safety gates; verify replacement access and obtain approval
pscale service-token delete <old-token-id> --org my-org
```

### Inspect a service token

`pscale service-token show` returns safe service-token metadata such as ID, name, creation time, expiry, last-used time, last-used IP, and last-used network organization. It does not print the token secret and does not include access grants; use `show-access` when grants are needed.

```bash
pscale service-token show <token-id> --org <org> --format json
pscale service-token show-access <token-id> --org <org> --format json
```

List/show human and CSV output uses `last_used_ip` and `last_used_organization` columns. JSON uses nullable `last_used_ip` and `last_used_asn_organization`; the latter identifies the IP's network/ASN organization, not the PlanetScale organization or an access grant. Missing values display as empty strings in the table; JSON retains nulls. Do not infer misuse, current permissions, or safety to delete from last-use metadata alone. Protect IP/network metadata in incident evidence and avoid publishing it.

Treat token IDs and grant details as sensitive operational metadata. Never ask the user to paste a service token secret into chat; use environment variables or a secrets manager.

## Troubleshooting

### Token authentication fails

**Error:** `401 Unauthorized`

**Solutions:**
- Verify both TOKEN_ID and TOKEN are set correctly
- Check token hasn't been deleted: `pscale service-token list`
- Ensure token has required permissions
- Inspect expiry and access first; create a replacement only with explicit approval and a secret-safe delivery path

### Token not showing in list

**Cause:** Tokens are organization-scoped

**Solution:**
```bash
# Ensure correct org
pscale org show

# List tokens for specific org
pscale service-token list --org <correct-org>
```

## Security Best Practices

1. **Rotate tokens regularly** (every 90 days recommended)
2. **Use separate tokens** for different CI/CD systems
3. **Review tokens for cleanup under the safety gates**; verify CI/CD dependencies before approving deletion
4. **Never commit tokens** to version control
5. **Use secrets management** (GitHub Secrets, environment variables, vault systems)
6. **Limit token scope** to approved grants; inspect `show-access` and separately authorize any grant changes

## Related Skills

- **pscale-auth** - Interactive authentication (development)
- **pscale-deploy-request** - Automated deployments via tokens
- **gitlab-cli-skills** - GitLab CI integration
- **github** - GitHub Actions integration

## References

See `references/commands.md` for complete command reference.
