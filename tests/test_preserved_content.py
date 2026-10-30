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
