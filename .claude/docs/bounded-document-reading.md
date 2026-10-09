# Bounded Document Reading

Use this protocol whenever a review needs a whole document or complete sections.
An unbounded `Read`, a summary, or a fixed-context grep preview is not evidence
that the full review scope was read. Bound each tool response, not the review's
breadth.

## Inventory, then read

1. List the in-scope paths before reading content. For each Markdown file, run:

   ```bash
   python3 .claude/scripts/read-markdown.py index "[path]" --offset 0 --limit 30
   ```

   Continue index pages using the returned `next_offset` until the inventory is
   complete. Record `sha256`, `total_lines`, headings, and section ranges;
   an incomplete heading inventory cannot establish the review scope. Include
   preamble and unheaded text when the workflow requires a whole-file review.
   A document with no headings still has a line range to read. Pass that first
   `sha256` as `--expected-sha [hash]` on every later index/read call for the file;
   a mismatch means rebuild its inventory and restart the affected review.

2. Select the scope the workflow requires. Whole-file means lines 1 through the
   reported total; section review means each selected heading's complete range,
   including nested subsections. Deduplicate overlapping ranges. Follow cited
   sections outside that scope when needed to judge a claim; record the expansion.

3. Read successive bounded chunks of every selected range:

   ```bash
   python3 .claude/scripts/read-markdown.py read "[path]" --start 1 --max-lines 120 --max-chars 8000
   ```

   Substitute the selected start line and add `--expected-sha [hash]`. Continue
   at `next_start` with `--column [next_column]`, using actual emitted
   `start`/`column` and `end`/`end_column`, until every required line is covered.
   Never advance by 120 merely because 120 was requested: the character limit
   may stop a chunk earlier. Reduce limits if the runtime's output cap is smaller.
   Analyze each chunk as it arrives; keep compact findings with path and line
   references rather than accumulating or copying the entire source into prompts.

4. Track a coverage ledger:

   | Path | Required ranges | Read ranges | Unreviewed ranges / reason |
   |---|---|---|---|
   | `[path]` | `1–[total]` or named sections | actual emitted ranges | `none` or exact gaps |

   Record truncation, read errors, and incomplete index pages. A tool response
   truncated before its completion metadata is not a completed chunk: re-read
   with smaller limits. A partial or oversized single line must be consumed with
   a supported character cursor or another bounded reader that proves all its
   characters were inspected. For helper fragments, resume at `next_start` and
   `next_column` with `--column [offset]`; count the line covered
   only after its final fragment. If that cannot be done, mark that line unreviewed;
   never skip it, loop on a stalled cursor, or count a clipped line as covered.
   The expected hash check establishes a stable version across chunks; verify
   that version again before recording a freshness receipt.

## Findings and verdicts

Heading presence and summaries support discovery, not semantic assessment.
Missing structure, no headings, or very large sections trigger bounded reads of
the necessary content; they do not remove a file from scope. Finish all required
ranges successively even when early chunks look sound. Context pressure is a
reason to keep compact notes or checkpoint coverage, not to replace the remaining
review with spot checks.

Every report gives the coverage ledger or a compact equivalent, with exact
unreviewed ranges and reasons. Mark unreviewed criteria `NOT ASSESSED`; never
issue approval while a required range is unreviewed. Keep known failures visible:
revision/failure verdicts outrank `NOT ASSESSED`, which outranks approval. A
partial report with findings does not establish a full review or a reusable
approval receipt. Old receipts without explicit complete coverage cannot prove
that an unchanged document received a complete review.

## Agent briefs and cross-document context

When delegation is authorized, each brief contains: objective/domain; source
paths; named sections or exact ranges; relevant project/configuration facts;
specific cross-document questions; findings so far; and this reading protocol.
Agents read those paths in bounded chunks themselves. Do not paste the GDD,
entire registry, or unrelated sibling documents into each brief. Give registry
matches and targeted dependency sections for cross-document facts; expand only
when the question requires it.

Return contract: coverage (required/read/unreviewed ranges), prioritized findings
with path/line evidence and proposed fixes, disagreements, and assessment status.
Return compact findings, not a restatement of the source. The parent verifies
coverage and gathers all required results before synthesis. Use the runtime's
available collaboration tools and concurrency slots; queue additional independent
work. Inherit the session's model/settings rather than selecting a model tier.
If delegation is unavailable, report which specialist checks did not run and
apply the workflow's `NOT ASSESSED` rule; do not invent plugin APIs or claim that
an internal perspective was an independent review.
