"""Offline documentation regressions; never invoke an installed pscale binary.

PSCALE_SKILLS_ROOT can point at a clean baseline export. TMPDIR can select an
approved scratch directory. Only extracted pscale examples run, through a shell
function that records argv; placeholders receive synthetic values.
"""
import os
from pathlib import Path
import re
import shlex
import subprocess
import tempfile
import unittest


ROOT = Path(os.environ.get("PSCALE_SKILLS_ROOT", Path(__file__).resolve().parents[1]))
GATED_SKILLS = {
    "planetscale-cli-skills", "pscale-backup", "pscale-billing", "pscale-branch",
    "pscale-database", "pscale-deploy-request", "pscale-neki", "pscale-org",
    "pscale-password", "pscale-pgbouncer", "pscale-read-only-replica",
    "pscale-service-token", "pscale-sql", "pscale-traffic-control", "pscale-webhook",
}
DESTRUCTIVE_VERBS = {"delete", "remove", "demote", "kill", "kill-transaction", "close", "revert"}
# Command paths, never resource names or substrings of flag names.
NESTED_GROUPS = {
    ("billing", "payment-method"), ("branch", "connections"),
    ("branch", "query-patterns"), ("branch", "shard"),
    ("keyspace", "read-only-regions"), ("database", "read-only-regions"),
    ("org", "member"), ("org", "sso", "domain"), ("org", "team"),
    ("org", "team", "member"), ("traffic-control", "budget"),
    ("traffic-control", "rule"),
}


def destructive_commands(text):
    """Classify authored examples statically; never run whole skill documents."""
    commands = []
    for line in command_lines(text):
        # A wrapped command is still examined, then rejected if risky. This is
        # deliberately not a shell evaluator; section recording is stricter.
        tails = re.split(r"\bpscale\s+", line)[1:]
        if not tails:
            raise AssertionError(f"Non-literal example: {line}")
        for tail in tails:
            try:
                argv = shlex.split(tail, comments=True)
            except ValueError as error:
                raise AssertionError(f"Non-literal example: {line}") from error
            depth = max([1] + [len(group) for group in NESTED_GROUPS
                               if tuple(argv[:len(group)]) == group])
            risky = len(argv) > depth and argv[depth] in DESTRUCTIVE_VERBS
            risky |= any(flag in argv for flag in (
                "--deletion-protected=false", "--protected=false",
                "--auto-delete-branch", "--auto-delete-branch=true"))
            if argv and argv[0] == "sql":
                risky |= any(re.search(r"\b(?:DELETE|DROP|TRUNCATE)\b", value, re.I)
                             for value in argv)
            if risky:
                commands.append(shlex.split(literal_command(line), comments=True)[1:])
    return commands


def section(path, heading):
    text = (ROOT / path).read_text()
    match = re.search(r"^" + re.escape(heading) + r"\n(.*?)(?=^#{2,3} |\Z)",
                      text, re.M | re.S)
    if not match:
        raise AssertionError(f"Missing section {heading} in {path}")
    return match.group(1)


def command_lines(text):
    """Logical authored Bash lines mentioning pscale, including indented lines."""
    for block in re.findall(r"```bash\n(.*?)```", text, re.S):
        for line in block.replace("\\\n", " ").splitlines():
            line = line.strip()
            if not line.startswith("#") and re.search(r"\bpscale\b", line):
                yield line


def literal_command(line):
    """Accept only the bounded literal grammar exercised by this suite."""
    line = re.sub(r"<([\w-]+)>", lambda m: "fixture-" + m[1], line)
    try:
        argv = shlex.split(line, comments=True)
    except ValueError as error:
        raise AssertionError(f"Non-literal example: {line}") from error
    unquoted = re.sub(r"'[^']*'|\"(?:\\.|[^\"\\])*\"", "", line)
    if (not argv or argv[0] != "pscale" or re.search(r"[`$]", line)
            or re.search(r"[;&|<>*?\[\]{}()~]", unquoted)):
        raise AssertionError(f"Non-literal example: {line}")
    return line


