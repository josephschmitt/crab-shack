# code-handoff

You spent an hour on your phone in Claude.ai working through a problem. You've got a plan, a stack of decisions, constraints that took real thought to settle. Now you want to continue in Claude Code (or Codex, OpenCode, Gemini CLI, whatever) and you're staring at a blank terminal wondering how much of the conversation to paste.

This packages the chat into a structured handoff document — objective, decisions with rationale, constraints, open questions, and pointers to the code that came up — so the next agent starts with the understanding you already built instead of re-litigating it.

## Why you'd use it

The default options for moving context between a chat and a coding agent both fail:

- **Paste too little** and the new agent reopens decisions you already made, asks for context you already established, and drags you back through the same loop.
- **Paste the whole conversation** and it drowns in small talk, dead ends, and clarifications that resolved into decisions three messages later.

The handoff synthesizes rather than transcribes. Every decision carries a one-line rationale so the coding agent knows *why* it was made and won't try to revisit it. It stops at knowledge transfer: it captures what was decided, not how to build it, and it won't invent an approach or prescribe first steps the coding agent should pick for itself with the full repo in front of it. References point at the paths and identifiers that actually came up, nothing guessed. Thin sections get dropped rather than padded. The output is a single markdown block you can copy directly on mobile.

## Sample usage

After a long planning conversation on your phone:

> **You:** Hand this off to Claude Code.

The skill writes `handoff.md` and prints it inline:

````markdown
# Handoff: Redis caching for /api/search endpoint

## Objective
Add Redis-backed result caching to /api/search, which hits the primary DB on every request and times out under load.

## Context
Production p95 latency crossed 2s last week. Tracing showed identical full-text queries repeating seconds apart. Short-TTL caching should bring common searches under 100ms.

## Decisions already made
- **Redis over Memcached**: Redis is already deployed for session storage; no new dependency.
- **Key format `search:v1:{sha256(normalized_query)}`**: versioned so the prefix can be bumped on a future schema change.
- **TTL: 60 seconds**: short enough to dodge staleness complaints, long enough to absorb bursts.

## Constraints
- **Tech stack:** Python 3.11, Flask, SQLAlchemy, redis-py already pinned.
- **Codebase:** `app/api/search.py` for the route; `app/cache/` is the existing Redis wrapper.
- **Style:** existing wrappers use a `@cached(ttl=...)` decorator — match it.

## Relevant references
- `app/api/search.py` — the /api/search route handler under discussion.
- `app/cache/` — existing Redis wrapper; uses a `@cached(ttl=...)` decorator worth matching.
````

Paste that into a fresh coding session and the next agent has the scope and the reasoning without you re-typing any of it — then it plans the actual work with the repo in front of it.

## Triggers

"handoff", "generate handoff", "hand this off", "hand off to Claude Code", "hand off to Codex", "prep for the agent", "move this to the coding agent".

## Install

### Claude Code

```
/plugin marketplace add josephschmitt/crab-shack
/plugin install code-handoff@joes-crab-shack
```

### Claude.ai (web or desktop)

Download [`code-handoff.zip`](https://github.com/josephschmitt/crab-shack/releases/latest/download/code-handoff.zip) from the [latest release](https://github.com/josephschmitt/crab-shack/releases/latest), then in Claude click **+** → **Create skill** and upload the zip.
