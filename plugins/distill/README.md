# distill

Turns a conversation into a reference note. It keeps the conclusions, decisions, and reasoning the conversation actually reached, drops the back-and-forth, and adds nothing from outside unless you ask.

## What it does

- Uses only what the conversation established. No new facts, sources, or alternatives from general knowledge.
- Keeps the latest state. Corrections replace what they superseded.
- Writes in an impersonal documentation voice, not "we discussed" or "you asked".
- Leaves unresolved questions unresolved.

Anything after the command scopes that run:

```
/distill
/distill keep this very short
/distill focus only on the final recommendation and rationale
/distill include the outside research we just discussed
/distill format this as a troubleshooting reference
```

Name a destination (a vault, folder, or file path) and the article goes there following that destination's conventions. Otherwise it comes back inline and, on claude.ai, as a downloadable `.md` file.

## Sample output

After a conversation about whether a small metrics collector needs Postgres:

> **You:** /distill focus on the final decision and why
>
> **Claude:**
> ```markdown
> # Running the metrics collector on SQLite instead of Postgres
>
> The collector writes roughly 200 rows a minute from a single process and is only
> queried by its own dashboard, so a shared Postgres instance adds an operational
> dependency without buying anything. SQLite in WAL mode handles the write rate with
> headroom and keeps the deployment to a single container.
>
> ## When to revisit
>
> Move to Postgres if a second writer appears or if dashboard queries start needing
> more than the last 30 days of data. Retention beyond that was left undecided.
> ```

## Triggers

`/distill` (`$distill` in Codex, `@distill` in ChatGPT), "write this up", "turn what we learned into an article", "make this a reference note", "make this something I can reference later".

## Install

### Claude Code

```
/plugin marketplace add josephschmitt/crab-shack
/plugin install distill@joes-crab-shack
```

### Claude.ai (web or desktop)

Download [`distill.zip`](https://github.com/josephschmitt/crab-shack/releases/latest/download/distill.zip) from the [latest release](https://github.com/josephschmitt/crab-shack/releases/latest), then in Claude click **+** → **Create skill** and upload the zip.
