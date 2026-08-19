---
name: pscale-maintenance
description: Inspect PlanetScale Vitess Enterprise maintenance schedules and historical windows with pscale. Use when listing planned maintenance, checking pending Vitess or MySQL versions, inspecting schedule deadlines, or reviewing completed maintenance windows. Triggers on pscale maintenance, maintenance schedule, maintenance window, planned maintenance, pending Vitess version, pending MySQL version.
---

# pscale maintenance

Inspect read-only maintenance schedule and window data for Vitess databases on Enterprise plans.

## Prerequisites

- Authenticate with `pscale auth check --format json`.
- Identify the exact organization and Vitess database.
- Pass `--org` explicitly rather than relying on the configured default organization.
- Prefer `--format json` for automation and preserve schedule IDs as opaque values.

## Inspect schedules

```bash
# Discover schedules and stable IDs
pscale maintenance list <database> \
  --org <org> \
  --format json

# Inspect one schedule in full
pscale maintenance show <database> <schedule-id> \
  --org <org> \
  --format json
```

Schedule output can include whether the schedule is enabled or required, frequency, day/week/hour, duration, next and last window times, pending Vitess/MySQL versions, expiry, and deadline metadata. Treat all timestamps in JSON as authoritative API values; do not infer a local timezone from human table output.

Monthly schedules include a week-of-month value. Non-monthly table rows show a dash for week because the field does not apply.

## Inspect maintenance windows

```bash
pscale maintenance windows <database> <schedule-id> \
  --org <org> \
  --format json
```

Windows are historical or active instances associated with the selected schedule. Use their start and finish timestamps to distinguish completed work from a future schedule. An empty result means no windows currently exist for that schedule; it does not prove maintenance is disabled.

## Safe review workflow

1. Run `pscale database show <database> --org <org> --format json` and confirm the database engine and identity.
2. List schedules and select the exact schedule ID from live output.
3. Show the schedule before interpreting pending versions, expiry, or deadline fields.
4. List its windows and report schedule metadata separately from observed window history.
5. Do not claim these read-only commands reschedule, approve, or cancel maintenance; the current CLI surface only lists and shows records.

## Troubleshooting

- **Command unavailable:** update `pscale` and verify live `pscale maintenance --help`.
- **Not found:** re-run the list against the exact organization/database and copy the schedule ID without modification.
- **No schedules:** confirm the database is Vitess and that the organization has the applicable Enterprise maintenance feature.
- **Unexpected day/week:** inspect JSON fields and frequency together; week-of-month applies only to monthly schedules.

See [references/commands.md](references/commands.md) for checksum-verified command help.
