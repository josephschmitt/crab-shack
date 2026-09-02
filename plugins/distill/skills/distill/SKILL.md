---
name: distill
description: Distills a conversation, research thread, or set of discoveries into a durable, impersonal knowledge-base article that keeps only what the conversation actually established. Use when the user invokes /distill (or mentions the skill as `$distill` or `@distill` on harnesses that use those), or says "write this up", "turn what we learned into an article", "save this to my knowledge vault", "make this a reference note", or "make this something I can reference later". It distills rather than expands, adding no outside research or general knowledge unless the user explicitly asks for it.
---

# Knowledge Distiller

Turn the useful substance of a conversation into reference material that still makes sense once the conversation is gone.

The goal is **distillation, not expansion**. Produce the article the conversation already earned, not the broader article that could be written about the topic in general.

## Invocation

`/distill` alone (or the equivalent skill mention on the current harness, such as `$distill` in Codex or `@distill` in ChatGPT) means: distill the current conversation using the defaults below. Text after the command scopes that one run:

```text
/distill keep this very short
/distill focus only on the final recommendation and rationale
/distill include the outside research we just discussed
/distill research the unresolved question first, then incorporate the answer
/distill format this as a troubleshooting reference
```

A narrow override does not relax unrelated defaults. Permission to research one unresolved detail is not permission to enrich the rest of the article.

If the conversation covers several unrelated subjects and the request does not say which, ask whether to distill one of them or produce a separate article per subject. Do not merge unrelated subjects into one note.

## Source boundary

The conversation is the only source by default. That includes facts, conclusions, decisions, examples, and constraints established in it; material from files, links, searches, or tools already used in it; and the user's corrections, measurements, and later clarifications.

Do not add facts from general knowledge, new research or sources, alternatives that were never discussed, or inferences presented as established. When unsure whether something was actually established, leave it out rather than completing it from memory.

Cross this boundary only when the user explicitly asks for research, outside context, gap-filling, fact-checking, or other enrichment, and then only as far as the request requires. Newly introduced claims follow normal research and citation practice. Integrate them naturally unless the user asks for them to be labeled or kept separate.

## Distillation rules

1. **Keep the durable knowledge:** conclusions, decisions, rationale, constraints, tradeoffs, and procedures that would still matter later.
2. **Use the latest state.** When a point was corrected or revised, keep only the final version unless the history explains a tradeoff that matters.
3. **Compress dead ends.** Drop abandoned options, exploratory questions, and back-and-forth unless they explain the final conclusion.
4. **Keep the reasoning that matters.** Preserve enough of *why* a decision was reached, especially when it rests on constraints or tradeoffs.
5. **Leave unresolved questions unresolved.** Say so plainly; do not settle them from memory.
6. **Do not pad.** No generic background, definitions, glossaries, checklists, or a "Conclusion" section the conversation did not earn.
7. **Say each thing once,** in the section where it is most useful.

A short conversation produces a short note. Fidelity beats completeness.

## Voice

Write impersonal documentation, not a recap of a chat. Never say "we discussed", "you asked", "I recommended", or "in this conversation", and avoid first and second person unless the subject genuinely requires it. State what the source supports directly and confidently, in plain language, with prose for explanation and bullets only where they help scanning. Do not cite the chat itself.

## Shape

Derive the structure from the material rather than forcing a template. A typical article:

```markdown
# [Specific, searchable title: the subject and its main takeaway]

[Optional short opening that establishes the subject and the main point.]

## [Major topic or decision]
[Concise explanation, including the reasoning that matters.]

## [Next major topic]
[Relevant details, tradeoffs, or procedure.]

## [Implementation / plan / open items]
[Only when the conversation actually established these.]
```

Use as few sections as the material needs. Headings name the subject, not the section's role ("Why WAL mode is enough" rather than "Background").

When the conversation reached a decision or recommendation, state the chosen direction, the reasons it won, and any conditions, thresholds, or triggers attached to it. Mention rejected alternatives only when the comparison helps understand the choice later, and never turn tentative discussion into a firm decision.

Keep links and citations from the conversation only when they have lasting reference value.

## Delivery

- If the user named a destination (a vault, folder, file path, or tool), deliver the article there and follow that destination's conventions, including frontmatter if it expects any.
- Otherwise return the article inline as a fenced Markdown block, and where the environment supports file outputs (such as `/mnt/user-data/outputs/` on claude.ai) also save it as `<slug-from-title>.md`.
- Keep commentary around the article to a sentence or two. The user asked for the article, not a description of it.

## Fidelity check

Before returning, verify silently:

- Every claim traces to the conversation, material already used in it, or outside information the user explicitly authorized.
- Superseded details are gone or clearly contextualized.
- Conversational scaffolding is gone.
- Important rationale and tradeoffs survived the compression.
- Open questions are still open.
- Nothing is repeated, and the article is no longer than the knowledge requires.

Remove any sentence that fails the first check.
