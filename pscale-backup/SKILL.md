---
name: pscale-backup
description: Create, list, show, restore, update protected status, and delete branch backups, and manage scheduled backup policies. Use when creating database backups, restoring from backups, protecting or unprotecting backups, managing backup lifecycle, configuring production/development backup schedules, retention, or policy targets. Triggers on backup, restore, database backup, backup branch, protected backup, backup update, backup policy, retention schedule.
---

# pscale backup

Create, list, show, restore, and delete branch backups; manage scheduled backup policies.

## Common Commands

```bash
# Create backup
pscale backup create <database> <branch>

# List backups
pscale backup list <database> <branch>

# Show backup details
pscale backup show <database> <branch> <backup-id>

# Protect or unprotect a backup only after explicit approval
pscale backup update <database> <branch> <backup-id> --protected=true --format json
pscale backup update <database> <branch> <backup-id> --protected=false --format json

# Delete backup
pscale backup delete <database> <branch> <backup-id>

# Inspect scheduled policies
pscale backup policy list <database> --format json
```

## Workflows

### Backup Before Migration

```bash
# Create backup before schema changes
pscale backup create my-database main

# Proceed with migration
pscale deploy-request deploy my-database 1

# If issues, restore from backup (contact PlanetScale support)
```

### Scheduled backup policies

Policies target either production or development branches and are separate from one-off `backup create` operations. Inspect current policies before writing, and confirm storage-cost implications for custom schedules.

```bash
pscale backup policy list <database> --org <org> --format json

pscale backup policy create <database> --org <org> \
  --target production \
  --frequency-value 1 --frequency-unit day \
  --schedule-time 03:00 \
  --retention-value 30 --retention-unit day \
  --name "daily production"

pscale backup policy show <database> <policy-id> --org <org> --format json
pscale backup policy update <database> <policy-id> --org <org> \
  --retention-value 60 --retention-unit day
```

Frequency units are `hour`, `day`, `week`, or `month`; retention also supports `year`. Weekly/monthly schedules can use `--schedule-day` (`0` Sunday through `6` Saturday), and monthly schedules can use `--schedule-week` (`0` first through `3` fourth). Updates send only supplied flags. Before deleting, show the exact policy, obtain approval, avoid `--force` unless explicitly authorized, and list policies afterward; required system policies cannot be deleted.

### Protect or unprotect a backup

`pscale backup update` toggles whether a backup is protected from deletion. The `--protected` flag is required; use an explicit `=true` or `=false` value so the requested state is clear.

```bash
# Inspect current state first
pscale backup show <database> <branch> <backup-id> --org <org> --format json

# After explicit approval for the exact backup and target state
pscale backup update <database> <branch> <backup-id> --org <org> \
  --protected=true \
  --format json

# Verify persisted protected state
pscale backup show <database> <branch> <backup-id> --org <org> --format json
```

Unprotecting a backup can make later deletion possible. Read back the organization, database, branch, backup ID, current state, requested state, and retention/recovery reason before changing it.

## Related Skills

- **pscale-branch** - Backup specific branches
- **pscale-deploy-request** - Backup before deploying

## References

See `references/commands.md` for complete command reference.
