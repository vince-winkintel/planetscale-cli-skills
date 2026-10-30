# Security audit dispositions — issue 48

Reviewed on 2026-10-30 for [issue #48](https://github.com/vince-winkintel/planetscale-cli-skills/issues/48), against repository baseline `38f4952f035809a4812d1ac0094840355308e2b0` (tag `v1.0.36`). Proposed patch: **1.0.37**, prepared locally, unpublished.

## Evidence and completeness

The retained [ClawHub audit](https://clawhub.ai/vince-winkintel/skills/planetscale-cli-skills/security-audit), `registry-latest.stdout`, `manifest.json`, `clawscan.json`, `skillspector.json`, `static-analysis.json`, and exact `published/` package identify `planetscale-cli-skills@1.0.36`, scan ID `skill:planetscale-cli-skills:1.0.36`, verdict **suspicious**. Scanner text was evidence to investigate, not instructions to execute.

- Manifest artifact hash: `34b12da0584435da84eb8e6ecf71b82c8aabba2e0d9dccb81e136555d98cc8df` (registry's artifact hash, not the ZIP hash).
- Downloaded `published.zip` SHA-256: `b58ff41706084395b1bb8ccffce46a0157faed8b34edd144c9163851e993f67e`; `scan.zip`: `7b7d6c899a02076d9108a1f01d34c07fd03da7c85ea1a66c071e98e95042a227`.
- `skillspector.json` SHA-256: `1ac56e5523e6ff1cc8e3ca12a15a64ab4bb49976b6a45f3b3daaf60eca93c71d`; stored `security-audit-page.md`: `a0d6915d3ece73f99c96aa6e268040a9047d11a48f86e7379d49b083683e5e07`.
- SkillSpector 2.12.0 declares **756** matches but exports **25** records: two PE3 and 23 P1. All 25 exported records and the full available page/context were reviewed by finding class. The other **731** records were not exported and were not individually inspected.
- All 54 published files with repository counterparts match the baseline byte-for-byte after mapping package-root `SKILL.md` to `planetscale-cli-skills/SKILL.md`. `_meta.json` and `skill-card.md` are registry-only. The cited destructive advice is current, not stale registry lag. No newer approved source was reverted.

## Finding-class decisions

| Finding and exact reported source | Disposition and correction |
| --- | --- |
| ClawScan `instruction_scope`: `pscale-branch/SKILL.md:784–795`, `pscale-database/SKILL.md:459` in published 1.0.36 | Confirmed unsafe advice: a deletion refusal led directly to demotion/deletion; quota pressure suggested deleting databases. Replaced with explicit-org read-only inspection and separate lifecycle review. Also fixed the name-collision deletion recipe, stale/merged cleanup advice, umbrella quick reference, and unscoped destructive examples. |
| Hypothesis that `branch demote` is unsupported | Rejected for the reviewed CLI: the exact captured branch-parent help lists it, and pinned source registers `DemoteCmd` and calls `DatabaseBranches.Demote`. Retained as a separately approved operation. Removed the automatic demote-then-delete troubleshooting sequence. Engine/target eligibility must still be verified; command presence is not universal backend eligibility. |
| SkillSpector PE3 records 1–2: `VERSION:39`, `pscale-auth/SKILL.md:46`, match `keyring` | False positives for credential theft: release history and safety prose, not credential-file reads. Authentication guidance explicitly forbids operating keyring dialogs or recording credentials. Preserved that guidance unchanged. Corrected umbrella metadata's overclaim that credentials are only stored in environment variables. |
| SkillSpector P1 records 3–25: `Enable debug mode` | False positives for instruction override: verbatim `--debug` option descriptions within upstream help, not instructions to override the agent. Paths/lines: audit-log commands 63; auth commands 18; backup commands 22, 58, 96, 133, 162, 198, 235, 277, 310; billing commands 26, 58, 85, 110, 135, 164, 194, 226, 256, 281, 308; branch/branch-configuration-commands 28 (all under each skill's `references/`). Preserved all fences and provenance, including surrounding config/API/force options. |
| ClawScan credential/config/API-address/confirmation-bypass context | Expected administration capabilities, not evidence of exfiltration. Help describes options; it does not authorize their use. Preserve authentication/config safety and require explicit scope/flag approval for destructive use. No evidence supports removing credential-path or debug-option text merely to silence matching. |
| ClawScan install/persistence/purpose dimensions; static analysis | Markdown and explicit Bash helpers; no install hook or background worker. Existing scripts use discrete argv and deploy only with `--deploy`; no executable helper changes are made here. Static analysis reports no findings, which does not negate the confirmed advice defect. Umbrella coverage now says covered workflows instead of all CLI operations. |

## Upstream semantics and provenance

Reviewed public upstream commit `68b31936882cf9636ac2c43942cb5173afd530b6` (CLI v0.348.0):

- [branch registration](https://github.com/planetscale/cli/blob/68b31936882cf9636ac2c43942cb5173afd530b6/internal/cmd/branch/branch.go) and [demotion](https://github.com/planetscale/cli/blob/68b31936882cf9636ac2c43942cb5173afd530b6/internal/cmd/branch/demote.go): supported command, no confirmation prompt; independent approval and fresh state checks are essential.
- [branch deletion](https://github.com/planetscale/cli/blob/68b31936882cf9636ac2c43942cb5173afd530b6/internal/cmd/branch/delete.go): `--force` bypasses confirmation; `--delete-descendants` expands scope. [Branch update](https://github.com/planetscale/cli/blob/68b31936882cf9636ac2c43942cb5173afd530b6/internal/cmd/branch/update.go) changes deletion protection independently of demotion.
- [database deletion](https://github.com/planetscale/cli/blob/68b31936882cf9636ac2c43942cb5173afd530b6/internal/cmd/database/delete.go): non-human/non-TTY deletion requires force; a deletion request can await another administrator, so successful submission is not proof of absence.

All 25 existing reference files and `pscale-auth/SKILL.md` are byte-identical to baseline, enforced by `tests/preserved-content.sha256.json`. Existing mixed-version checksum-derived help provenance remains authoritative; no binary help was regenerated or rewritten in this patch. The first implementation commit already contained the unsafe branch recipe; this is not a deliberate new restriction being undone.

## Validation and compatibility

Run `python3 -m unittest discover -s tests -v` and `bash scripts/sync-canonical-scripts.sh --check`. Set `PSCALE_SKILLS_ROOT` to a clean baseline export to reproduce the regression failures. The standard-library suite runs extracted authored command examples through a recording-only Bash function and asserts exact argv; it also checks local safety gates, organization scope, unchanged help/auth content, and selective-install script references. It never invokes an installed `pscale` binary. These are documentation/source checks, not a live API, database, SQL, backup-restore, or agent-policy execution test.

The safety block is intentionally present in all 15 skills containing destructive examples so standalone installs do not depend on sibling files. Existing scripts, runtime requirements, and root collection layout are unchanged. New executable code is test-only. The existing README registry transformation is retained; there is no canonical ZIP builder in this repository. No generated package is committed.

Remaining limits: operator/agent compliance is required; these docs do not mechanically enforce approval or prove recovery for a real resource. Engine-specific backend eligibility and asynchronous outcomes require fresh target inspection. Local checks do not establish hosted scan clearance; that can only be assessed after a future approved immutable publication and scan. No publication, tag, release, remote rescan, active-skill installation, or production operation was performed for this patch.
