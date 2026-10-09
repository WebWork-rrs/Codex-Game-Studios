# Agent Coordination Rules

1. **Vertical Delegation**: Leadership agents delegate to department leads, who
   delegate to specialists. Never skip a tier for complex decisions.
2. **Horizontal Consultation**: Agents at the same tier may consult each other
   but must not make binding decisions outside their domain.
3. **Conflict Resolution**: When two agents disagree, escalate to the shared
   parent. If no shared parent, escalate to `creative-director` for design
   conflicts or `technical-director` for technical conflicts.
4. **Change Propagation**: When a design change affects multiple domains, the
   `producer` agent coordinates the propagation.
5. **No Unilateral Cross-Domain Changes**: An agent must never modify files
   outside its designated directories without explicit delegation.

## Model Tier Assignment

Read `.claude/docs/model-tiers.md` on demand. It carries the tier table, the
per-skill assignments and the authoring rule.

**Key point:** whether a skill's `model:` is used
depends on how the skill starts. Typed as `/skill-name`: yes, except a `haiku`
pin in auto mode. Started by Claude through the Skill tool: no. Never tell a
user a `haiku` skill saves money; an `opus` skill typed in a Sonnet session
costs more. The agent-side `model:` is a different mechanism, and is applied.

## Subagents vs Agent Teams

This project uses two distinct multi-agent patterns:

### Subagents (current, always active)
Spawned via the `Agent` tool within a single Claude Code session (renamed from
`Task` in Claude Code 2.1.63; `Task` still works as an alias). Used by all
`team-*` skills and orchestration skills. Subagents share the session's
permission context, run sequentially or in parallel within the session, and
return results to the parent.

**When to spawn in parallel**: If two subagents' inputs are independent (neither
needs the other's output to begin), spawn both `Agent` calls simultaneously
rather than waiting. Example: `/review-all-gdds` **Phase 2** (consistency) and
**Phase 3** (design theory) are independent — spawn both at the same time.
Phase 1 loads the GDDs and both depend on it, so it is the one phase here that
must NOT be parallelised.

### Agent Teams (experimental — opt-in)
Multiple independent Claude Code *sessions* coordinated via a shared task list.
Opt-in only — read `.claude/docs/agent-teams.md` on demand before proposing one.

## Parallel Task Protocol

When an orchestration skill spawns multiple independent agents:

1. Issue all independent `Agent` calls before waiting for any result
2. Collect all results before proceeding to dependent phases
3. If any agent is BLOCKED, surface it immediately — do not silently skip
4. Always produce a partial report if some agents complete and others block

## Document Review Briefs and Returns

Use `.claude/docs/bounded-document-reading.md` for document-review delegation.
Each brief names the objective/domain, source paths, named sections or exact
ranges, relevant configuration, cross-document questions, and compact findings
so far. Agents inventory headings and read their assigned ranges in successive
bounded chunks themselves; do not multiply full documents across agent prompts.

Each return contains required/read/unreviewed ranges, prioritized findings with
path/line evidence and fixes, disagreements, and assessment status. The parent
verifies coverage before synthesis; summaries and truncated reads are not proof
of complete review. Carry exact gaps as `NOT ASSESSED`, keep known failures
visible, and withhold approval while required scope remains unreviewed. Queue
additional independent reviews within the runtime's concurrency slots.
