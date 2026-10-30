"""Integrity and selective-install checks; no credentials or network required."""
import hashlib
import json
import os
from pathlib import Path
import re
import unittest


ROOT = Path(os.environ.get("PSCALE_SKILLS_ROOT", Path(__file__).resolve().parents[1]))


class PreservedContentTests(unittest.TestCase):
    def test_upstream_help_and_authentication_guidance_are_unchanged(self):
        # Captured from 38f4952f035809a4812d1ac0094840355308e2b0; includes
        # provenance paragraphs as well as complete upstream help fences.
        manifest = json.loads(Path(__file__).with_name("preserved-content.sha256.json").read_text())
        self.assertEqual(set(manifest),
                         {str(p.relative_to(ROOT)) for p in ROOT.glob("*/references/*.md")}
                         | {"pscale-auth/SKILL.md"})
        for path, expected in manifest.items():
            with self.subTest(path=path):
                self.assertEqual(hashlib.sha256((ROOT / path).read_bytes()).hexdigest(), expected)

    def test_selective_install_script_references_resolve(self):
        for skill in ROOT.glob("*/SKILL.md"):
            for reference in re.findall(r"scripts/[a-z-]+\.sh", skill.read_text()):
                with self.subTest(skill=skill.parent.name, reference=reference):
                    local = skill.parent / reference
                    self.assertTrue(local.is_file())
                    self.assertEqual(local.read_bytes(), (ROOT / reference).read_bytes())
        self.assertFalse((ROOT / "SKILL.md").exists(), "Keep multi-skill discovery layout")


if __name__ == "__main__":
    unittest.main()
