List, show, switch, and update organizations; manage organization SSO, members, teams, and custom roles. The complete SSO command family is documented in [`sso-commands.md`](sso-commands.md); the custom-role and member-binding contract is in [`custom-roles.md`](custom-roles.md).

Unless a section says otherwise, help fences below are exact output from the official, checksum-verified PlanetScale CLI v0.324.0 macOS arm64 release binary after normalizing only trailing whitespace.

See [custom roles and member binding](custom-roles.md) for the current slug-based contract. The custom-role group and its list/show/create/update/delete leaves are intentionally documented there as a source-backed contract, not embedded help captures here. The release audit's complete help-capture count includes external verification evidence, not only shipped fences. Unchanged historical fences retain their original provenance and are not current command inventories.

## Self-removal resolution

**CLI v0.356.0** fixes `org member remove` (alias `rm`) so leaving the organization need not list members first. With explicit required `--org`, it calls `GET /v1/user`; an exact current-user ID or case-insensitive current-user email matches self and skips member listing. If current-user lookup fails or does not match, it falls back to the existing paginated member resolver. A membership ID is not the current-user ID and does not take this shortcut. This changes removal resolution, not list/show permissions or the minimum for the existing remove command.

Leaving is a destructive access-control write. Confirm the current identity and exact organization, remaining administration/recovery path, access/dependency impact, and obtain explicit authorization to remove that exact identity. Another member's removal requires admin rights; the last admin cannot be removed. `--delete-passwords` and `--delete-service-tokens` must not be used for self-removal; they require separately approved cleanup when removing someone else. `--force` bypasses confirmation and needs explicit advance authorization for headless use. The client forwards cleanup flags; server rejection is not permission to retry different flags.

JSON success is `result: "member removed"` with `org` and the resolved `user` ID; human output names the removed email and organization. Confirm those identifiers, then arrange independent membership read-back by an already-authorized remaining admin or approved organization UI. Losing access can prevent the departing user's own member list/show read-back. Authentication/permission failures alone do not prove removal; report verification as incomplete if independent read-back is unavailable. Do not automatically rejoin, delete credentials or retry removal.

