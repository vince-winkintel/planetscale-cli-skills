---
name: planetscale-cli-skills
description: PlanetScale CLI (pscale) command reference and workflows. Use for authentication, organizations, teams, members, billing, invoices, payment methods, databases, branches, PostgreSQL point-in-time recovery, branch maintenance, extension catalogs, metrics, insights, diagnostics, SQL, deploy requests, schema migrations, keyspaces, VTGate sizing, database/deploy/tablet throttlers, aggressive cutover, Postgres switchovers, Traffic Control, PgBouncers, Postgres role connection targets, Postgres IP restrictions, read-only regions, backups, audit logs, service tokens, passwords, binary-native agent guidance, Cloudflare D1 imports, and automation. Routes to specialized pscale sub-skills. Triggers on PlanetScale CLI, pscale, pscale --skill, restore point, point-in-time recovery, PITR, pscale maintenance, maintenance window, pscale metrics, performance report, pscale insights, pscale inspect, pscale sql, pscale role get, deploy request, deploy queue, unblock deploy, aggressive cutover, branch maintenance, branch extensions, branch switchover, traffic control, force cutover, storage readiness, keyspace routing rules, database settings, database branch, VTGate resize, pgbouncer, billing, invoice, payment method, backup policy, database diagnostics, org member, org team, or pscale import d1.
requirements:
  binaries:
    - pscale
    - jq
  env_optional:
    - PLANETSCALE_SERVICE_TOKEN_ID
    - PLANETSCALE_SERVICE_TOKEN
  notes: |
    Requires PlanetScale CLI authentication via 'pscale auth login' (stores token in ~/.config/planetscale/).
    Automation scripts use jq for structure-aware parsing of pscale JSON output.
metadata:
  openclaw:
    purpose: >
      Provide command reference and automation for PlanetScale CLI (pscale) operations only.
      Scope is limited to: database and branch management, maintenance schedule inspection, dedicated PostgreSQL PgBouncers, Postgres Traffic Control, VTGate sizing, Vitess read-only-region access, billing inspection/payment-method management, deploy requests,
      non-interactive SQL queries, historical/current performance metrics, query insights, read-only diagnostics, Cloudflare D1 imports, backups, audit-log exports, passwords,
      authentication-attempt exports, service tokens, and organization management via the pscale CLI tool.
    capabilities:
      - Run pscale CLI commands to manage PlanetScale databases, branches, maintenance inspection, dedicated PgBouncers, Postgres Traffic Control, billing, deploy requests, D1 imports, non-interactive SQL queries, performance metrics, query insights, read-only diagnostics, audit-log exports, and authentication-attempt exports
      - Execute bundled automation scripts (create-branch-for-mr.sh, deploy-schema-change.sh, sync-branch-with-main.sh)
      - Read PlanetScale CLI output and help users interpret results
    install_mechanism: >
      Skill files are loaded into agent context when a matching PlanetScale/pscale task is detected.
      Automation scripts are executed directly via shell (bash). No network access beyond pscale CLI calls.
      Scripts do not use eval or dynamic code execution; all pscale arguments are passed as discrete tokens.
    requires:
      credentials:
        - name: PLANETSCALE_SERVICE_TOKEN_ID
          description: >
            PlanetScale service token ID for CI/CD authentication. Optional — interactive login
            via 'pscale auth login' can be used instead. Token stored in environment variable only;
            this skill does not read, store, or transmit credentials beyond passing them to pscale CLI.
          required: false
        - name: PLANETSCALE_SERVICE_TOKEN
          description: >
            PlanetScale service token secret for CI/CD authentication. Optional — interactive login
            via 'pscale auth login' can be used instead. Token stored in environment variable only;
            this skill does not read, store, or transmit credentials beyond passing them to pscale CLI.
          required: false
---

# PlanetScale CLI Skills

Comprehensive `pscale` command reference and workflows for managing PlanetScale databases via terminal.

## Overview

The PlanetScale CLI brings database branches, deploy requests, and schema migrations to your fingertips. This skill provides command references, automation scripts, and decision trees for all `pscale` operations.

## Configuration and credential safety

- Directory-local `.pscale.yml` files are project configuration, not trusted credential configuration. The CLI accepts only `org`, `database`, and `branch` from them and warns while ignoring keys such as API endpoints or tokens.
- Keep API URLs and credentials in the user config, environment/secret manager, or explicit approved flags. Never commit them to a repository-local config.
- `pscale api` follows cross-host redirects without forwarding authentication or caller-supplied headers. Even with this protection, pass secret-bearing headers only to an explicitly verified API host and do not expose them in logs.
- When `--format json` is active, API error codes are preserved in the top-level `code` field instead of being collapsed to `COMMAND_FAILED`. Branch automation should branch on exact codes when present; for `schema_mutation_blocked`, wait for the active vtctld mutation or deploy to finish before retrying.

## Binary-native agent bootstrap

