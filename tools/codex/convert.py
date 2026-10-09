"""Generate project-scoped Codex skills and roles from the upstream template."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re

MANIFEST = 'tools/codex/generated.json'

COMPATIBILITY = """## Codex execution adapter

Read the repository's `AGENTS.md` before this workflow. Its Codex mappings and
the user's existing authorization govern this workflow and all referenced
upstream documents. Work from the repository root.

- `$studio-NAME` invokes a repository skill; arguments are the text supplied
  with the invocation. Do not expect Claude slash commands or `$ARGUMENTS`
  substitution. Read another skill's `SKILL.md` when chaining workflows.
- Run each **Execute before proceeding** shell block explicitly; Codex does
  not run Claude's inline shell preprocessing. Use the real configuration
  output. Report command failures rather than silently assuming defaults.
- `AskUserQuestion` means ask with an available Codex question tool or plain
  text, and wait when the answer is required. Previously authorized routine
  edits need no repeated per-file approval. Preserve unresolved game-design
  choices and the configured automation mode.
- Claude `Agent`/`Task`, `subagent_type`, and named roles mean Codex subagents.
  Use `.codex/agents/<role>.toml` when custom role selection is supported;
  otherwise pass its `developer_instructions` to the available spawn tool.
  Use only actual available tools, inherit the user's model, respect the
  concurrency limit, and collect results. If delegation is unavailable,
  perform the roles sequentially and label that limitation.
- `Read`/`Glob`/`Grep`/`Write`/`Edit`/`Bash`/`WebSearch`/`WebFetch` are capability
  labels: map them to available file, patch, shell, and browsing tools.
  `TeamCreate`, `SendMessage`, and task lists map to available collaboration
  tools and a written task ledger; do not invent tools.
- Shared `.claude/docs`, `.claude/scripts`, `.claude/hooks`, and templates are
  intentional runtime dependencies. Relative `references/` and `scripts/`
  paths resolve against this skill's folder. Original references may still
  show `/NAME`: interpret known studio workflows as `$studio-NAME`.
- `CLAUDE.md` is a legacy engine/configuration mirror. Codex reads engine
  settings from `project.yaml` and explicitly reads the matching version
  reference. `@file` imports, Claude settings, status lines, and permissions
  do not configure Codex. Preserve `AGENTS.md` during engine setup.
- Edit upstream skill/role sources under `.claude/`, then run
  `python3 tools/codex/studio.py sync` to regenerate Codex copies. Do not edit
  generated files directly. Apply the same rule to framework self-tests.

