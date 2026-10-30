"""Exercise the test transport's boundary before it can run authored examples."""
import unittest

from test_security_guidance import destructive_commands, recorded_commands


class ExampleParserTests(unittest.TestCase):
    def test_destructive_classification_uses_commands_and_flag_values(self):
        risky = (
            'branch connections kill db branch id --query',
            'branch connections kill-transaction db branch id',
            'deploy-request close db 1', 'deploy-request revert db 1',
            'branch demote db branch', 'branch delete db branch',
            'deploy-request update db 1 --auto-delete-branch',
            'deploy-request update db 1 --auto-delete-branch=true',
            'branch update db branch --deletion-protected=false',
            'backup update db branch id --protected=false',
            'sql db branch --query "DELETE FROM sessions WHERE id = 1"',
        )
        safe = (
            'deploy-request update db 1 --auto-delete-branch=false',
            'branch show db delete', 'branch show db close',
            'branch update db branch --deletion-protected=true',
            'backup update db branch id --protected=true',
        )
        for command in risky + safe:
            with self.subTest(command=command):
                self.assertEqual(bool(destructive_commands('```bash\npscale ' + command + '\n```')),
                                 command in risky)

    def test_destructive_detection_shares_logical_lines(self):
        text = '```bash\n  pscale branch update <db> <branch> --org <org> \\\n    --deletion-protected=false\n```'
        self.assertEqual(destructive_commands(text), recorded_commands(text))

    def test_destructive_detection_rejects_wrapped_commands(self):
        for line in ('echo y | pscale branch delete db branch',
                     'if pscale deploy-request close db 1; then :; fi',
                     'echo "$(pscale branch delete db branch)"',
                     'pscale branch list db; pscale branch delete db branch',
                     'pscale branch list db | pscale branch delete db branch'):
            with self.subTest(line=line), self.assertRaisesRegex(AssertionError, 'Non-literal'):
                destructive_commands('```bash\n' + line + '\n```')

    def test_indentation_and_continuations_preserve_argv(self):
        text = '```bash\n  pscale branch update <db> <branch> --org <org> \\\n    --deletion-protected=false\n```'
        self.assertEqual(recorded_commands(text), [[
            'branch', 'update', 'fixture-db', 'fixture-branch', '--org',
            'fixture-org', '--deletion-protected=false']])

    def test_unsupported_shell_is_rejected_before_execution(self):
        for line in ('echo y | pscale branch delete db branch',
                     'if pscale branch delete db branch; then :; fi',
                     'echo "$(pscale branch delete db branch)"',
                     'pscale branch delete "$DB" branch',
                     'pscale branch delete db *',
                     'pscale branch delete db branch > output'):
            with self.subTest(line=line), self.assertRaisesRegex(AssertionError, 'Non-literal'):
                recorded_commands('```bash\n' + line + '\n```')

    def test_comments_and_help_fences_are_not_commands(self):
        self.assertEqual(recorded_commands('```text\npscale branch delete db branch\n```\n'
                                           '```bash\n # pscale branch delete db branch\n```'), [])


if __name__ == '__main__':
    unittest.main()
