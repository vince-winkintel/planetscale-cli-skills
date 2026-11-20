---
name: pscale-auth
description: Manage PlanetScale CLI authentication including login/logout, check auth status, and switch accounts. Use when setting up pscale for first time, troubleshooting auth issues, switching PlanetScale accounts, or managing authentication sessions. Triggers on auth, login, logout, authentication, credentials, PlanetScale account.
---

# pscale auth

Manage authentication for the PlanetScale CLI.

## Common Commands

```bash
# Login to PlanetScale (opens browser)
pscale auth login

# Login in automation-friendly JSON mode
pscale auth login --format json

# Logout only after explicit authorization for the intended session (see below)
pscale auth logout

# Check current authentication status
pscale org show
```

## Authentication Methods

### 1. Interactive Login (Default)

Opens browser for OAuth flow:

```bash
pscale auth login
```

**Best for:** Local development, first-time setup

For agentic or scripted onboarding, prefer JSON output so required user actions can be parsed and relayed without scraping human text:

```bash
pscale auth login --format json
```

JSON login emits its initial pending authorization envelope to stderr and its final result to stdout; inspect both without capturing credentials. If output indicates user action is required, relay only the required action/URL to the user and do not print or store credentials. Device authorization expiry or denial requires a deliberate new login attempt, not repeated polling of the same code.

In human mode, **Access approved. Saving credentials to your system keyring** means browser approval finished and credential persistence may be waiting on a keyring unlock; it is not still waiting for browser approval. Do not enter a password or operate a keyring dialog on the user's behalf. Treat token-save failure as an unconfirmed login, distinguish it from organization-setup failure after credentials were saved, and verify access with read-only `pscale auth check --format json` before switching organizations or using the session. For unattended jobs, use an existing approved service-token configuration rather than starting interactive login.

The CLI resolves its built-in OAuth client values at runtime and omits their values from `pscale auth login --help`. Do not scrape, record, or reproduce OAuth credentials from help output. Treat `--client-id` and `--client-secret` as advanced overrides: use them only when the user explicitly supplies a trusted custom OAuth client, and pass the secret through a secret-safe mechanism rather than shell history or logs.

### 2. Service Tokens (CI/CD)

For automated environments, have the user inject both fields directly from an approved secret manager; do not type, read back, or capture their values:

```bash
# User-controlled CI secret injection supplies PLANETSCALE_SERVICE_TOKEN_ID
# and PLANETSCALE_SERVICE_TOKEN; no agent-side token handling.
pscale database list --org <org>
```

**Best for:** CI/CD pipelines, automation, production deployments

See `pscale-service-token` skill for token creation.

### 3. API token flags/env

Recent `pscale` global flags also accept API-token based auth for automation:

```bash
pscale database list --org <org> --api-token <token>
```

Prefer environment/secret-manager injection over putting tokens in shell history. Never commit tokens to skill repos or scripts.

## Credential loading and logout

Help, version, and skill discovery do not load stored credentials. Protected commands, `auth check`, `api`, and live branch-connection inspection load them when needed; a read-only command can still prompt for credential access or migrate a legacy token. Direct API tokens and either service-token field bypass ordinary stored-token loading, but a partial service-token pair fails authentication. Avoid mixed credential methods: raw `api` and ordinary API clients differ in precedence. See the [credential behavior reference](references/commands.md) for compatibility minima and precise source behavior.

Logout intentionally loads the stored user token even with service-token credentials set; it does not revoke those service tokens or unset their environment variables. A nonempty explicit API token becomes the revocation target; after successful revocation, logout also deletes the stored login locally without revoking that separate session and without the unreadable-token warning. Obtain explicit authorization for the intended session before logout, including both affected credentials when an explicit API token differs from the stored session. Unreadable stored tokens can be deleted locally without remote revocation, with a warning; local deletion is never verified revocation of the stored session, whether or not a warning appears. Keyring logout removes the legacy token file before the keyring entry; fallback file logout also removes the default config. Errors can leave partial cleanup. Do not read credential files, operate the keyring, or use logout as an automatic troubleshooting probe.

