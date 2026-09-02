# writing-clearly-and-concisely

Your agent writes a lot of prose nobody asked it to polish: commit messages, README sections, error strings, PR descriptions, the explanation at the end of every task. Most of it is padded, passive, and vague in the way LLM output tends to be. Strunk fixed this in 1918, in about twelve thousand words.

This is a copy of Jesse Vincent's [`writing-clearly-and-concisely`](https://github.com/obra/the-elements-of-style) skill, packaged for this marketplace. It gives the agent the full text of William Strunk Jr.'s *The Elements of Style* and tells it to apply the rules whenever it writes sentences a human will read.

## What it does

The skill file itself is short. It lists all eighteen of Strunk's rules at a glance (use the active voice, omit needless words, put statements in positive form, keep related words together) and points to `elements-of-style.md`, the complete 1918 text with the "Words and Expressions Commonly Misused" glossary. The agent reads the full reference only while drafting or editing prose, since it costs roughly 12,000 tokens.

When context is tight, the skill tells the agent to write the draft on its own judgment, then hand the draft and the reference to a subagent for the copyedit.

## Why you'd use it

You could tell the agent "write clearly" and hope. The trouble is that "clearly" has no content on its own, so the model falls back on its defaults, which is how you get "In order to facilitate the utilization of" instead of "to use". Strunk's rules are specific enough to act on: rule 13 says omit needless words and gives the offending phrases by name, and rule 12 says prefer the concrete to the abstract and shows the before and after.

This pairs well with `copy-editor` from the same marketplace. That one edits prose you already wrote. This one shapes what the agent writes in the first place.

## Sample usage

The agent picks it up on its own. Ask for a commit message and the difference looks like this:

> **Before:** "This commit makes changes to the retry logic in order to address an issue where requests were not being retried in some cases."
>
> **After:** "Retry failed requests on connection reset. The old check only caught timeouts."

Or ask for it directly:

> **You:** Rewrite this error message using the writing-clearly-and-concisely skill: "An error has occurred while attempting to process your request. Please try again at a later time."
>
> **Claude:** "Request failed. Try again in a few minutes."

## Triggers

The agent loads it whenever it writes documentation, commit messages, error text, reports, or explanations. You can also invoke it by name, or ask to "apply Strunk" or "tighten this per Elements of Style".

## Source and license

The skill and its reference text come from [obra/the-elements-of-style](https://github.com/obra/the-elements-of-style). The 1918 text is public domain, taken from [Project Gutenberg #37134](https://www.gutenberg.org/files/37134/37134-h/37134-h.htm).

## Install

### Just the skill

Works in Claude Code, Cursor, Codex, Copilot, and most other agents. Copies only the skill folder, no plugin wrapper:

```
npx skills add josephschmitt/crab-shack --skill writing-clearly-and-concisely
```

### Claude Code

```
/plugin marketplace add josephschmitt/crab-shack
/plugin install writing-clearly-and-concisely@joes-crab-shack
```

### Claude.ai (web or desktop)

Download [`writing-clearly-and-concisely.zip`](https://github.com/josephschmitt/crab-shack/releases/latest/download/writing-clearly-and-concisely.zip) from the [latest release](https://github.com/josephschmitt/crab-shack/releases/latest), then in Claude click **+** → **Create skill** and upload the zip.

### Codex / ChatGPT

```
codex plugin marketplace add josephschmitt/crab-shack
```

Then install **Writing Clearly And Concisely** from the plugin directory.

### Cursor

Add `josephschmitt/crab-shack` under **Customize → Plugins**, or clone the repo and copy `plugins/writing-clearly-and-concisely` into `~/.cursor/plugins/local/`.
