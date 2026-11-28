#!/usr/bin/env python3
"""A project's client originals: one byte-exact file per item, the best held.

Files live in private/client-originals/; the manifest, docs/brand/client-originals.json,
records each file's source, bytes, pixel size and hash. The rules:

- Each file goes in with add as it arrives, before a review page or edit uses it.
- A review page, crop or edit reads from the store and writes elsewhere.
- Anything sent to the client is built with send; a folder built any other
  way passes check before it goes.
- A worse copy never replaces a held one. A replaced file moves to
  superseded/ and stays listed under its item; nothing is deleted.

python3 client-originals.py <command>, from the project's root:
  init                         make the folder and manifest; refuse an unignored folder
  add <id> <file> --status exact|degraded --source <url or note> [--note ..]
      [--supersede "<why this file beats the held one>"]
  verify                       every file present, unchanged and listed
  send <dir> <id>=<name> ...   copy byte-exact, then check
  check <dir> [--allow-degraded]   every file in <dir> is a held original

exact: the file as its source served it. degraded: the best copy we hold of an
original we lack. A file with no pixel size (an SVG, a PDF) records none.
Exit 0 on success, 1 on a refusal or a problem found. Needs Pillow for add.
"""

import argparse
import hashlib
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
from datetime import date

ROUND_SCRIPTS = str(
    pathlib.Path(__file__).resolve().parents[2] / "design-round/scripts"
)
sys.path.append(ROUND_SCRIPTS)
import siblings  # noqa: E402
from fail_open import expected  # noqa: E402

runner = siblings.load(ROUND_SCRIPTS, "runner.py")

STORE = "private/client-originals"
MANIFEST = "docs/brand/client-originals.json"
SUPERSEDED = "superseded"
SUPERSEDED_SHA_CHARS = 8  # guess, #501


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def git_root():
    r = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True
    )
    return r.stdout.strip() if r.returncode == 0 else None


def ignored(a):
    probe = os.path.join(a.store, "probe")
    return (
        subprocess.run(["git", "-C", a.root, "check-ignore", "-q", probe]).returncode
        == 0
    )


def load(a):
    if not os.path.exists(a.manifest):
        return {}
    with open(a.manifest, encoding="utf-8") as f:
        return json.load(f)


def save(a, m):
    os.makedirs(os.path.dirname(a.manifest), exist_ok=True)
    with open(a.manifest, "w", encoding="utf-8") as f:
        json.dump(dict(sorted(m.items())), f, indent=2, ensure_ascii=False)
        f.write("\n")


def describe(path):
    try:
        from PIL import Image, UnidentifiedImageError
    except ImportError:
        sys.exit(f"client-originals.py add needs Pillow: {runner.PIP_INSTALL}")
    try:
        with Image.open(path) as im:
            w, h = im.size
    except UnidentifiedImageError as exc:
        expected(exc, "no pixel size")
        w = h = None
    return {"w": w, "h": h, "bytes": os.path.getsize(path), "sha256": sha256(path)}


def size(e):
    return f"{e['w']}x{e['h']} {e['bytes']} B" if e["w"] else f"{e['bytes']} B"


def cmd_init(a):
    os.makedirs(a.store, exist_ok=True)
    if not ignored(a):
        print(
            f"REFUSED: {a.store} is not gitignored; add /private/ to .gitignore and run init again"
        )
        return 1
    if not os.path.exists(a.manifest):
        save(a, {})
    print(f"init: {a.store} is ignored; manifest at {a.manifest}")
    return 0


def cmd_add(a):
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", a.id):
        print(f"REFUSED {a.id}: an id is letters, digits, '_' and '-'")
        return 1
    if not os.path.isfile(a.file):
        print(f"REFUSED {a.id}: {a.file} is not a file")
        return 1
    if not ignored(a):
        print(f"REFUSED {a.id}: {a.store} is not gitignored; run init")
        return 1
    m = load(a)
    d = describe(a.file)
    old = m.get(a.id)
    held = old and os.path.exists(os.path.join(a.store, old["file"]))
    if old and old["sha256"] == d["sha256"]:
        if not held:
            os.makedirs(a.store, exist_ok=True)
            shutil.copyfile(a.file, os.path.join(a.store, old["file"]))
            print(f"{a.id}: restored the lost file")
        else:
            print(f"{a.id}: already held, unchanged")
        return 0
    for other, e in m.items():
        if other != a.id and e["sha256"] == d["sha256"]:
            print(f"REFUSED {a.id}: this file is already held as {other}")
            return 1
    if old:
        if d["w"] and old["w"] and d["w"] * d["h"] < old["w"] * old["h"]:
            print(
                f"REFUSED {a.id}: {d['w']}x{d['h']} has fewer pixels than the held {old['w']}x{old['h']}"
            )
            return 1
        if d["w"] and not old["w"]:
            print(
                f"REFUSED {a.id}: a {d['w']}x{d['h']} raster cannot replace the held file, which has no pixel size"
            )
            return 1
        if a.status == "degraded" and old["status"] == "exact":
            print(
                f"REFUSED {a.id}: a degraded copy cannot replace the exact original held"
            )
            return 1
        if not a.supersede:
            print(
                f"REFUSED {a.id}: a file is already held ({size(old)}, {old['status']}). "
                f'Pass --supersede "<why>" if this one is the better original.'
            )
            return 1
    os.makedirs(a.store, exist_ok=True)
    name = a.id + os.path.splitext(a.file)[1].lower()
    tmp = os.path.join(a.store, f".incoming-{name}")
    shutil.copyfile(a.file, tmp)
    if sha256(tmp) != d["sha256"]:
        os.remove(tmp)
        print(
            f"FAIL {a.id}: the copy does not match its source; the store is unchanged"
        )
        return 1
    history = []
    if old:
        kept = None
        if held:
            os.makedirs(os.path.join(a.store, SUPERSEDED), exist_ok=True)
            kept = os.path.join(
                SUPERSEDED,
                f"{a.id}-{old['sha256'][:SUPERSEDED_SHA_CHARS]}{os.path.splitext(old['file'])[1]}",
            )
            os.replace(os.path.join(a.store, old["file"]), os.path.join(a.store, kept))
        history = old.get("superseded", []) + [
            {
                **{k: v for k, v in old.items() if k != "superseded"},
                "file": kept,
                "why_replaced": a.supersede,
            }
        ]
    os.replace(tmp, os.path.join(a.store, name))
    m[a.id] = {
        "file": name,
        **d,
        "source": a.source,
        "status": a.status,
        "note": a.note or "",
        "added": date.today().isoformat(),
    }
    if history:
        m[a.id]["superseded"] = history
    save(a, m)
    print(f"{a.id}: held {size(d)} ({a.status})")
    return 0


