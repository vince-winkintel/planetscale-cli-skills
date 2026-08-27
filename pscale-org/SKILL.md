---
name: pscale-org
description: List, show, switch, update PlanetScale organizations, and inspect or manage organization members and teams. Use when managing multiple organizations, switching between accounts, viewing organization details, changing billing email/spend alerts/IDP-managed roles, listing members, showing a member by email or user ID, updating member roles, removing members, creating/updating/deleting teams, adding/removing team members, or troubleshooting organization access. Triggers on org, organization, switch org, list orgs, org update, spend alert, billing email, IDP roles, org member, organization member, member role, remove member, org team, team member.
---

# pscale org

List, show, and switch organizations.

## Common Commands

```bash
# List all organizations
pscale org list

# Show current organization
pscale org show

# Switch organization
pscale org switch <org-name>

# List/show organization members
pscale org member list --org <org> --format json
pscale org member show <email-or-user-id> --org <org> --format json

# Update or remove a member only after explicit approval
pscale org member update <email-or-user-id> --org <org> --role member --format json
pscale org member remove <email-or-user-id> --org <org> --format json

# Update organization settings only after explicit approval
pscale org update --org <org> --billing-email billing@example.com --format json
pscale org update --org <org> --spend-alert --spend-alert-amount 2500 --format json

# Manage teams only after explicit approval for writes
pscale org team list --org <org> --format json
pscale org team show <team-id> --org <org> --format json
pscale org team create --org <org> --name <name> --description <description> --format json
pscale org team member add <team-id> <email-or-user-id> --org <org> --format json
```

## Workflows

### Switch Between Organizations

```bash
# View current org
pscale org show

# List available orgs
pscale org list

# Switch to different org
pscale org switch my-other-org

# Verify switch
pscale database list --org my-other-org
```

### Inspect organization members

`pscale org member list` is read-only and paginated. Use `--query` to filter by name or email prefix, and page through large organizations with `--page`/`--per-page`. `show`, `update`, and `remove` accept either an email address or the `USER_ID` from `list`.

```bash
pscale org member list --org <org> --page 1 --per-page 100 --format json
pscale org member list --org <org> --query <name-or-email-prefix> --format json
pscale org member show <email-or-user-id> --org <org> --format json
```

### Update or remove members

Only organization admins can update another member's role or remove someone else. Nobody can change their own role. A member can remove themselves from the organization, but the last admin cannot be removed. Assignable roles are `admin`, `member`, and `analyst`.

```bash
# Inspect the target first
pscale org member show <email-or-user-id> --org <org> --format json

# After explicit approval for the exact member and role
pscale org member update <email-or-user-id> --org <org> --role analyst --format json

# After explicit approval for the exact member and cleanup flags
pscale org member remove <email-or-user-id> --org <org> \
  --delete-passwords \
  --delete-service-tokens \
  --format json

# Verify after the write
pscale org member show <email-or-user-id> --org <org> --format json
pscale org member list --org <org> --format json
```

Treat updates and removals as external access-control writes. `--force` on remove only skips the confirmation prompt; it is not approval. Do not use `--delete-passwords` or `--delete-service-tokens` when removing yourself.

### Update organization settings

`pscale org update` sends only flags explicitly supplied. It can change billing email, IDP-managed-role behavior, and billing spend alerts. These are organization-wide settings; confirm the exact target organization and proposed diff, and obtain explicit approval before running the update.

```bash
# Optional: confirms only the locally active organization name; it does not inspect settings
pscale org show --format json

# After approval for the exact org and values
pscale org update --org <org> \
  --billing-email billing@example.com \
  --spend-alert \
  --spend-alert-amount 2500 \
  --format json

# Verification: the update's JSON response above returns the resulting settings;
# `pscale org show` only prints the locally active org name and ignores --org
```

`--spend-alert-amount` must be a valid monthly amount. Do not claim that disabling spend alerts clears the stored amount; the CLI validates contradictory combinations rather than silently dropping them.

### Manage organization teams

Team commands are organization-scoped and paginated. List and show teams before changing membership or deleting anything.

```bash
pscale org team list --org <org> --page 1 --per-page 100 --format json
pscale org team show <team-id> --org <org> --format json
pscale org team member list <team-id> --org <org> --format json

# Writes require explicit approval for the exact org, team, and user/member
pscale org team create --org <org> --name <name> --description <description> --format json
pscale org team update <team-id> --org <org> --name <new-name> --format json
pscale org team member add <team-id> <email-or-user-id> --org <org> --format json
pscale org team member remove <team-id> <email-or-user-id> --org <org> --format json
pscale org team delete <team-id> --org <org>
```

Deleting a team or removing a team member can remove access and optionally delete passwords created through the team. Avoid `--force` unless non-interactive execution was explicitly approved, and verify the team/member list afterward. Team-member JSON output omits password metadata; do not infer credential cleanup from hidden fields.

## Troubleshooting

### Cannot see expected databases

**Solution:** Check current organization

```bash
pscale org show
pscale org switch <correct-org>
```

## Related Skills

- **pscale-auth** - Authentication and account management
- **pscale-database** - Organization-scoped database operations

## References

See `references/commands.md` for complete command reference.
