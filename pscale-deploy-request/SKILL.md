---
name: pscale-deploy-request
description: Create, review, inspect, deploy, update, throttle, unblock, and revert schema changes via deploy requests. Use when deploying schema migrations to production, inspecting deployment queues or operations, checking reviews or storage readiness, changing auto-apply or auto-delete-branch settings, managing per-deploy throttling, unblocking a queue after a failed deploy or revert, forcing a blocked cutover, or reverting deployed changes. Essential for safe production schema deployments. Triggers on deploy request, schema deployment, deploy queue, unblock deploy queue, failed deploy, failed revert, deploy operations, storage check, deploy request update, auto apply, auto delete branch, force cutover, deploy throttler, review deployment, revert deployment, production migration.
---

# pscale deploy-request

Create, review, diff, revert, and manage deploy requests for schema changes.

## Common Commands

```bash
# Create deploy request from branch
pscale deploy-request create <database> <branch-name>

# List deploy requests
pscale deploy-request list <database>

# Show deploy request details
pscale deploy-request show <database> <number>

# View deploy request diff
pscale deploy-request diff <database> <number>

# Inspect reviews, storage, deployment, and operation progress
pscale deploy-request reviews <database> <number> --format json
pscale deploy-request storage-check <database> <number> --format json
pscale deploy-request deployment <database> <number> --format json
pscale deploy-request operations <database> <number> --format json

# Inspect the database-wide deployment queue
pscale deploy-request queue <database> --format json

# Unblock only after a failed deploy/revert is diagnosed and approved
pscale deploy-request unblock <database> <number> --format json

# Deploy (apply changes)
pscale deploy-request deploy <database> <number>

# Update deploy request settings (edit is an alias)
pscale deploy-request update <database> <number> --enable-auto-apply --format json
pscale deploy-request update <database> <number> --auto-delete-branch=false --format json

# Explicit strategy (parallel requires database support and approval)
pscale deploy-request deploy <database> <number> --strategy parallel --wait

# Close without deploying
pscale deploy-request close <database> <number>

# Revert deployed changes
pscale deploy-request revert <database> <number>
```

## Workflows

### Complete Schema Migration (Recommended)

This is the safest way to deploy schema changes to production:

```bash
# 1. Create development branch
pscale branch create my-database feature-schema-v2 --from main

# 2. Make schema changes
pscale shell my-database feature-schema-v2
# ... execute ALTER TABLE, etc.

# 3. Review changes locally
pscale branch diff my-database feature-schema-v2

# 4. Create deploy request
pscale deploy-request create my-database feature-schema-v2

# 5. Review deploy request diff
pscale deploy-request diff my-database 1

# 6. Deploy to production
pscale deploy-request deploy my-database 1

# 7. Verify deployment
pscale deploy-request show my-database 1
```

### Select serial or parallel deployment

`pscale deploy-request deploy` accepts `--strategy serial|parallel`. Omit the
flag to keep the default serial strategy. Before selecting `parallel`, confirm
that parallel deployments are enabled and appropriate for the target database,
review the deploy-request diff, and obtain the same production-change approval
required for deployment itself. Do not use parallel merely to make an unknown
migration finish sooner.

```bash
# Preserve the default
pscale deploy-request deploy <database> <number> --strategy serial

# Use only after eligibility and operational impact are confirmed
pscale deploy-request deploy <database> <number> --strategy parallel --wait
```

### Inspect readiness and progress

Use the read-only inspection commands before and during deployment rather than inferring state from `show` alone:

```bash
# Before deployment: confirm reviews and capacity
pscale deploy-request reviews <database> <number> --org <org> --format json
pscale deploy-request storage-check <database> <number> --org <org> --format json

# Understand queue placement and deployment state
pscale deploy-request queue <database> --org <org> --format json
pscale deploy-request deployment <database> <number> --org <org> --format json

# Track table/keyspace operations, including progress and ETA
pscale deploy-request operations <database> <number> --org <org> --format json
```

Treat `enough_storage: false`, a paused queue, a non-deployable deployment, or an unresolved required review as a stop condition. Do not deploy merely because one inspection endpoint is clear. During a migration, use operation state, `progress_percentage`, and `eta_seconds` as observations, not promises.