"""


def split_frontmatter(text: str) -> tuple[dict[str, str], str]:
    match = re.match(r'\A---\r?\n(.*?)\r?\n---\r?\n', text, re.S)
    if not match:
        raise ValueError('Missing YAML frontmatter')
    fields = {}
    for line in match[1].splitlines():
        key, separator, value = line.partition(':')
        if separator and not line.startswith((' ', '#')):
            value = value.strip()
            if value.startswith('"'):
                value = json.loads(value)
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1].replace("''", "'")
            fields[key] = value
    return fields, text[match.end():]


def adapt(text: str, names: list[str], skill: str | None = None) -> str:
    # Match command tokens, not filesystem paths or URL segments.
    pattern = r'(?<![\w./-])/(' + '|'.join(map(re.escape, sorted(names, key=len, reverse=True))) + r')(?![\w/-])'
    text = re.sub(pattern, lambda m: '$studio-' + m[1], text)
    for name in names:
        text = text.replace(f'.claude/skills/{name}/', f'.agents/skills/studio-{name}/')
    text = text.replace('${CLAUDE_SKILL_DIR}/../../hooks/', '.claude/hooks/')
    if skill:
        text = text.replace('${CLAUDE_SKILL_DIR}', f'.agents/skills/studio-{skill}')
        text = text.replace('$CLAUDE_SKILL_DIR', f'.agents/skills/studio-{skill}')
    text = re.sub(r'^!`([^\n]+)`\s*$',
                  lambda m: '**Execute before proceeding** (from the repository root):\n\n```bash\n' + m[1] + '\n```',
                  text, flags=re.M)
    text = text.replace('Welcome to Claude Code Game Studios!', 'Welcome to Codex Game Studios!')
    return re.sub(r'^[ \t]+$', '', text, flags=re.M)


def build_artifacts(root: Path) -> dict[str, bytes]:
    sources = sorted((root / '.claude/skills').glob('*/SKILL.md'))
    names = [p.parent.name for p in sources]
    artifacts: dict[str, bytes] = {}
    catalog = ['# Codex studio workflows', '',
               'Invoke a skill using `$studio-NAME` or ask for the workflow in plain language.', '',
               '| Skill | Purpose |', '| --- | --- |']
    for source in sources:
        meta, body = split_frontmatter(source.read_text(encoding='utf-8'))
        name = source.parent.name
        description = adapt(meta['description'], names, name)
        entry = f'---\nname: studio-{name}\ndescription: {json.dumps(description, ensure_ascii=False)}\n---\n\n'
        content = entry + COMPATIBILITY + adapt(body, names, name)
        destination = f'.agents/skills/studio-{name}'
        artifacts[destination + '/SKILL.md'] = content.encode()
        for resource in sorted(source.parent.rglob('*')):
            if resource.is_symlink():
                raise ValueError(f'Symlink resource is not supported: {resource}')
            if not resource.is_file() or resource == source:
                continue
            relative = resource.relative_to(source.parent)
            # Markdown instructions are adapted; runnable scripts retain their
            # original behavior and share the upstream configuration helpers.
            data = resource.read_bytes()
            if resource.suffix == '.md':
                data = adapt(data.decode('utf-8'), names, name).encode()
            artifacts[f'{destination}/{relative.as_posix()}'] = data
        catalog.append(f'| `$studio-{name}` | {description.replace(chr(124), chr(92) + chr(124))} |')
    for source in sorted((root / '.claude/agents').glob('*.md')):
        meta, body = split_frontmatter(source.read_text(encoding='utf-8'))
        role = {'name': meta['name'], 'description': meta['description'],
                'developer_instructions': COMPATIBILITY + adapt(body, names)}
        content = '# Generated by tools/codex/convert.py; edit the .claude source.\n'
        content += '\n'.join(f'{key} = {json.dumps(value, ensure_ascii=False)}' for key, value in role.items()) + '\n'
        artifacts[f'.codex/agents/{source.stem}.toml'] = content.encode()
    artifacts['docs/codex-workflows.md'] = ('\n'.join(catalog) + '\n').encode()
    for filename in ('hooks.json', 'config.toml'):
        source = root / 'tools/codex' / filename
        if source.exists():
            artifacts[f'.codex/{filename}'] = source.read_bytes()
    return artifacts


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def generate(root: Path, check: bool = False) -> dict[str, bytes]:
    root = root.resolve()
    artifacts = build_artifacts(root)
    manifest_path = root / MANIFEST
    previous = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    previous_hashes = previous.get('files', {})
    # Validate the whole write set before changing anything. Do not overwrite
    # customized copies or follow a destination symlink outside the project.
    mismatches = []
    for relative, data in artifacts.items():
        target = root / relative
        if target.resolve() != target or any(parent.is_symlink() for parent in target.parents if parent != root):
            raise ValueError(f'Symlink destination is not supported: {relative}')
        if not target.exists() or target.read_bytes() != data:
            mismatches.append(relative)
            if not check and target.exists() and digest(target.read_bytes()) != previous_hashes.get(relative):
                raise ValueError(f'Generated file modified locally; preserve or move edits before sync: {relative}')
    stale = set(previous_hashes) - set(artifacts)
    manifest = {'format_version': 1, 'files': {p: digest(d) for p, d in artifacts.items()}}
    manifest_bytes = (json.dumps(manifest, indent=2, sort_keys=True) + '\n').encode()
    if check:
        if mismatches or stale or not manifest_path.exists() or manifest_path.read_bytes() != manifest_bytes:
            raise ValueError('Codex generated files are out of date; run sync. ' + ', '.join(mismatches[:8] or sorted(stale)))
        return artifacts
    # A removed upstream skill must not be silently left discoverable.
    for relative in stale:
        target = root / relative
        if target.exists():
            if target.resolve() != target or digest(target.read_bytes()) != previous_hashes[relative]:
                raise ValueError(f'Stale generated file modified locally: {relative}')
    for relative, data in artifacts.items():
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    for relative in stale:
        (root / relative).unlink(missing_ok=True)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_bytes(manifest_bytes)
    return artifacts
