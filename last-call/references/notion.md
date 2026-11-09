# Notion layout

One page, two inline databases under it.

## Page: Last Call

Create it with this body. Settings are plain `Key: value` lines so both you and the user can read and edit them.

```markdown
Memory for the Last Call email agent. Edit anything here; the agent reads this page on every run.

## Settings
- Mode: Dry run
- Gmail address:
- Last Call label ID:
- Reports label ID:
- Last run: never
- Backlog cursor:
- Last report: never
- Report threads:
- Handled replies:

## Your preferences
Not set yet. By default only promotional and marketing mail is cleared.

## Run log
```

- **Mode**: `Dry run` (propose only), `Live`, or `Paused`.
- **Backlog cursor**: `YYYY/MM/DD`, or `done` once the old inbox has been worked through.
- **Report threads**: comma-separated Gmail thread IDs of the last 6 reports, each as `threadId (report messageId)` so you can tell your report apart from the user's replies.
- **Handled replies**: comma-separated message IDs of the user's replies you've already applied (last 30).

## Database: Last Call Ledger

One row per Gmail thread the agent has moved or found in the label.

```sql
CREATE TABLE (
  "Subject" TITLE,
  "Sender" RICH_TEXT,
  "Domain" RICH_TEXT,
  "Thread ID" RICH_TEXT,
  "Status" SELECT('Waiting':yellow, 'Trashed':red, 'Rescued':green, 'Trashed by you':orange, 'Returned':blue),
  "Source" SELECT('Agent':purple, 'You':blue),
  "Moved on" DATE,
  "Trashed on" DATE,
  "Reason" RICH_TEXT,
  "Open" URL
)
```

- **Open** is the thread's Gmail `viewUrl`, so the user can jump to it from Notion.
- **Status** meanings: `Waiting` (in Last Call, timer running), `Trashed` (agent trashed it after 7 days), `Rescued` (user took it out), `Trashed by you` (user trashed it from the label), `Returned` (new mail arrived in the thread, so it went back to the inbox).

## Database: Last Call Rules

One row per sender address or domain.

```sql
CREATE TABLE (
  "Pattern" TITLE,
  "Kind" SELECT('Sender':blue, 'Domain':purple),
  "Verdict" SELECT('Keep':green, 'Junk promos':orange, 'Junk all':red),
  "Origin" SELECT('You said':blue, 'Rescued':green, 'You moved':orange, 'You trashed':red),
  "Evidence" NUMBER,
  "Note" RICH_TEXT,
  "Updated" DATE
)
```

- **Pattern**: lowercase address (`deals@zara.com`) or domain (`zara.com`).
- **Evidence**: how many times the user's actions backed this rule.

The user can add, edit or delete rows directly. Treat rows they add by hand as Origin `You said`.
