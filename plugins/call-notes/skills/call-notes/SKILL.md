---
name: call-notes
description: Turns a raw call or meeting transcript into structured, actionable notes — not a cleaned-up transcript, but actual notes with summary, key points, decisions, action items, follow-ups, and notable details. Triggers when the user pastes a transcript (from iOS call recording, Zoom, FaceTime, Otter, in-person recording, or anywhere else) and asks for "notes", "call notes", "meeting notes", "summary", "write this up", "structure this", "TL;DR this call", "what came out of this", "extract action items", "/call-notes", or otherwise signals they want a structured write-up of a recorded conversation. Also supports an optional template mode — if the user pastes a scorecard, checklist, or structured form alongside the transcript, the skill maps the conversation to that structure instead of the default.
---

# Call Notes

Turn a raw transcript into the kind of write-up a sharp EA would hand you after sitting in on the call. The goal is reference material the user can scan in 30 seconds, not a polished retelling and not a reformatted transcript.

## What this skill is for

The user records calls (phone, FaceTime, Zoom, in-person) and ends up with a wall of transcript text. They want:

- The substance, organized by topic — not a chronological replay.
- Decisions, action items, and follow-ups pulled out cleanly so nothing falls through the cracks.
- Specific details worth remembering — names, numbers, prices, dates, recommendations.
- Honesty about what's uncertain (who said what, ambiguous commitments, garbled audio).

What this skill is **not**: a cleaned-up transcript, a verbatim summary, or a creative retelling. If the output reads like prose paragraphs about the call, it's wrong.

## When to invoke

Trigger when the user pastes a block of transcript text (typically with timestamps, speaker labels like "Speaker 1:", or obvious conversational back-and-forth) and asks for any of: notes, a summary, a write-up, action items, decisions, "what came out of this", or pastes silently with the expectation that the skill will recognize it.

If the input is short (a few lines) or doesn't look like a transcript, ask before processing. Don't assume.

## Default output structure

Use this structure unless the user provides a template. Omit a section entirely if the call produced nothing for it — don't pad. A two-person call about a contractor estimate doesn't need an "Open questions" section just for symmetry.

```markdown
# <descriptive title — e.g., "Call with Mike Reyes re: kitchen reno estimate (May 2)">

## Summary
<2-3 sentences. What the call was about, who was on it (if known), and the headline outcome. No fluff.>

## Key points
- <substantive thing discussed, organized by topic not chronology>
- <next topic>
- <...>

## Decisions made
- <decision>: <one-line context if needed>
- <...>

## Action items
- **<owner>** — <what they're doing> (by <date if mentioned>)
- **<owner>** — <...>

## Notable details
- <name, number, price, recommendation, date — anything specific worth remembering>
- <...>

## Follow-ups
- <thing that needs to happen next, or a question left open>
- <...>

## Open questions
- <unresolved item or thing that needs clarification>
- <...>
```

### Title

Make it specific enough to find later. "Call notes" is useless. "Call with Mike Reyes re: kitchen reno estimate" is findable. Include the date if it's evident from the transcript or the user mentions it; otherwise skip.

### Summary

Two or three sentences max. The first sentence states the topic and participants. The second states the headline outcome ("agreed on a $42K bid, decision pending wife's review"). A third is fine if there's a meaningful nuance, but resist the urge to expand.

### Key points

Organize by topic, not chronology. Calls jump around — the notes shouldn't. If three different points about pricing came up at minutes 4, 17, and 38, group them under one bullet. Use short phrases, not full sentences. Sub-bullets are fine when one point has obvious sub-items.

### Decisions made

Anything that was actually agreed on or committed to. "We'll go with the cedar option" is a decision. "Cedar might be nice" is a key point. If a decision has a stated rationale on the call, include it briefly. If it doesn't, don't invent one.

### Action items

Format: **Owner** — what — by when. Use the actual name from the transcript when known, "Joe" if it's clearly the user, or "Unclear" if the transcript doesn't make it obvious. Don't fabricate owners. Don't invent deadlines — only include dates that were actually said.

### Notable details

The catch-all for specifics worth keeping: a contractor's name and phone number, a price quote, a recommended product, a vendor referral, a measurement, an address. This is often the most useful section months later — be generous with what you capture here, as long as it's actually in the transcript.

### Follow-ups

Things that need to happen next that aren't owned action items — pending information, scheduled next steps, "we'll circle back after she hears from her sister." If there's an obvious next conversation or milestone, name it.