### Update deploy request settings

Use canonical `pscale deploy-request update`; `edit` remains an alias. This is an operational write because auto-apply changes cutover behavior and auto-delete controls whether the source branch is deleted after a successful deploy. At least one setting flag is required, and omitted flags are not sent.

```bash
# Inspect first
pscale deploy-request show <database> <number> --org <org> --format json
pscale deploy-request deployment <database> <number> --org <org> --format json

# After explicit approval for the exact settings
pscale deploy-request update <database> <number> --org <org> \
  --enable-auto-apply \
  --auto-delete-branch=false \
  --format json

# Verify readback
pscale deploy-request show <database> <number> --org <org> --format json
```

Never pass `--enable-auto-apply` and `--disable-auto-apply` together; `--auto-delete-branch` can be updated on its own. Use `--auto-delete-branch=false` to preserve the branch; `--auto-delete-branch` enables deletion after completion. Do not use the `edit` alias in prose or scripts except when explaining backwards compatibility.

### Unblock after a failed deploy or revert

`pscale deploy-request unblock` is the CLI equivalent of the dashboard's **Unblock deploy queue** action. It is accepted only when the selected deployment state is `complete_error` or `complete_revert_error`. The CLI rejects `pending_cutover` (use `apply`), deploy-check `error` (fix the check failure), and states without a failed deploy.

```bash
# Diagnose the exact failed request and blocked queue
pscale deploy-request show <database> <number> --org <org> --format json
pscale deploy-request deployment <database> <number> --org <org> --format json
pscale deploy-request queue <database> --org <org> --format json

# After explaining the failed state and receiving explicit approval
pscale deploy-request unblock <database> <number> --org <org> --format json

# Verify the request and queue after the write
pscale deploy-request show <database> <number> --org <org> --format json
pscale deploy-request queue <database> --org <org> --format json
```

Unblocking does not repair the failed migration, retry it, apply a gated cutover, or resolve failed deploy checks. It marks the failed deploy/revert complete so later queue work can proceed; the API determines whether the failed action was a deploy or revert. Treat it as a production operational write and preserve the failure evidence before running it.

### Manage per-deploy throttling

This throttler is scoped to one deploy request; it is separate from the database/tablet throttler under `pscale branch vtctld throttler`. Inspect the current eligible keyspaces and configuration first. Updating it changes live migration behavior and requires explicit approval.

```bash
pscale deploy-request throttler show <database> <number> --org <org> --format json

# One ratio for every eligible keyspace
pscale deploy-request throttler update <database> <number> --org <org> \
  --ratio 50 --format json

# Or individual ratios; this mode cannot be combined with --ratio
pscale deploy-request throttler update <database> <number> --org <org> \
  --configuration commerce=50 \
  --configuration lookup=25 \
  --format json

pscale deploy-request throttler show <database> <number> --org <org> --format json
```

Ratios are integers from `0` through `95`: `0` effectively disables throttling and `95` slows migrations the most. Pass exactly one mode. After an approved update, re-run `throttler show` and verify every keyspace ratio.

### Force a blocked cutover

`force-cutover` is only accepted when the deployment is in `in_progress_cutover`. It skips PlanetScale's wait (up to one hour) and kills long-running transactions blocking the table lock. This is an emergency operational write, not a routine acceleration option.

```bash
# Diagnose first
pscale deploy-request deployment <database> <number> --org <org> --format json
pscale deploy-request operations <database> <number> --org <org> --format json

# After explicit approval in an interactive terminal
pscale deploy-request force-cutover <database> <number> --org <org>

# Non-interactive execution only after the same approval
pscale deploy-request force-cutover <database> <number> --org <org> --force --format json

# Verify that cutover resumes/completes
pscale deploy-request deployment <database> <number> --org <org> --format json
pscale deploy-request operations <database> <number> --org <org> --format json
```

Before approval, identify the blocking deployment, explain that transactions will be killed, and confirm the expected application impact. Do not use `--force` merely to bypass an unavailable prompt.

### Review Before Deploy

