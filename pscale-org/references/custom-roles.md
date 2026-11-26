# Organization custom roles and member binding

Custom-role commands and binding by custom-role slug require **CLI v0.357.0**. Existing built-in member roles retain their earlier compatibility. These organization roles are separate from database SQL roles.

Use explicit `--org` (required by this command family). `custom-roles` aliases `custom-role`; `ls` aliases `list`, and `rm` aliases `delete`.

| Command after `pscale org custom-role` | Contract |
| --- | --- |
| `list` | `--page` (default 0), `--per-page` (default 100); returns one page, not all roles |
| `show <slug>` | Exact slug comparison; scans pages of 100 starting at page 1; does not accept role ID or display name |
| `create` | Required nonempty `--name` and nonempty `--permissions`; optional `--description`; server assigns the slug from the name |
| `update <slug>` | At least one effective changed `name`, `description`, or `permissions` flag; changed fields are sent, including values preset from environment/user configuration |
| `delete <slug>` | Confirmation; `--force` skips it and is required for JSON/non-interactive execution |

`--permissions` accepts repeated or comma-separated actions and replaces the **complete permission set** when supplied. Include `show_organization`. The client does not check that action's presence or validate action names; server acceptance and authorization remain necessary. Update forwards explicitly empty name, description, or permission values rather than treating them as omission. `--description ""` requests clearing the description; an empty permission set is not a valid least-privilege shortcut. Create omits an empty description. Do not infer rename/slug stability, binding migration, or deletion cascades from client code.

Prefer JSON: list returns an array; show/create/update return the original role object (`id`, `slug`, `name`, nullable `description`, `permissions` objects with `action`, `created_at`, `updated_at`). Human/CSV columns flatten permission actions and description; human create/update print a success message with the returned slug. Delete JSON returns `result: "custom role deleted"`, `org`, and `slug`.

## Authorization and verification

The root initializer presets unset flags from nonempty `PLANETSCALE_*` environment values or trusted user configuration and marks them changed. Thus `PLANETSCALE_PERMISSIONS`, `PLANETSCALE_NAME` or `PLANETSCALE_DESCRIPTION` can add fields to a description-only argv, and configured `force` can bypass a delete confirmation. Inspect only the relevant nonsecret effective settings, including member `role`, before approving the write. Neutralize unapproved noncredential defaults with approval, considering both environment and user config; merely unsetting an environment value does not remove a config value. Do not pass an empty permission set as an omission substitute, dump credential-bearing configuration, or alter credentials. Stop if the exact effective field set cannot be established. Project-scoped config permits only org/database/branch; this does not disable trusted user-config/environment defaults.

Before create/update/delete, inspect the exact organization, role and full permissions; review existing bindings, privilege escalation/revocation, SSO/directory-managed roles, administration continuity and recovery. Obtain explicit approval for the exact operation, slug/name and complete permission diff. Create/update have no confirmation gate. Deletion and headless `--force` require explicit approval; never use force to bypass a server refusal or automatically reassign affected users.

```bash
pscale org custom-role list --org <org> --page 1 --per-page 100 --format json
pscale org custom-role show <slug> --org <org> --format json
pscale org member list --org <org> --page 1 --per-page 100 --format json
```

Page through the member inventory and compare each member's `role` with the exact custom-role slug. This is an inspection method, not a complete server dependency guarantee; the CLI has no custom-role binding-list command. Stop when dependencies or recovery cannot be established.

Binding uses `pscale org member update <email-or-user-id> --org <org> --role <slug> --format json`, only after exact member/role authorization. Built-ins remain `admin`, `member`, `analyst`. The client now accepts any nonempty role string, resolves the member and sends the slug in the shared `role` field; it does not resolve or validate the custom role first. Only org admins can change another member's role; self-role changes are prohibited. These permissions are server-enforced, not proven by parsing the flag.

After an authorized create/update, inspect the returned slug and use it for fresh `custom-role show`; compare name, description and every permission action with the approved state. After binding, use `org member show <email-or-user-id> --org <org> --format json` and compare the returned user ID and role. After deletion, expect `custom-role show <slug>` to exit nonzero with the specific diagnostic `custom role <slug> does not exist in organization <org>` after scanning successful list responses. Corroborate absence with `custom-role list --org <org> --page 1 --per-page 100 --format json`, incrementing the page until a short page (fewer than 100 roles, including an empty page) with no exact matching slug on any page. A successful `show` means the role still exists. Authentication/permission/network errors and `organization <org> does not exist` do not prove role absence. Independently verify affected members/access; do not claim effective access or server cascade behavior without authorized independent verification.

Source: [root environment/config flag initialization](https://github.com/planetscale/cli/blob/46b515a6b57b73fb73c2d45e36ede5e08e89d161/internal/cmd/root.go), [commands and validation](https://github.com/planetscale/cli/blob/46b515a6b57b73fb73c2d45e36ede5e08e89d161/internal/cmd/org/custom_role.go), [member binding](https://github.com/planetscale/cli/blob/46b515a6b57b73fb73c2d45e36ede5e08e89d161/internal/cmd/org/member_update.go), [request/output models](https://github.com/planetscale/cli/blob/46b515a6b57b73fb73c2d45e36ede5e08e89d161/internal/planetscale/organization_custom_roles.go), [slug and omission fixtures](https://github.com/planetscale/cli/blob/46b515a6b57b73fb73c2d45e36ede5e08e89d161/internal/cmd/org/custom_role_test.go). This is a source-backed contract, not evidence of live API acceptance.