- `pscale --skill` prints the current binary's installable `pscale-cli` skill file to stdout when no positional arguments follow it. `pscale agent-guide --skill` is equivalent.
- Both forms still emit the raw Markdown skill when `--format json` is present; redirect the output to an approved skills directory when a standalone binary-native guide is wanted.
- Validate automated bootstrap output starts with `---\nname: pscale-cli`; `pscale --skill <extra-arg>` prints root help and exits zero instead of emitting the skill.
- The binary-native guide is useful for first-party command discovery, but it does not replace this repository's specialized safety workflows, focused references, and helper scripts.
- When a command name is assembled dynamically, validate the expected JSON/resource shape as well as the exit code. A bare unrecognized root token currently prints root help and exits zero, so zero alone does not prove that a resource operation ran.

## Sub-Skills

| Command | Skill | Use When |
|---------|-------|----------|
| **auth** | `pscale-auth` | Login, logout, service tokens, authentication management |
| **branch** | `pscale-branch` | Create, restore to a PostgreSQL recovery point, rename, protect, delete, promote, diff, list, and switchover branches; inspect branch infra, manage Postgres size/replicas/parameters/maintenance/extensions, resize Vitess VTGates, manage live keyspace routing rules and tablet throttling, manage query pattern reports, manage Vitess MoveTables workflows |
| **deploy-request** | `pscale-deploy-request` | Create, review, inspect queues/operations, check storage, throttle, deploy, update auto-apply/auto-delete settings, unblock failed deploy/revert queues, force cutover, and revert schema changes |
| **database** | `pscale-database` | Create, list, show, update, delete, and dump databases; manage database-level Vitess throttler/aggressive-cutover defaults, keyspaces, PostgreSQL IP restrictions, and read-only regions |
| **maintenance** | `pscale-maintenance` | Inspect Vitess Enterprise maintenance schedules, pending versions, deadlines, and historical windows |
| **sql** | `pscale-sql` | Run non-interactive SQL queries with JSON output and ephemeral credentials |
| **metrics** | `pscale-metrics` | Query historical/current branch metrics and engine-aware grouped performance reports |
| **insights** | `pscale-insights` | Analyze production query statistics, execution samples, query tags, error details, anomaly correlations, and schema recommendations |
| **traffic-control** | `pscale-traffic-control` | Inventory and safely manage Postgres Traffic Control budgets and fingerprint/keyspace/tag rules |
| **inspect** | `pscale-inspect` | Run point-in-time, read-only MySQL/Vitess and PostgreSQL diagnostic checks |
| **import d1** | `pscale-import-d1` | Import Cloudflare D1 SQLite exports into PlanetScale Postgres |
| **backup** | `pscale-backup` | Create, list, show, restore, and delete branch backups; manage scheduled backup policies |
| **billing** | `pscale-billing` | Inspect invoices and manage organization payment methods with sensitive billing-data safeguards |
| **audit-log** | `pscale-audit-log` | List audit events and export filtered authentication attempts |
| **password** | `pscale-password` | Create, list, show, update, delete, and scope Vitess connection passwords to read-only regions |
| **pgbouncer** | `pscale-pgbouncer` | List, inspect, create, resize, cancel, and delete dedicated PostgreSQL PgBouncers |
| **org** | `pscale-org` | List, show, switch, update organizations, and inspect or manage members and teams |
| **service-token** | `pscale-service-token` | Create, show, and manage CI/CD service tokens |

## Decision Trees

### Should I use a branch or deploy request?

```
What's your goal?
├─ Experimenting with schema changes → Create branch (pscale-branch)
├─ Testing schema in isolation → Create branch (pscale-branch)
├─ Ready to deploy schema to production → Create deploy request (pscale-deploy-request)
└─ Reviewing schema changes before production → Review deploy request (pscale-deploy-request)
```

### Service token vs password?

```
What's your use case?
├─ CI/CD pipeline → Service token (pscale-service-token)
├─ Local development → Password (pscale-password)
├─ Production application → Service token (rotatable, secure)
└─ One-off admin task → Password (temporary)
```

### Direct promotion vs deploy request?

```
Production readiness?
├─ Immediate promotion (dangerous) → pscale branch promote (pscale-branch)
├─ Review + approval workflow → pscale deploy-request create (pscale-deploy-request)
└─ Safe production deployment → Always use deploy requests
```

## Common Workflows

### Schema Migration Workflow

Complete workflow from branch creation to production deployment:

```bash
# 1. Create development branch
pscale branch create <database> <branch-name>

# 2. Make schema changes (via shell, ORM, or direct SQL)
pscale shell <database> <branch-name>

# 3. View schema diff
pscale branch diff <database> <branch-name>

# 4. Create deploy request
pscale deploy-request create <database> <branch-name>

# 5. Review and deploy
pscale deploy-request deploy <database> <deploy-request-number>

# 6. Verify deployment
pscale deploy-request show <database> <deploy-request-number>
```

See `scripts/` directory for automation.

### Branch Development Workflow

```bash
# Create branch from main
pscale branch create <database> <feature-branch> --from main

# Work on schema changes
pscale shell <database> <feature-branch>

# Check diff before deploying
pscale branch diff <database> <feature-branch>

# Create deploy request when ready
pscale deploy-request create <database> <feature-branch>
```

### CI/CD Integration

