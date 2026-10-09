"""Exercise engine selection through the real coherence script and CLI boundary."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / '.claude/scripts/project-coherence.sh'
SCRATCH = ROOT / '.codex-test-tmp'
SCRATCH.mkdir(exist_ok=True)


class GodotVersionProbeTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(dir=SCRATCH)
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.bin = self.root / 'bin'
        self.bin.mkdir()
        # Keep the host's Godot installation out of fallback tests.
        for command in ('dirname', 'awk', 'grep', 'head', 'tr', 'sed'):
            (self.bin / command).symlink_to(shutil.which(command))

    def executable(self, name, version, status=0):
        path = self.bin / name
        path.write_text('#!/bin/sh\n[ "$1" = "--version" ] || exit 7\n'
                        f"printf '%s\\n' '{version}'\nexit {status}\n")
        path.chmod(0o755)
        return path

    def run_check(self, command, engine_path=''):
        (self.root / 'project.yaml').write_text(
            'engine:\n  name: Godot\n  version: 4.7.2\n'
            f'  path: {engine_path}\ncommands:\n  test: {command}\n')
        result = subprocess.run(
            ['/bin/bash', str(SCRIPT)], cwd=self.root,
            env={**os.environ, 'PATH': str(self.bin),
                 'CLAUDE_PROJECT_DIR': str(self.root)},
            capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    def test_python_wrapper_uses_configured_godot(self):
        self.executable('python3', 'Python 3.14.6')
        engine = self.executable('custom-engine', '4.7.2.stable.official.abcdef')
        output = self.run_check('python3 tools/game/run_checks.py unit', engine)
        self.assertIn('[MATCH]       engine.version 4.7.2 matches the installed binary (4.7.2.stable.official.abcdef)', output)
        self.assertNotIn('Python', output)

    def test_wrapped_command_falls_back_to_godot_on_path(self):
        self.executable('python3', 'Python 3.14.6')
        self.executable('godot', '4.7.2.stable.official.abcdef')
        output = self.run_check('python3 tools/game/run_checks.py unit')
        self.assertIn('engine.version 4.7.2 matches the installed binary (4.7.2.stable.official.abcdef)', output)

    def test_direct_quoted_engine_with_spaces_keeps_real_mismatch(self):
        selected = self.executable('Godot old', '4.6.3.stable.official.abcdef')
        configured = self.executable('Godot', '4.7.2.stable.official.abcdef')
        output = self.run_check(f'"{selected}" --headless', configured)
        self.assertIn("[DIFFERS]     engine.version is '4.7.2' but the installed binary reports '4.6.3.stable.official.abcdef'", output)

    def test_wrong_program_version_cannot_count_as_godot_match(self):
        wrong = self.executable('Godot', 'Python 4.7.2')
        output = self.run_check(str(wrong), wrong)
        self.assertIn('[NOT CHECKED] declared version vs installed binary', output)
        self.assertNotIn('matches the installed binary', output)

    def test_failed_probe_cannot_count_as_godot_match(self):
        failed = self.executable('Godot', '4.7.2.stable.official.abcdef', status=1)
        output = self.run_check(str(failed), failed)
        self.assertIn('[NOT CHECKED] declared version vs installed binary', output)
        self.assertNotIn('matches the installed binary', output)

    def test_quoted_argument_is_not_executed_as_engine(self):
        self.executable('python3', 'Python 3.14.6')
        argument = self.executable('Godot argument', '4.6.3.stable.official.abcdef')
        engine = self.executable('Godot', '4.7.2.stable.official.abcdef')
        output = self.run_check(f'python3 "{argument}" unit', engine)
        self.assertIn('engine.version 4.7.2 matches the installed binary (4.7.2.stable.official.abcdef)', output)


if __name__ == '__main__':
    unittest.main()
