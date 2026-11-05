# hairmaxxing

A Cursor agent skill for previewing men's haircuts on your own photos before you see a barber. The agent analyzes your photos, quizzes you with multiple-choice questions, renders clearly different options through the image MCP server you connect, learns your taste, and ends with final images of every view to show your barber.

There is no app. It runs inside Cursor.

## Install

```bash
npx skills add dogukanteber/skills --skill hairmaxxing
```

Or copy this folder to `~/.cursor/skills/hairmaxxing` by hand. Install it globally so `/hairmaxxing` works in every Cursor window, including one with no folder open.

## Requirements

- Cursor.
- A Runware API key in `~/.hairmaxxing/.env` as `RUNWARE_API_KEY=...` (create one on Runware's API Keys page; the first session creates the file for you). `scripts/render.py` then renders straight from your local photos with Nano Banana 2. Without a key, the skill falls back to an image MCP server that edits a photo from a text prompt; that path is slower and uses more tokens. Text-only generators can't keep your face. The skill never uses Cursor's built-in image tool.
- Python 3 with Pillow (`pip install pillow`).

## Use

1. Open Cursor, with or without a folder, and run `/hairmaxxing`.
2. Attach front, left and right photos when asked (a single photo grid works too).
3. React to the images. Say "go back to r004", "tweak: shorter on top", "compare r002 and r005" or "lock it" whenever you like.

Every run creates a new folder in `~/.hairmaxxing/sessions/` with your photos, every render and its prompt (`renders/log.md`), the spec, and a `final/` folder with the chosen look from every view. At the end the agent opens `final/` in Finder.

## Where things are stored

Everything is in `~/.hairmaxxing/` (set `HAIRMAXXING_HOME` to move it):

- **`sessions/<date-time>/`:** one folder per run.
- **`profile.md`:** your lasting preferences, vocabulary and image server quirks, reused in every session. Edit it by hand any time.
- **`.env`:** your `RUNWARE_API_KEY`.

`~/.hairmaxxing` is hidden in Finder; press Cmd+Shift+. to show hidden folders, or Cmd+Shift+G and type the path.

Your photos are sent to whichever image service renders them.

## Status

Tested by one person so far, with straight to wavy hair. Curly and coily hair are covered in the vocabulary but untested. Each session writes `feedback.md`; please open an issue with it when something goes wrong.