def cmd_verify(a):
    m = load(a)
    listed = set()
    bad = 0
    for item, e in m.items():
        for entry in [e] + e.get("superseded", []):
            if entry["file"] is None:
                continue
            listed.add(os.path.normpath(entry["file"]))
            p = os.path.join(a.store, entry["file"])
            if not os.path.exists(p):
                print(f"MISSING {item}: {p}")
                bad += 1
            elif sha256(p) != entry["sha256"]:
                print(f"CHANGED {item}: {p} no longer matches the manifest")
                bad += 1
    for root, _, files in os.walk(a.store):
        for f in files:
            rel = os.path.normpath(os.path.relpath(os.path.join(root, f), a.store))
            if rel not in listed:
                print(f"UNLISTED {rel}: in the store but not in the manifest")
                bad += 1
    print("verify: ok" if not bad else f"verify: {bad} problem(s)")
    return 1 if bad else 0


def cmd_check(a):
    m = load(a)
    by_hash = {e["sha256"]: item for item, e in m.items()}
    bad = degraded = seen = 0
    for root, _, files in os.walk(a.dir):
        for f in sorted(files):
            p = os.path.join(root, f)
            rel = os.path.relpath(p, a.dir)
            seen += 1
            item = by_hash.get(sha256(p))
            if item is None:
                print(
                    f"NOT HELD {rel}: no original in the store matches it byte for byte"
                )
                bad += 1
            elif m[item]["status"] != "exact":
                print(f"DEGRADED {rel} = {item}: {m[item]['note']}")
                degraded += 1
            else:
                print(f"ok {rel} = {item}")
    if not seen:
        print(f"check: {a.dir} holds no files")
        return 1
    line = f"check: {seen} file(s), {bad} not held, {degraded} degraded"
    if degraded:
        line += (
            " (allowed)"
            if a.allow_degraded
            else "; pass --allow-degraded to accept them"
        )
    print(line)
    return 1 if bad or (degraded and not a.allow_degraded) else 0


def cmd_send(a):
    m = load(a)
    plan = {}
    for pair in a.pairs:
        item, _, name = pair.partition("=")
        if item not in m:
            print(
                f"REFUSED {item}: not in the store; add its best file first. Nothing was sent"
            )
            return 1
        ext = os.path.splitext(m[item]["file"])[1]
        stem = name or item
        if stem.lower().endswith(ext):
            stem = stem[: -len(ext)]
        if stem + ext in plan:
            print(
                f"REFUSED {item}: {stem + ext} is already named for {plan[stem + ext]}. Nothing was sent"
            )
            return 1
        plan[stem + ext] = item
    os.makedirs(a.dir, exist_ok=True)
    for out, item in plan.items():
        shutil.copyfile(
            os.path.join(a.store, m[item]["file"]), os.path.join(a.dir, out)
        )
    return cmd_check(a)


def main(argv=None):
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument(
        "--root",
        help="the project's repo (default: the git repo holding the current directory)",
    )
    s = p.add_subparsers(dest="cmd", required=True)
    s.add_parser("init")
    x = s.add_parser("add")
    x.add_argument("id")
    x.add_argument("file")
    x.add_argument("--source", required=True)
    x.add_argument("--status", choices=("exact", "degraded"), required=True)
    x.add_argument("--note")
    x.add_argument("--supersede")
    s.add_parser("verify")
    for name in ("check", "send"):
        x = s.add_parser(name)
        x.add_argument("dir")
        x.add_argument("--allow-degraded", action="store_true")
        if name == "send":
            x.add_argument("pairs", nargs="+")
    a = p.parse_args(argv)
    a.root = a.root or git_root()
    if not a.root:
        p.error("not inside a git repo; pass --root")
    a.root = os.path.abspath(a.root)
    a.store = os.path.join(a.root, STORE)
    a.manifest = os.path.join(a.root, MANIFEST)
    cmds = {
        "init": cmd_init,
        "add": cmd_add,
        "verify": cmd_verify,
        "check": cmd_check,
        "send": cmd_send,
    }
    return cmds[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
