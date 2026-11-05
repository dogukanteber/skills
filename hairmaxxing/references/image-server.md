# Image server

Render only through an external image service. Never use Cursor's built-in `GenerateImage` tool, even when the service is slow or failing; if it fails, tell the user.

## Runware via `scripts/render.py` (default)

Use this when `new_session.py` printed `api key: set`. The key lives in `~/.hairmaxxing/.env` as `RUNWARE_API_KEY=...` (the environment variable, or a `.env` in or above the current directory, also work). Never print the key. This needs no MCP calls, no uploads and no model lookups: the script sends the local photos as data URIs, renders all jobs of a round in one batch, downloads them, logs the prompts and builds the sheet.

Settings live in the profile's Image server section and in `prompt.json` (`"server"` overrides the defaults `google:4@3`, `1K`, `PNG`). Don't call `list_models` or `model_schema` unless a run fails on a parameter.

Run it: `python3 <skill>/scripts/render.py <session> <session>/rounds/<round>.json`. Add `--dry-run` to see the assembled prompts without spending anything.

## MCP server (fallback)

Use this only when there's no API key. Tell the user once that adding `RUNWARE_API_KEY` to `~/.hairmaxxing/.env` makes every later session faster.

1. If the profile's Image server section names a namespace and tool, confirm it with `GetDynamicTools` (`namespace` and `toolName`). Otherwise call `GetDynamicTools` with no arguments, look through the MCP-backed namespaces for image editing tools (ignore `cursor`) and fetch each candidate's schema. One fit: use it. Several: ask once with `AskQuestion`. None: stop and say what's needed.
2. If the namespace status is `needsAuth` or `error`, call its `mcp_auth` tool through `CallDynamicTool`, then check again.
3. The tool must edit an input photo with a text prompt. A text-only generator can't keep the user's face; don't use it. If it can't read local paths, follow the upload workaround in the profile's quirks, and suggest adding an API key so the next session can use `render.py`.
4. Fill in the profile's Image server section the first time: namespace and tool, parameter names, settings and quirks.

Calling it: build each prompt with `render.py --dry-run` and pass it unchanged. Name renders `rNNN-slug` sequentially, save them in `renders/`, call a round's renders in parallel, and build the sheet with `scripts/contact_sheet.py`. Choose the strongest identity-preserving settings the tool exposes and keep the input photo's aspect ratio.

## Failures

- **Transient error or timeout:** rerun the failed jobs once (a jobs file with only those), then tell the user.
- **Refusal:** rephrase once in plain grooming terms. If it's refused again, tell the user what was refused.
- **Output missing or unreadable:** report it; don't log a render that doesn't exist.