```bash
# Create service token for CI/CD
pscale service-token create --org <org>

# Use in CI/CD pipelines (GitHub Actions, GitLab CI, etc.)
export PLANETSCALE_SERVICE_TOKEN_ID=<token-id>
export PLANETSCALE_SERVICE_TOKEN=<token>

# Create and deploy via CI/CD after review/approval gates pass
pscale deploy-request create <database> <branch> --format json
pscale deploy-request deploy <database> <deploy-request-number>
```

### Cloudflare D1 to PlanetScale Postgres import

```bash
# Lint and dry-run first; review the JSON migration ID and warnings
pscale import d1 lint --input ./d1-export.sql --format json
pscale import d1 start <database> <branch> --input ./d1-export.sql --dry-run --format json

# After explicit confirmation, run and verify the import
pscale import d1 start <database> <branch> --input ./d1-export.sql --migration-id <id> --format json
pscale import d1 verify <database> <branch> --migration-id <id> --input ./d1-export.sql --format json
```

## Quick Reference

### Most Common Commands

```bash
# Authentication
pscale auth login
pscale auth logout

# Branch management
pscale branch create <database> <branch> [--from <source-branch>]
pscale branch list <database>
pscale branch delete <database> <branch>
pscale branch parameters list <database> <branch> --format json
pscale branch resize status <database> <branch> --format json
pscale branch vtgate show <database> <branch> --format json
pscale branch update <database> <branch> --deletion-protected=true --format json

# Discover and use a Vitess read-only region
pscale keyspace read-only-regions <database> <branch> <keyspace> --format json
pscale keyspace read-only-regions add <database> <branch> <keyspace> <region> --cluster-size <size> --replicas <count>
pscale password create <database> <branch> <name> --read-only-region <region> --format json

# Deploy requests
pscale deploy-request create <database> <branch>
pscale deploy-request list <database>
pscale deploy-request storage-check <database> <number> --format json
pscale deploy-request operations <database> <number> --format json
pscale deploy-request deploy <database> <number>

# Dedicated PostgreSQL PgBouncers
pscale pgbouncer list <database> <branch> --format json
pscale pgbouncer show <database> <branch> <name> --format json

# Database operations
pscale database create <database> --org <org>
pscale database list
pscale database show <database> --format json
pscale database ip-restriction list <database> --format json
pscale database throttler show <database> --org <org> --format json
pscale database aggressive-cutover show <database> --org <org> --format json
pscale shell <database> <branch>

# Maintenance schedules and windows (Vitess Enterprise)
pscale maintenance list <database> --org <org> --format json
pscale maintenance windows <database> <schedule-id> --org <org> --format json

# Backup policies and authentication-attempt exports
pscale backup policy list <database> --format json
pscale audit-log auth-attempts download --org <org> --since 24h --outcome deny

# Non-interactive read query for agents/scripts
pscale sql <database> <branch> --org <org> --format json --query "SELECT 1"

# Point-in-time diagnostics, branch metrics, and query-fingerprint analysis
pscale inspect all <database> <branch> --org <org> --format json
pscale metrics report <database> <branch> --org <org> --period 1d --format json
pscale metrics show <database> <branch> --org <org> --metric queries --metric latency_p99 --period 1h --format json
pscale insights queries <database> <branch> --org <org> --sort p99Latency --period 1h --format json
pscale insights queries samples <database> <branch> <fingerprint> --org <org> --keyspace <keyspace> --format json
pscale insights tags summaries <database> <branch> --org <org> --tags app --sort totalTime --format json
pscale insights errors show <database> <branch> <full-error-fingerprint> --org <org> --format json
pscale insights anomalies show <database> <branch> <anomaly-id> --org <org> --format json
pscale insights recommendations <database> --org <org> --format json
pscale insights recommendations show <database> <number> --org <org> --format json
pscale insights queries show <database> <branch> <query-id> --org <org> --format json
pscale insights queries summary <database> <branch> <fingerprint> --org <org> --keyspace <keyspace> --format json

# Postgres Traffic Control inventory
pscale traffic-control budget list <database> <branch> --org <org> --format json

# Organization billing inspection
pscale billing invoice list --org <org> --page 1 --per-page 25 --format json
pscale billing payment-method show --org <org> --format json

# Cloudflare D1 import dry-run
pscale import d1 start <database> <branch> --input ./d1-export.sql --dry-run --format json
```

## Related Skills

- **drizzle-kit** - ORM schema management and migrations
- **gitlab-cli-skills** - GitLab MR workflow integration
- **github** - GitHub PR and CI/CD integration

## Automation Scripts

See `scripts/` directory for token-efficient automation:

- `create-branch-for-mr.sh` - Create PlanetScale branch matching your MR/PR branch name
- `deploy-schema-change.sh` - Complete schema migration workflow
- `sync-branch-with-main.sh` - Create a replacement branch from main/base for conflict resolution

Scripts execute without loading into context (~90% token savings).

## Resources

- Official docs: https://planetscale.com/docs/reference/planetscale-cli
- GitHub: https://github.com/planetscale/cli
- Community: https://github.com/planetscale/discussion
