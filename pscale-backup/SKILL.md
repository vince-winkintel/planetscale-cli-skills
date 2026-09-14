---
name: pscale-backup
description: Create, list, show, restore, update protected status, and delete branch backups, and manage scheduled backup policies. Use when creating database backups, restoring from backups including Neki restores, protecting or unprotecting backups, managing backup lifecycle, configuring production/development backup schedules, retention, or policy targets. Triggers on backup, restore, database backup, backup branch, Neki restore, backup restore show, protected backup, backup update, backup policy, retention schedule.
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

# Restore to a new MySQL branch; pass --cluster-size explicitly
pscale backup restore <database> <new-branch> <backup-id> --cluster-size <size>

# Restore to a new PostgreSQL branch; optionally set additional replicas
pscale backup restore <database> <new-branch> <backup-id> --cluster-size <size> --replicas 2

# Restore to a new Neki branch; omit --cluster-size/--replicas unless overriding Neki sizing
pscale backup restore <database> <new-branch> <backup-id> \
  --config-profile name=<profile>,cluster-size=<size>,replicas=<count> \
  --router name=<router>,size=<size>,replicas-per-cell=<count>
pscale backup restore show <database> <source-branch> <backup-id> --format json

# Protect or unprotect a backup only after explicit approval
pscale backup update <database> <branch> <backup-id> --protected=true --format json
pscale backup update <database> <branch> <backup-id> --protected=false --format json

# Delete backup
pscale backup delete <database> <branch> <backup-id>

# Inspect scheduled policies
pscale backup policy list <database> --format json
```

## Workflows

### Restore to a new branch

Inspect the source backup and target database first. Valid SKUs are engine-specific: read the database `kind`, then list sizes with `--engine postgresql`, `--engine mysql`, or `--engine neki`. Do not choose from the unfiltered mixed-engine list. Backup-restore `--cluster-size` completion is generic and not database-kind aware, so verify the selected value against the filtered list. For MySQL and PostgreSQL restores, always pass `--cluster-size` explicitly; only Neki restores may omit it to inherit the source default-profile size. For PostgreSQL restores, optional `--replicas` sets the number of **additional** replicas: `0` creates a single-node branch, while omitting the flag uses the selected cluster size's default. The CLI rejects `--replicas` for Vitess/MySQL restores.

```bash
pscale backup show <database> <source-branch> <backup-id> --org <org> --format json
pscale database show <database> --org <org> --format json

# Choose the filter that matches the returned database kind
pscale size cluster list --org <org> --engine postgresql --format json
# pscale size cluster list --org <org> --engine mysql --format json
# pscale size cluster list --org <org> --engine neki --format json

# Restore MySQL and then verify the new branch
pscale backup restore <database> <new-branch> <backup-id> --org <org> \
  --cluster-size <size> --format json
pscale branch show <database> <new-branch> --org <org> --format json

# Restore PostgreSQL with two additional replicas, then verify the new branch
pscale backup restore <database> <new-branch> <backup-id> --org <org> \
  --cluster-size <size> --replicas 2 --format json
pscale branch show <database> <new-branch> --org <org> --format json
```

For Neki restores, use `pscale backup restore show <database> <source-branch> <backup-id> --format json` before restore. It previews the configuration profile and router sizes that will be used when overrides are omitted. Those values come from the live source branch, not the backup, so source-current-state can differ from backup-time sizing. Omitted Neki profile/router values inherit from the source; do not pass PostgreSQL `--replicas`, and omit `--cluster-size` unless intentionally overriding the default profile size. Use repeatable Neki `--config-profile name=<profile>[,cluster-size=<size>][,replicas=<n>]` and `--router name=<router>[,size=<sku>][,replicas-per-cell=<n>]` overrides only after reviewing `pscale-neki`.

Restoring creates a new branch and can incur capacity cost. Confirm the source branch, database, backup ID, new branch name, cluster size or inherited Neki profile/router sizes, and replica count before execution. Treat the returned branch as provisioning until its readiness fields confirm it can accept connections.

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
