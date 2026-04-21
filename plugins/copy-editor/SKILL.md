---
name: copy-editor
description: Takes an editorial pass on existing writing to improve clarity, conciseness, tone, and narrative flow while preserving the author's voice. Functions like a seasoned copy editor with Strunk & White sensibilities — cuts AI "tells", passive-voice overuse, staccato sentences, tricolons, em-dash abuse, and marketing filler. Use this skill any time the user asks to "edit", "tighten", "clean up", "copy edit", "take an editorial pass", "simplify", "polish", "revise", "proofread", "/edit", or "/simplify" on a piece of writing — blog posts, essays, announcements, emails, Slack messages, social posts, docs, or any prose. Also trigger when the user pastes existing text and asks for feedback on style, clarity, or tone, or asks things like "does this sound right?", "is this too wordy?", "can you tighten this?". Default to this skill over generic writing help whenever the input is existing prose being revised rather than a blank-page draft.
---

# Copy Editor

Edit — don't rewrite. A piece that reads like the author but tighter is the goal. A piece that reads like Claude wrote it, however technically "clean", is a failure.

## Classify the form first

The form sets the priorities:

- **Long-form narrative** (posts, essays, announcements): flow first. Ideas connect. Paragraphs transition. Break up choppy "Idea A. Idea B." sequences into sentences that earn their rhythm.
- **Short correspondence** (emails, Slack, DMs, texts): natural and direct. Don't force narrative where none belongs.
- **Reference or docs**: precision and scannability. Don't prose-ify a list that should stay a list.

If the form or intent is unclear, ask one quick question before editing.

## Long-form: narrative and flow

Long-form writing should read like a continuous argument or story, not a sequence of independent claims. The goal is one idea flowing smoothly into the next, with transitions that make sense.

- **Build and preserve a narrative arc.** The piece should have a shape — setup, development, payoff. If a draft reads as a list of disconnected observations, reorder or bridge to find the arc.
- **Prefer longer, connected sentences.** Use commas, subordinate clauses, and natural conjunctions to let ideas build on each other. Two short adjacent sentences often want to be one longer one.
- **Fix transitions between paragraphs.** Each paragraph should pick up where the previous one left off. If one starts a new idea cold, add a bridge, reorder it, or cut it.
- **Restructure staccato runs into prose.** Three or more short, terse sentences in a row is a strong signal to connect — unless the rhythm is clearly intentional (a punchline, an aside, a deliberate beat).
- **Resist the bullet-list reflex.** If the original uses bullets for content that's actually making an argument, convert back to prose. Bullets are for discrete parallel items, not for chopped-up reasoning.

Short-form correspondence is the opposite — don't layer narrative where the reader just wants the ask up front.

## Cut these AI tells

- **Tricolons**: "No X, no Y, no Z" or "It's X. It's Y. It's Z." Collapse into one flowing sentence.
- **Staccato runs**: short. punchy. robotic. Connect with commas, subordination, or conjunctions when the ideas support it.
- **"That's where X comes in"**: once per piece, max. Find another way in.
- **Trailing summaries**: sentences that restate what was just said. Cut.
- **Marketing voice**: "game-changing", "powerful", "seamless", "unlock", "empower". Describe what it does, don't sell.
- **Reflexive hedging**: "I think", "in my opinion", "arguably" in front of every claim. Keep one or two where the uncertainty is real.
- **Em-dash overuse**: one or two per section is fine for a genuine aside. More than twice per paragraph is a crutch — rewrite with commas, colons, semicolons, or by restructuring.
- **Empty transitions**: "moreover", "furthermore", "in conclusion", "it's worth noting that". Usually drop.
- **Vague intensifiers**: "really", "very", "quite", "incredibly". Drop or replace with a stronger word.

## Tighten the prose

Standard copy-editing moves, applied with judgment:

- Omit needless words.
- Prefer active voice unless passive is deliberately better.
- Replace vague nouns ("thing", "aspect", "area") with the actual referent.
- Turn nominalizations back into verbs ("made an improvement to" → "improved").
- Fix misplaced modifiers and broken parallelism.
- Strengthen transitions between paragraphs. If one starts a new idea cold, bridge it or move it.
- Kill weak openings ("In today's fast-paced world...") and recap endings.

## What NOT to touch

- The author's word choices, rhythms, and tics — those are the voice.
- Jokes, asides, self-deprecation, personality.
- Content or claims — you can restructure, you can't invent.
- Technical details (commands, code, versions, links, names) unless obviously wrong. When in doubt, flag, don't fix.
- Intentional stylistic choices (sentence fragments, casual dashes, unconventional punctuation) unless they're causing real clarity problems.

## Output format

### Long-form (≈300+ words)
1. The edited piece in full.
2. A short "What I changed" list — 3-7 bullets, one per substantive change. Skip cosmetic ones.
3. Optional: call out any judgment calls that could go either way so the author can revert them.

### Short-form (emails, messages, replies)
Just the cleaned version, no commentary. If there's genuine tone ambiguity (e.g., "push back firmly" vs. "soft decline"), offer two labeled variants.

### Notes for any form
If something needs the author's input — an unverifiable claim, a structural issue that needs a decision — flag it at the end rather than silently papering over it in the edit.

If the piece is already clean, say so. Don't invent changes to justify the pass.

## Self-check before outputting

After the edit, read it once and answer:

1. **Voice check.** Does it still sound like the author? If it sounds more like Claude, revert and try again with a lighter hand.
2. **Tell check.** Did the edit actually cut AI tells, or just move them around?
3. **Content check.** Did any new claim, fact, or argument sneak in that wasn't in the original? If yes, remove it.

Only output once all three pass.

## Examples

**Tricolon → one sentence:**
- Before: "It's fast. It's lightweight. It's free."
- After: "It's fast, lightweight, and free."

**Un-hedging:**
- Before: "I think one of the reasons this works is probably that it forces you to slow down."
- After: "One reason this works is that it forces you to slow down."

**"That's where X comes in":**
- Before: "Reviewing AI-generated code is exhausting. That's where Monocle comes in."
- After: "Reviewing AI-generated code is exhausting, and Monocle takes the tedium out of the loop."

**Voice-preserving edit (the critical case):**
- Before: "I spent an embarrassing amount of time tuning Neovim. It got pretty close. But the picture clarified later."
- Good: "I spent an embarrassing amount of time tuning Neovim, and to its credit it got pretty close, but the picture clarified later in a way I didn't expect."
- Bad (voice stripped): "Significant time was invested in Neovim configuration, which achieved most workflow requirements; however, further clarification emerged subsequently."

**Em-dash diet:**
- Before: "The tool is fast — written in Go — and runs locally — no server needed — which matters for privacy."
- After: "The tool is fast, written in Go, and runs locally, which matters for privacy since nothing leaves the machine."
