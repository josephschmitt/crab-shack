# task-capture

Someone asks you for something in a Slack thread. You say "sure, I'll take a look," and the thread scrolls out of sight. Three days later you remember there was a thing, but not who asked, what they wanted, or where the link was.

Say "track this" and this skill turns that message into a Linear issue. It gets the title, the ask, the person who made it, the links, and a suggested project. It shows you the draft first, and nothing is created until you say so.

## Why you'd use it

Filing the issue by hand means copying a link, retyping the ask, remembering who said it, and picking a team and project. That is just enough friction that the task stays in your head instead.

Asking Claude to "make a Linear ticket for this" works, but the result is inconsistent. You tend to get a vague title, the whole message pasted into the description, the link buried in prose, and a duplicate of something you filed last week.

This skill fixes those specific problems:

- **Titles describe the action**, not the conversation. "Review the tech spec for the email template," not "Request from Slack."
- **Links become attachments** on the issue, not text in the description. The source thread stays one click away.
- **It checks for duplicates** before drafting, and offers to update the existing issue instead.
- **Status defaults to your backlog.** A captured task is a reminder, not a commitment. It only moves up if you say you're doing it soon or right now.
- **PR work is titled after what the PR builds**, never "Merge ...". Merging is part of the process, not the goal.

## Sample usage

You're looking at a Slack thread where a teammate asks if you can review their spec by Friday.

> **You:** Track this.
>
> **Claude:**

```
Team:       Engineering
Project:    Spec Reviews (matches: a design doc awaiting review)
Title:      Review Sam's tech spec for the email template
Status:     Backlog
Priority:   None
Assignee:   me
Due:        Friday
Links:      Slack thread (#eng-design)

Description:
Sam asked in #eng-design for a review of the email template tech spec
before Friday's planning meeting.

> "Can you take a look at the spec by Friday? Mostly want a sanity check
> on the retry approach."
```

> **You:** Looks good, create it.
>
> **Claude:** Created ENG-412: https://linear.app/example/issue/ENG-412

If you don't paste anything, the skill can look at what you were just working on through the Dayflow MCP or CLI, when you have it. Without that, it asks you to paste the message, share a link, or attach a screenshot.

## Setup

The skill needs a Linear MCP server connected. There's nothing to configure. On first use it reads your teams and statuses from Linear, asks only what it can't work out (usually which team is your personal one), and remembers the answers if your agent has persistent memory. Without memory, it looks them up each time.

Project routing is optional. By default the skill reads your team's active projects from Linear and picks the closest match. If you want a hard rule ("anything about billing goes to Payments"), tell it and it will remember that too.

## Triggers

"track this", "create a task", "add this to Linear", "file this", "make an issue for this", or any similar request to capture something in Linear. Also "/task-capture".

## Install

### Just the skill

Works in Claude Code, Cursor, Codex, Copilot, and most other agents. Copies only the skill folder, no plugin wrapper:

```
npx skills add josephschmitt/crab-shack --skill task-capture
```

### Claude Code

```
/plugin marketplace add josephschmitt/crab-shack
/plugin install task-capture@joes-crab-shack
```

### Claude.ai (web or desktop)

Download [`task-capture.zip`](https://github.com/josephschmitt/crab-shack/releases/latest/download/task-capture.zip) from the [latest release](https://github.com/josephschmitt/crab-shack/releases/latest), then in Claude click **+** → **Create skill** and upload the zip.

### Codex / ChatGPT

```
codex plugin marketplace add josephschmitt/crab-shack
```

Then install **Task Capture** from the plugin directory.

### Cursor

Add `josephschmitt/crab-shack` under **Customize → Plugins**, or clone the repo and copy `plugins/task-capture` into `~/.cursor/plugins/local/`.
