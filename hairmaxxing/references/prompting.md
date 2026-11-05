# Prompting the image server

`scripts/render.py` builds every prompt from two parts:

- **`<session>/prompt.json`, written once at Intake:** one entry per photo, holding its file and its view line ("It shows a front view of his face, looking straight at the camera."; for profiles, which image edge his nose points to). It also holds the `keep` list: identity, exact facial hair, hair color and density, hairline, clothing and accessories, lighting, camera quality and background. A photo can carry its own `keep` when its view hides or shows different things (the top view has no beard).
- **The `change` block of each job, written per round.** This is the only prompt text you write while rendering.

The script wraps `change` in the header and footer of the job's pattern, so never repeat the identity list in `change`. Before writing a round, reread `spec.md` and the profile's quirks. `render.py` saves every full prompt in `renders/log.md`.

## Jobs file

Write it to `<session>/rounds/<sheet>.json`:

```json
{
  "sheet": "round3-top",
  "originals": true,
  "jobs": [
    {"slug": "textured-crop", "view": "front", "label": "1 Textured crop", "change": "..."},
    {"slug": "top-5-6cm", "view": "front", "parent": "r007", "label": "A 5-6 cm", "change": "..."}
  ]
}
```

- `view` is a key of `prompt.json`'s photos. `slug` becomes the file name `rNNN-slug`, and `label` the sheet caption.
- `"originals": true` puts each view's original photo before its renders on the sheet. Use it for every Explore round.
- At most 4 jobs per file.

## Pattern A: new look from an original photo (no `parent`)

The script sends: "Edit this photo of a man. [view]", then "Identity preservation is the top priority. Keep exactly, unchanged: [keep]. Do not beautify, slim, smooth or airbrush, and do not sharpen or re-grade the photo.", then your `change`, then "Photorealistic, same photo quality as the original. Facial hair untouched."

Write `change` like this:

```
The hair on top of his head and at the front must stay pixel-identical to the original photo: same length, same shape, same height. Do not restyle, lengthen, smooth or sweep back the top.   <- one such line per area not being explored and not locked

Change ONLY his haircut:
- Sides and back: [physical spec with measurements and anatomical anchors]
- Top: [...]
- Front: [...]
- Finish: [...]
Not [the nearest wrong readings].
```

List only the areas that change or are locked. Locked areas are written out in full, copied from the spec's Target table.

## Pattern B: minimal tweak of a render (`parent`)

The script sends: "Minimal edit. [view]", then "Keep everything identical, including the framing: [keep]. Do not sharpen or re-grade the photo.", then your `change`, then "Everything else stays exactly as it is."

Write `change` like this:

```
Keep [every hair area not being changed, named one by one, e.g. "the low skin fade on the sides exactly as it is"].

Change ONLY [one thing]: from [current state] to [target state]. [How it should read: "the same hairstyle after a fresh trim, not a different style".]

Not [nearest wrong readings].
```

## Pattern C: style reference (`refs`)

Use it when the user brings a reference photo of a haircut he likes. Copy it into `photos/` and add `"refs": ["photos/ref1.jpg"]`, plus a full `"prompt"` (which replaces the template):

```
Edit Image 1. Image 1 is [view] of a man. Image 2 is a HAIRCUT REFERENCE ONLY.

Keep from Image 1, unchanged: [keep list from prompt.json].

Copy from Image 2 ONLY the haircut:
- [Area]: [physical spec, written out even though it's in the image].

Do not copy Image 2's face, facial hair, hair color, lighting, background or framing. The result should look like a real photo of the man in Image 1 after this haircut.
```

## Rules

- **One reference per job.** Passing the original and a render together makes the model copy the render. To merge looks, describe the other one in text. Pattern C is the only exception.
- **One view per render.** Never ask for a multi-panel image.
- **Concrete beats adjectives:** "7-8 cm on top", "bare skin from the bottom up to the top of the ear", "the sides stay dark above the top of the ear".
- **Name the nearest wrong reading:** "textured and piece-y, not tousled bedhead, not slick".
- **Left and right:** say whose side and where it is in the image: "his own right side (the LEFT side of a front-view image)".
- **Overstate after an undershoot, and for small steps.** If the last render was too subtle, ask for "noticeably longer, about 11-12 cm", not "a bit longer". A requested 2 cm change tends to come out as almost none.

## Known drift and fixes

Confirmed on Nano Banana 2 (`google:4@3`) unless the profile says otherwise. Record new findings in the profile's quirks.

| Drift | Fix |
|---|---|
| Face changes or gets beautified | Identity line first (the template does this); or use Pattern B from a render whose face is right |
| Facial hair changes | Describe the facial hair exactly in `prompt.json`'s keep list |
| An area that isn't being edited drifts (the top gets longer or swept back while exploring sides) | Add "must stay pixel-identical to the original photo ... Do not restyle, lengthen, smooth or sweep back" for that area |
| Fade climbs to mid or high | Give the height with an anatomical anchor and add "above the top of the ear the sides stay dark with hair" |
| Fade heights look the same from the front | Explore and judge fades on a profile view |
| Fade-height brackets collapse into one standard fade | Don't bracket fade height with fresh Pattern A renders; tweak an accepted render with Pattern B |
| Change too subtle | Overstate the amount, change one thing per render |
| Output copies the reference render | Pass a single reference and describe the rest in text |
| Photo gets sharpened or re-graded | Already in the templates; if it still happens, mention it rather than re-rendering |
| Lighting, background or clothing changes | Name them in the keep list |
| "Messy" comes out as bedhead | Say "textured, piece-y, separated pieces with a few defined spikes; not tousled" |
