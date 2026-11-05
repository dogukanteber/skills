# Critique a render before showing it

`Read` the round's sheet from `render.py`. It puts the original photo of each view before its renders, at about the original photo's resolution, so one read covers the whole round. Open a single render only when the sheet can't settle a detail that matters for the decision. Check each render in order:

1. **Identity:** same eyes, nose, brows, ears, skin texture and tone, face shape and age. No beautifying, slimming or smoothing.
2. **Requested change:** present, at the requested amount. Measure against anchors: the top of the ear, the temples, the eyebrows, the original length.
3. **Nothing else changed:** facial hair, hair color, clothing, background, lighting, expression, and any hair area that wasn't being edited.
4. **View:** the same view and head angle as the original.
5. **Feasible for the user:** density, hairline and crown match what they actually have. Flag renders that invent a lower hairline or thicker hair.
6. **Artifacts:** hair melting into the background, smeared edges, plastic skin, warped ears.
7. **Sheets:** options are distinguishable at thumbnail size; views on a Combine sheet show the same haircut.

## Decide

- **Fails 1 or 2:** fix the prompt using the drift table in prompting.md and re-render only the failed jobs (one jobs file for all of them). After two failed retries, show the best attempt, say what's wrong, and offer a different approach.
- **Fails 3-6:** re-render if the flaw would mislead their decision (the fade height when the fade is what's being decided); otherwise mention it.
- **Passes:** show it.

## Report

One sentence of verdict, then only the flaws that matter for the decision. Don't hide flaws, and don't list trivia.