Immutable source: [self resolver](https://github.com/planetscale/cli/blob/431a54b0fa6360d34d2e7f765d58296782b3cb39/internal/cmd/org/member.go), [remove flags, confirmation and output](https://github.com/planetscale/cli/blob/431a54b0fa6360d34d2e7f765d58296782b3cb39/internal/cmd/org/member_remove.go), [current-user endpoint](https://github.com/planetscale/cli/blob/431a54b0fa6360d34d2e7f765d58296782b3cb39/internal/planetscale/users.go), [self-removal fixture](https://github.com/planetscale/cli/blob/431a54b0fa6360d34d2e7f765d58296782b3cb39/internal/cmd/org/member_test.go). Existing help below retains its stated immutable historical provenance; this summary is source-backed, not a new binary capture.

## pscale org

Complete help from the official checksum-verified CLI v0.357.0 macOS arm64 binary; only trailing horizontal terminal padding removed.

```text
Manage organizations

Usage:
  pscale org [command]

Available Commands:
  custom-role Manage organization custom roles
  list        List the currently active organizations
  member      List, show, update, and remove organization members
  show        Display the currently active organization
  sso         Manage organization SSO
  switch      Switch the currently active organization
  team        Manage organization teams
  update      Update an organization's settings

Flags:
  -h, --help[=true|false]   help for org

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug[=true|false]        Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color[=true|false]     Disable color output
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Use "pscale org [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale org list

```text
List the currently active organizations

Usage:
  pscale org list [flags]

Aliases:
  list, ls

Flags:
  -h, --help   help for list

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale org show

```text
Display the currently active organization

Usage:
  pscale org show [flags]

Flags:
  -h, --help   help for show

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale org switch

```text
Switch the currently active organization

Usage:
  pscale org switch <organization> [flags]

Flags:
  -h, --help                 help for switch
      --save-config string   Path to store the organization. By default the configuration is deducted automatically based on where pscale is executed.

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale org member

Complete help from the official checksum-verified CLI v0.357.0 macOS arm64 binary; only trailing horizontal terminal padding removed.

```text
Manage organization members and their roles.

show, update, and remove take an email or a user id (the USER_ID column from
'org member list'). Email is usually the easiest.

Only organization admins can change another member's role or remove someone
else. Nobody can change their own role. Members can still leave the organization
themselves. A role is a built-in name (admin, member, analyst) or a custom
role slug.

Usage:
  pscale org member [command]

Available Commands:
  list        List members of an organization
  remove      Remove a member from an organization
  show        Show an organization member
  update      Update an organization member's role

Flags:
  -h, --help[=true|false]   help for member
      --org string          The organization for the current user

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug[=true|false]        Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color[=true|false]     Disable color output
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Use "pscale org member [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale org member list

```text
List members of an organization.

Results are paginated: 100 members per page by default. Use --page and
--per-page to walk organizations with more members than one page holds.

Usage:
  pscale org member list [flags]

Aliases:
  list, ls

Flags:
  -h, --help           help for list
      --page int       Page number to fetch
      --per-page int   Number of results per page (default 100)
      --query string   Filter members by name or email prefix

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale org member show

```text
Show an organization member by email or user id.

'org member list' prints both EMAIL and USER_ID.

Usage:
  pscale org member show <email|user-id> [flags]

Flags:
  -h, --help   help for show

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale org member update

Complete help from the official checksum-verified CLI v0.357.0 macOS arm64 binary; only trailing horizontal terminal padding removed.

```text
Update another member's organization role.

Identify the member by email or by the USER_ID from 'org member list'.
Only organization admins can do this. You cannot change your own role.
--role is a built-in name (admin, member, analyst) or a custom role slug.

Usage:
  pscale org member update <email|user-id> [flags]

Flags:
  -h, --help[=true|false]   help for update
      --role string         Role to assign: a built-in name (admin, member, analyst) or a custom role slug

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug[=true|false]        Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color[=true|false]     Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale org member remove

```text
Remove a member from an organization.

Identify the member by email or by the USER_ID from 'org member list'.
Removing someone else requires organization admin. You can remove yourself
(leave) without being an admin. The last admin cannot be removed.

Usage:
  pscale org member remove <email|user-id> [flags]

Aliases:
  remove, rm

Flags:
      --delete-passwords        Delete passwords created by the member. Cannot be used when removing yourself.
      --delete-service-tokens   Delete service tokens created by the member. Cannot be used when removing yourself.
      --force                   Remove the member without confirmation
  -h, --help                    help for remove

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale org update

This help fence is exact output from the official, checksum-verified PlanetScale CLI v0.328.0 macOS arm64 release binary after normalizing only trailing whitespace.

```text
Update an organization's settings

Usage:
  pscale org update [flags]

Flags:
      --billing-email string     The billing email for the organization
  -h, --help                     help for update
      --idp-managed-roles        Whether the identity provider manages organization roles through directory sync
      --idp-sso-managed-roles    Whether the identity provider manages organization roles through SSO
      --org string               The organization for the current user (required)
      --spend-alert              Enable or disable billing spend alerts
      --spend-alert-amount int   Monthly spend amount that triggers spend alerts

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale org team

All help fences in this section are exact output from the official, checksum-verified PlanetScale CLI v0.327.0 macOS arm64 release binary after normalizing only trailing whitespace.

```text
Manage organization teams

Usage:
  pscale org team [command]

Available Commands:
  create      Create an organization team
  delete      Delete an organization team
  list        List organization teams
  member      Manage organization team members
  show        Show an organization team
  update      Update an organization team

Flags:
  -h, --help         help for team
      --org string   The organization for the current user

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Use "pscale org team [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale org team list

All help fences in this section are exact output from the official, checksum-verified PlanetScale CLI v0.327.0 macOS arm64 release binary after normalizing only trailing whitespace.

```text
List organization teams.

Results are paginated: 100 teams per page by default. Use --page and
--per-page to walk organizations with more teams than one page holds.

Usage:
  pscale org team list [flags]

Aliases:
  list, ls

Flags:
  -h, --help           help for list
      --page int       Page number to fetch
      --per-page int   Number of results per page (default 100)
      --query string   Filter teams by name

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale org team show

All help fences in this section are exact output from the official, checksum-verified PlanetScale CLI v0.327.0 macOS arm64 release binary after normalizing only trailing whitespace.

```text
Show an organization team

Usage:
  pscale org team show <team-id-or-name> [flags]

Flags:
  -h, --help   help for show

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale org team create

All help fences in this section are exact output from the official, checksum-verified PlanetScale CLI v0.327.0 macOS arm64 release binary after normalizing only trailing whitespace.

```text
Create an organization team

Usage:
  pscale org team create [flags]

Flags:
      --description string   Description of the team
  -h, --help                 help for create
      --name string          Name of the team (required)

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale org team update

All help fences in this section are exact output from the official, checksum-verified PlanetScale CLI v0.327.0 macOS arm64 release binary after normalizing only trailing whitespace.

```text
Update an organization team

Usage:
  pscale org team update <team> [flags]

Flags:
      --description string   New description for the team
  -h, --help                 help for update
      --name string          New name for the team

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale org team delete

All help fences in this section are exact output from the official, checksum-verified PlanetScale CLI v0.327.0 macOS arm64 release binary after normalizing only trailing whitespace.

```text
Delete an organization team

Usage:
  pscale org team delete <team> [flags]

Aliases:
  delete, rm

Flags:
      --force   Delete the team without confirmation
  -h, --help    help for delete

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale org team member

All help fences in this section are exact output from the official, checksum-verified PlanetScale CLI v0.327.0 macOS arm64 release binary after normalizing only trailing whitespace.

```text
Manage organization team members

Usage:
  pscale org team member [command]

Available Commands:
  add         Add an organization member to a team
  list        List members of an organization team
  remove      Remove a member from an organization team

Flags:
  -h, --help   help for member

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Use "pscale org team member [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale org team member list

All help fences in this section are exact output from the official, checksum-verified PlanetScale CLI v0.327.0 macOS arm64 release binary after normalizing only trailing whitespace.

```text
List members of an organization team.

Results are paginated: 100 members per page by default. Use --page and
--per-page to walk teams with more members than one page holds.

Usage:
  pscale org team member list <team> [flags]

Aliases:
  list, ls

Flags:
  -h, --help           help for list
      --page int       Page number to fetch
      --per-page int   Number of results per page (default 100)

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale org team member add

All help fences in this section are exact output from the official, checksum-verified PlanetScale CLI v0.327.0 macOS arm64 release binary after normalizing only trailing whitespace.

```text
Add an organization member to a team

Usage:
  pscale org team member add <team> <email-or-id> [flags]

Flags:
  -h, --help   help for add

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale org team member remove

All help fences in this section are exact output from the official, checksum-verified PlanetScale CLI v0.327.0 macOS arm64 release binary after normalizing only trailing whitespace.

```text
Remove a member from an organization team

Usage:
  pscale org team member remove <team> <email-or-id> [flags]

Aliases:
  remove, rm

Flags:
      --delete-passwords   Delete passwords created through this team
      --force              Remove the team member without confirmation
  -h, --help               help for remove

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```
