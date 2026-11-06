# pantry

A Claude skill that tracks your pantry. It keeps a rough inventory of the food you have, and uses that inventory to suggest recipes from what you already own, deduct ingredients when you cook, and learn your taste over time.

There is no app or database to host. The skill uses Claude's Notion connector as its database: your pantry, cooked history and preferences all live in pages in your own Notion workspace, which you can open and edit directly.

Tracking is deliberately approximate. Say "add 3 eggs and 500g spinach", "I'm out of milk", or send a photo of your fridge or a receipt, and Claude updates the pantry without asking you to weigh anything.

## Install

```bash
npx skills add dogukanteber/skills --skill pantry
```

Or zip this folder and upload it in Claude under Settings > Capabilities > Skills.

## Requirements

- Claude with skills enabled.
- Claude's Notion connector, connected to your workspace (Settings > Connectors).
- A Notion page called **Chef** with two databases under it:
  - **Pantry**: Name (title), Amount (number), Unit (select: `g`, `kg`, `ml`, `l`, `pcs`), Category (select), Expires (date).
  - **Cooked Recipes**: Name (title), Cooked on (date), Servings (number), Vibe (multi-select), Rating (select), Notes (text).

  The body of the Chef page holds your preferences (diet, allergies, dislikes, default servings, equipment). Claude fills it in on first run.

Paste the Chef page ID and the two database data source IDs into the placeholders at the top of `SKILL.md`. If you leave a placeholder in, Claude asks you for the ID or offers to create the page or database for you, then gives you the ID to paste in.

## Use

- **Update the pantry:** text or photos of your fridge, shelves, groceries or receipts. Photos only add and update items; nothing is removed unless you say so.
- **Ask for food:** "date night for two", "quick and high protein", "what should I cook?". You get 2 to 3 options built from your pantry, with anything missing called out.
- **Pick one:** "let's do the second one". Claude gives the full recipe, deducts the ingredients, and logs the dish in Cooked Recipes.
- **Give feedback:** "loved it", "too salty". It updates the rating and folds lasting taste into your preferences.

On first run with an empty pantry, Claude asks you to tell it or show it what you have before suggesting anything.

Everything is metric. Cups, ounces and pounds are converted.
