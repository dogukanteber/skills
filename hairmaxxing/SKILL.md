---
name: hairmaxxing
description: Previews men's haircuts on the user's own photos before a barber visit. Analyzes the photos, quizzes the user with multiple-choice rounds, renders clearly different options through an external image-editing MCP server, critiques every render, learns the user's taste across sessions, and ends with final images of every view to show the barber. Use when the user runs /hairmaxxing.
disable-model-invocation: true
---

# Hairmaxxing

Help the user find a haircut by showing options on their own face. They react to images; you turn their reactions into precise specs, render, critique and converge. They need no prompting skill: you drive.

## Ground rules

1. **Hair only.** Change the haircut and nothing else. Face, facial hair, clothing, background and lighting stay exactly as they are in every render.
2. **Look before you ask.** Analyze the photos first. Never ask something the photos answer.
3. **Ask with `AskQuestion`.** At most 4 questions per round. Every question has concrete options plus "Suggest for me".
4. **One area at a time.** Options in a round differ in one area only, and the difference must be obvious at thumbnail size. If you can't tell two options apart at a glance, they aren't two options.
5. **Critique before showing.** `Read` the round's sheet and check every render on it with [references/critique.md](references/critique.md). Tell the user the flaws that matter for their decision.
6. **Files are memory.** `render.py` logs every prompt. After each verdict, update `spec.md` in one edit and append one round entry to `renders/log.md` with each render's critique and their verdict. Don't edit individual log entries. Reread `spec.md` before writing each round's jobs; long chats lose detail.
7. **Lean into their direction.** "More X" means X is clearly visible in the next render. When the amount is unclear, bracket: render "a little" and "a lot" side by side.
8. **Pin down vague words.** When they say "messy", "clean", "volume", "short" and so on, confirm the meaning with options once, then record it in the profile.
9. **Be honest about feasibility.** If their density, texture, hairline or crown can't support a look, say so and show the closest realistic version.
10. **Never delete renders.** Any past render can become the base again.
11. **Keep rounds small.** At most 4 renders per round, so they react often and nothing is wasted.

## Start a session

Every `/hairmaxxing` invocation starts a brand new session in a new folder. Never reuse or write into an earlier session folder.

1. Run `python3 <this skill's folder>/scripts/new_session.py` from any directory; no workspace is needed. It creates `~/.hairmaxxing/sessions/<timestamp>/` with the layout below, creates `~/.hairmaxxing/profile.md` from the template if it's missing, prints both absolute paths and says whether the Runware API key is set. Use absolute paths from then on, and write only inside `~/.hairmaxxing/`.
2. Read the profile. Apply its hard nos, likes and vocabulary from the first round.
3. Connect to the image server: follow [references/image-server.md](references/image-server.md). If no suitable server is connected, stop and say what's needed.
4. Start Intake.

Session folder:

```
photos/           original photos, never edited
spec.md           current target and phase
prompt.json       view lines and keep list for every prompt, filled at Intake
rounds/           one jobs file per round for render.py
renders/          every render, r001-short-slug.<ext>, r002-...
renders/log.md    every prompt (written by render.py), plus one verdict entry per round
sheets/           contact sheets shown to the user
final/            the locked look, one image per view, filled at the end
feedback.md       notes for improving this skill
```

## Phases

Record the current phase at the top of `spec.md`.

### 1. Intake

Follow [references/intake.md](references/intake.md): collect the photos into `photos/`, analyze them into the spec's Current state and `prompt.json`, then ask one round about what photos can't show.

### 2. Explore

Areas: **Sides and back**, **Top**, **Front** (fringe, part, hairline), **Finish** (texture and product look). For each area open to change, one at a time:

1. Pick 3-4 clearly different options that suit their photos and profile, using [references/vocabulary.md](references/vocabulary.md). Make one a wildcard that stretches their taste slightly.
2. Write one jobs file for the round, with one job per option as a separate edit of the original photo (Pattern A in [references/prompting.md](references/prompting.md)), and run `scripts/render.py` on it. Explore on the front view, except for Sides and back: explore those on a profile view when they sent one, because fade height can't be judged from the front. Areas already locked stay fixed in the prompt.
3. Critique the sheet `render.py` wrote, then show it.
4. Ask which options pulled them in, what to push (more or less of what), or whether none fit. Always offer "keep my current [area]".

Never ask the image model for a grid of options: model-made grids blur the differences and drift the face.

### 3. Combine

Merge the winners into one look and render it in every view they supplied: one jobs file with one job per view, each from that view's original photo, all with the same `change` text. Show the sheet. If picks conflict (a fringe versus an open forehead), resolve it, say how, and offer the other path.

### 4. Refine

Make minimal tweaks to the render they like: Pattern B (`"parent": "rNNN"`), that render as the only reference, one change per render. Refine on the front view; once they're happy, apply the same change to each side view's latest render and check that the views agree. If they go back to an older render, branch from it and record it as the parent in the log.

### 5. Lock and deliver

When every area in the spec is Locked or Skipped:

1. Copy the final render of each view into `final/` as `<view>.<ext>` (`front.png`, `left.png`, ...) and combine them into `final/all-views.png` with `scripts/contact_sheet.py`. These images are all they bring to the barber; don't write cutting instructions.
2. Show `final/all-views.png` inline, and run `open <session>/final` so they can find the files in Finder (`~/.hairmaxxing` is hidden there).
3. Update `~/.hairmaxxing/profile.md`: confirmed likes and hard nos, vocabulary, lifestyle facts, image server quirks, and a History row with the date, session folder and outcome.
4. Append to `feedback.md`:

```
## YYYY-MM-DD
- Went well:
- Where the user corrected me:
- Image server failures and the fix that worked:
- Suggested changes to the hairmaxxing skill:
```

## Learning from the user

- **After each verdict:** update the spec's Target table, and add rejections with the reason in their own words and the render id.
- **Promote to the profile** when they state a general preference ("I never want a fringe"), the same preference shows up in two or more verdicts, a vocabulary meaning is confirmed, or you find and fix an image server quirk.
- **Before proposing options:** drop anything the profile rules out and favor patterns they liked, but keep one wildcard.

## Shortcuts the user might type

"show me options for the sides" (explore that area), "tweak: shorter on top" (refine), "go back to r004" (branch), "compare r002 and r005" (contact sheet), "lock it" (deliver).

## Showing images

Embed renders and sheets inline with their absolute path: `![r003 textured crop](/abs/path/renders/r003-textured-crop.png)`. Show two or more renders as one contact sheet.

## Scripts

Run them; don't read them. They need Python 3 and Pillow (`pip install pillow`). Each prints its usage with `--help`.

- `scripts/new_session.py [--root DIR]`: create a new session folder in `~/.hairmaxxing/sessions/` and the profile if missing; reports whether the API key is set.
- `scripts/render.py SESSION JOBS.json [--dry-run]`: render a round on Runware in one batch, save it as `renders/rNNN-slug.png`, log the prompts and write `sheets/<sheet>.png` (originals included). Prints one line per render, the cost and the sheet path.
- `scripts/split_grid.py GRID --grid 2x2 --outdir photos --names front,right,left,top`: split a photo grid into one file per view.
- `scripts/contact_sheet.py OUT IMG... [--labels "1 Crop,2 Quiff"] [--cols 2]`: labeled comparison sheet, for comparisons outside a round and for `final/all-views.png`.
