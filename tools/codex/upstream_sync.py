#!/usr/bin/env python3
"""Prepare upstream updates on a review branch; never push or modify main."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import subprocess
import sys

from convert import generate

UPSTREAM_REPOSITORY = 'Donchitos/Claude-Code-Game-Studios'


def git(root: Path, *arguments: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(['git', *arguments], cwd=root, text=True,
                          capture_output=True, check=check)


def revision(root: Path, ref: str) -> str:
    return git(root, 'rev-parse', '--verify', ref + '^{commit}').stdout.strip()


def ancestor(root: Path, earlier: str, later: str) -> bool:
    result = git(root, 'merge-base', '--is-ancestor', earlier, later, check=False)
    if result.returncode not in (0, 1):
        raise ValueError(result.stderr)
    return result.returncode == 0


def prepare(root: Path, upstream_ref: str, base_ref: str,
            branch: str = 'automation/upstream-sync', existing_ref: str | None = None) -> dict:
    root = root.resolve()
    if not re.fullmatch(r'automation/upstream-sync(?:-[0-9a-f-]+)?', branch):
        raise ValueError('Use a branch under automation/upstream-sync')
    if git(root, 'status', '--porcelain').stdout.strip():
        raise ValueError('Upstream preparation requires a clean working tree')
    upstream_sha, base_sha = revision(root, upstream_ref), revision(root, base_ref)
    result = {'changed': False, 'branch': branch, 'base_sha': base_sha,
              'upstream_sha': upstream_sha, 'head_sha': base_sha}
    if ancestor(root, upstream_sha, base_sha):
        return result
    if git(root, 'merge-base', base_sha, upstream_sha, check=False).returncode:
        raise ValueError('No shared upstream history. Template-generated games require a selective migration; do not force unrelated histories.')
    previous_sha = revision(root, existing_ref) if existing_ref else None
    if previous_sha and ancestor(root, upstream_sha, previous_sha) and ancestor(root, base_sha, previous_sha):
        return {**result, 'head_sha': previous_sha}
    initial = git(root, 'symbolic-ref', '--short', '-q', 'HEAD', check=False).stdout.strip()
    initial_sha = revision(root, 'HEAD')
    start = previous_sha or base_sha
    local = git(root, 'show-ref', '--verify', '--quiet', 'refs/heads/' + branch, check=False)
    if local.returncode == 0:
        if revision(root, branch) != start:
            raise ValueError('Update branch has local commits outside the selected baseline; preserve and review them first')
        git(root, 'switch', branch)
    else:
        git(root, 'switch', '--create', branch, start)
    for ref in (base_sha, upstream_sha):
        merge = git(root, 'merge', '--no-edit', ref, check=False)
        if merge.returncode:
            conflicts = git(root, 'diff', '--name-only', '--diff-filter=U').stdout.strip()
            if (root / '.git/MERGE_HEAD').exists() or git(root, 'rev-parse', '-q', '--verify', 'MERGE_HEAD', check=False).returncode == 0:
                git(root, 'merge', '--abort')
            if initial:
                git(root, 'switch', initial)
            else:
                git(root, 'switch', '--detach', initial_sha)
            raise ValueError('Merge conflict or merge failure; no update published. ' +
                             (conflicts or merge.stderr or merge.stdout))
    generate(root)
    metadata = root / 'tools/codex/upstream.json'
    metadata.write_text(json.dumps({'repository': UPSTREAM_REPOSITORY, 'branch': 'main',
                                    'commit': upstream_sha}, indent=2) + '\n')
    git(root, 'add', '--', '.agents', '.codex', 'docs/codex-workflows.md',
        'tools/codex/generated.json', 'tools/codex/upstream.json')
    if git(root, 'diff', '--cached', '--quiet', check=False).returncode:
        git(root, 'commit', '-m', 'chore: regenerate Codex adapters for upstream ' + upstream_sha[:12])
    result.update(changed=True, head_sha=revision(root, 'HEAD'))
    if previous_sha and not ancestor(root, previous_sha, result['head_sha']):
        raise ValueError('Update would rewrite the existing bot branch; refusing')
    return result


def export_bundle(root: Path, result: dict, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    git(root, 'bundle', 'create', str(destination.resolve()),
        'refs/heads/' + result['branch'], '^' + result['base_sha'])


def publish_branch(root: Path, bundle: Path, branch: str,
                   expected_head: str | None = None) -> None:
    if not re.fullmatch(r'automation/upstream-sync(?:-[0-9a-f-]+)?', branch):
        raise ValueError('Publication is restricted to the upstream review branch')
    git(root, 'bundle', 'verify', str(bundle.resolve()))
    git(root, 'fetch', str(bundle.resolve()),
        'refs/heads/' + branch + ':refs/heads/' + branch)
    if expected_head and revision(root, branch) != expected_head:
        raise ValueError('Bundle head does not match the verified preparation output')
    git(root, 'fetch', 'origin', 'main:refs/remotes/origin/main')
    if not ancestor(root, 'origin/main', branch):
        raise ValueError('main advanced during preparation; rerun instead of publishing a stale proposal')
    # Ordinary push rejects any concurrent branch divergence. Credentials are
    # supplied only to this Git process, never stored in project/user config.
    git(root, '-c', 'credential.helper=', '-c', 'credential.helper=!gh auth git-credential',
        'push', 'origin', branch + ':refs/heads/' + branch)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--upstream-ref', default='upstream/main')
    parser.add_argument('--base-ref', default='origin/main')
    parser.add_argument('--existing-ref')
    parser.add_argument('--branch', default='automation/upstream-sync')
    parser.add_argument('--output', type=Path, help='Write a GitHub Actions output file')
    parser.add_argument('--bundle', type=Path, help='Export the proposal as a Git bundle')
    parser.add_argument('--report', type=Path, help='Write the pull request description')
    parser.add_argument('--publish-bundle', type=Path, help='Publish a tested bundle to the review branch only')
    parser.add_argument('--expected-head', help='Verify the preparation output SHA before pushing')
    args = parser.parse_args()
    root = Path(git(Path.cwd(), 'rev-parse', '--show-toplevel').stdout.strip())
    try:
        if args.publish_bundle:
            publish_branch(root, args.publish_bundle, args.branch, args.expected_head)
            print('Published review branch: ' + args.branch)
            return 0
        result = prepare(root, args.upstream_ref, args.base_ref, args.branch, args.existing_ref)
        if result['changed']:
            if args.bundle:
                export_bundle(root, result, args.bundle)
            if args.report:
                args.report.parent.mkdir(parents=True, exist_ok=True)
                args.report.write_text(
                    '# Upstream game studio update\n\n'
                    f'Integrates [{UPSTREAM_REPOSITORY}](https://github.com/{UPSTREAM_REPOSITORY}) '
                    f'through commit [`{result["upstream_sha"][:12]}`]'
                    f'(https://github.com/{UPSTREAM_REPOSITORY}/commit/{result["upstream_sha"]}).\n\n'
                    'Original commits and authorship are preserved. Codex skills and roles are regenerated '
                    'from the updated sources, and the integrated revision is recorded in '
                    '`tools/codex/upstream.json`.\n\n'
                    'The preparation job must pass the adapter tests, generated-file check, and asset '
                    'validation before this proposal is published. Review framework changes, engine '
                    'assumptions, and Codex behavior before merging. No automatic merge is performed.\n')
        if args.output:
            with args.output.open('a') as output:
                for key, value in result.items():
                    output.write(f'{key}={str(value).lower() if isinstance(value, bool) else value}\n')
        print(json.dumps(result, indent=2))
        return 0
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f'Upstream sync: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
