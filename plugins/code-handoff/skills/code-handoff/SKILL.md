---
name: code-handoff
description: Packages the current conversation into a handoff document for a fresh coding agent session (Claude Code, Codex CLI, OpenCode, Gemini CLI, or similar). Used when the user says "handoff", "generate handoff", "create a handoff", "hand this off", "hand off to the agent", "hand off to claude code", "hand off to codex", "hand off to opencode", "prep for the agent", "prep for claude code", "move this to the coding agent", "code handoff", "package this up for the agent", or otherwise signals they're ready to move investigatory work from this chat into a coding session. Runs with zero arguments — everything is pulled from the conversation itself.
---

# Code Handoff

## What a handoff is (and isn't)

A handoff transfers knowledge; it does not design the solution. Your job is to capture what the conversation actually established — the goal, the decisions, the constraints, the open questions — so a fresh coding agent starts with the same understanding you have.

It is **not** your job to plan the implementation, invent an approach, pick the files to touch, or prescribe first steps. The coding agent does that with full repo access and far more context than this skill has. Every assumption you bake in is something it then has to either refute (at best) or follow blindly (at worst), so don't bake any in. When in doubt, transfer the fact and let the coding agent decide what to do with it.

## What to do

1. **Review the full conversation.** Identify:
   - The goal (what's being built, investigated, or decided)
   - Decisions actually reached, with brief rationale — only choices the conversation genuinely settled, not ones you'd infer
   - Approaches considered and rejected, with why
   - Constraints: tech stack, repo or path names, style conventions, team/org factors
   - Open questions the coding agent should be aware of
   - Any file paths, repo names, library names, commands, or URLs that were actually mentioned

2. **Synthesize, don't transcribe.** The handoff is not a conversation dump. Pull out what's decided and relevant, drop small talk, dead ends that went nowhere, and clarifications that resolved into decisions (just capture the resulting decision).

3. **Collect references, don't invent them.** List the concrete file paths, identifiers, commands, and URLs that actually came up in the conversation, each with a word on what it is. These are pointers to where relevant things live — not an ordered investigation or an implementation plan. Do not guess at file paths, `rg`/`grep` patterns, "files to open first", or a sequence of steps that weren't discussed; the coding agent will work that out itself with the repo in front of it. If nothing concrete was mentioned, drop the section rather than manufacturing one.

4. **Self-verify before writing.** Run these checks on the draft:
   - Every Decision reflects a choice actually made in the conversation and carries a one-line rationale. If you inferred it or it's really the coding agent's call, cut it.
   - Every reference actually appeared in the conversation — a real path, a real identifier, a real command. No invented paths, patterns, or commands.
   - The handoff describes *what was decided*, not *how to implement it*. If a line prescribes an approach or a first step beyond the decisions actually made, cut it — that's the coding agent's job.
   - Thin sections MUST be deleted rather than padded. If there's nothing real to say under "Approaches considered and rejected," the section doesn't appear in the output.

5. **Write the handoff to `/mnt/user-data/outputs/handoff.md`** using the template below.

6. **Present the file and also output it inline** as a fenced markdown code block so it can be copied directly on mobile without opening the file. Keep any surrounding commentary short — the user ran this to get the doc, not to read about it.

## Handoff template

````markdown
# Handoff: <short descriptive title>

## Objective
<one or two sentences: what is being built or investigated, and why it matters>

## Context
<background from the conversation — what triggered this, the problem being solved, relevant prior work. Keep tight. 2-5 sentences.>

## Decisions already made
- <decision>: <one-line rationale>
- <decision>: <one-line rationale>

## Approaches considered and rejected
- <approach>: <why it was ruled out>

## Constraints
- **Tech stack / language:** <...>
- **Repo / codebase:** <path or name if mentioned, otherwise describe>
- **Style or patterns to follow:** <...>
- **Team / organizational:** <...>

## Open questions
- <question the coding agent should keep in mind or resolve early>

## Relevant references
Concrete paths, identifiers, and commands that came up in the conversation, each with a note on what it is. Pointers to where things live — not an ordered plan.

- `<path or identifier>` — <what it is / why it was mentioned>
- `<path or identifier>` — <what it is / why it was mentioned>

---
*Generated from a mobile investigation session. Paste into a new coding agent session to continue.*
````

## Example

If the conversation discussed adding Redis caching to a Flask `/api/search` endpoint that was hitting database timeouts, a good handoff looks like this (abbreviated for illustration):

```markdown
# Handoff: Redis caching for /api/search endpoint

## Objective
Add Redis-backed result caching to /api/search, which currently hits the primary DB on every request and times out under load.

## Context
Production p95 latency crossed 2s last week. Tracing showed the endpoint re-runs the same full-text query for identical inputs seconds apart. Short-TTL caching should bring common searches to sub-100ms.

## Decisions already made
- **Redis over Memcached**: Redis is already deployed for session storage; avoids adding a new dependency.
- **Key format `search:v1:{sha256(normalized_query)}`**: versioned so the prefix can be bumped during a future result-schema change.
- **TTL: 60 seconds**: short enough that staleness complaints are unlikely, long enough to absorb bursts.

## Constraints
- **Tech stack / language:** Python 3.11, Flask, SQLAlchemy, redis-py already pinned.
- **Repo / codebase:** `app/api/search.py` for the route; `app/cache/` is the existing Redis wrapper.
- **Style or patterns to follow:** existing cache wrappers use a `@cached(ttl=...)` decorator — match it.

## Open questions
- Should invalidation hook into the content-update pipeline, or is 60s TTL the only staleness bound? Needs product confirmation.

## Relevant references
- `app/api/search.py` — the /api/search route handler under discussion.
- `app/cache/` — existing Redis wrapper; uses a `@cached(ttl=...)` decorator worth matching.
```

What the example does right: Context stays tight at three sentences instead of recapping the whole discussion. Each Decision carries a one-line rationale rather than standing alone. Relevant references point at the real paths that came up and say what they are, without prescribing which to open first or turning them into an investigation script — the coding agent decides that. There's no "First task" dictating the implementation, because *which* decorator call to write and *how* to verify it are the coding agent's job with the repo in front of it, not assumptions to bake in here. The "Approaches considered and rejected" section is omitted entirely because no real alternatives were discussed — that's the thin-section rule in action.

## Output format

After writing the file:

1. Call `present_files` with the handoff path so it's downloadable.
2. Output the full handoff inline as a fenced markdown code block (use four backticks on the outer fence so the inner template fences render correctly).
3. Close with at most one short sentence — e.g., "Ready to paste into your coding agent." No recap, no marketing.
