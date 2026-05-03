# call-notes

You got off a 45-minute call with the contractor. Your phone has a transcript ready. You scroll through it once, lose track of what was actually decided versus what was just floated, and realize you'll never read this thing again. The price quote is in there somewhere. So is whatever you agreed to send him. Good luck finding either next week.

This takes a raw call transcript and gives you back the write-up you'd hand a coworker after the meeting: a one-paragraph summary, the decisions, the action items with owners, the specifics worth remembering, and what's still open. Notes you can scan in 30 seconds, not a cleaner version of the wall of text you started with.

## Why you'd use it

Asking Claude to "summarize this call" without a skill produces one of two outputs:

- A polite recap that reads like a blog post, in chronological order, burying the action items in paragraph three.
- A bullet list of every topic mentioned, weighted equally, so the actual decisions are mixed in with the small talk.

This skill optimizes for the use case behind the request: reference material you'll come back to. Decisions live in their own section. Action items have owners and dates. Notable details — names, prices, phone numbers, recommendations — get their own bucket so the contractor's number doesn't get lost between two unrelated bullets. Speaker attribution stays honest: if the transcript says "Speaker 2", the notes don't pretend it was Mike.

It also handles the messy reality of real transcripts. Filler gets cut. Crosstalk gets ignored. Tangents get dropped unless they surface a real follow-up. Transcription errors that look like errors get flagged instead of silently "corrected."

If you paste a scoring template or checklist alongside the transcript, the skill maps the conversation to that structure instead — pre-filling what it can, suggesting scores with rationale, and flagging what the transcript didn't cover.

## Sample usage

Paste a transcript and ask for notes:

> **You:** Notes from this call please.
>
> *[transcript pasted: 30 minutes with a contractor about a kitchen remodel]*
>
> **Claude:**

```markdown
# Call with Mike Reyes re: kitchen reno estimate (May 2)

## Summary
30-minute call with Mike Reyes (Reyes Construction) walking through the kitchen scope. Mike quoted $42K for the base bid with a 6-8 week lead time once signed. Decision pending after Sarah reviews the line items this weekend.

## Key points
- Scope: full gut, new cabinets, quartz counters, keep existing footprint
- Mike pushed back on relocating the sink — would add ~$3K for plumbing rerouting
- Two cabinet options on the table: Shaker (in-budget) vs. inset (+$4K)
- Permit timeline is the long pole — town is running 3-4 weeks on kitchen permits

## Decisions made
- Keep the existing sink location to stay in budget
- Quartz over butcher block for counters (durability with two kids)

## Action items
- **Mike** — send itemized line-item bid by Friday (May 5)
- **Mike** — send three recent kitchen references with photos
- **Joe** — review line items with Sarah over the weekend
- **Joe** — confirm cabinet choice (Shaker vs. inset) by Monday

## Notable details
- Mike Reyes, Reyes Construction, (508) 555-0142
- Base bid: $42,000. Inset cabinet upgrade: +$4,000. Sink relocation: +$3,000
- Recommended tile vendor: Stonewood in Natick
- Lead time: 6-8 weeks from signed contract
- Permit timeline: 3-4 weeks (town backlog)

## Follow-ups
- Schedule walkthrough for Sarah once line-item bid arrives
- Mike will pull permit on our behalf if we move forward

## Open questions
- Whether the existing electrical panel can handle the new induction range — Mike flagged uncertainty, said his electrician would need to look
```

Paste a scoring rubric alongside an interview transcript and the output uses the rubric's sections instead of the default — pre-filled with evidence and a suggested score per dimension, with anything the call didn't cover flagged as `N/A — not discussed`.

## Triggers

"call notes", "meeting notes", "notes from this call", "summarize this call", "write this up", "extract action items", "what came out of this", or paste a transcript and ask for a summary. Also "/call-notes".

## Install

### Claude Code

```
/plugin marketplace add josephschmitt/crab-shack
/plugin install call-notes@joes-crab-shack
```

### Claude.ai (web or desktop)

Download [`call-notes.zip`](https://github.com/josephschmitt/crab-shack/releases/latest/download/call-notes.zip) from the [latest release](https://github.com/josephschmitt/crab-shack/releases/latest), then in Claude click **+** → **Create skill** and upload the zip.
