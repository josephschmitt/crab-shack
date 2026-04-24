# Plugin README guidance

Each plugin's `README.md` is a product page, not a spec sheet. Before anyone installs this thing, the README has to answer the only question they actually care about: *why should I give a shit about this?*

If the reader finishes the first paragraph and still doesn't know what the plugin does for them, the README has failed — no matter how thorough the feature list below is.

## What every plugin README should cover

In roughly this order:

1. **The hook (1–2 sentences).** Open with the pain or the payoff. A specific scenario the reader recognizes beats any abstract description. Skip the restated one-liner from the marketplace manifest.
2. **What it does.** Concrete behavior, not a reworded name. What does invoking this skill actually produce?
3. **Why you'd use it.** The specific problem it solves or the annoying default it replaces. A short "the naive approach fails because…" framing usually lands better than a benefits list.
4. **Sample usage.** At least one worked example: a trigger phrase, an input, and a sketch of the output. Show, don't claim. Real examples do more work than three paragraphs of adjectives.
5. **Triggers.** The natural phrases that invoke the skill, so a reader knows how to use it once installed. A single line is enough.
6. **Install.** Claude Code and Claude.ai instructions, kept at the bottom where they belong.

Sections can combine or reorder if the plugin calls for it. The checklist isn't a template — it's a floor.

## Voice

- Write for a skeptical reader, not one who already bought in.
- Describe what it does; don't promise what it unlocks.
- Short paragraphs, plain sentences, concrete nouns. Examples beat adjectives.
- Keep personality. A dry joke or a pointed opinion beats a bulleted list of benefits.
- Match the copy-editor skill's sensibilities: no tricolons, no "that's where X comes in", no em-dash pileups, no marketing voice ("game-changing", "seamless", "powerful", "unlock").

## What to avoid

- Feature dumps without context. A capability list isn't a reason to install.
- Three restatements of the skill's description.
- Hedged claims ("can help with…", "may be useful for…"). Commit to the value or cut the line.
- Install boilerplate before the reader knows why they'd bother.
- Screenshots or diagrams that don't add something a sentence can't.

## A good opening vs. a weak one

**Weak:** "copy-editor is a skill that helps you improve your writing by making editorial passes to fix common issues."

**Better:** "You wrote something. It's fine. But it reads like every other LLM post on the internet — tricolons, staccato sentences, em-dashes everywhere. You want to tighten it without losing your voice."

The first tells the reader what the skill *is*. The second tells them why they already need it.
