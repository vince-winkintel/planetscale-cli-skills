"""Offline documentation regressions; never invoke an installed pscale binary.

PSCALE_SKILLS_ROOT can point at a clean baseline export. TMPDIR can select an
approved scratch directory. Only extracted pscale examples run, through a shell
function that records argv; placeholders receive synthetic values.
"""
import os
from pathlib import Path
import re
import subprocess
import unittest


ROOT = Path(os.environ.get("PSCALE_SKILLS_ROOT", Path(__file__).resolve().parents[1]))
DESTRUCTIVE = re.compile(
    r"^pscale .*(?:\b(?:delete|remove|demote|drop|truncate)\b|--(?:deletion-)?protected=false)",
    re.I | re.M,
)


def section(path, heading):
    text = (ROOT / path).read_text()
    match = re.search(r"^" + re.escape(heading) + r"\n(.*?)(?=^#{2,3} |\Z)",
                      text, re.M | re.S)
    if not match:
        raise AssertionError(f"Missing section {heading} in {path}")
    return match.group(1)


def recorded_commands(text):
    """Run authored CLI lines in Bash with a recording-only transport function."""
    commands = []
    for block in re.findall(r"```bash\n(.*?)```", text, re.S):
        for line in block.replace("\\\n", " ").splitlines():
            if line.startswith("pscale "):
                line = re.sub(r"<([^>]+)>", lambda m: "fixture-" + m[1], line)
                # This suite only accepts literal argv examples, not shell effects.
                if re.search(r"[;&|`$<>]", line):
                    raise AssertionError(f"Non-literal example: {line}")
                commands.append(line)
    script = 'pscale() { printf "%s\\0" "$@"; printf "\\n"; }\n' + "\n".join(commands)
    result = subprocess.run(["/bin/bash", "--noprofile", "--norc", "-c", script],
                            env={"PATH": "/usr/bin:/bin"}, capture_output=True, check=True)
    return [line.decode().rstrip("\0").split("\0")
            for line in result.stdout.splitlines()]


class SecurityGuidanceTests(unittest.TestCase):
    def test_destructive_examples_use_explicit_organization(self):
        for path in sorted(ROOT.glob("*/SKILL.md")):
            for line in path.read_text().replace("\\\n", " ").splitlines():
                if DESTRUCTIVE.search(line):
                    with self.subTest(skill=path.parent.name, command=line):
                        self.assertIn("--org ", line)

    def test_database_retirement_reads_back_and_handles_pending_request(self):
        text = section("pscale-database/SKILL.md", "### Database retirement")
        self.assertEqual(recorded_commands(text), [
            ["database", "show", "fixture-database", "--org", "fixture-org", "--format", "json"],
            ["branch", "list", "fixture-database", "--org", "fixture-org", "--page", "1", "--per-page", "100", "--format", "json"],
            ["database", "delete", "fixture-database", "--org", "fixture-org"],
            ["database", "list", "--org", "fixture-org", "--format", "json"],
        ])
        for phrase in ("another database administrator", "pending", "recovery", "health", "--force"):
            self.assertIn(phrase, text)

    def test_umbrella_does_not_claim_complete_cli_coverage(self):
        text = (ROOT / "planetscale-cli-skills/SKILL.md").read_text()
        self.assertNotIn("for all `pscale` operations", text)
        self.assertNotIn("Token stored in environment variable only", text)
        self.assertIn("CLI manages credential persistence", text)

    def test_standalone_destructive_advice_has_local_safety_gates(self):
        # Select by executable examples, including mirrors; no dependency on an
        # umbrella skill that a selective installation may not contain.
        count = 0
        for path in sorted(ROOT.glob("*/SKILL.md")):
            text = path.read_text()
            if not DESTRUCTIVE.search(text):
                continue
            count += 1
            with self.subTest(skill=path.parent.name):
                gates = section(path.relative_to(ROOT), "## Destructive-operation safety")
                for requirement in ("explicit approval", "organization", "database", "branch",
                                    "resource", "dependencies", "availability", "verified recovery",
                                    "read-back", "stop"):
                    self.assertIn(requirement, gates.lower())
        self.assertGreaterEqual(count, 10)

    def test_branch_cleanup_is_scoped_and_verified(self):
        text = section("pscale-branch/SKILL.md", "### Branch Cleanup")
        self.assertEqual(recorded_commands(text), [
            ["branch", "show", "fixture-database", "fixture-old-branch-name", "--org", "fixture-org", "--format", "json"],
            ["branch", "delete", "fixture-database", "fixture-old-branch-name", "--org", "fixture-org"],
            ["branch", "list", "fixture-database", "--org", "fixture-org", "--page", "1", "--per-page", "100", "--format", "json"],
        ])
        for phrase in ("descendant", "recovery", "approval", "health", "not-found", "--force"):
            self.assertIn(phrase, text)

    def test_name_collision_does_not_delete_existing_branch(self):
        text = section("pscale-branch/SKILL.md", '### "Branch already exists"')
        self.assertEqual(recorded_commands(text), [
            ["branch", "show", "fixture-database", "fixture-existing-branch", "--org", "fixture-org", "--format", "json"],
        ])
        self.assertIn("different name", text)

    def test_quota_failure_does_not_authorize_database_deletion(self):
        text = section("pscale-database/SKILL.md", "### Cannot create database")
        self.assertEqual(recorded_commands(text), [
            ["database", "list", "--org", "fixture-org", "--format", "json"],
        ])
        self.assertNotIn("or delete unused", text)
        self.assertIn("separate", text)

    def test_refused_branch_delete_only_inspects_target(self):
        text = section("pscale-branch/SKILL.md", "### Cannot delete branch")
        self.assertEqual(recorded_commands(text), [
            ["database", "show", "fixture-database", "--org", "fixture-org", "--format", "json"],
            ["branch", "show", "fixture-database", "fixture-branch-name", "--org", "fixture-org", "--format", "json"],
        ])
        self.assertIn("stop", text.lower())


if __name__ == "__main__":
    unittest.main()
