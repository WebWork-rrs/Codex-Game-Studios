# Keep the Codex adaptation current

The original framework is created and maintained by
[Donchitos](https://github.com/Donchitos/Claude-Code-Game-Studios).
This adaptation retains its history. `origin` is your Codex repository and
`upstream` is the original framework. The latest integrated upstream revision
is recorded in `tools/codex/upstream.json`.

## Daily proposals

The **Sync upstream studio** GitHub Actions workflow checks upstream every
day around **09:17 Asia/Dhaka (03:17 UTC)**. When nothing is new it exits
without creating a pull request. When updates arrive, it:

1. Fetches upstream `main` and the existing `automation/upstream-sync` branch.
2. Merges your latest `main` and upstream history into the review branch.
3. Regenerates Codex skills, roles, and the catalog; records the upstream SHA.
4. Runs adapter tests, generated-file checks, and asset validation.
5. Pushes the verified branch and opens or updates one pull request into `main`.

You review and merge the proposal. **No automatic merge or force push is
performed.** Original upstream commits and authorship remain intact. New
skills and roles are discovered from the source tree rather than limited to
the initial 74/49 counts. New schemas, tool assumptions, or template layouts
may still require a change to the adapter and manual review.

Preparation has read-only repository credentials. Publishing is a separate
job that consumes a Git bundle and runs the helper from your current `main`;
it does not execute proposed scripts with write credentials. The workflow
uses the standard `GITHUB_TOKEN`, with write access only in the publishing
job, so no personal access token is needed.

In repository **Settings → Actions → General**, **Allow GitHub Actions to
create and approve pull requests** must be enabled for automatic PR creation.
GitHub bundles creation and approval in this single permission; the workflow
never approves or merges proposals. Also set the repository Actions variable
`UPSTREAM_CREATE_PULL_REQUESTS` to `true` after enabling that permission.
Without this variable, the workflow still checks, tests, and pushes the review
branch, then shows a link for creating a PR manually. Keep default workflow
permissions read-only.
GitHub may require **Approve workflows to run** on bot-created pull requests
before the separate compatibility workflow starts. Tests have already run
inside the preparation job; still review the updated code and engine behavior.

Merge conflicts, failed tests, converter errors, or a concurrent `main` update
stop publication and appear as a failed Actions run. The previous PR, if
one exists, remains available. Resolve the conflict or adapt the converter,
then rerun the workflow. No partial merge is applied to `main`.

The bot branch advances through normal merge commits. If you reject an update
and want future proposals to start from `main` again, close the PR and delete
its bot branch in GitHub. Closed proposals are not reopened on unchanged
upstream; newly arriving changes can produce a new proposal on the retained
branch. Main and the bot branch should not be force-pushed.

GitHub schedules can be delayed, and public repository schedules are disabled
after 60 days without repository activity. Re-enable the workflow in Actions
if needed. See [scheduled workflow behavior](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule).

## Check immediately

Open **Actions → Sync upstream studio → Run workflow**, or run:

```bash
gh workflow run upstream-sync.yml --repo WebWork-rrs/Codex-Game-Studios
```

See [GitHub's manual-run instructions](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow).
Ask Codex to review and integrate the proposed upstream update when ready.

## Manual local integration

Start with a clean working tree and current `main`. Commit or preserve your
own changes first; the helper refuses dirty trees. If `upstream` is missing,
add it once with the original repository's URL.

```bash
git switch main
git pull --ff-only origin main
git fetch upstream main
python3 tools/codex/upstream_sync.py
python3 -m unittest discover -s tools/codex/tests -v
python3 tools/codex/studio.py sync --check
python3 tools/codex/studio.py validate
```

If updates exist, the helper creates `automation/upstream-sync`, merges the
source commits, and commits regenerated files. Review that branch before
pushing it and opening a pull request. It never pushes on your behalf. For
an existing remote proposal, fetch origin and pass
`--existing-ref origin/automation/upstream-sync`. Preserve local changes if
the helper reports that your local proposal differs from its selected baseline.

On a conflict, the helper aborts that merge and returns to the starting branch.
For regeneration/test failures, inspect the proposal branch and fix the
adapter there; do not push a failing proposal. Keep `project.yaml`, engine
settings, and game-specific source changes during conflict resolution.

Never edit generated files to resolve upstream differences: change the
`.claude/` sources or converter, then regenerate. See upstream's
[upgrade guide](https://github.com/Donchitos/Claude-Code-Game-Studios/blob/main/UPGRADING.md)
for version-specific migrations.

## New games made from this template

GitHub's **Use this template** creates a new repository with independent
history. Those game repositories do not automatically receive updates from
this adaptation. The daily schedule is limited to
`WebWork-rrs/Codex-Game-Studios`; copied games are not silently updated.

For games with shared clone history, merge the updated Codex adaptation on a
review branch and preserve game configuration. For template-generated games
without shared history, follow a selective framework migration from the
upstream guide and copy the updated Codex adapter alongside it. Do not use
`--allow-unrelated-histories` or overwrite your game configuration wholesale.
