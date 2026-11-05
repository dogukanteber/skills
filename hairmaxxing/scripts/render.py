#!/usr/bin/env python3
"""Render one round of haircut edits on Runware, log the prompts and build the contact sheet.

Example:
  python3 render.py SESSION_DIR SESSION_DIR/rounds/round1-sides.json

Jobs file:
  {
    "sheet": "round1-sides",
    "originals": true,
    "jobs": [
      {"slug": "taper", "view": "right", "label": "1 Taper", "change": "Change ONLY the sides ..."},
      {"slug": "top-5-6cm", "view": "front", "parent": "r007", "change": "Change ONLY the length ..."}
    ]
  }

A job is Pattern A (edit of the view's original photo) unless "parent" names a render
("r007" or a path), which makes it Pattern B (minimal edit of that render). "prompt"
replaces the whole prompt, and "refs" adds reference images (Pattern C). View lines,
the keep list and photo files come from SESSION_DIR/prompt.json. "originals": true puts
each view's original photo on the sheet before its renders.

Needs RUNWARE_API_KEY in the environment, in ~/.hairmaxxing/.env (HAIRMAXXING_HOME
overrides the folder) or in a .env in or above the current directory. Writes renders/rNNN-slug.<ext>, appends every prompt to
renders/log.md and writes sheets/<sheet>.png. --dry-run prints the prompts only.
"""
import argparse
import base64
import json
import mimetypes
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path

API = "https://api.runware.ai/v1"
DEFAULTS = {"model": "google:4@3", "resolution": "1K", "outputFormat": "PNG"}
SCRIPTS = Path(__file__).resolve().parent
HOME = Path(os.environ.get("HAIRMAXXING_HOME", Path.home() / ".hairmaxxing"))

PATTERN_A = """Edit this photo of a man. {view}

Identity preservation is the top priority. Keep exactly, unchanged: {keep}. Do not beautify, slim, smooth or airbrush, and do not sharpen or re-grade the photo.

{change}

Photorealistic, same photo quality as the original. Facial hair untouched."""

PATTERN_B = """Minimal edit. {view}

Keep everything identical, including the framing: {keep}. Do not sharpen or re-grade the photo.

{change}

Everything else stays exactly as it is."""


def find_api_key():
    if os.environ.get("RUNWARE_API_KEY"):
        return os.environ["RUNWARE_API_KEY"]
    cwd = Path.cwd()
    for env in (HOME / ".env", *(d / ".env" for d in (cwd, *cwd.parents))):
        if not env.is_file():
            continue
        for line in env.read_text().splitlines():
            m = re.match(r"\s*(?:export\s+)?RUNWARE_API_KEY\s*=\s*(.*)", line)
            if m and m.group(1).strip().strip("'\""):
                return m.group(1).strip().strip("'\"")
    return None


def data_uri(path):
    mime = mimetypes.guess_type(path.name)[0] or "image/png"
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode()}"


def resolve_image(session, ref):
    if re.fullmatch(r"r\d{3}", ref):
        hits = sorted((session / "renders").glob(f"{ref}-*.*"))
        if not hits:
            sys.exit(f"no render named {ref} in renders/")
        return hits[0]
    path = Path(ref)
    path = path if path.is_absolute() else session / path
    if not path.is_file():
        sys.exit(f"missing image: {path}")
    return path


def next_number(session):
    nums = [int(m.group(1)) for f in (session / "renders").glob("r*-*.*") if (m := re.match(r"r(\d{3})-", f.name))]
    return max(nums, default=0) + 1


def build(session, cfg, job):
    view = cfg["photos"].get(job["view"])
    if not view:
        sys.exit(f"view {job['view']!r} is not in prompt.json")
    keep = view.get("keep", cfg["keep"]).rstrip(". ")
    if job.get("parent"):
        source, pattern = resolve_image(session, job["parent"]), "B"
    else:
        source, pattern = resolve_image(session, view["file"]), "A"
    if job.get("prompt"):
        prompt, pattern = job["prompt"], "custom"
    else:
        template = PATTERN_B if pattern == "B" else PATTERN_A
        prompt = template.format(view=view["view"], keep=keep, change=job["change"].strip())
    refs = [source] + [resolve_image(session, r) for r in job.get("refs", [])]
    return {"prompt": prompt, "pattern": pattern, "source": source, "refs": refs, "original": resolve_image(session, view["file"])}


def post(key, tasks):
    req = urllib.request.Request(
        API,
        data=json.dumps(tasks).encode(),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=200) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        try:
            return json.loads(body)
        except json.JSONDecodeError:
            return {"errors": [{"message": f"HTTP {e.code}: {body[:300]}"}]}


