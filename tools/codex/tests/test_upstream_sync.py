"""Exercise real Git histories without network access or publishing changes."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

TOOLS = Path(__file__).resolve().parents[1]
ROOT = TOOLS.parents[1]
sys.path.insert(0, str(TOOLS))
SCRATCH = ROOT / '.codex-test-tmp'
SCRATCH.mkdir(exist_ok=True)


class UpstreamTests(unittest.TestCase):
    def git(self, root, *args):
        return subprocess.run(['git', *args], cwd=root, text=True,
                              capture_output=True, check=True).stdout.strip()

    def fixture(self, root):
        from convert import generate
        self.git(root, 'init', '-q', '-b', 'main')
        self.git(root, 'config', 'user.name', 'Adaptation maintainer')
        self.git(root, 'config', 'user.email', 'maintainer@example.invalid')
        shutil.copytree(ROOT / '.claude', root / '.claude')
        (root / '.claude/docs/codex-sync-test.md').write_text('Original content\n')
        (root / '.gitignore').write_text('.codex-test-tmp/\n__pycache__/\n')
        (root / 'project.yaml').write_text('schema_version: 1\n')
        self.git(root, 'add', '.')
        self.git(root, 'commit', '-qm', 'Original framework')
        self.git(root, 'branch', 'upstream')
        generate(root)
        self.git(root, 'add', '.')
        self.git(root, 'commit', '-qm', 'Codex adaptation')

    def update_upstream(self, root, message='New upstream workflow'):
        self.git(root, 'switch', '-q', 'upstream')
        skill = root / '.claude/skills/continuous-update/SKILL.md'
        skill.parent.mkdir(exist_ok=True)
        skill.write_text('---\nname: continuous-update\ndescription: A new upstream capability.\n---\n' + message + '\n')
        self.git(root, 'add', '.')
        self.git(root, 'commit', '-qm', message, '--author', 'Original creator <creator@example.invalid>')
        tip = self.git(root, 'rev-parse', 'HEAD')
        self.git(root, 'switch', '-q', 'main')
        return tip

    def test_no_updates_does_not_create_branch_or_change_main(self):
        from upstream_sync import prepare
        with tempfile.TemporaryDirectory(dir=SCRATCH) as directory:
            root = Path(directory)
            self.fixture(root)
            before = self.git(root, 'rev-parse', 'main')
            result = prepare(root, 'upstream', 'main')
            self.assertFalse(result['changed'])
            self.assertEqual(self.git(root, 'rev-parse', 'HEAD'), before)
            self.assertEqual(self.git(root, 'branch', '--list', 'automation/upstream-sync'), '')

    def test_update_keeps_authorship_and_regenerates_new_skill_off_main(self):
        from upstream_sync import prepare
        with tempfile.TemporaryDirectory(dir=SCRATCH) as directory:
            root = Path(directory)
            self.fixture(root)
            tip = self.update_upstream(root)
            main = self.git(root, 'rev-parse', 'main')
            result = prepare(root, 'upstream', 'main')
            self.assertTrue(result['changed'])
            self.assertEqual(result['upstream_sha'], tip)
            self.assertEqual(self.git(root, 'rev-parse', 'main'), main)
            self.assertEqual(self.git(root, 'show', '-s', '--format=%an', tip), 'Original creator')
            self.git(root, 'merge-base', '--is-ancestor', tip, 'HEAD')
            self.assertTrue((root / '.agents/skills/studio-continuous-update/SKILL.md').exists())
            self.assertEqual(self.git(root, 'status', '--porcelain'), '')

    def test_existing_update_branch_advances_without_rewriting_commits(self):
        from upstream_sync import prepare
        with tempfile.TemporaryDirectory(dir=SCRATCH) as directory:
            root = Path(directory)
            self.fixture(root)
            self.update_upstream(root)
            first = prepare(root, 'upstream', 'main')
            self.git(root, 'switch', '-q', 'main')
            (root / 'credit.md').write_text('Original creator credit remains prominent.\n')
            self.git(root, 'add', 'credit.md')
            self.git(root, 'commit', '-qm', 'Maintain project credits')
            self.update_upstream(root, 'Another upstream improvement')
            second = prepare(root, 'upstream', 'main', existing_ref=first['head_sha'])
            self.assertTrue(second['changed'])
            self.git(root, 'merge-base', '--is-ancestor', first['head_sha'], 'HEAD')
            self.assertTrue((root / 'credit.md').exists())
            self.assertIn('Another upstream improvement',
                          (root / '.agents/skills/studio-continuous-update/SKILL.md').read_text())

    def test_conflict_aborts_merge_and_leaves_main_untouched(self):
        from upstream_sync import prepare
        with tempfile.TemporaryDirectory(dir=SCRATCH) as directory:
            root = Path(directory)
            self.fixture(root)
            source = root / '.claude/docs/codex-sync-test.md'
            source.write_text('Maintainer content\n')
            self.git(root, 'add', '.')
            self.git(root, 'commit', '-qm', 'Customize onboarding')
            main = self.git(root, 'rev-parse', 'main')
            self.git(root, 'switch', '-q', 'upstream')
            source.write_text('Upstream content\n')
            self.git(root, 'add', '.')
            self.git(root, 'commit', '-qm', 'Change upstream onboarding')
            self.git(root, 'switch', '-q', 'main')
            with self.assertRaisesRegex(ValueError, 'Merge conflict'):
                prepare(root, 'upstream', 'main')
            self.assertEqual(self.git(root, 'rev-parse', 'HEAD'), main)
            self.assertEqual(self.git(root, 'status', '--porcelain'), '')
            self.assertFalse((root / '.git/MERGE_HEAD').exists())

    def test_dirty_tree_is_rejected_before_any_checkout(self):
        from upstream_sync import prepare
        with tempfile.TemporaryDirectory(dir=SCRATCH) as directory:
            root = Path(directory)
            self.fixture(root)
            self.update_upstream(root)
            (root / 'personal-notes.md').write_text('Preserve this work')
            before = self.git(root, 'rev-parse', 'HEAD')
            with self.assertRaisesRegex(ValueError, 'clean working tree'):
                prepare(root, 'upstream', 'main')
            self.assertEqual(self.git(root, 'rev-parse', 'HEAD'), before)
            self.assertEqual((root / 'personal-notes.md').read_text(), 'Preserve this work')

    def test_bundle_publishes_original_commits_to_a_separate_review_branch(self):
        from upstream_sync import prepare, export_bundle, publish_branch
        with tempfile.TemporaryDirectory(dir=SCRATCH) as directory:
            workspace = Path(directory)
            root = workspace / 'prepare'
            root.mkdir()
            self.fixture(root)
            tip = self.update_upstream(root)
            main = self.git(root, 'rev-parse', 'main')
            result = prepare(root, 'upstream', 'main')
            bundle = workspace / 'proposal.bundle'
            export_bundle(root, result, bundle)
            remote = workspace / 'remote.git'
            self.git(workspace, 'init', '-q', '--bare', str(remote))
            self.git(root, 'remote', 'add', 'origin', str(remote))
            self.git(root, 'push', '-q', 'origin', 'main')
            publisher = workspace / 'publish'
            self.git(workspace, 'clone', '-q', '--no-local', '--single-branch',
                     '--branch', 'main', str(remote), str(publisher))
            publish_branch(publisher, bundle, result['branch'], result['head_sha'])
            self.assertEqual(self.git(remote, 'rev-parse', 'main'), main)
            self.assertEqual(self.git(remote, 'rev-parse', result['branch']), result['head_sha'])
            self.git(remote, 'merge-base', '--is-ancestor', tip, result['branch'])

    def test_publish_rejects_a_proposal_when_main_has_advanced(self):
        from upstream_sync import prepare, export_bundle, publish_branch
        with tempfile.TemporaryDirectory(dir=SCRATCH) as directory:
            workspace = Path(directory)
            root = workspace / 'prepare'
            root.mkdir()
            self.fixture(root)
            self.update_upstream(root)
            result = prepare(root, 'upstream', 'main')
            bundle = workspace / 'proposal.bundle'
            export_bundle(root, result, bundle)
            self.git(root, 'switch', '-q', 'main')
            (root / 'new-work.md').write_text('Keep new work on main')
            self.git(root, 'add', '.')
            self.git(root, 'commit', '-qm', 'Main advanced during preparation')
            remote = workspace / 'remote.git'
            self.git(workspace, 'init', '-q', '--bare', str(remote))
            self.git(root, 'remote', 'add', 'origin', str(remote))
            self.git(root, 'push', '-q', 'origin', 'main')
            publisher = workspace / 'publish'
            self.git(workspace, 'clone', '-q', '--no-local', '--single-branch',
                     '--branch', 'main', str(remote), str(publisher))
            with self.assertRaisesRegex(ValueError, 'main advanced'):
                publish_branch(publisher, bundle, result['branch'])
            self.assertEqual(self.git(remote, 'branch', '--list', result['branch']), '')


if __name__ == '__main__':
    unittest.main()
