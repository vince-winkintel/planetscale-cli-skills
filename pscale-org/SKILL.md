---
name: pscale-org
description: List, show, switch PlanetScale organizations, and inspect or manage organization members. Use when managing multiple organizations, switching between accounts, viewing organization details, listing members, showing a member by email or user ID, updating member roles, removing members, or troubleshooting organization access. Triggers on org, organization, switch org, list orgs, org member, organization member, member role, remove member.
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
