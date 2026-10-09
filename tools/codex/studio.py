#!/usr/bin/env python3
"""Codex studio setup checks and lifecycle payload translation (stdlib only)."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tomllib

from convert import generate


def project_root(start: Path) -> Path:
    for path in [start.resolve(), *start.resolve().parents]:
        if (path / '.claude/hooks/yaml-helper.sh').is_file():
            return path
    raise ValueError(f'No game studio project found above {start}')


def run_upstream(root: Path, script: str, payload: dict) -> subprocess.CompletedProcess:
    env = {**os.environ, 'CLAUDE_PROJECT_DIR': str(root)}
    return subprocess.run(['bash', str(root / '.claude/hooks' / script)], cwd=root,
                          input=json.dumps(payload), text=True, capture_output=True,
                          timeout=20, env=env)


def context(event: str, message: str) -> None:
    print(json.dumps({'hookSpecificOutput': {'hookEventName': event,
                                            'additionalContext': message}}))


def asset_paths(root: Path) -> list[Path]:
    paths = []
    for folder in ('assets', 'Assets', 'Content'):
        base = root / folder
        if not base.exists():
            continue
        for path in base.rglob('*.json'):
            relative = path.relative_to(base)
            if folder == 'assets' or any(p.lower() == 'data' for p in relative.parts[:-1]):
                paths.append(path)
    return sorted(paths)


def validate(root: Path, staged: bool = False) -> int:
    failures = []
    if staged:
        result = subprocess.run(['git', 'diff', '--cached', '--name-only', '--diff-filter=ACMR', '-z'],
                                cwd=root, capture_output=True, check=True)
        paths = [p.decode() for p in result.stdout.split(b'\0') if p.endswith(b'.json')]
        for path in paths:
            data = subprocess.run(['git', 'show', ':' + path], cwd=root,
                                  capture_output=True, check=True).stdout
            try:
                json.loads(data)
            except (ValueError, UnicodeError) as error:
                failures.append(f'{path}: invalid staged JSON: {error}')
    else:
        for path in asset_paths(root):
            try:
                json.loads(path.read_bytes())
            except (ValueError, OSError) as error:
                failures.append(f'{path.relative_to(root)}: invalid asset JSON: {error}')
    if failures:
        print('\n'.join(failures), file=sys.stderr)
        return 1
    print('Staged JSON validation passed.' if staged else 'Asset JSON validation passed.')
    return 0


def changed_paths(root: Path, payload: dict) -> set[Path]:
    arguments = payload.get('tool_input', {})
    if not isinstance(arguments, dict):
        arguments = {'command': arguments} if isinstance(arguments, str) else {}
    paths = set()
    if isinstance(arguments.get('file_path'), str):
        paths.add(arguments['file_path'])
    command = arguments.get('command', arguments.get('cmd', arguments.get('input', '')))
    if isinstance(command, str):
        paths.update(re.findall(r'^\*\*\* (?:Add File|Update File|Delete File|Move to): (.+)$', command, re.M))
    resolved = set()
    cwd = Path(payload.get('cwd') or root)
    for name in paths:
        path = Path(name)
        # Patch paths follow the tool's cwd; root-relative paths are supported
        # when the caller explicitly supplies an absolute target.
        path = (cwd / path).resolve() if not path.is_absolute() else path.resolve()
        if path.is_relative_to(root):
            resolved.add(path)
    return resolved


def hook(root: Path, event: str, payload: dict) -> int:
    if event == 'SessionStart':
        # No write/log side effects at startup; recovery lives in active.md.
        result = run_upstream(root, 'session-start.sh', payload)
        message = result.stdout + '\nCodex studio: use $studio-start for onboarding; $studio-help lists workflows. '
        message += 'Read AGENTS.md and production/session-state/active.md when present.'
        context(event, message[:10000])
        return result.returncode
    arguments = payload.get('tool_input', {})
    if not isinstance(arguments, dict):
        arguments = {'command': arguments} if isinstance(arguments, str) else {}
    if event == 'PreToolUse':
        command = arguments.get('command', arguments.get('cmd', ''))
        if payload.get('tool_name') not in ('Bash', 'PowerShell', 'exec_command', 'shell_command', 'shell'):
            return 0
        if not isinstance(command, str) or not re.search(r'\bgit\b', command, re.I):
            return 0
        normalized = {**payload, 'tool_name': 'Bash', 'tool_input': {'command': command}}
        messages = []
        for script in ('validate-commit.sh', 'validate-push.sh'):
            result = run_upstream(root, script, normalized)
            if result.returncode:
                print(result.stderr or result.stdout, file=sys.stderr)
                return 2
            messages.append(result.stdout + result.stderr)
        if ''.join(messages).strip():
            context(event, ''.join(messages))
        return 0
    if event == 'PostToolUse':
        failures, messages = [], []
        for path in changed_paths(root, payload):
            if not path.is_file():
                continue
            normalized = {**payload, 'tool_name': 'Write', 'tool_input': {'file_path': str(path)}}
            result = run_upstream(root, 'validate-assets.sh', normalized)
            if result.returncode:
                failures.append(result.stderr or result.stdout)
            else:
                messages.append(result.stdout + result.stderr)
        # Shell tools can edit arbitrary files without listing paths. Validate
        # data JSON for such edits too; no execution/parsing of the shell text.
        if payload.get('tool_name') in ('Bash', 'PowerShell', 'exec_command', 'shell_command', 'shell'):
            for path in asset_paths(root):
                try:
                    json.loads(path.read_bytes())
                except (ValueError, OSError) as error:
                    failures.append(f'{path.relative_to(root)}: invalid asset JSON: {error}')
        if failures:
            print('\n'.join(failures), file=sys.stderr)
            return 2
        if ''.join(messages).strip():
            context(event, ''.join(messages))
        return 0
    raise ValueError(f'Unsupported hook event: {event}')


def doctor(root: Path) -> int:
    errors = []
    for binary in ('git', 'bash'):
        if not shutil.which(binary):
            errors.append(f'{binary} is required')
    try:
        artifacts = generate(root, check=True)
        for name, data in artifacts.items():
            if name.startswith('.codex/agents/') and name.endswith('.toml'):
                role = tomllib.loads(data.decode())
                if not all(role.get(key) for key in ('name', 'description', 'developer_instructions')):
                    errors.append(f'Incomplete Codex role: {name}')
        skills = sum(p.startswith('.agents/skills/studio-') and p.endswith('/SKILL.md') for p in artifacts)
        craft = sum(p.startswith('.agents/skills/') and not p.startswith('.agents/skills/studio-')
                    and p.endswith('/SKILL.md') for p in artifacts)
        roles = sum(p.startswith('.codex/agents/') for p in artifacts)
        print(f'{skills} studio workflows and {roles} custom roles are synchronized.')
        if craft:
            print(f'{craft} pinned game-craft skills are synchronized with their resources and licenses.')
    except (ValueError, OSError) as error:
        errors.append(str(error))
    result = subprocess.run(['bash', '.claude/hooks/yaml-helper.sh', 'resolve_config',
                             '--keys', 'rigor,workflow,automation,engine.name,engine.version'],
                            cwd=root, text=True, capture_output=True)
    if result.returncode:
        errors.append(result.stderr or 'Configuration resolution failed')
    else:
        print(result.stdout.strip())
    engine = subprocess.run(['bash', '-c',
                             '. .claude/hooks/yaml-helper.sh; get_effective_yaml_key engine.name'],
                            cwd=root, text=True, capture_output=True, check=True).stdout.strip()
    if not engine:
        print('Engine is not configured. Start with $studio-start, then $studio-setup-engine.')
    else:
        print(f'Configured engine: {engine}')
    for error in errors:
        print(error, file=sys.stderr)
    return 1 if errors else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='action', required=True)
    sync = sub.add_parser('sync', help='Regenerate skills and roles; refuses local edits')
    sync.add_argument('--check', action='store_true', help='Check without writing files')
    sub.add_parser('doctor', help='Check adapter, tools, and effective configuration')
    validation = sub.add_parser('validate', help='Validate asset data JSON')
    validation.add_argument('--staged', action='store_true', help='Validate staged JSON from the Git index')
    hooks = sub.add_parser('hook', help='Translate a native Codex lifecycle payload')
    hooks.add_argument('event', choices=['SessionStart', 'PreToolUse', 'PostToolUse'])
    args = parser.parse_args()
    try:
        payload = json.load(sys.stdin) if args.action == 'hook' else {}
        if not isinstance(payload, dict):
            raise ValueError('Hook input must be a JSON object')
        root = project_root(Path(payload.get('cwd') or Path.cwd()))
        if args.action == 'sync':
            artifacts = generate(root, check=args.check)
            print(f'{len(artifacts)} Codex files ' + ('verified.' if args.check else 'generated.'))
            return 0
        if args.action == 'doctor':
            return doctor(root)
        if args.action == 'validate':
            return validate(root, args.staged)
        return hook(root, args.event, payload)
    except (ValueError, OSError, subprocess.SubprocessError) as error:
        print(f'Codex studio: {error}', file=sys.stderr)
        return 2 if args.action == 'hook' else 1


if __name__ == '__main__':
    sys.exit(main())
