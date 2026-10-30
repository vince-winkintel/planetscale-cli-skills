"""Exercise Git export rules on an isolated candidate tree, without commits."""
import io
import os
from pathlib import Path
import shutil
import subprocess
import tarfile
import tempfile
import unittest


ROOT = Path(os.environ.get('PSCALE_SKILLS_ROOT', Path(__file__).resolve().parents[1]))


class DistributionTests(unittest.TestCase):
    def test_archive_excludes_developer_files_and_keeps_runtime_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            checkout = root / 'candidate'
            checkout.mkdir()
            home = root / 'home'
            home.mkdir()
            env = {'PATH': '/usr/bin:/bin', 'HOME': str(home), 'TMPDIR': directory,
                   'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': os.devnull}
            # No source index changes. Include new, uncommitted candidate tests.
            for path in ROOT.iterdir():
                if path.name in ('docs', 'tests', 'scripts') or (path / 'SKILL.md').is_file():
                    shutil.copytree(path, checkout / path.name, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
                elif path.name in ('.gitattributes', 'VERSION', 'README.md', 'LICENSE'):
                    shutil.copy2(path, checkout / path.name)

            def git(*args):
                return subprocess.run(['git', *args], cwd=checkout, env=env, input=b'',
                                      capture_output=True, check=True).stdout

            git('init', '-q')
            git('add', '.')
            tree = git('write-tree').decode().strip()
            archive = git('archive', '--format=tar', tree)
            with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
                files = {m.name: tar.extractfile(m).read() for m in tar if m.isfile()}
            self.assertFalse(any(p.startswith(('docs/', 'tests/')) for p in files))
            runtime = [p for p in checkout.rglob('*') if p.is_file() and
                       (p.relative_to(checkout).parts[0].startswith(('pscale-', 'planetscale-'))
                        or (p.relative_to(checkout).parts[0] == 'scripts' and p.suffix == '.sh'))]
            for path in runtime:
                name = path.relative_to(checkout).as_posix()
                self.assertEqual(files.get(name), path.read_bytes(), name)
            self.assertEqual(files['VERSION'], (ROOT / 'VERSION').read_bytes())
            # Existing registry recipe: move the orchestrator to root, retain
            # standalone skills and canonical scripts. No merged builder exists.
            package = {p: b for p, b in files.items() if not p.startswith('planetscale-cli-skills/')}
            package['SKILL.md'] = files['planetscale-cli-skills/SKILL.md']
            skills = sorted(ROOT.glob('pscale-*/SKILL.md'))
            self.assertEqual(sum(p.endswith('/SKILL.md') for p in package), len(skills))
            for script in (ROOT / 'planetscale-cli-skills/scripts').glob('*.sh'):
                self.assertEqual(package['scripts/' + script.name], script.read_bytes())


if __name__ == '__main__':
    unittest.main()
