# Insights Agent command reference

## Compatibility and source

Except for feedback (v0.356.0), the `insights agent` family and the original output contracts below require **PlanetScale CLI v0.354.0 or later**. This does not raise the minimum for existing Insights query/recommendation commands. Check installed help and organization feature availability; do not invent substitute raw APIs or enable the feature after a refusal.

Immutable source: [agent parent and number validation](https://github.com/planetscale/cli/blob/48817e75a58151e931cf7dfc792f919c837858b5/internal/cmd/insights/agent.go), [run list and filters](https://github.com/planetscale/cli/blob/48817e75a58151e931cf7dfc792f919c837858b5/internal/cmd/insights/agent_runs.go), [create](https://github.com/planetscale/cli/blob/48817e75a58151e931cf7dfc792f919c837858b5/internal/cmd/insights/agent_run_create.go), [show](https://github.com/planetscale/cli/blob/48817e75a58151e931cf7dfc792f919c837858b5/internal/cmd/insights/agent_run_show.go), [cancel](https://github.com/planetscale/cli/blob/48817e75a58151e931cf7dfc792f919c837858b5/internal/cmd/insights/agent_run_cancel.go), [schedules](https://github.com/planetscale/cli/blob/48817e75a58151e931cf7dfc792f919c837858b5/internal/cmd/insights/agent_schedules.go), [schedule update (final one-row output)](https://github.com/planetscale/cli/blob/48817e75a58151e931cf7dfc792f919c837858b5/internal/cmd/insights/agent_schedule_update.go), [JSON models and requests](https://github.com/planetscale/cli/blob/48817e75a58151e931cf7dfc792f919c837858b5/internal/planetscale/insights_agent.go), [pagination](https://github.com/planetscale/cli/blob/48817e75a58151e931cf7dfc792f919c837858b5/internal/planetscale/client.go), [fingerprint/keyspace filters](https://github.com/planetscale/cli/blob/48817e75a58151e931cf7dfc792f919c837858b5/internal/planetscale/insights_tags.go). These behavior statements come from source, not live service execution.

## Scope, options, and authorization

All operations target the explicit `--org`, database, and branch. Runs and schedules use runnable plural parents; `run` and `schedule` are aliases, not separate APIs. There is no `runs list` or `schedules list` child. Do not confuse these with root `agent-guide` or schema recommendation dismissal.

| Operation | Options / contract | Authorization |
| --- | --- | --- |
| `runs <database> <branch>` | Newest first. `--fingerprint` string, optional `--keyspace` string, `--schema-recommendation` integer, `--page` integer, `--per-page` integer (25 by default). | Read-only inventory. |
| `runs show <database> <branch> <number>` | Positive integer run number, not the opaque run `id`. No operation-specific flags. | Read-only details. |
| `runs create <database> <branch>` | One target mode: repeated/comma-separated `--fingerprint` strings plus one shared `--keyspace`, or repeated/comma-separated `--schema-recommendation` integers. Up to five targets. | Explicit approval for exact branch, targets, connected repository changes and potentially billable work. No confirmation, force, or dry-run option. |
| `runs cancel <database> <branch> <number>` | Positive run number; optional `--force` skips confirmation (false by default). Pending/running runs. | Fresh show, explicit cancellation approval, separate force approval for headless use, then read back. Does not promise rollback of repository changes. |
| `schedules <database> <branch>` | No operation-specific flags or pagination options. | Read-only inventory. |
| `schedules update <database> <branch> <run-type>` | `slow_query` or `schema_recommendation`; at least one setting below. | Explicit approval for exact schedule, ongoing cost and repository impact; read back with `schedules`. |

Run-list filters differ from creation: a keyspace without a nonempty fingerprint is rejected, but a fingerprint alone is accepted. Recommendation filtering is sent only for a positive number; zero/negative values omit that filter rather than select a recommendation. The CLI permits fingerprint and recommendation filters together for listing and forwards both; do not assume union/intersection behavior not established by the client. Empty string filters are omitted. Page defaults to 0 and is omitted from the request; positive page/per-page values are sent, nonpositive values are omitted. The default per-page is 25. No client-enforced maximum or automatic all-page aggregation is defined here. Use explicit positive pagination and interpret an empty page only within its filter/scope.

Creation requires fingerprint/keyspace flags together, requires one selector mode, and rejects mixing the two modes. The five-target contract is stated in upstream help; the command does not itself count/validate the maximum, so enforce it when preparing approved input. Resolve fingerprints/keyspaces from `insights queries <database> <branch>` and recommendation numbers from database-scoped `insights recommendations <database>`; independently confirm selected recommendations belong to/are eligible for the intended run branch. A connected repository is required. Do not treat permissive flag parsing as target eligibility.

Schedule settings:

- `--enabled=true|false` explicitly sets enabled state. Always use `--enabled=true` or `--enabled=false` with `=`. With all three required positionals supplied, `--enabled false` sets enabled to **true** and leaves `false` as an extra positional argument; the CLI accepts and ignores that extra argument, so this form can enable recurring work instead of disabling it.
- `--frequency day|week|month` sets recurrence.
- `--time HH:MM` is local time in `--time-zone <IANA-zone>` (for example `UTC` or `America/New_York`).
- `--day-of-week 0..6` selects Sunday through Saturday for weekly recurrence; explicit zero is meaningful.
- `--day-of-month 1..31` selects the monthly day; shorter months run on their last day.

The boolean parsing follows [pflag v1.1.0 boolean defaults](https://github.com/spf13/pflag/blob/v1.1.0/bool.go#L66-L70) and [long-flag parsing](https://github.com/spf13/pflag/blob/v1.1.0/flag.go#L1102-L1112). The pinned CLI uses [minimum-only required arguments](https://github.com/planetscale/cli/blob/48817e75a58151e931cf7dfc792f919c837858b5/internal/cmdutil/cmdutil.go#L127-L143) and reads only the first three positionals in [schedule update](https://github.com/planetscale/cli/blob/48817e75a58151e931cf7dfc792f919c837858b5/internal/cmd/insights/agent_schedule_update.go#L37-L51).

Only changed settings are sent as pointer fields; omission preserves existing values, including when flag help shows a false/zero default. Update creates or changes the run-type schedule. Do not infer server-side new-schedule defaults from Go flag defaults. At least one of the six settings is required; value/range/time-zone validity is left to the service beyond CLI type parsing. Confirm the whole intended schedule and read back `enabled`, recurrence, local time/time zone and `next_run_at`. Scheduled slow-query runs use queries recorded over the last 24 hours; schema-recommendation runs use the branch's open recommendations. No targets means the run is skipped. Disabling future scheduling does not cancel an active run.

## JSON, human, and CSV output

JSON run lists are arrays of full run objects, not a `{data: ...}` envelope; create/show/cancel return a single full run object. Run fields include `id`, `number`, `run_type`, `state`, `created_at`, `updated_at`, and optional `outcome`, `title`, `summary`, `failure_message`, `agent_model`, string `cost`, `html_url`, actor, schedule, repository/commit, query patterns, schema recommendations, pull request (and optional deploy request), attempt, stages, and submitted/started/finished timestamps. Optional fields may be absent; the CLI defines no exhaustive run-state/outcome enum. Inspect state and outcome together; a successful request or existing pull request does not establish successful completion, review, merge, or deployment.

Human/CSV run lists summarize NUMBER, TYPE, STATE, OUTCOME, TITLE (truncated to 80), CREATED_AT. Human show prints labeled details, target query patterns/recommendations, stages with statuses/messages, summary, and any failure or pull-request/deploy-request link. Human create prints a started message plus a follow-up show command; human cancel prints a cancellation message. CSV create/show/cancel each use a one-row run summary list, omitting rich detail available in JSON.

JSON schedule lists are arrays; schedule update returns **one object**, not an array. Fields are `id`, `run_type`, `enabled`, `frequency_unit`, `schedule_time`, `time_zone`, nullable `day_of_week`, `day_of_month`, `next_run_at`, and optional actor. Human/CSV schedules summarize TYPE, ENABLED, FREQUENCY, DAY, TIME, TIME_ZONE, NEXT_RUN_AT. DAY is a weekday name for weekly or day number for monthly schedules; next-run time may be absent/null. The final schedule-update implementation wraps its summary in a **one-row list** for human and CSV output, so CSV works; it does not alter the JSON object's shape. Human empty lists print explanatory messages; JSON list output is the decoded slice (an array when populated, possibly null if the service supplies no slice). Preserve null/absent data rather than fabricating rows or next-run times.

On not-found, inspect scope and feature availability: the database/branch or run may not exist, or Insights Agent may not be enabled for the organization. Do not enable it, start replacement work, or retry a write automatically. Treat normalized SQL, summaries, actor/repository metadata and links as potentially sensitive. Help examples below do not grant permission to execute writes.

## Completed-run feedback

`insights agent runs feedback <database> <branch> <number>` (also `agent run feedback`) requires **CLI v0.356.0 or later**; existing run/schedule commands retain v0.354.0. Supply explicit `--org` and required `--rating useful|not_useful`. The run number must be a positive integer, not its opaque ID. Optional `--reason` accepts only `wrong_diagnosis`, `fix_wont_work`, `too_risky`, `already_known`, `doesnt_fit`, or `other`; an empty reason is omitted. Reason is not required for `not_useful`, and the client does not forbid a valid reason with `useful`. Optional `--note` is documented as up to 2000 characters; the handler does not enforce that limit locally. Keep notes within the limit and free of secrets or unnecessary private SQL/repository details.

This is a feedback write for a completed run: it sends PUT to the scoped run's `/feedback` endpoint and replaces the caller's previous feedback on repeated rating. There is no confirmation, force, or dry-run option. Inspect the exact run with `runs show`, confirm completion and the intended organization/database/branch/run number, and obtain explicit approval for the rating, reason, note, and replacement of any earlier feedback. A request to review a run is not permission to rate it. Do not invoke feedback as a probe or retry automatically after an ambiguous response.

JSON returns one feedback object with `rating`, `reason`, `note`, `created_at`, and `updated_at`; human output confirms the returned rating; CSV uses a one-row feedback list. Check the response against the approved values and inspect the saved feedback on the run's dashboard page for read-back. `runs show` returns a run model without feedback fields in this version: it can confirm run identity/state, but cannot independently verify saved feedback. If dashboard read-back is unavailable, report that verification is incomplete rather than resubmitting.

Immutable source: [flags, validation and output](https://github.com/planetscale/cli/blob/431a54b0fa6360d34d2e7f765d58296782b3cb39/internal/cmd/insights/agent_run_feedback.go), [number validation](https://github.com/planetscale/cli/blob/431a54b0fa6360d34d2e7f765d58296782b3cb39/internal/cmd/insights/agent.go), [PUT and feedback/run models](https://github.com/planetscale/cli/blob/431a54b0fa6360d34d2e7f765d58296782b3cb39/internal/planetscale/insights_agent.go), [request fixture](https://github.com/planetscale/cli/blob/431a54b0fa6360d34d2e7f765d58296782b3cb39/internal/planetscale/insights_agent_test.go). This is source-backed guidance, not a live service result or a new binary capture.

## Capture provenance

Complete help fences below were captured by the parent from the official checksum-verified PlanetScale CLI v0.354.0 macOS arm64 binary, with fresh credential-free HOME/XDG/config/cwd and network denied. Archive SHA-256: `ef619110dec4d7714b2d858a708d15146027a7455a169b4c9d7dee48d08d5f85`; binary SHA-256: `860140c902d3bc6e5674f42db9242cb98560c3d6809214a738fe6f1e7d1907ab`. Only trailing horizontal terminal padding is removed. Singular `run`/`schedule` aliases and their children were also captured and compared.

The following fences retain their immutable v0.354.0 provenance. In particular, the historical `runs` parent inventory predates `feedback`; use the source-backed feedback section above for current behavior. No v0.356.0 help equality is claimed.

## pscale insights agent --help

```text
The Insights Agent reviews slow queries or implements schema recommendations
against the repository connected to a database, and opens a pull request with
the changes it makes.

Runs belong to a branch. Each run reviews up to five slow query patterns or
implements up to five schema recommendations from that branch.

Usage:
  pscale insights agent [command]

Available Commands:
  runs        List Insights Agent runs on a branch, newest first
  schedules   List the Insights Agent schedules on a branch

Flags:
  -h, --help[=true|false]   help for agent

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

Use "pscale insights agent [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale insights agent runs --help

```text
List Insights Agent runs on a branch, newest first

Usage:
  pscale insights agent runs <database> <branch> [flags]
  pscale insights agent runs [command]

Aliases:
  runs, run

Examples:
  pscale insights agent runs mydb main --org myorg
  pscale insights agent runs mydb main --org myorg --fingerprint 59801dae501c --keyspace mydb
  pscale insights agent runs mydb main --org myorg --schema-recommendation 3

Available Commands:
  cancel      Cancel a pending or running Insights Agent run
  create      Start an Insights Agent run that reviews slow queries or implements schema recommendations
  show        Show an Insights Agent run, its stages, and the pull request it opened

Flags:
      --fingerprint string          Only list runs that reviewed the slow query with this fingerprint
  -h, --help[=true|false]           help for runs
      --keyspace string             Keyspace of the --fingerprint query
      --page int                    Page number to fetch
      --per-page int                Number of results per page (default 25)
      --schema-recommendation int   Only list runs that implemented the schema recommendation with this number

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

Use "pscale insights agent runs [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale insights agent runs create --help

```text
Start an Insights Agent run on a branch. The database needs a connected
repository, and the agent opens a pull request against it with the changes it
makes.

Pass up to five slow query fingerprints with --fingerprint and their --keyspace
to review slow queries, or up to five schema recommendation numbers with
--schema-recommendation to implement them. Find fingerprints with
"pscale insights queries" and recommendation numbers with
"pscale insights recommendations".

Usage:
  pscale insights agent runs create <database> <branch> [flags]

Examples:
  pscale insights agent runs create mydb main --org myorg --fingerprint 59801dae501c --keyspace mydb
  pscale insights agent runs create mydb main --org myorg --schema-recommendation 3,4

Flags:
      --fingerprint strings          Fingerprint of a slow query to review (repeat or comma-separate)
  -h, --help[=true|false]            help for create
      --keyspace string              Keyspace of the --fingerprint queries
      --schema-recommendation ints   Number of a schema recommendation to implement (repeat or comma-separate)

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

## pscale insights agent runs show --help

```text
Show an Insights Agent run, its stages, and the pull request it opened

Usage:
  pscale insights agent runs show <database> <branch> <number> [flags]

Examples:
  pscale insights agent runs show mydb main 12 --org myorg
  pscale insights agent runs show mydb main 12 --org myorg --format json

Flags:
  -h, --help[=true|false]   help for show

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

## pscale insights agent runs cancel --help

```text
Cancel a pending or running Insights Agent run

Usage:
  pscale insights agent runs cancel <database> <branch> <number> [flags]

Examples:
  pscale insights agent runs cancel mydb main 12 --org myorg --force

Flags:
      --force[=true|false]   Cancel without confirmation
  -h, --help[=true|false]    help for cancel

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

## pscale insights agent schedules --help

```text
List the Insights Agent schedules on a branch

Usage:
  pscale insights agent schedules <database> <branch> [flags]
  pscale insights agent schedules [command]

Aliases:
  schedules, schedule

Examples:
  pscale insights agent schedules mydb main --org myorg

Available Commands:
  update      Turn on, turn off, or change the schedule for a run type

Flags:
  -h, --help[=true|false]   help for schedules

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

Use "pscale insights agent schedules [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale insights agent schedules update --help

```text
Turn on, turn off, or change when the Insights Agent runs on its own for one
run type on a branch. <run-type> is slow_query or schema_recommendation.

Scheduled runs choose their own targets: slow query runs look at the queries
Insights recorded in the last 24 hours, and schema recommendation runs work on
the branch's open recommendations. A run with nothing to work on is skipped.

Flags that are not passed keep their current value.

Usage:
  pscale insights agent schedules update <database> <branch> <run-type> [flags]

Examples:
  pscale insights agent schedules update mydb main slow_query --org myorg --enabled --frequency week --day-of-week 1 --time 03:00 --time-zone America/New_York
  pscale insights agent schedules update mydb main schema_recommendation --org myorg --enabled=false

Flags:
      --day-of-month int       The day of the month for monthly schedules, from 1 to 31. Shorter months run on their last day.
      --day-of-week int        The day of the week for weekly schedules, from 0 (Sunday) to 6 (Saturday)
      --enabled[=true|false]   Whether the schedule runs
      --frequency string       How often the schedule runs: day, week, or month
  -h, --help[=true|false]      help for update
      --time string            The local time of day to run, in HH:MM format
      --time-zone string       The IANA time zone for --time, such as America/New_York

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