## Workflows

### First-Time Setup

```bash
# 1. Login
pscale auth login

# 2. Verify authentication
pscale org show

# 3. List databases to confirm access
pscale database list --org <org>
```

### Switch Between Accounts

```bash
# Confirm credential method and authorize all affected sessions under the local
# logout gates above before logout; stop on ambiguity or partial cleanup.
pscale auth logout

# Login with different account
pscale auth login
```

### CI/CD Authentication

Management requires approved user/API-token authentication, not service-token authentication; do not silently switch credentials. Create/duplicate require explicit approval for the organization, operation, name/expiry and access scope, plus a user-controlled secret-delivery mechanism that keeps the response out of agent output; stop if none is available. Never display or store returned token values in chat, logs, evidence, temporary files, or this repository. Have the user provision the result directly into approved CI secrets; verify safe metadata and access without exposing the secret.

Before creation, approve the exact organization, token name, complete CIDR list and positive integer TTL, check dependent automation egress, and confirm installed flag support using the [local compatibility notes](references/commands.md). Create without effective CIDRs is unrestricted; empty/whitespace-only CIDRs normalize to no restrictions. Unrestricted creation requires explicit approval. Check `PLANETSCALE_NAME`, `PLANETSCALE_TTL`, `PLANETSCALE_CIDRS` and user-config defaults without dumping values. Widening or removing restrictions needs separate approval. Read back the new ID with `show` and `show-access` to verify CIDRs, expiry and grants before use. Create/duplicate TTL does not accept `never`; zero/omission sends no TTL. Route full omission, normalization, duplicate-copy expectations and compatibility details to the `pscale-service-token` skill.

```bash
# Only through the approved user-controlled secret-delivery mechanism above
pscale service-token create --name <approved-name> --cidrs <approved-ip-or-cidr-list> --ttl <approved-positive-seconds> --org <org>

# Use in CI/CD environment
# User-controlled CI secret injection supplies PLANETSCALE_SERVICE_TOKEN_ID
# and PLANETSCALE_SERVICE_TOKEN; no agent-side token handling.

# Test authentication
pscale database list --org <org>
```

## Troubleshooting

### Login fails / browser doesn't open

**Symptoms:** `pscale auth login` hangs or fails

**Solutions:**
- Check network connectivity
- Ensure firewall allows https://auth.planetscale.com
- Try headless browser auth (not supported by pscale, use service tokens instead)
- Use service token for non-interactive environments

### "Unauthorized" errors

**Symptoms:** `401 Unauthorized` or `403 Forbidden` responses

**Solutions:**
- Inspect an authorized `pscale auth check --format json` result; propose logout/login only after confirming the credential method and obtaining approval for the intended session
- Verify organization access: `pscale org show`
- Check service token hasn't expired (if using tokens)
- Ensure token has required permissions (database read/write, branch create, etc.)

### Multiple accounts / wrong org

**Symptoms:** Cannot access expected databases

**Solutions:**
- Check current org: `pscale org show`
- Switch org: `pscale org switch <org-name>`
- List all orgs: `pscale org list`
- Switch accounts only after confirming the credential method and explicitly authorizing all affected sessions under the local logout gates above; never use logout/login as an automatic probe

### Service token authentication fails

**Symptoms:** Token authentication not working in CI/CD

**Solutions:**
- Verify both `PLANETSCALE_SERVICE_TOKEN_ID` and `PLANETSCALE_SERVICE_TOKEN` are set
- Check token hasn't been revoked: `pscale service-token list --org <org>`
- Ensure token has required permissions for the operation
- Inspect sanitized error codes and credential method only; do not enable credential-bearing debug capture

## Related Skills

- **pscale-service-token** - Create and manage service tokens for CI/CD
- **pscale-org** - Switch between organizations
- **pscale-database** - Database operations requiring authentication

## References

See `references/commands.md` for complete `pscale auth` command reference.
