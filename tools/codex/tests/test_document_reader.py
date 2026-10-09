"""Bounded reads must make all source text recoverable, including giant lines."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
ROOT = Path(__file__).resolve().parents[3]
READER = ROOT/'.claude/scripts/read-markdown.py'
SCRATCH=ROOT/'.codex-test-tmp'
class DocumentReaderTests(unittest.TestCase):
    def call(self,*args):
        result=subprocess.run([sys.executable,str(READER),*map(str,args)],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertLessEqual(len(result.stdout.encode()),8001)
        return json.loads(result.stdout)
    def test_index_pages_include_late_sections_ignore_code_fences(self):
        with tempfile.TemporaryDirectory(dir=SCRATCH) as directory:
            p=Path(directory)/'large.md'
            p.write_text('# Design\n```md\n## Fake\n```\n'+''.join(f'## Section {i}\nRule {i}.\n' for i in range(100)))
            offset=0; headings=[]
            while True:
                data=self.call('index',p,'--offset',offset,'--limit',7)
                headings.extend(data['sections'])
                if data['next_offset'] is None: break
                self.assertGreater(data['next_offset'],offset)
                offset=data['next_offset']
            self.assertIn('Section 99',[h['heading'] for h in headings])
            self.assertNotIn('Fake',[h['heading'] for h in headings])
            self.assertEqual(data['total_lines'],204)
    def test_cursor_reconstructs_every_character_without_overflow(self):
        with tempfile.TemporaryDirectory(dir=SCRATCH) as directory:
            p=Path(directory)/'long.md'
            body='# Design\n## Rules\n'+('😀"\\'*7000)+'\nLate rule.\n'
            p.write_text(body)
            start=1;column=0;chunks=[]
            for _ in range(100):
                data=self.call('read',p,'--start',start,'--column',column,'--max-lines',2,'--max-chars',8000)
                chunks.append(data['content'])
                if data['next_start'] is None: break
                self.assertNotEqual((data['next_start'],data['next_column']),(start,column))
                start,column=data['next_start'],data['next_column']
            else: self.fail('cursor never finished')
            self.assertEqual(''.join(chunks),body)
    def test_changed_document_cannot_reuse_old_inventory(self):
        with tempfile.TemporaryDirectory(dir=SCRATCH) as directory:
            p=Path(directory)/'x.md';p.write_text('# Before\n')
            snapshot=self.call('index',p)
            p.write_text('# After\n')
            result=subprocess.run([sys.executable,str(READER),'read',str(p),'--expected-sha',snapshot['sha256']],capture_output=True,text=True)
            self.assertNotEqual(result.returncode,0)
            self.assertIn('document changed',result.stderr)

    def test_backtick_inline_span_is_not_a_fence(self):
        with tempfile.TemporaryDirectory(dir=SCRATCH) as directory:
            p=Path(directory)/'x.md';p.write_text('```inline code```\n## Actual Section\nRule.\n')
            data=self.call('index',p)
            self.assertIn('Actual Section',[x['heading'] for x in data['sections']])

    def test_missing_file_and_invalid_cursor_fail_explicitly(self):
        with tempfile.TemporaryDirectory(dir=SCRATCH) as directory:
            p=Path(directory)/'x.md';p.write_text('Only line\n')
            for args in [('index',str(p)+'missing'),('read',p,'--start','20'),('read',p,'--max-lines','0')]:
                result=subprocess.run([sys.executable,str(READER),*map(str,args)],capture_output=True,text=True)
                self.assertNotEqual(result.returncode,0)
                self.assertIn('NOT ASSESSED',result.stderr)
if __name__=='__main__':unittest.main()
