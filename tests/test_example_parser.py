"""Exercise the test transport's boundary before it can run authored examples."""
import re
import unittest

from test_security_guidance import DESTRUCTIVE_VERBS, ROOT, destructive_commands, recorded_commands


class ExampleParserTests(unittest.TestCase):
    def test_documented_destructive_usage_paths_are_classified(self):
        paths = []
        for reference in sorted(ROOT.glob('*/references/*.md')):
            # Read command paths only: placeholders and optional flags in help
            # are usage notation, not executable shell examples.
            for block in re.findall(r'^Usage:[ \t]*\n((?:[ \t]+[^\n]+\n)+)',
                                    reference.read_text(), re.M):
                for line in block.splitlines():
                    words = line.split()
                    if not words or words[0] != 'pscale':
                        continue
                    path = []
                    for word in words[1:]:
                        if not re.fullmatch(r'[a-z][a-z0-9-]*', word):
                            break
                        path.append(word)
                    if path and path[-1] in DESTRUCTIVE_VERBS:
                        paths.append((reference, path))
        self.assertTrue(paths, 'No destructive Usage paths found')
        for reference, path in paths:
            with self.subTest(reference=reference.relative_to(ROOT), command=path):
                text = '```bash\npscale ' + ' '.join(path) + '\n```'
                self.assertEqual(destructive_commands(text), [path])

    def test_nested_destructive_paths_preserve_literal_boundaries(self):
        for group in ('backup policy', 'branch config-profile', 'branch router'):
            with self.subTest(group=group):
                command = 'pscale ' + group + ' delete <database> <id> --org <org>'
                text = '```bash\n  ' + command + '\n```'
                expected = [group.split() + ['delete', 'fixture-database', 'fixture-id',
                                             '--org', 'fixture-org']]
                self.assertEqual(destructive_commands(text), expected)
                self.assertEqual(recorded_commands(text), expected)
                self.assertEqual(destructive_commands(
                    '```bash\npscale ' + group + ' show db delete\n```'), [])
                for wrapped in ('echo y | ' + command,
                                'pscale branch list db; ' + command,
                                'echo "$(' + command + ')"'):
                    with self.subTest(wrapped=wrapped), self.assertRaisesRegex(AssertionError, 'Non-literal'):
                        destructive_commands('```bash\n' + wrapped + '\n```')

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
