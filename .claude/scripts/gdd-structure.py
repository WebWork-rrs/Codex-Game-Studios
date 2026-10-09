#!/usr/bin/env python3
"""Shared GDD heading schema: presence, tier rules, and advisory staged checks."""
import argparse
from pathlib import Path
import re
import subprocess
import sys

# Conditional judgments are supplied by design review, not inferred from prose.
SECTIONS = {
    'Summary': ('Summary',), 'Overview': ('Overview',),
    'Player Fantasy': ('Player Fantasy',),
    'Detailed Rules': ('Detailed Rules', 'Detailed Design'),
    'Formulas': ('Formulas',), 'Edge Cases': ('Edge Cases',),
    'Dependencies': ('Dependencies',), 'Tuning Knobs': ('Tuning Knobs',),
    'Acceptance Criteria': ('Acceptance Criteria',),
    'Visual/Audio Requirements': ('Visual/Audio Requirements', 'Visual/Audio'),
    'Game Feel': ('Game Feel',), 'UI Requirements': ('UI Requirements',),
    'Cross-References': ('Cross-References',), 'Open Questions': ('Open Questions',),
}
BASE = {'Summary','Overview','Detailed Rules','Edge Cases','Dependencies','Acceptance Criteria'}
CATEGORIES = ('Core','Gameplay','Progression','Economy','Persistence','UI','Audio','Narrative','Meta')
GOVERNANCE = {'game-concept.md','systems-index.md','game-pillars.md','gameplay-tags.md',
              'fixture-swap-ledger.md','entity-registry.md','sound-bible.md'}

def is_system(path):
    p = Path(path)
    return p.parent == Path('design/gdd') and p.suffix == '.md' and p.name not in GOVERNANCE and not p.name.startswith('gdd-cross-review-')

def headings(body):
    fence = None
    for line in body.splitlines():
        m = re.match(r'^ {0,3}(`{3,}|~{3,})(.*)$', line)
        if m:
            token, rest = m.groups()
            if fence is None:
                if token[0] == '`' and '`' in rest: continue
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence) and not rest.strip():
                fence = None
            continue
        if fence is not None: continue
        m = re.match(r'^ {0,3}#{2,6}[ \t]+(.+?)\s*$', line)
        if m:
            name = re.sub(r'[ \t]+#+[ \t]*$', '', m[1])
            name = re.sub(r'^\d+[.)]?[ \t]+', '', name)
            yield name.casefold()

def present_sections(body):
    names = set(headings(body))
    return {label for label, aliases in SECTIONS.items() if any(alias.casefold() in names for alias in aliases)}

def requirements(tier, category=None, numeric='unknown', dependencies='unknown', tuning=False):
    required = set(BASE)
    unknown = []
    if tier == 'full': required.update(('Player Fantasy','Formulas','Tuning Knobs'))
    if tuning: required.add('Tuning Knobs')
    if tier != 'minimal':
        if category is None: unknown.append('category-dependent Visual/Audio and Game Feel')
        else:
            if category in ('Gameplay','UI','Narrative','Audio'): required.add('Visual/Audio Requirements')
            if category in ('Gameplay','UI'): required.add('Game Feel')
        if tier == 'standard':
            if numeric == 'yes': required.add('Formulas')
            elif numeric == 'unknown': unknown.append('numeric-rule Formulas')
        if dependencies == 'yes': required.add('Cross-References')
        elif dependencies == 'unknown': unknown.append('dependency Cross-References')
    return required, unknown

def inspect(path, args):
    if args.commit and not is_system(path): return
    if args.commit and args.tier == 'minimal': return  # GDD optional; brief is required instead.
    if args.commit and path not in args.working_tree_paths.splitlines():
        prefix = subprocess.run(['git','rev-parse','--show-prefix'],
                                capture_output=True,text=True,check=True).stdout.strip()
        data = subprocess.run(['git','show',':'+prefix+path],capture_output=True,check=True).stdout
        body = data.decode('utf-8')
    else: body = Path(path).read_text(encoding='utf-8')
    present = present_sections(body)
    if not args.commit:
        print(f'{path} PRESENT: '+','.join(label for label in SECTIONS if label in present))
        absent = [label for label in SECTIONS if label not in present]
        if absent: print(f'{path} ABSENT: '+','.join(absent))
    if args.tier:
        required, unknown = requirements(args.tier,args.category,args.numeric_rules,args.has_dependencies,args.tuning_knobs)
        missing = [label for label in SECTIONS if label in required and label not in present]
        if args.commit:
            for label in missing: print(f'DESIGN: {path} missing section required at workflow={args.tier}: {label}')
        else:
            print(f'{path} REQUIRED: '+','.join(label for label in SECTIONS if label in required))
            if missing: print(f'{path} MISSING REQUIRED: '+','.join(missing))
        if unknown:
            print(f'NOT ASSESSED: {path} conditional requirements ({"; ".join(unknown)}). '
                  'Design review must classify these from the design; heading presence is not completeness.')

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('paths',nargs='*')
    parser.add_argument('--tier',choices=('minimal','standard','full'))
    parser.add_argument('--category',choices=CATEGORIES)
    parser.add_argument('--numeric-rules',choices=('yes','no','unknown'),default='unknown')
    parser.add_argument('--has-dependencies',choices=('yes','no','unknown'),default='unknown')
    parser.add_argument('--tuning-knobs',action='store_true')
    parser.add_argument('--commit',action='store_true',help='Check active GDDs from the Git index; paths from stdin.')
    parser.add_argument('--working-tree-paths',default='',help='Newline-separated paths explicitly included by pending add/commit commands.')
    args = parser.parse_args()
    try:
        if args.commit:
            paths = [p for p in sys.stdin.read().splitlines() if p]
            if not args.tier: raise ValueError('--commit requires --tier')
        else:
            paths = args.paths or [str(p) for p in sorted(Path('design/gdd').glob('*.md')) if is_system(str(p))]
            if not paths: print('No system GDDs found in design/gdd/.')
        for path in paths: inspect(path,args)
    except (OSError,ValueError,UnicodeError,subprocess.CalledProcessError) as error:
        print(f'NOT ASSESSED: GDD structure check could not run: {error}',file=sys.stderr)
        return 1
    return 0

if __name__=='__main__': sys.exit(main())
