# Shared GDD Structure Checks

`.claude/scripts/gdd-structure.py` owns the section labels, heading aliases,
tier requirements, and conditional rules used by design review and the commit
hook. `gdd-structure-check.sh` is its Bash compatibility entry point. Python 3
is required; a missing interpreter/checker reports NOT ASSESSED or SKIPPED.

Presence checks recognize actual Markdown headings outside fenced code. A
section name in prose or a code example does not count. Numbered headings and
Detailed Design / Detailed Rules are accepted. A heading does not establish
that its content is complete or meaningful.

Run presence checks from the project root:

```bash
bash .claude/scripts/gdd-structure-check.sh design/gdd/combat.md
```

After reading the design, resolve its tier and classify its category from the
systems index, whether it defines numeric rules, and whether it references
another GDD. Pass those grounded classifications to the same checker:

```bash
python3 .claude/scripts/gdd-structure.py --tier standard --category Gameplay \
  --numeric-rules yes --has-dependencies yes design/gdd/combat.md
```

Use the actual values, not the example's category. `--numeric-rules` and
`--has-dependencies` accept `yes`, `no`, or `unknown`; omit `--category` if
unresolved. Add `--tuning-knobs` when the effective workflow override requires
it. The output names PRESENT, ABSENT, REQUIRED, MISSING REQUIRED, and unresolved
conditions as NOT ASSESSED. Missing sections or unknown conditions prevent
structural approval; semantic completeness still requires reading the design.

Summary is included in every authored system GDD. Full and standard requirements
and category/dependency conditions follow the authoring workflow; a voluntarily
authored minimal GDD uses Summary and the five standard core sections, without
conditional Formulas/feel requirements. The game brief remains the minimal
pipeline's required artifact, rather than a mandatory GDD.

Commit checks are advisory and read staged content. They cover only active,
top-level system GDDs, excluding governance files, archives and review copies.
At minimal rigor they skip optional GDD structure checks. They do not infer
numeric rules or category from keyword mentions: unresolved conditional rules
are explicitly deferred to design review. They do not certify completeness.
