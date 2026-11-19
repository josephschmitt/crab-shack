---
name: task-capture
description: Turns a request from a Slack thread, email, chat message, or recent screen activity into a well-formed Linear issue, with a clear title, a description that quotes the ask, attached links, a suggested project, and a backlog status by default. Checks for duplicates and shows a draft before creating anything. Use when the user says "track this", "create a task", "add this to Linear", "file this", "make an issue for this", or otherwise wants a request captured in Linear.
license: MIT
metadata:
  author: Joe Schmitt
  version: "1.0.0"
---

# Task Capture to Linear

Turn a request from a conversation (Slack, email, chat, PR comment, etc.) into a well-formed Linear issue.

## Configuration

Adjust these defaults to match your workspace. Anything not set here should be looked up from Linear (`list_teams`, `list_projects`, `list_issue_statuses`) rather than guessed.

| Setting             | Default                                                                  |
| ------------------- | ------------------------------------------------------------------------ |
| Default team        | `<your work team>` for work requests                                     |
| Personal team       | `<your personal team>` for private, household, or non-work tasks         |
| Default status      | Your backlog state (e.g. "Backlog" or "Someday")                         |
| Default assignee    | `me`                                                                     |
| Default priority    | No priority (0)                                                          |
| Project routing     | Optional. Keep keyword-to-project rules in a private file, not this one. |

## Trigger phrases

- "track this"
- "create a task"
- "add this to Linear"
- "file this"
- "make an issue for this"
- Any similar intent to capture a request into Linear

## Workflow

1. **Gather context.** Use what the user gave you: pasted text, an attached image, or a link or ID you can fetch through an available Slack, email, or other MCP. If the user gave nothing (e.g. just "track this") use Dayflow to look up what they were recently looking at, then pull out the relevant conversation. Prefer the Dayflow MCP if it's connected. If it isn't, fall back to the `dayflow` CLI (check with `which dayflow`). Useful read-only commands:
   - `dayflow timeline today --detailed --json` for today's activities with full write-ups
   - `dayflow search <text> --json` to find an activity by title or summary
   - `dayflow card <id> --json` for one activity in full detail

   Only use the read commands. Never run `timeline update`, `timeline delete`, or other editing commands. Extract:
   - Who is asking (name, handle, or email)
   - What they are asking for
   - Deadlines, links, or references
   - Channel or thread context

   If the context is still missing or ambiguous after that (or neither the Dayflow MCP nor the CLI is available), ask the user to paste the message, share a link, or attach a screenshot instead of guessing.

2. **Check for duplicates.** Search Linear for an existing issue covering the same request. If one exists, tell the user and offer to update it instead of creating a new one.

3. **Draft the title.** Describe the action concisely, and include context naturally when it helps identify the work. Examples:
   - `Review <person>'s tech spec for the email template`
   - `Follow up with <person> on laptop status`
   - `Check the cloud spend dashboard`

   Keep it short and scannable. Don't use rigid `[Name]` prefixes.

   For PR work, title the issue after what the PR builds (e.g. `Add <feature> plugin to <repo>`), never "Merge ...". Merging is part of the lifecycle, not the goal. Reference the repo or PR in the title or description.

4. **Draft the description** in markdown:
   - Quote or summarize the ask
   - Put relevant links (the source message or thread, docs, PRs, tickets) in the issue's attachments via the `links` field rather than only pasting them into the description. Mention a link inline only when the description needs it to make sense. If the Linear MCP doesn't support `links`, put them in the description instead.
   - Include channel or thread context if helpful
   - Note any stated deadlines
   - Note who made the request (e.g. "Asked by <person> in #<channel>")

5. **Pick the team.** Use the default work team unless the task is clearly personal, in which case use the personal team.

6. **Pick the project.** Suggest the best match and say why it fits.
   - Fetch the team's active projects with `list_projects` and match on the task's content.
   - If the user keeps a routing file (keyword to project), use it.
   - Never assign to completed, canceled, or archived projects.
   - If nothing fits, say so and ask: "This doesn't clearly fit an existing project. Should I file it under [closest match], or create a new project?"
   - If it's still unclear, leave it without a project and note that in the description.
   - If the work seems to need a project that doesn't exist yet, suggest creating one rather than using a catch-all.

7. **Pick the status.** Default to the backlog state so the task isn't lost; the user promotes it when triaging. Move further along only on explicit signals:
   - **Soon / Next**: the user says they'll do it soon, or says it's the next thing to do
   - **In Progress**: the user is working on it right now
   - **In Review**: the user's part is done and it's waiting on someone else
   - When in doubt, use the backlog state

   Adapt the state names to your team's workflow.

8. **Set remaining defaults.**
   - Priority: No priority unless urgency is obvious
   - Assignee: the user (`me`)
   - Due date: only if one is stated or the deadline is obvious

9. **Show the draft, then create.** Present the issue (team, project, title, status, priority, assignee, links, description) in one compact block and ask the user to confirm. Ask a question only when a value truly can't be inferred (e.g. project or priority), and fold the answer into the draft. After confirmation, create it with the Linear MCP `save_issue` tool.

10. **Report back** with the issue identifier and URL.

## Edge cases

- If the request spans multiple people or teams, suggest sub-issues or a project update.
- If one conversation contains several distinct asks, propose one issue per ask and confirm the list before creating them.
