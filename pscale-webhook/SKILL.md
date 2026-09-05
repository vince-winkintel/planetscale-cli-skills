---
name: pscale-webhook
description: Manage PlanetScale database webhooks with the pscale CLI. Use when listing, inspecting, creating, updating, testing, or deleting webhooks, configuring event subscriptions, enabling or disabling delivery, or setting or clearing an Authorization header. Triggers on pscale webhook, database webhook, webhook authorization header, webhook events, webhook test.
---

# pscale webhook

Manage database webhooks and their event subscriptions.

## Inspect first

```bash
pscale webhook list <database> --org <org> --format json
pscale webhook show <database> <webhook-id> --org <org> --format json
```

Use JSON for identifiers and persisted state. Current output exposes `authorization_header_configured` as a boolean; it does not reveal the configured header value. Treat any signing secret returned at creation as sensitive and do not print, store in logs, or commit it.

## Create

```bash
pscale webhook create <database> \
  --url https://hooks.example.com/planetscale \
  --events branch.ready,deploy_request.opened \
  --enabled=true \
  --org <org> --format json
```

`--url` is required. Confirm the destination host, TLS endpoint, subscribed events, enabled state, and receiver ownership before creation. The create response may contain a webhook signing secret; route it directly to an approved secret store and redact command output.

### Authorization header

`--authorization-header` accepts the complete HTTP `Authorization` value, such as `Bearer …`. It is a secret-bearing argument. Do not place a literal credential in documentation, shell history, logs, chat, source control, or process captures. Use an approved secret source and preserve only the variable reference in reusable command text:

```bash
pscale webhook create <database> \
  --url https://hooks.example.com/planetscale \
  --authorization-header "$PLANETSCALE_WEBHOOK_AUTHORIZATION_HEADER" \
  --org <org> --format json
```

Do not run this form until the environment variable is populated outside the agent-visible context. Verify only `authorization_header_configured: true`; never attempt to read the value back.

## Update

Pass at least one of `--url`, `--authorization-header`, `--clear-authorization-header`, `--events`, or `--enabled`. Only supplied fields change.

```bash
# Review current state
pscale webhook show <database> <webhook-id> --org <org> --format json

# Disable or change subscriptions
pscale webhook update <database> <webhook-id> \
  --enabled=false \
  --events branch.ready \
  --org <org> --format json

# Remove the configured header explicitly
pscale webhook update <database> <webhook-id> \
  --clear-authorization-header \
  --org <org> --format json

# Verify persisted non-secret state
pscale webhook show <database> <webhook-id> --org <org> --format json
```

`--authorization-header` and `--clear-authorization-header` are mutually exclusive. An empty `--authorization-header` value is rejected; use the clear flag. Changing or clearing authentication can interrupt deliveries, so coordinate the receiver update and verify `authorization_header_configured` afterward.

## Test and delete

`webhook test` sends a real event to the external receiver. Confirm the destination and downstream side effects before running it. A successful CLI response proves dispatch was accepted, not that the receiver processed it; verify receiver-side evidence when available.

```bash
pscale webhook show <database> <webhook-id> --org <org> --format json
pscale webhook test <database> <webhook-id> --org <org> --format json
```

Deletion has no CLI confirmation flag. Treat it as destructive: inspect the exact webhook, inventory dependencies, obtain explicit approval, delete, and read back the list.

```bash
pscale webhook show <database> <webhook-id> --org <org> --format json
pscale webhook delete <database> <webhook-id> --org <org> --format json
pscale webhook list <database> --org <org> --format json
```

## Reference

See `references/commands.md` for checksum-verified command help surfaces.
