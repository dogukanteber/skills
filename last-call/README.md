# last-call

A Cursor skill that keeps your Gmail inbox free of junk promotional email without you thinking about it.

Every day, promotional and marketing email older than 7 days moves out of your inbox into a Gmail label called **Last Call**. It sits there for another 7 days, then goes to Gmail Trash, where Gmail purges it after 30 days. If you take something out of Last Call, the agent never touches that sender again. If you drop something into Last Call yourself, it learns to clear that sender's mail too.

It's conservative on purpose. Receipts, orders, bookings, security codes, banking, account notices and anything a person wrote to you are never touched unless you explicitly say so. When it isn't sure, it leaves the email alone.

There is no app to host. The agent reads only senders, subjects, Gmail's short snippets and Gmail's labels, never full email bodies. Its memory (your preferences, learned sender rules and a ledger of everything it moved) lives in a Notion page you can open and edit.

## Requirements

- Cursor with the **Gmail** and **Notion** plugins connected (Cursor Settings > Plugins).
- A Cursor Automation to run it daily (below).

## Set up

1. Copy this folder into `~/.cursor/skills/` so you can talk to it in any chat.
2. In a Cursor chat, say "set up Last Call". The agent creates the **Last Call** page and its two databases in Notion and the **Last Call** label in Gmail, then asks once about senders to always keep and anything besides promotional mail it may clear.
3. It scans your inbox and shows what it would move. Nothing moves until you say "go". You can add exceptions: "go, but keep Uber".
4. Create a Cursor Automation:
   - **Trigger:** every day.
   - **Repo:** this repo (`dogukanteber/skills`), default branch.
   - **Tools:** the Gmail and Notion MCP servers.
   - **Prompt:** `Do a scheduled run of the Last Call skill. Follow last-call/SKILL.md exactly.`

If you skip step 2, the first scheduled run does the setup and emails you the proposal instead. Reply "go" to that email to start.

## Use

- **Do nothing.** It runs daily.
- **Rescue an email:** move it out of Last Call. That sender is safe from now on.
- **Clear more:** move an email into Last Call. That sender's mail goes automatically from now on.
- **Weekly report:** once a week you get a short email filed under **Last Call/Reports** with what moved, what was trashed, what it learned, and close calls it left alone. Reply to it to teach it ("never touch Substack", "also clear Strava").
- **In chat:** "never touch X", "you can clear LinkedIn notifications", "what did you delete this week?", "pause Last Call", "run Last Call now".
- **In Notion:** edit the preferences, rules or Mode (`Live`, `Paused`) directly.

## Limits

- Gmail only.
- Trash, not hard delete. Anything it trashed is recoverable from Gmail Trash for 30 days.
- No unsubscribing. Unsubscribe links in emails are a phishing risk, so it never clicks them.
- It works through an old inbox gradually, at most 150 moves a day.
