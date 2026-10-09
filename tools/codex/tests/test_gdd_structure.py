"""Real staged-GDD checks and section schema, including misleading documents."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]
SCRATCH = ROOT / '.codex-test-tmp'
SCRATCH.mkdir(exist_ok=True)
BASE = ['Summary', 'Overview', 'Detailed Design', 'Edge Cases', 'Dependencies', 'Acceptance Criteria']
FULL = BASE + ['Player Fantasy', 'Formulas', 'Tuning Knobs']

def document(headings):
    return '# Combat\n' + ''.join(f'## {h}\nContent.\n' for h in headings)

class GDDChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=SCRATCH)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copytree(ROOT / '.claude', self.root / '.claude')
        (self.root / 'project.yaml').write_text('schema_version: 1\nmodes:\n  rigor: full\n')
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True)

    def stage(self, path, text):
        p = self.root / path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
        subprocess.run(['git', 'add', path], cwd=self.root, check=True)
        return p

    def hook(self):
        result = subprocess.run([sys.executable, str(ROOT / 'tools/codex/studio.py'), 'hook', 'PreToolUse'],
                                cwd=self.root, input=json.dumps({'tool_name':'exec_command', 'tool_input':{'cmd':'git commit -m audit'}}),
                                text=True, capture_output=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    def test_archives_reviews_and_governance_are_skipped(self):
        for path in ['design/gdd/archive/combat.md', 'design/gdd/reviews/combat-review.md', 'design/gdd/systems-index.md']:
            self.stage(path, '# Old notes\n')
        self.assertNotIn('DESIGN:', self.hook())

    def test_prose_and_fenced_headings_do_not_satisfy_sections(self):
        self.stage('design/gdd/combat.md', '# Combat\n'+' '.join(FULL)+'\n```markdown\n'+document(FULL)+'```\n')
        output = self.hook()
        self.assertIn('Summary', output)
        self.assertIn('Overview', output)

    def test_pending_add_checks_the_content_that_will_be_staged(self):
        p = self.root/'design/gdd/combat.md'
        p.parent.mkdir(parents=True); p.write_text('# Incomplete\n')
        result = subprocess.run([sys.executable, str(ROOT/'tools/codex/studio.py'), 'hook', 'PreToolUse'],
                                cwd=self.root, input=json.dumps({'tool_name':'exec_command','tool_input':{'cmd':'git add design/gdd/combat.md && git commit -m audit'}}),
                                text=True,capture_output=True,timeout=30)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertIn('missing section required at workflow=full: Overview',result.stdout)

    def test_backtick_inline_span_does_not_hide_real_headings(self):
        self.stage('design/gdd/combat.md','```inline code```\n'+document(FULL))
        self.assertNotIn('missing section', self.hook())

    def test_missing_summary_is_reported(self):
        self.stage('design/gdd/combat.md', document(FULL[1:]))
        self.assertIn('Summary', self.hook())

    def test_staged_doc_is_checked_not_unstaged_repair(self):
        p = self.stage('design/gdd/combat.md', '# Incomplete\n')
        p.write_text(document(FULL))
        self.assertIn('Overview', self.hook())

    def test_aliases_numbered_headings_and_tiers(self):
        self.stage('design/gdd/combat.md', document(['1. '+h for h in FULL]))
        self.assertNotIn('missing section', self.hook())
        (self.root / 'project.yaml').write_text('schema_version: 1\nmodes:\n  rigor: standard\n')
        self.stage('design/gdd/combat.md', document(BASE))
        self.assertNotIn('missing section', self.hook())
        (self.root / 'project.yaml').write_text('schema_version: 1\nmodes:\n  rigor: minimal\n')
        self.stage('design/gdd/combat.md', '# Optional stub\n')
        self.assertNotIn('DESIGN:', self.hook())

    def test_conditional_requirements_are_grounded_not_guessed(self):
        self.stage('design/gdd/combat.md', document(BASE))
        result = subprocess.run([sys.executable, str(self.root/'.claude/scripts/gdd-structure.py'),
                                 '--tier','standard','--category','Gameplay','--numeric-rules','yes','--has-dependencies','yes',
                                 'design/gdd/combat.md'], cwd=self.root, text=True,capture_output=True)
        self.assertEqual(result.returncode,0,result.stderr)
        missing = next(line for line in result.stdout.splitlines() if 'MISSING REQUIRED:' in line)
        for label in ['Formulas','Visual/Audio Requirements','Game Feel','Cross-References']:
            self.assertIn(label,missing)

    def test_unknown_conditions_are_reported_without_guessing(self):
        self.stage('design/gdd/combat.md', document(FULL))
        output = self.hook()
        self.assertIn('NOT ASSESSED',output)
        self.assertNotIn('missing section',output)

    def test_nested_project_reads_index_with_repository_prefix(self):
        parent = self.root
        child = parent/'games/example'
        shutil.copytree(parent/'.claude', child/'.claude')
        (child/'project.yaml').write_text('schema_version: 1\nmodes:\n  rigor: full\n')
        self.root = child
        self.stage('design/gdd/combat.md', '# Incomplete\n')
        self.assertIn('missing section required at workflow=full: Overview',self.hook())

    def test_absent_checker_cannot_silently_pass(self):
        self.stage('design/gdd/combat.md', '# Combat\n')
        checker = self.root/'.claude/scripts/gdd-structure.py'
        if checker.exists(): checker.unlink()
        self.assertIn('SKIPPED', self.hook())

if __name__ == '__main__': unittest.main()