### Open questions

Genuinely unresolved items. Distinct from follow-ups: a follow-up is a planned next step; an open question is something nobody has an answer to yet. If the call surfaced no real ambiguity, drop the section.

## Template mode

If the user provides a scorecard, checklist, evaluation rubric, or structured form alongside the transcript, **use that structure instead of the default**. Don't append the default after the templated output — replace it.

How to handle templates:

1. **Map the transcript to the template's structure.** Pre-fill every field you can support with evidence from the transcript.
2. **Quote or paraphrase briefly** when filling a field, so the user can see why you scored it that way. Short evidence beats long evidence.
3. **Suggest scores when the template asks for them**, with a one-line rationale. The user can override — that's expected. Better to take a position than to dump evidence and make them score from scratch.
4. **Flag what you can't determine.** If the template asks about something the transcript doesn't cover, say so explicitly: `Score: N/A — not discussed on this call`. Don't guess.
5. **Preserve the template's section order and naming** — don't reorganize it to match your preferences.

If a template is provided but is ambiguous or missing context (e.g., a scoring scale isn't defined), ask one quick question before filling it in.

## Speaker attribution

Transcripts vary wildly in quality. Handle speakers honestly:

- **If speaker labels are present and seem reliable** (e.g., "Joe:" / "Mike:" used consistently), use names in attribution: "Mike said the lead time is 6-8 weeks."
- **If labels are generic** ("Speaker 1", "Speaker 2"), use the user's best guess if context makes it obvious (the user is likely the one who said "we" about their own house, etc.) but flag uncertainty: "Speaker 2 (likely the contractor) quoted $42K."
- **If attribution is genuinely unclear**, don't fabricate. Either drop the attribution and state the fact ("Lead time is 6-8 weeks") or flag it ("Someone — unclear who — committed to sending references").
- **Never invent names.** If the transcript only has "Speaker 1", don't decide it's "Mike" because the user mentioned a Mike earlier in conversation. Ask if you need to.

## Voice and density

- Bullet points and short phrases. Reference material, not prose.
- Concrete nouns over abstractions. "$42K bid" not "a substantial estimate."
- No editorializing. The notes capture what happened; they don't comment on it.
- No filler ("It's worth noting that...", "Interestingly...", "The participants discussed..."). Cut.
- No marketing voice. This isn't a recap blog post.
- One bullet per point. If a bullet runs three lines, it's two bullets.

## Handling messy inputs

Real transcripts are dirty. Common issues and how to handle them:

- **Filler and crosstalk** ("yeah, yeah", "right, right, exactly", false starts): ignore. The notes capture meaning, not text.
- **Transcription errors** (homophones, garbled names, misheard numbers): if a name or number looks wrong, flag it: `Mike Reyes (transcription unclear — could be "Reyez")`. Don't silently correct.
- **Long tangents** (small talk, off-topic stretches): omit. If something off-topic surfaces a real follow-up ("oh, send me that book recommendation"), capture just the follow-up.
- **Very long transcripts** (60+ minutes): the structure is the same — group by topic, not chronology. Length of the notes scales with substance, not with transcript length. A 90-minute call with three real decisions produces shorter notes than a 20-minute call with twelve action items.
- **Missing context** (the call references "the email from yesterday" or "what we talked about last time"): note it as an open question or follow-up rather than guessing.

## Self-check before outputting

After drafting the notes, run through:

1. **Is anything fabricated?** Every action item, decision, and notable detail must trace back to the transcript. If you can't point to where it came from, cut it.
2. **Are the sections actually distinct?** Action items aren't decisions aren't follow-ups. If the same item appears in two sections, pick one.
3. **Is anything padded?** A section with one weak bullet should be folded into another section or dropped.
4. **Would the user be able to act on this in 30 seconds?** If the notes need a re-read to extract what's actionable, restructure.
5. **Are speaker attributions honest?** No invented names, no over-confident guesses on "Speaker 1 vs Speaker 2."

If any check fails, fix before outputting.

## Output

Output the notes inline as markdown. No preamble ("Here are the notes from your call:"), no closing summary ("Let me know if you'd like me to adjust anything!") — just the notes. The user pasted a transcript to get notes back; deliver them and stop.

If the call type strongly suggests a useful follow-up the user might want (e.g., a calendar reminder for a deadline mentioned, a draft email to one of the action item owners), offer it as a single short line at the end: "Want me to draft the follow-up email to Mike?" One offer, not a menu.
