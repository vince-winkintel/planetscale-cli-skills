"""Integrity and selective-install checks; no credentials or network required."""
import os
from pathlib import Path
import re
import unittest


ROOT = Path(os.environ.get("PSCALE_SKILLS_ROOT", Path(__file__).resolve().parents[1]))


class PreservedContentTests(unittest.TestCase):
    def test_authentication_safety_contract(self):
        text = (ROOT / "pscale-auth/SKILL.md").read_text()
        for prohibition in (
            "Do not enter a password or operate a keyring dialog on the user's behalf.",
            "Do not scrape, record, or reproduce OAuth credentials from help output.",
            "do not print or store credentials",
            "Never commit tokens to skill repos or scripts.",
        ):
            self.assertIn(prohibition, text)

    def test_token_secret_delivery_is_local_and_consistent(self):
        for skill in ('pscale-service-token', 'pscale-auth', 'planetscale-cli-skills'):
            with self.subTest(skill=skill):
                text = (ROOT / skill / 'SKILL.md').read_text()
                for phrase in (
                    'user/API-token authentication',
                    'user-controlled secret-delivery mechanism',
                    'stop if none is available',
                    'Never display or store returned token values in chat, logs, evidence, temporary files, or this repository.',
                ):
                    self.assertIn(phrase, text)
                self.assertNotIn('# Returns:', text)
                self.assertNotRegex(text, r'#\s+TOKEN(?:_ID)?:')
                self.assertNotIn('export PLANETSCALE_SERVICE_TOKEN=<token>', text)
                # Every authored create/duplicate example retains an adjacent gate.
                for match in re.finditer(r'^pscale service-token (?:create|duplicate) .+$', text, re.M):
                    previous = text[:match.start()].splitlines()[-1]
                    self.assertRegex(previous, r'(?:secret-delivery mechanism|secret-safe delivery)')

    def test_logout_gates_and_nonrevocation_are_local(self):
        for skill in ('pscale-auth', 'pscale-database', 'planetscale-cli-skills'):
            with self.subTest(skill=skill):
                text = (ROOT / skill / 'SKILL.md').read_text()
                for phrase in ('explicit authorization', 'stored login', 'without',
                               'keyring', 'automatic troubleshooting probe'):
                    self.assertIn(phrase, text)
                self.assertNotIn('pscale auth logout && pscale auth login', text)
                self.assertNotIn('Logout and login with correct account', text)
        auth = (ROOT / 'pscale-auth/SKILL.md').read_text()
        self.assertIn('Obtain explicit authorization for the intended session before logout', auth)
        self.assertIn('without revoking that separate session and without the unreadable-token warning', auth)
        self.assertIn('# Confirm credential method and authorize all affected sessions', auth)
        reference = (ROOT / 'pscale-auth/references/commands.md').read_text()
        for phrase in ('After successful revocation of that explicit token, local stored-login deletion still runs',
                       'If revocation fails, local deletion does not run',
                       'there was no read error'):
            self.assertIn(phrase, reference)

    def test_effective_omission_and_upstream_help_warning(self):
        for path in ('pscale-service-token/SKILL.md', 'pscale-service-token/references/commands.md'):
            text = (ROOT / path).read_text()
            for phrase in ('PLANETSCALE_NAME', 'PLANETSCALE_TTL', 'user-config',
                           'name', 'ttl', 'PLANETSCALE_TTL=never'):
                self.assertIn(phrase, text)
        reference = (ROOT / 'pscale-service-token/references/commands.md').read_text()
        warning = reference.split('## pscale service-token delete-access --help\n', 1)[1].split('```text', 1)[0]
        self.assertIn('Known upstream help typo', warning)
        correction = 'pscale service-token delete-access <token-id> delete_databases --org <org> --database=""'
        self.assertIn(correction, warning)
        self.assertIn('`--org` alone does not clear that inherited scope', warning)
        import test_security_guidance as guidance
        self.assertIn(['service-token', 'delete-access', 'fixture-token-id',
                       'delete_databases', '--org', 'fixture-org', '--database='],
                      guidance.recorded_commands('```bash\n' + correction + '\n```'))
        # Preserve the known bad upstream example in its audited fence, not as advice.
        self.assertIn('  pscale service-token add-access <token id> delete_databases', reference)

    def test_common_token_mutation_examples_record_exact_argv(self):
        import test_security_guidance as guidance
        text = (ROOT / 'pscale-service-token/SKILL.md').read_text()
        common = text.split('## Common Commands\n', 1)[1].split('\n## ', 1)[0]
        commands = guidance.recorded_commands(common)
        self.assertIn(['service-token', 'duplicate', 'fixture-id', '--name',
                       'fixture-approved-name', '--org', 'fixture-org'], commands)
        self.assertIn(['service-token', 'update', 'fixture-id', '--name',
                       'fixture-approved-name', '--ttl', 'fixture-seconds-or-never',
                       '--org', 'fixture-org'], commands)

    def test_selective_install_script_references_resolve(self):
        for skill in ROOT.glob("*/SKILL.md"):
            for reference in re.findall(r"scripts/[a-z-]+\.sh", skill.read_text()):
                with self.subTest(skill=skill.parent.name, reference=reference):
                    local = skill.parent / reference
                    self.assertTrue(local.is_file())
                    self.assertEqual(local.read_bytes(), (ROOT / reference).read_bytes())
        self.assertFalse((ROOT / "SKILL.md").exists(), "Keep multi-skill discovery layout")

    def test_selective_install_document_references_resolve(self):
        for skill in ROOT.glob("*/SKILL.md"):
            for reference in re.findall(r"references/[a-z-]+\.md", skill.read_text()):
                with self.subTest(skill=skill.parent.name, reference=reference):
                    self.assertTrue((skill.parent / reference).is_file())


if __name__ == "__main__":
    unittest.main()
