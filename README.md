# skills

Agent skills I use in Cursor and Claude. Each folder is a self-contained skill with its own `SKILL.md` and `README.md`.

| Skill | For | What it does |
| --- | --- | --- |
| [hairmaxxing](hairmaxxing) | Cursor | Preview men's haircuts on your own photos, refine them with the agent, and take final images to your barber. |
| [pantry](pantry) | Claude | Pantry tracker that keeps a rough inventory of your food and suggests recipes from what you have. Uses Claude's Notion connector as its database. |
| [last-call](last-call) | Cursor | Moves junk promotional Gmail into a "Last Call" label, trashes it a week later, and learns from what you rescue. Runs daily as a Cursor Automation with Notion as its memory. |

## A confession

Every skill here used to be a full mobile app. I built each one from scratch, and most of the work was plumbing: data models, REST endpoints, and the glue between them. I'm a little embarrassed by how much code that was. Keeping all of the apps alive turned into more tech debt than I could keep up with, and agent harnesses kept getting better, so I shut the apps down and rewrote each one as a skill. Now the agent does what the plumbing used to do.

## Install

Install one skill:

```bash
npx skills add dogukanteber/skills --skill hairmaxxing
```

Or install by hand. For Cursor skills, copy the folder into `~/.cursor/skills/` (global) or `.cursor/skills/` in a project. For Claude skills, zip the folder and upload it under Settings > Capabilities > Skills.

## License

[MIT](LICENSE)
