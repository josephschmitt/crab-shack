# copy-editor

You wrote something. It's fine. But it reads like every other LLM post on the internet — tricolons everywhere, staccato punch-lines, a dozen em-dashes, and somewhere near the bottom the inevitable "that's where X comes in." You want it tightened without it coming back sounding like Claude wrote it.

This takes an editorial pass on prose you already have: cuts the AI tells, kills filler, fixes passive voice, and leaves your jokes, rhythms, and tics alone. It edits. It doesn't rewrite.

## Why you'd use it

"Edit this" prompts tend to produce one of two outcomes:

- A version that's technically cleaner but sounds nothing like you.
- A version that's longer than the original because Claude decided to "polish" it.

This skill optimizes for the opposite — preserve voice, cut filler, ship it shorter than it started. It applies Strunk & White basics (omit needless words, active voice, concrete nouns) plus a hit list of modern AI tells: tricolons, "that's where X comes in", em-dash pileups, trailing summaries, staccato runs, marketing voice, reflexive hedging. It also checks itself before outputting — if the edit accidentally stripped your voice or added a claim that wasn't there, it reverts.

## Sample usage

Paste some prose and ask for an edit:

> **You:** Edit this. "Our new tool is fast. It's lightweight. It's free. That's where Monocle comes in — a truly game-changing way to empower developers and unlock powerful workflows."
>
> **Claude:** "Monocle is fast, lightweight, and free. It gives developers a smaller, cheaper tool for the same workflows they already have."
>
> *What I changed:*
> - Collapsed the "It's X. It's Y. It's Z." tricolon into one sentence.
> - Cut "that's where X comes in."
> - Replaced the marketing voice ("game-changing", "empower", "unlock powerful") with what the tool actually does.

On long-form pieces it returns the full edit plus a short "what I changed" list. On emails, Slack messages, and other short correspondence it returns just the cleaned version, no commentary — with two variants when tone is genuinely ambiguous (firm pushback vs. soft decline).

Works on blog drafts, announcements, launch posts, essays, README intros, cold emails, Slack messages — any prose that's already written and wants a once-over without losing its personality.

## Triggers

"edit this", "tighten this up", "copy edit", "take an editorial pass", "is this too wordy?", "does this sound right?", or paste some text and ask what could be better.

## Install

### Claude Code

```
/plugin marketplace add josephschmitt/crab-shack
/plugin install copy-editor@joes-crab-shack
```

### Claude.ai (web or desktop)

Download [`copy-editor.zip`](https://github.com/josephschmitt/crab-shack/releases/latest/download/copy-editor.zip) from the [latest release](https://github.com/josephschmitt/crab-shack/releases/latest), then in Claude click **+** → **Create skill** and upload the zip.