def recorded_commands(text):
    """Validate the entire section before running any recording-only commands."""
    commands = [literal_command(line) for line in command_lines(text)]
    script = 'set -e\npscale() { printf "%s\\0" "$@"; printf "\\n"; }\n' + "\n".join(commands)
    with tempfile.TemporaryDirectory() as home:
        result = subprocess.run(["/bin/bash", "--noprofile", "--norc", "-c", script],
                                cwd=home, env={"PATH": "/usr/bin:/bin", "HOME": home,
                                               "TMPDIR": home}, input=b"",
                                capture_output=True, check=True)
    if result.stderr:
        raise AssertionError(result.stderr.decode())
    return [line.decode().rstrip("\0").split("\0")
            for line in result.stdout.splitlines()]


class SecurityGuidanceTests(unittest.TestCase):
    def test_disruptive_workflow_inspections_use_the_same_organization(self):
        for path, heading in (
            ("pscale-branch/SKILL.md", "### Connection inspection and safe termination"),
            ("pscale-deploy-request/SKILL.md", "### Revert Deployment"),
            ("pscale-deploy-request/SKILL.md", "### Deploy fails midway"),
        ):
            for argv in recorded_commands(section(path, heading)):
                with self.subTest(path=path, command=argv):
                    self.assertIn("--org", argv)
                    self.assertEqual(argv[argv.index("--org") + 1], "fixture-org")

    def test_cleanup_advice_requires_safety_review(self):
        for path, heading, obsolete in (
            ("pscale-service-token/SKILL.md", "## Security Best Practices", "Delete unused tokens"),
            ("pscale-service-token/SKILL.md", "### Token Rotation", "# 4. Delete old token"),
            ("pscale-password/SKILL.md", "### Local Development", "# Delete when done"),
            ("pscale-deploy-request/SKILL.md", "## Best Practices", "close stale ones"),
        ):
            with self.subTest(path=path, heading=heading):
                text = section(path, heading)
                self.assertNotIn(obsolete, text)
                self.assertIn("safety gates", text)

    def test_close_refusal_does_not_authorize_revert(self):
        text = section("pscale-deploy-request/SKILL.md", "### Cannot close deploy request")
        self.assertEqual(recorded_commands(text), [[
            "deploy-request", "show", "fixture-database", "fixture-number",
            "--org", "fixture-org", "--format", "json"]])
        self.assertIn("separate", text)
        self.assertIn("stop", text.lower())

    def test_revert_decision_requires_safety_review(self):
        text = section("pscale-deploy-request/SKILL.md", "### Should I revert?")
        self.assertNotIn("Revert immediately", text)
        self.assertIn("safety gates", text)

    def test_destructive_examples_use_explicit_organization(self):
        for path in sorted(ROOT.glob("*/SKILL.md")):
            for argv in destructive_commands(path.read_text()):
                with self.subTest(skill=path.parent.name, command=argv):
                    self.assertIn("--org", argv)
                    index = argv.index("--org")
                    self.assertLess(index + 1, len(argv))
                    self.assertFalse(argv[index + 1].startswith("--"))

    def test_database_retirement_reads_back_and_handles_pending_request(self):
        text = section("pscale-database/SKILL.md", "### Database retirement")
        self.assertEqual(recorded_commands(text), [
            ["database", "show", "fixture-database", "--org", "fixture-org", "--format", "json"],
            ["branch", "list", "fixture-database", "--org", "fixture-org", "--page", "1", "--per-page", "100", "--format", "json"],
            ["database", "delete", "fixture-database", "--org", "fixture-org"],
            ["database", "delete", "fixture-database", "--org", "fixture-org", "--force", "--format", "json"],
            ["database", "list", "--org", "fixture-org", "--page", "1", "--per-page", "100", "--format", "json"],
        ])
        for phrase in ("another database administrator", "pending", "recovery", "health", "--force"):
            self.assertIn(phrase, text)
        for phrase in ("increment --page until empty", "complete successful inventory", "every page"):
            self.assertIn(phrase, text)
        self.assertIn("up front", text.split("```bash", 1)[0])
        self.assertIn("Choose exactly one", text)

    def test_umbrella_does_not_claim_complete_cli_coverage(self):
        text = (ROOT / "planetscale-cli-skills/SKILL.md").read_text()
        self.assertNotIn("for all `pscale` operations", text)
        self.assertNotIn("Token stored in environment variable only", text)
        self.assertIn("CLI manages credential persistence", text)

    def test_standalone_destructive_advice_has_local_safety_gates(self):
        # Explicit standalone contract, plus detection of newly risky skills.
        # Compare copies to each other so coordinated future updates remain valid.
        copies = {}
        for path in sorted(ROOT.glob("*/SKILL.md")):
            text = path.read_text()
            risky = destructive_commands(text)
            if not risky and "## Destructive-operation safety\n" not in text:
                continue
            with self.subTest(skill=path.parent.name):
                gates = section(path.relative_to(ROOT), "## Destructive-operation safety")
                copies[path.parent.name] = gates
                for requirement in ("explicit approval", "organization", "database", "branch",
                                    "resource", "dependencies", "availability", "verified recovery",
                                    "read-back", "stop", "connection/transaction termination",
                                    "deploy-request closure/revert", "up front",
                                    "never add them to work around a refusal"):
                    self.assertIn(requirement, gates.lower())
        self.assertEqual(set(copies), GATED_SKILLS)
        self.assertEqual(len(set(copies.values())), 1, "Standalone safety gates drifted")

    def test_branch_cleanup_is_scoped_and_verified(self):
        text = section("pscale-branch/SKILL.md", "### Branch Cleanup")
        self.assertEqual(recorded_commands(text), [
            ["branch", "show", "fixture-database", "fixture-old-branch-name", "--org", "fixture-org", "--format", "json"],
            ["branch", "delete", "fixture-database", "fixture-old-branch-name", "--org", "fixture-org"],
            ["branch", "delete", "fixture-database", "fixture-old-branch-name", "--org", "fixture-org", "--force", "--format", "json"],
            ["branch", "list", "fixture-database", "--org", "fixture-org", "--page", "1", "--per-page", "100", "--format", "json"],
        ])
        for phrase in ("descendant", "recovery", "approval", "health", "not-found", "--force"):
            self.assertIn(phrase, text)
        self.assertIn("up front", text.split("```bash", 1)[0])
        self.assertIn("Choose exactly one", text)
        self.assertIn("every page", text)

    def test_name_collision_does_not_delete_existing_branch(self):
        text = section("pscale-branch/SKILL.md", '### "Branch already exists"')
        self.assertEqual(recorded_commands(text), [
            ["branch", "show", "fixture-database", "fixture-existing-branch", "--org", "fixture-org", "--format", "json"],
        ])
        self.assertIn("different name", text)

    def test_quota_failure_does_not_authorize_database_deletion(self):
        text = section("pscale-database/SKILL.md", "### Cannot create database")
        self.assertEqual(recorded_commands(text), [
            ["database", "list", "--org", "fixture-org", "--page", "1", "--per-page", "100", "--format", "json"],
        ])
        self.assertNotIn("or delete unused", text)
        self.assertIn("separate", text)
        self.assertIn("increment --page until empty", text)
        self.assertIn("every page", text)

    def test_refused_branch_delete_only_inspects_target(self):
        text = section("pscale-branch/SKILL.md", "### Cannot delete branch")
        self.assertEqual(recorded_commands(text), [
            ["database", "show", "fixture-database", "--org", "fixture-org", "--format", "json"],
            ["branch", "show", "fixture-database", "fixture-branch-name", "--org", "fixture-org", "--format", "json"],
        ])
        self.assertIn("stop", text.lower())


if __name__ == "__main__":
    unittest.main()
