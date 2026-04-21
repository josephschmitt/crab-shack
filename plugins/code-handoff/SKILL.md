---
name: code-handoff
description: Packages the current conversation into a handoff document for a fresh coding agent session (Claude Code, Codex CLI, OpenCode, Gemini CLI, or similar). Used when the user says "handoff", "generate handoff", "create a handoff", "hand this off", "hand off to the agent", "hand off to claude code", "hand off to codex", "hand off to opencode", "prep for the agent", "prep for claude code", "move this to the coding agent", "code handoff", "package this up for the agent", or otherwise signals they're ready to move investigatory work from this chat into a coding session. Runs with zero arguments — everything is pulled from the conversation itself.
---

# Code Handoff

## What to do

1. **Review the full conversation.** Identify:
   - The goal (what's being built, investigated, or decided)
   - Decisions already made, with brief rationale
   - Approaches considered and rejected, with why
   - Constraints: tech stack, repo or path names, style conventions, team/org factors
   - Open questions the coding agent should be aware of
   - Any file paths, repo names, library names, commands, or URLs that were mentioned

2. **Synthesize, don't transcribe.** The handoff is not a conversation dump. Pull out what's decided and relevant, drop small talk, dead ends that went nowhere, and clarifications that resolved into decisions (just capture the resulting decision).

3. **Infer concrete starting actions.** Based on what was discussed, suggest specific first moves for the new session:
   - Files or directories to open first (use actual paths if mentioned; otherwise describe what to look for)
   - `rg` or `grep` patterns to locate relevant code (use identifiers, function names, or strings that came up in the conversation)
   - Shell commands to orient (`git log`, `ls`, reading a specific config, checking a dependency version)
   - Docs or library references to consult if a new dependency or API is involved

   Keep the actions tool-agnostic — prefer plain shell commands (`rg`, `git`, `cat`, `ls`) that work in any coding agent's environment rather than commands specific to one agent's toolset.

4. **Self-verify before writing.** Run these checks on the draft:
   - Every Decision MUST have a one-line rationale, not just the decision itself.
   - Every Starting action MUST reference something specific that came up in the conversation (a real path, a real identifier, a real command). If an action is plausible but unverified, replace it with an honest "investigate X" note or delete it.
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

## Starting actions
Concrete first moves for the new session, in order:

1. <action — e.g., `Open src/handlers/channel.ts to understand the existing MCP handler pattern`>
2. <action — e.g., `rg 'registerChannel' --type ts to find all call sites`>
3. <action — e.g., `git log --oneline -20 -- src/handlers/ to see recent changes in this area`>

## First task
<the specific next thing to do after orientation — ideally small and well-defined, not the whole project>

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

## Starting actions
1. `cat app/api/search.py` to see the current handler and response shape.
2. `rg -n '@cached' app/ --type py` to find existing decorator uses and match style.
3. `cat app/cache/__init__.py` to understand the wrapper's API (serialization, key namespacing).

## First task
Add `@cached(ttl=60, key_prefix="search:v1")` to the /api/search handler, verify response serialization is correct, and run the existing endpoint tests to confirm no behavioral regression.
```

What the example does right: Context stays tight at three sentences instead of recapping the whole discussion. Each Decision carries a one-line rationale rather than standing alone. Starting actions use plain shell (`cat`, `rg`), reference real file paths from the conversation, and progress from orientation toward investigation rather than jumping straight to implementation. The First task is one concrete step, not the whole project. The "Approaches considered and rejected" section is omitted entirely because no real alternatives were discussed — that's the thin-section rule in action.

## Output format

After writing the file:

1. Call `present_files` with the handoff path so it's downloadable.
2. Output the full handoff inline as a fenced markdown code block (use four backticks on the outer fence so the inner template fences render correctly).
3. Close with at most one short sentence — e.g., "Ready to paste into your coding agent." No recap, no marketing.
