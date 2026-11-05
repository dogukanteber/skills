# Intake

## Photos

Ask for these in one message:

- Front, left profile and right profile. A back or top view helps for the crown, cowlicks and the fade line.
- Even daylight or soft indoor light, neutral expression, no hat or glasses, hair in its usual everyday state.
- All taken in the same session, head filling a good part of the frame.

Images attached in the chat are saved to disk, and their paths appear in the message. Copy them into `photos/` as `front`, `left`, `right`, `back` or `top`, keeping each file's extension. Never edit the originals.

If they send one grid image, keep it as `photos/grid.<ext>` and split it with `scripts/split_grid.py`. If they only have a front selfie, start with it and say what you can't judge yet (fade line, crown, profile).

For every photo, record in the spec's Photos line which view it is and which edge of the image their nose points to. Prompts need it.

## Analyze before asking

Write this into the spec's Current state:

- **Hair:** color, texture (straight, wavy, curly, coily; curl type if visible), density, strand thickness, current cut and estimated lengths in cm on the sides, top and front, part side.
- **Hairline and crown:** straight, rounded or receding at the temples; cowlicks; crown swirl direction.
- **Facial hair:** exact length, shape and lines, so prompts can keep it unchanged. "Clean-shaven" counts.
- **Face:** shape, forehead height, ears, anything a cut can balance or emphasize.
- **Feasibility limits:** what their hair can't do (fine straight hair won't hold a tall quiff without a blow-dryer; a receding temple shows with a high fade and a slicked-back top).

Then fill in `<session>/prompt.json` (see [prompting.md](prompting.md)): one entry per photo with its view line, and the keep list with their exact facial hair, clothing, accessories and background. Drop template entries for photos they didn't send. Every render reuses it, so get it right once.

Tell the user in two or three sentences what you see, so they can correct you early.

## First question round

Only ask what the photos can't show. Typical topics, each with concrete options plus "Suggest for me":

- **What's changing:** sides and back, top, front, finish; which stay as they are.
- **Vibe:** clean and professional, rugged, edgy or streetwear, classic, effortless. Allow several.
- **Maintenance:** styling time per day, tools they own (blow-dryer), products they'll use, how often they'll visit the barber.
- **Constraints:** work dress codes, sports, helmets, an upcoming event.
- **Hard nos:** things they never want.

If they mention a habit ("I always get a low fade"), record it and treat it as the default, not a fixed rule, unless they say it's fixed.
