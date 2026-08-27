---
name: pscale-billing
description: Inspect and manage PlanetScale organization billing with pscale. Use when showing or updating payment methods, deleting payment methods, checking payment-method setup status, listing invoices, showing invoice details, or listing invoice line items. Triggers on billing, invoice, payment method, billing invoice, payment-method, spend, billing data.
---

# pscale billing

Inspect organization billing data and manage payment methods from the PlanetScale CLI.

Billing output can contain sensitive business, payment, invoice, tax, address, and usage data. Always pass `--org` explicitly, prefer `--format json` for structured private review, and do not paste raw invoice or payment-method output into public logs, issues, or chat unless the user has reviewed and approved the disclosure.

## Common commands

```bash
# Show the current organization payment method
pscale billing payment-method show --org <org> --format json

# Start a Stripe Checkout flow to update the payment method
pscale billing payment-method update --org <org> --format json

# Check a setup started by update
pscale billing payment-method status <setup-id> --org <org> --format json

# Delete the current payment method only after explicit approval
pscale billing payment-method delete --org <org>

# Inspect invoices one page at a time
pscale billing invoice list --org <org> --page 1 --per-page 25 --format json
pscale billing invoice show <invoice-id> --org <org> --format json
pscale billing invoice line-items <invoice-id> --org <org> --page 1 --per-page 25 --format json
```

## Payment method workflow

`payment-method show` and `status` are read-only, but they still expose sensitive billing metadata. Use them to confirm the organization and current state before proposing a change.

`payment-method update` starts an external Stripe Checkout setup flow. Read back the organization and expected operator action before running it, then return only the setup URL or setup ID needed by the approved operator. Poll `payment-method status <setup-id>` only for that setup; if the command returns an API error, surface the real error instead of treating it as an interrupted setup.

`payment-method delete` is a destructive billing change. Show the current payment method, explain the operational impact, obtain explicit approval for the exact organization, avoid `--force` unless non-interactive deletion was specifically approved, and verify with `payment-method show` afterward.

## Invoice workflow

Invoice list and line-item commands fetch one page per call. Use `--page` and `--per-page` deliberately, and tell the user when more pages exist rather than hiding a long billing crawl inside one command.

```bash
# List invoices and inspect one invoice
pscale billing invoice list --org <org> --page 1 --per-page 25 --format json
pscale billing invoice show <invoice-id> --org <org> --format json

# Page through line items for cost attribution
pscale billing invoice line-items <invoice-id> --org <org> --page 1 --per-page 25 --format json
pscale billing invoice line-items <invoice-id> --org <org> --page 2 --per-page 25 --format json
```

Line items may include database names, resource names, metric names, subtotals, and Cloudflare billing indicators. Summarize costs at the level the user asked for, and redact or aggregate details before sharing outside the billing context.

## Safety gates

- Read back the organization before every billing command.
- Never invent or store card, bank, tax, personal address, or invoice data.
- Never ask the user to paste a full card number or payment secret.
- Treat payment-method deletion and update as billing writes requiring explicit approval.
- Treat invoice and line-item output as sensitive read-only billing data.

## Related skills

- **pscale-org** — organization settings, members, and teams
- **pscale-service-token** — CI/CD service token lifecycle

## References

See [references/commands.md](references/commands.md) for checksum-verified command help.
