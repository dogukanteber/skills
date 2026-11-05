#!/usr/bin/env python3
"""Create a new hairmaxxing session folder, and the user's profile if it's missing.

Run from anywhere:
  python3 path/to/hairmaxxing/scripts/new_session.py

Everything lives in ~/.hairmaxxing (override with HAIRMAXXING_HOME): profile.md, .env
with RUNWARE_API_KEY, and sessions/YYYY-MM-DD-HHMM/ with photos/, renders/, rounds/,
sheets/, final/, spec.md, prompt.json, renders/log.md and feedback.md. Never reuses
an existing session folder.
"""
import argparse
import shutil
from datetime import datetime
from pathlib import Path

from render import HOME, find_api_key

SKILL = Path(__file__).resolve().parent.parent
TEMPLATES = SKILL / "templates"


def new_folder(root):
    stamp = datetime.now().strftime("%Y-%m-%d-%H%M")
    path = root / stamp
    n = 2
    while path.exists():
        path = root / f"{stamp}-{n}"
        n += 1
    path.mkdir(parents=True)
    return path


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--root", default=HOME / "sessions", help=f"parent folder for sessions (default {HOME / 'sessions'})")
    args = p.parse_args()

    session = new_folder(Path(args.root).expanduser().resolve())
    for sub in ("photos", "renders", "rounds", "sheets", "final"):
        (session / sub).mkdir()
    shutil.copy(TEMPLATES / "spec.md", session / "spec.md")
    shutil.copy(TEMPLATES / "prompt.json", session / "prompt.json")
    shutil.copy(TEMPLATES / "log.md", session / "renders" / "log.md")
    (session / "feedback.md").write_text("# Session feedback\n")

    HOME.mkdir(parents=True, exist_ok=True)
    profile = HOME / "profile.md"
    if profile.exists():
        status = "existing"
    else:
        shutil.copy(TEMPLATES / "profile.md", profile)
        status = "created"

    env = HOME / ".env"
    if not env.exists():
        env.write_text("RUNWARE_API_KEY=\n")

    print(f"session: {session}")
    print(f"profile: {profile} ({status})")
    print(f"api key: {'set' if find_api_key() else f'missing, add RUNWARE_API_KEY to {env}'}")


if __name__ == "__main__":
    main()
