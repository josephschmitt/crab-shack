# code-handoff

Packages the current conversation into a structured handoff document for a fresh coding agent session. Use it when you're done investigating in Claude.ai and want to continue in Claude Code, Codex CLI, OpenCode, or any other coding agent — it synthesizes decisions, constraints, and concrete first steps so you don't have to re-explain context.

**Trigger:** Say "handoff", "generate handoff", "hand this off", or similar.

## Install

### Claude Code

```
/plugin marketplace add josephschmitt/crab-shack
/plugin install code-handoff@joes-crab-shack
```

### Claude.ai (web or desktop)

Download [`code-handoff.zip`](https://github.com/josephschmitt/crab-shack/releases/latest/download/code-handoff.zip) from the [latest release](https://github.com/josephschmitt/crab-shack/releases/latest), then in Claude click **+** → **Create skill** and upload the zip.
