"""Mutation proofs for standalone gate and troubleshooting regressions."""
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import test_security_guidance as guidance
import test_preserved_content as preserved


class GuardMutationTests(unittest.TestCase):
    def test_reference_refresh_is_allowed_but_auth_prohibitions_remain(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for pattern in ('*/SKILL.md', '*/references/*.md', '**/scripts/*.sh', 'scripts/*.sh'):
                for path in guidance.ROOT.glob(pattern):
                    target = root / path.relative_to(guidance.ROOT)
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(path.read_bytes())
            reference = root / 'pscale-auth/references/commands.md'
            reference.write_text(reference.read_text() + '\nFuture verified CLI refresh.\n')
            (reference.parent / 'future-command.md').write_text('# Future command\n')
            with patch.object(preserved, 'ROOT', root):
                result = unittest.TestResult()
                unittest.defaultTestLoader.loadTestsFromTestCase(preserved.PreservedContentTests).run(result)
                self.assertTrue(result.wasSuccessful(), result.failures + result.errors)
                auth = root / 'pscale-auth/SKILL.md'
                auth.write_text(auth.read_text().replace(
                    "Do not enter a password or operate a keyring dialog on the user's behalf.", ''))
                result = unittest.TestResult()
                unittest.defaultTestLoader.loadTestsFromTestCase(preserved.PreservedContentTests).run(result)
                self.assertFalse(result.wasSuccessful(), 'Missing keyring prohibition accepted')

    def check_mutation(self, name, mutate):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for path in guidance.ROOT.glob('*/SKILL.md'):
                target = root / path.relative_to(guidance.ROOT)
                target.parent.mkdir()
                target.write_bytes(path.read_bytes())
            mutate(root)
            with patch.object(guidance, 'ROOT', root):
                result = unittest.TestResult()
                guidance.SecurityGuidanceTests(name).run(result)
            self.assertFalse(result.wasSuccessful(), 'Guard accepted mutated guidance')
            return result

    def test_nested_destructive_examples_require_organization(self):
        for group in ('backup policy', 'branch config-profile', 'branch router'):
            with self.subTest(group=group):
                def mutate(root):
                    path = root / 'new-skill/SKILL.md'
                    path.parent.mkdir()
                    path.write_text('```bash\npscale ' + group + ' delete <database> <id>\n```\n')
                result = self.check_mutation('test_destructive_examples_use_explicit_organization', mutate)
                self.assertFalse(result.errors, result.errors)
                self.assertEqual(len(result.failures), 1)
                self.assertIn("'--org' not found", result.failures[0][1])

    def test_nested_destructive_examples_require_local_gate(self):
        for group in ('backup policy', 'branch config-profile', 'branch router'):
            with self.subTest(group=group):
                def mutate(root):
                    path = root / 'new-skill/SKILL.md'
                    path.parent.mkdir()
                    path.write_text('```bash\npscale ' + group +
                                    ' delete <database> <id> --org <org>\n```\n')
                result = self.check_mutation('test_standalone_destructive_advice_has_local_safety_gates', mutate)
                self.assertFalse(result.errors, result.errors)
                self.assertEqual(len(result.failures), 1)
                self.assertIn('Missing section ## Destructive-operation safety in new-skill/SKILL.md',
                              result.failures[0][1])

    def test_gate_drift_is_rejected(self):
        def mutate(root):
            path = root / 'pscale-branch/SKILL.md'
            path.write_text(path.read_text().replace('Command examples and CLI confirmation prompts are not authorization.',
                                                     'Command examples alone are not authorization.'))
        self.check_mutation('test_standalone_destructive_advice_has_local_safety_gates', mutate)

    def test_missing_standalone_gate_is_rejected(self):
        self.check_mutation('test_standalone_destructive_advice_has_local_safety_gates',
                            lambda root: (root / 'pscale-billing/SKILL.md').unlink())

    def test_continuation_only_destructive_example_requires_gate(self):
        def mutate(root):
            path = root / 'new-skill/SKILL.md'
            path.parent.mkdir()
            path.write_text('```bash\n  pscale branch update db branch --org org \\\n    --deletion-protected=false\n```\n')
        self.check_mutation('test_standalone_destructive_advice_has_local_safety_gates', mutate)

    def test_troubleshooting_guards_reject_hidden_deletes(self):
        sections = (
            ('pscale-branch', '### Cannot delete branch', 'test_refused_branch_delete_only_inspects_target'),
            ('pscale-branch', '### "Branch already exists"', 'test_name_collision_does_not_delete_existing_branch'),
            ('pscale-database', '### Cannot create database', 'test_quota_failure_does_not_authorize_database_deletion'),
        )
        for skill, heading, check in sections:
            for command in ('  pscale branch delete db branch',
                            'echo y | pscale branch delete db branch',
                            'if pscale branch delete db branch; then :; fi',
                            'echo "$(pscale branch delete db branch)"'):
                with self.subTest(skill=skill, command=command):
                    def mutate(root):
                        path = root / skill / 'SKILL.md'
                        path.write_text(path.read_text().replace(heading + '\n',
                            heading + '\n\n```bash\n' + command + '\n```\n'))
                    self.check_mutation(check, mutate)


if __name__ == '__main__':
    unittest.main()