```bash
# List pending deploy requests
pscale deploy-request list <database> --state open

# Show details
pscale deploy-request show <database> <number>

# View schema diff
pscale deploy-request diff <database> <number>

# Deploy if approved
pscale deploy-request deploy <database> <number>
```

### Revert Deployment

If a deployed schema change causes issues:

```bash
# View deployment status
pscale deploy-request show <database> <number>

# Revert the deployment
pscale deploy-request revert <database> <number>

# Verify revert
pscale deploy-request show <database> <number>
```

## Decision Trees

### Should I deploy or close?

```
Deploy request ready?
├─ Schema changes tested → Deploy
├─ Changes need revision → Close and create new DR from updated branch
├─ Changes no longer needed → Close
└─ Breaking changes detected → Close, fix in branch, create new DR
```

### Should I revert?

```
After deployment issues?
├─ Production errors caused by schema → Revert immediately
├─ Data integrity issues → Revert, then investigate
├─ Performance degradation → Revert if severe
└─ Minor issues / non-urgent → Leave deployed, fix forward
```

## Troubleshooting

### Deploy request creation fails

**Error:** "No schema changes detected"

**Cause:** Branch schema matches production

**Solution:**
```bash
# Verify schema diff exists
pscale branch diff <database> <branch-name>

# If no diff, make schema changes first
pscale shell <database> <branch-name>
```

### "Cannot deploy: conflicts detected"

**Cause:** Production schema changed since branch creation

**Solution:**
```bash
# Close conflicting deploy request
pscale deploy-request close <database> <number>

# Create a fresh branch from the current base branch
pscale branch create <database> <new-branch-name> --from main

# Reapply your schema changes to the new branch, then verify the diff
pscale branch diff <database> <new-branch-name>

# Create new deploy request
pscale deploy-request create <database> <new-branch-name>
```

### Deploy fails midway

**Error:** Deployment started but failed

**Solution:**
```bash
# Check deploy request status
pscale deploy-request show <database> <number>

# If partially deployed, may need to revert
pscale deploy-request revert <database> <number>

# Contact PlanetScale support for stuck deployments
```

### Cannot close deploy request

**Error:** "Deploy request is deployed"

**Cause:** Already deployed requests cannot be closed

**Solution:**
```bash
# Deployed requests can only be reverted
pscale deploy-request revert <database> <number>
```

## Deploy Request States

| State | Description | Actions Available |
|-------|-------------|-------------------|
| `open` | Pending deployment | deploy, close, diff, review |
| `in_progress` | Currently deploying | (wait for completion) |
| `complete` | Successfully deployed | revert, show |
| `closed` | Closed without deploying | (none - read-only) |
| `reverted` | Deployed then reverted | (none - read-only) |

## Related Skills

- **pscale-branch** - Create branches for deploy requests
- **drizzle-kit** - Generate migration SQL for schema changes
- **gitlab-cli-skills** - GitLab MR integration (link deploy request to MR)

## Best Practices

1. **Always review diff** before deploying (`pscale deploy-request diff`)
2. **Test schema in branch** before creating deploy request
3. **Use descriptive names** for branches (matches MR/issue number)
4. **Deploy during maintenance windows** for breaking changes
5. **Have rollback plan** - know how to revert
6. **Monitor after deployment** - watch for errors
7. **Clean up old deploy requests** - close stale ones

## Automation

See `scripts/deploy-schema-change.sh` for complete automation:

```bash
# Automated deploy workflow
./scripts/deploy-schema-change.sh \
  --database my-database \
  --branch feature-schema-v2 \
  --deploy
```

## Integration with Drizzle

Common pattern for Drizzle ORM users:

```bash
# 1. Edit your schema.sql file
# 2. Create PlanetScale branch
pscale branch create my-database <branch-name>

# 3. Apply schema changes
pscale shell my-database <branch-name> < schema.sql

# 4. Create deploy request
pscale deploy-request create my-database <branch-name>

# 5. Deploy
pscale deploy-request deploy my-database <number>

# 6. Pull schema back to Drizzle
pnpm drizzle-kit introspect

# 7. Review and apply generated schema
```

## References

See `references/commands.md` for complete `pscale deploy-request` command reference.
