# skills

Agent skills I use in Cursor and Claude. Each folder is a self-contained skill with its own `SKILL.md` and `README.md`.

| Skill | For | What it does |
| --- | --- | --- |
| [hairmaxxing](hairmaxxing) | Cursor | Preview men's haircuts on your own photos, refine them with the agent, and take final images to your barber. |
| [pantry](pantry) | Claude | Pantry tracker that keeps a rough inventory of your food and suggests recipes from what you have. Uses Claude's Notion connector as its database. |

## Install

Install one skill:

```bash
npx skills add dogukanteber/skills --skill hairmaxxing
```

Or install by hand. For Cursor skills, copy the folder into `~/.cursor/skills/` (global) or `.cursor/skills/` in a project. For Claude skills, zip the folder and upload it under Settings > Capabilities > Skills.

## License

[MIT](LICENSE)
