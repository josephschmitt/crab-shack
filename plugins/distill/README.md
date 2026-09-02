# distill

You just spent forty minutes with Claude working out why a backup job was silently skipping one volume, and now you actually understand it. Tomorrow that understanding lives in a scrollback nobody will reread. Asking for "a summary" gets you a recap of the chat ("first we looked at X, then you mentioned Y"), and asking for "an article" gets you a general-purpose blog post padded with things you never discussed.

This distills a conversation into a reference note that reads as if it had been written as documentation from the start. It keeps the conclusions, decisions, and reasoning the conversation actually reached, drops the dead ends and the back-and-forth, and adds nothing from outside unless you ask.

## Why you'd use it

The failure mode with "write this up" prompts is expansion. Claude knows a lot about most topics, so a request for an article tends to become the article Claude *could* write about the subject rather than the one your conversation earned. This skill holds a hard line:

- **Conversation-only by default.** No new facts, sources, alternatives, or best practices sneak in. If something wasn't established, it's left out rather than filled in from memory.
- **Latest state wins.** Corrections and revisions replace what they superseded instead of being narrated as history.
- **Impersonal voice.** No "we discussed" or "you asked". The result is documentation, not a transcript.
- **Unresolved stays unresolved.** Open questions are recorded as open, not quietly answered.

When you *do* want outside material, say so in the command and it expands only within that scope.

## Sample usage

After a conversation working through whether a small metrics collector needs Postgres:

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

Anything after `/distill` scopes that one run:

```
/distill keep this very short
/distill include the outside research we just discussed
/distill research the unresolved question first, then incorporate the answer
/distill format this as a troubleshooting reference
```

If you name a destination (a vault, a folder, a file path), the article goes there and follows that destination's conventions. Otherwise you get it inline and, on claude.ai, as a downloadable `.md` file.

## Triggers

"/distill", "write this up", "turn what we learned into an article", "save this to my knowledge vault", "make this a reference note", "make this something I can reference later".

## Install

### Claude Code

```
/plugin marketplace add josephschmitt/crab-shack
/plugin install distill@joes-crab-shack
```

### Claude.ai (web or desktop)

Download [`distill.zip`](https://github.com/josephschmitt/crab-shack/releases/latest/download/distill.zip) from the [latest release](https://github.com/josephschmitt/crab-shack/releases/latest), then in Claude click **+** → **Create skill** and upload the zip.
