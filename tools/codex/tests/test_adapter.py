"""Exercise the adapter's observable output and real validation boundaries."""
import json
import re
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import tomllib
import unittest

TOOLS = Path(__file__).resolve().parents[1]
ROOT = TOOLS.parents[1]
sys.path.insert(0, str(TOOLS))
SCRATCH = ROOT / '.codex-test-tmp'
SCRATCH.mkdir(exist_ok=True)


class ConversionTests(unittest.TestCase):
    def test_full_conversion_keeps_resources_and_runs_configuration(self):
        from convert import build_artifacts
        artifacts = build_artifacts(ROOT)
        skills = [p for p in artifacts if p.startswith('.agents/skills/studio-') and p.endswith('/SKILL.md')]
        roles = [p for p in artifacts if p.startswith('.codex/agents/')]
        self.assertEqual(len(skills), len(list((ROOT / '.claude/skills').glob('*/SKILL.md'))))
        self.assertEqual(len(roles), len(list((ROOT / '.claude/agents').glob('*.md'))))
        self.assertIn('.agents/skills/studio-setup-engine/references/7.5-scaffold.md', artifacts)
        skill = artifacts['.agents/skills/studio-dev-story/SKILL.md'].decode()
        self.assertIn('name: studio-dev-story', skill)
        self.assertNotIn('!`', skill)
        self.assertNotIn('CLAUDE_SKILL_DIR', skill)
        self.assertIn('$studio-story-done', skill)
        role = tomllib.loads(artifacts['.codex/agents/gameplay-programmer.toml'].decode())
        self.assertEqual(role['name'], 'gameplay-programmer')
        self.assertNotIn('model', role)
        self.assertIn('Data-Driven Design', role['developer_instructions'])
        command = re.search(r'```bash\n([^\n]*resolve_config[^\n]*)\n```', skill)[1]
        config = subprocess.run(['bash', '-c', command], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(config.returncode, 0, config.stderr)
        self.assertIn('minimal', config.stdout)

    def test_generation_is_repeatable_and_refuses_user_edits(self):
        from convert import generate
        with tempfile.TemporaryDirectory(dir=SCRATCH) as directory:
            root = Path(directory)
            shutil.copytree(ROOT / '.claude', root / '.claude')
            generate(root)
            first = (root / '.agents/skills/studio-start/SKILL.md').read_bytes()
            generate(root)
            self.assertEqual(first, (root / '.agents/skills/studio-start/SKILL.md').read_bytes())
            path = root / '.agents/skills/studio-start/SKILL.md'
            path.write_text('personal edits\n')
            with self.assertRaisesRegex(ValueError, 'modified'):
                generate(root)
            self.assertEqual(path.read_text(), 'personal edits\n')

    def test_check_detects_drift_and_missing_files_without_writing(self):
        from convert import generate
        with tempfile.TemporaryDirectory(dir=SCRATCH) as directory:
            root = Path(directory)
            shutil.copytree(ROOT / '.claude', root / '.claude')
            generate(root)
            path = root / '.agents/skills/studio-help/SKILL.md'
            path.unlink()
            with self.assertRaisesRegex(ValueError, 'out of date'):
                generate(root, check=True)
            self.assertFalse(path.exists())

    def test_upstream_changes_sync_and_retired_skills_stop_loading(self):
        from convert import generate
        with tempfile.TemporaryDirectory(dir=SCRATCH) as directory:
            root = Path(directory)
            shutil.copytree(ROOT / '.claude', root / '.claude')
            generate(root)
            source = root / '.claude/skills/start/SKILL.md'
            source.write_text(source.read_text() + '\nA project-specific onboarding step.\n')
            shutil.rmtree(root / '.claude/skills/help')
            generate(root)
            self.assertIn('A project-specific onboarding step.',
                          (root / '.agents/skills/studio-start/SKILL.md').read_text())
            self.assertFalse((root / '.agents/skills/studio-help/SKILL.md').exists())
            generate(root, check=True)

    def test_sync_does_not_follow_destination_symlinks(self):
        from convert import generate
        with tempfile.TemporaryDirectory(dir=SCRATCH) as directory:
            root = Path(directory)
            shutil.copytree(ROOT / '.claude', root / '.claude')
            external = root / 'preserve-my-file.md'
            external.write_text('personal content')
            target = root / '.agents/skills/studio-start/SKILL.md'
            target.parent.mkdir(parents=True)
            target.symlink_to(external)
            with self.assertRaisesRegex(ValueError, 'Symlink'):
                generate(root)
            self.assertEqual(external.read_text(), 'personal content')


class RuntimeTests(unittest.TestCase):
    def run_adapter(self, root, *args, payload=None):
        return subprocess.run([sys.executable, str(TOOLS / 'studio.py'), *args],
                              cwd=root, input=json.dumps(payload) if payload is not None else None,
                              capture_output=True, text=True)

    def fixture(self, root):
        shutil.copytree(ROOT / '.claude', root / '.claude')
        (root / 'project.yaml').write_text('schema_version: 1\n')
        subprocess.run(['git', 'init', '-q', str(root)], check=True)

    def test_invalid_asset_json_fails_explicit_validation(self):
        with tempfile.TemporaryDirectory(dir=SCRATCH) as directory:
            root = Path(directory)
            self.fixture(root)
            asset = root / 'assets/data/stats.json'
            asset.parent.mkdir(parents=True)
            asset.write_text('{broken')
            bad = self.run_adapter(root, 'validate')
            self.assertNotEqual(bad.returncode, 0)
            self.assertIn('stats.json', bad.stderr)
            asset.write_text('{"health": 10}')
            good = self.run_adapter(root, 'validate')
            self.assertEqual(good.returncode, 0, good.stderr)

    def test_patch_hook_reports_every_asset_and_handles_nested_cwd(self):
        with tempfile.TemporaryDirectory(dir=SCRATCH) as directory:
            root = Path(directory)
            self.fixture(root)
            (root / 'src').mkdir()
            asset = root / 'assets/data/stats.json'
            asset.parent.mkdir(parents=True)
            asset.write_text('{broken')
            payload = {'cwd': str(root / 'src'), 'tool_name': 'apply_patch',
                       'tool_input': {'command': '*** Begin Patch\n*** Add File: ../assets/data/stats.json\n+{broken\n*** End Patch'}}
            result = self.run_adapter(root / 'src', 'hook', 'PostToolUse', payload=payload)
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            self.assertIn('stats.json', result.stderr)
            self.assertFalse((root / 'src/production').exists())

    def test_staged_validator_reads_index_instead_of_working_tree(self):
        with tempfile.TemporaryDirectory(dir=SCRATCH) as directory:
            root = Path(directory)
            self.fixture(root)
            asset = root / 'assets/data/stats.json'
            asset.parent.mkdir(parents=True)
            asset.write_text('{broken')
            subprocess.run(['git', 'add', 'assets/data/stats.json'], cwd=root, check=True)
            asset.write_text('{"fixed_but_unstaged": true}')
            result = self.run_adapter(root, 'validate', '--staged')
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('stats.json', result.stderr)

    def test_session_hook_emits_codex_context_and_does_not_mutate(self):
        with tempfile.TemporaryDirectory(dir=SCRATCH) as directory:
            root = Path(directory)
            self.fixture(root)
            result = self.run_adapter(root, 'hook', 'SessionStart', payload={'cwd': str(root)})
            self.assertEqual(result.returncode, 0, result.stderr)
            output = json.loads(result.stdout)
            self.assertEqual(output['hookSpecificOutput']['hookEventName'], 'SessionStart')
            self.assertIn('studio-start', output['hookSpecificOutput']['additionalContext'])
            self.assertFalse((root / 'production/session-logs').exists())

    def test_pretool_hook_normalizes_cmd_and_blocks_bad_staged_json(self):
        with tempfile.TemporaryDirectory(dir=SCRATCH) as directory:
            root = Path(directory)
            self.fixture(root)
            asset = root / 'assets/data/stats.json'
            asset.parent.mkdir(parents=True)
            asset.write_text('{broken')
            subprocess.run(['git', 'add', 'assets/data/stats.json'], cwd=root, check=True)
            payload = {'cwd': str(root), 'tool_name': 'exec_command',
                       'tool_input': {'cmd': 'git commit -m "example"'}}
            result = self.run_adapter(root, 'hook', 'PreToolUse', payload=payload)
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            harmless = self.run_adapter(root, 'hook', 'PreToolUse',
                                        payload={**payload, 'tool_input': {'cmd': 'git status'}})
            self.assertEqual(harmless.returncode, 0, harmless.stderr)

    def test_doctor_distinguishes_unconfigured_from_configured_engine(self):
        from convert import generate
        with tempfile.TemporaryDirectory(dir=SCRATCH) as directory:
            root = Path(directory)
            self.fixture(root)
            generate(root)
            fresh = self.run_adapter(root, 'doctor')
            self.assertEqual(fresh.returncode, 0, fresh.stderr)
            self.assertIn('Engine is not configured', fresh.stdout)
            (root / 'project.yaml').write_text('schema_version: 1\nengine:\n  name: godot\n  version: "4.6"\n')
            configured = self.run_adapter(root, 'doctor')
            self.assertEqual(configured.returncode, 0, configured.stderr)
            self.assertIn('Configured engine: godot', configured.stdout)
            self.assertNotIn('Engine is not configured', configured.stdout)


if __name__ == '__main__':
    unittest.main()
