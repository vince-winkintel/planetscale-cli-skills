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

`--url` is required. Confirm the destination host, TLS endpoint, subscribed events, enabled state, and receiver ownership before creation. Successful `create` output includes the generated webhook signing `secret` in both human and JSON formats. Capture it from that response directly into an approved secret manager; do not print it into logs, paste it into tickets, or commit it. Treat the create response as the one reliable capture point.

`--events` accepts a comma-separated list. Published event names are:

```text
branch.anomaly
branch.out_of_memory
branch.primary_promoted
branch.ready
branch.schema_recommendation
branch.sleeping
branch.start_maintenance
backup.failed
backup.succeeded
cluster.storage
database.access_request
deploy_request.closed
deploy_request.errored
deploy_request.in_progress
deploy_request.opened
deploy_request.pending_cutover
deploy_request.queued
deploy_request.reverted
deploy_request.schema_applied
keyspace.storage
webhook.test
```

The CLI forwards event strings to the PlanetScale API without client-side validation. Use the [webhook events reference](https://planetscale.com/docs/api/webhook-events) as the source of truth; an unknown or unsupported name is not normalized by the CLI and can fail at the API.

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

Before updating, save the non-secret configuration from `webhook show` (`url`, `events`, and `enabled`) and ensure the current Authorization value is available separately if rollback may need to restore it—the API does not return that header value. To roll back, re-run `webhook update` with the previous `--url`, `--events`, and explicit `--enabled=<true|false>` values, plus either the prior `--authorization-header` value or `--clear-authorization-header`, then verify with `webhook show` and `webhook test`.

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

When scripting against `--format json`, probe one representative response first and handle optional fields defensively. The CLI serializes the underlying API webhook model for JSON, while human and CSV output use a smaller normalized view, so fields can differ and the JSON model can gain fields as the API evolves. Do not build strict decoders from the command-reference snippets or assume table and JSON output have identical fields.

## Reference

See `references/commands.md` for checksum-verified command help surfaces.