def run_tasks(key, tasks, poll_seconds=300):
    results, errors = {}, {}

    def absorb(resp):
        for item in resp.get("data", []):
            if item.get("imageURL"):
                results[item["taskUUID"]] = item
        for err in resp.get("errors", []):
            errors[err.get("taskUUID", "?")] = err.get("message", str(err))

    absorb(post(key, tasks))
    pending = [t["taskUUID"] for t in tasks if t["taskUUID"] not in results and t["taskUUID"] not in errors]
    deadline = time.time() + poll_seconds
    while pending and time.time() < deadline:
        time.sleep(3)
        absorb(post(key, [{"taskType": "getResponse", "taskUUID": u} for u in pending]))
        pending = [u for u in pending if u not in results and u not in errors]
    for u in pending:
        errors[u] = "timed out waiting for the result"
    return results, errors


def append_log(session, name, job, b, item):
    parent = b["source"].relative_to(session) if b["source"].is_relative_to(session) else b["source"]
    extra = f"; refs: {', '.join(str(r.relative_to(session)) for r in b['refs'][1:])}" if len(b["refs"]) > 1 else ""
    cost = f"; cost ${item['cost']:.4f}" if item.get("cost") is not None else ""
    entry = (
        f"\n## {name}\n"
        f"- View: {job['view']}; Pattern {b['pattern']}; parent: {parent}{extra}\n"
        f"- Runware: imageUUID {item.get('imageUUID')}; seed {item.get('seed')}{cost}\n"
        f"- Prompt:\n\n```text\n{b['prompt']}\n```\n"
    )
    with open(session / "renders" / "log.md", "a") as f:
        f.write(entry)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("session", help="session folder")
    p.add_argument("jobs", help="jobs JSON file")
    p.add_argument("--dry-run", action="store_true", help="print the prompts without calling Runware")
    args = p.parse_args()

    session = Path(args.session).resolve()
    cfg = json.loads((session / "prompt.json").read_text())
    spec = json.loads(Path(args.jobs).read_text(), strict=False)
    server = {**DEFAULTS, **cfg.get("server", {})}
    jobs = spec["jobs"]
    if not 1 <= len(jobs) <= 4:
        sys.exit(f"a round has 1-4 renders, got {len(jobs)}")
    built = [build(session, cfg, j) for j in jobs]

    if args.dry_run:
        for j, b in zip(jobs, built):
            print(f"=== {j['slug']} ({j['view']}, Pattern {b['pattern']}, from {b['source'].name})\n{b['prompt']}\n")
        return

    key = find_api_key()
    if not key:
        sys.exit(f"RUNWARE_API_KEY not found in the environment or {HOME / '.env'}")

    tasks = []
    for b in built:
        tasks.append({
            "taskType": "imageInference",
            "taskUUID": str(uuid.uuid4()),
            "model": server["model"],
            "positivePrompt": b["prompt"],
            "inputs": {"referenceImages": [data_uri(r) for r in b["refs"]]},
            "resolution": server["resolution"],
            "outputFormat": server["outputFormat"],
            "outputType": "URL",
            "numberResults": 1,
            "includeCost": True,
        })

    started = time.time()
    results, errors = run_tasks(key, tasks)
    elapsed = time.time() - started

    n = next_number(session)
    ext = server["outputFormat"].lower().replace("jpeg", "jpg")
    done, total = [], 0.0
    for j, b, t in zip(jobs, built, tasks):
        u = t["taskUUID"]
        if u not in results:
            print(f"FAILED {j['slug']}: {errors.get(u) or errors.get('?') or 'no result'}")
            continue
        name = f"r{n:03d}-{j['slug']}"
        n += 1
        out = session / "renders" / f"{name}.{ext}"
        with urllib.request.urlopen(results[u]["imageURL"], timeout=120) as r:
            out.write_bytes(r.read())
        append_log(session, name, j, b, results[u])
        total += results[u].get("cost") or 0
        done.append((j, b, name, out))
        print(f"{out.name}  view={j['view']}  pattern={b['pattern']}  from={b['source'].name}")

    print(f"{len(done)}/{len(jobs)} rendered in {elapsed:.0f}s, cost ${total:.4f}")
    if not done:
        sys.exit(1)

    cells, labels = [], []
    views = list(dict.fromkeys(j["view"] for j, *_ in done))
    for v in views:
        if spec.get("originals"):
            original = next(b["original"] for j, b, *_ in done if j["view"] == v)
            cells.append(original)
            labels.append("Current" if len(views) == 1 else f"Current {v}")
        for j, b, name, out in done:
            if j["view"] == v:
                cells.append(out)
                labels.append(f"{j.get('label', j['slug'])} ({name[:4]})".replace(",", " "))
    sheet = session / "sheets" / f"{spec.get('sheet', 'round')}.png"
    subprocess.run(
        [sys.executable, str(SCRIPTS / "contact_sheet.py"), str(sheet), *map(str, cells), "--labels", ",".join(labels), "--cols", "2"],
        check=True,
    )
    print(f"sheet: {sheet}")


if __name__ == "__main__":
    main()
