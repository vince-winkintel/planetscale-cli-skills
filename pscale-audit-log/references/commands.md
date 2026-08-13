# pscale audit-log

```text
Usage:
  pscale audit-log [command]

Available Commands:
  auth-attempts Download authentication-attempt export reports
  list          List all audit logs of an organization
```

## pscale audit-log auth-attempts download

```text
Usage:
  pscale audit-log auth-attempts download [flags]

Flags:
      --backend-route strings          Backend route: postgres, pgbouncer, unknown
      --branch strings                 Branch public ID or database/branch name (repeat or comma-separate)
      --end-at string                  Exclusive end: now, today, yesterday, YYYY-MM-DD, local ISO, or RFC3339; defaults to now
      --export-format string           Artifact format: jsonl, csv, parquet; defaults from --format
      --failure-reason strings         Failure reason: bad_password, unknown_user, authorization_failed, ip_not_allowed, other
      --outcome strings                Authentication outcome: allow or deny
      --output string                  Output file name, or - to write raw ZIP bytes to stdout
      --since string                   Export window ending now: positive duration such as 24h, 7d, or 2w
      --source-ip strings              Source IP address or CIDR range (repeat or comma-separate)
      --start-at string                Inclusive start: now, today, yesterday, YYYY-MM-DD, local ISO, or RFC3339
      --startup-database stringArray   Startup database name (repeatable)
      --username stringArray           Authentication username (repeatable; commas are part of the name)
```

`--since` is mutually exclusive with `--start-at`/`--end-at`; without `--since`, `--start-at` is required. The command generates the export, waits, and downloads its ZIP artifact.
