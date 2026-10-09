"""Verify that game-craft skills ship intact and drift cannot pass synchronization."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

TOOLS = Path(__file__).resolve().parents[1]
ROOT = TOOLS.parents[1]
sys.path.insert(0, str(TOOLS))
from convert import generate


class GameCraftIntegrationTests(unittest.TestCase):
    def fixture(self, root):
        vendor = root / 'third_party/gamedev-skills'
        files = {
            'LICENSE': b'Apache License, Version 2.0\n',
            'NOTICE': b'Copyright game-craft contributors\n',
            'skills/create-game-assets/SKILL.md': (
                b'---\nname: create-game-assets\ndescription: Generate game art\n---\n'
                b'Read references/art.md; run scripts/check.py.\n'),
            'skills/create-game-assets/references/art.md': b'Preserve a coherent palette.\n',
            'skills/create-game-assets/scripts/check.py': b'print("asset check")\n',
            'skills/create-game-assets/assets/manifest.json': b'{"assets": []}\n',
        }
        for name, data in files.items():
            target = vendor / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        metadata = {
            'format_version': 1,
            'repository': 'https://github.com/gamedev-skills/awesome-gamedev-agent-skills',
            'commit': '1' * 40,
            'skills': {'create-game-assets': {
                'upstream_path': 'skills/disciplines/create-game-assets',
                'description': 'Generate game art',
            }},
            'files': {name: hashlib.sha256(data).hexdigest() for name, data in files.items()},
        }
        (vendor / 'SOURCE.json').write_text(json.dumps(metadata))
        return vendor

    def test_sync_installs_complete_portable_skill_with_license(self):
        with tempfile.TemporaryDirectory(dir=ROOT / '.codex-test-tmp') as folder:
            root = Path(folder)
            vendor = self.fixture(root)
            generate(root)
            skill = root / '.agents/skills/create-game-assets'
            self.assertTrue((skill / 'SKILL.md').is_file(), 'Native game-craft skill was omitted')
            for relative in ('SKILL.md', 'references/art.md', 'scripts/check.py', 'assets/manifest.json'):
                self.assertEqual((skill / relative).read_bytes(),
                                 (vendor / 'skills/create-game-assets' / relative).read_bytes())
            self.assertEqual((skill / 'LICENSE').read_bytes(), b'Apache License, Version 2.0\n')
            self.assertEqual((skill / 'NOTICE').read_bytes(), b'Copyright game-craft contributors\n')
            generate(root, check=True)

    def test_missing_supporting_resource_fails_before_writing(self):
        with tempfile.TemporaryDirectory(dir=ROOT / '.codex-test-tmp') as folder:
            root = Path(folder)
            vendor = self.fixture(root)
            (vendor / 'skills/create-game-assets/references/art.md').unlink()
            with self.assertRaisesRegex(ValueError, 'Missing.*art.md'):
                generate(root)
            self.assertFalse((root / '.agents').exists())

    def test_unpinned_source_edit_cannot_pass_check(self):
        with tempfile.TemporaryDirectory(dir=ROOT / '.codex-test-tmp') as folder:
            root = Path(folder)
            vendor = self.fixture(root)
            generate(root)
            target = vendor / 'skills/create-game-assets/scripts/check.py'
            target.write_text('print("changed without updating pin")\n')
            with self.assertRaisesRegex(ValueError, 'hash.*check.py'):
                generate(root, check=True)

    def test_manifest_path_cannot_escape_vendor_directory(self):
        with tempfile.TemporaryDirectory(dir=ROOT / '.codex-test-tmp') as folder:
            root = Path(folder)
            vendor = self.fixture(root)
            path = vendor / 'SOURCE.json'
            metadata = json.loads(path.read_text())
            metadata['files']['../outside.txt'] = '0' * 64
            path.write_text(json.dumps(metadata))
            with self.assertRaisesRegex(ValueError, 'Invalid.*path'):
                generate(root)


if __name__ == '__main__':
    unittest.main()
