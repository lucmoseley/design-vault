#!/usr/bin/env python3
"""USAGE
  python3 check-clip.py <clip.mp4>… [--range MIN-MAX] [--log <higgsfield-spend.jsonl>]

Length (vault.length), with --range, the motion brief's range in seconds: the
clip's duration over its timescale, from the MP4 header's `moov`/`mvhd` box,
lies inside the range, its ends included. With no --range, the length is printed and NOT JUDGED. A header that
gives no duration, a fragmented clip's, is NOT JUDGED.

Loop (vault.clip-loop): the clip's spend-log line, in --log or else the log
beside each clip, sent the same still as
the model's start frame and its end frame, as one URL, the fields read from
references/loop-fields.json with their source. A model with no row there, or a
clip with no log line, is NOT JUDGED, never passed.

EXITS 0 every clip passes / 1 a clip fails / 2 the arguments are wrong, or a
clip, the log or loop-fields.json cannot be read / 6 no clip fails but one cannot be judged. It
never exits 3. Exits 0, 1 and 6 are
results and print on stdout; the rest print on stderr.
An exception it does not handle once loaded exits 2, its traceback on stderr.
"""

import argparse
import json
import pathlib
import re
import struct
import sys

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import siblings  # noqa: E402
from crash_exit import run_main  # noqa: E402

FIELDS = HERE.parent / "references" / "loop-fields.json"


spend_log = siblings.load(HERE, "spend-log.py")
UnreadableError = spend_log.UnreadableError

PASS, FAIL, UNJUDGED = "PASS", "FAIL", "NOT JUDGED"

RANGE = re.compile(r"(\d+(?:\.\d+)?)-(\d+(?:\.\d+)?)")


def read_fields():
    try:
        models = json.loads(FIELDS.read_text(encoding="utf8"))["models"]
        for model, row in models.items():
            if not all(
                isinstance(row.get(k), str) and row[k]
                for k in ("start", "end", "source")
            ):
                raise ValueError(f"{model} lacks a start, an end or a source")
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as err:
        raise UnreadableError(f"cannot read {FIELDS}: {err}") from err
    return models


def boxes(f, start, end):
    at = start
    while at + 8 <= end:
        f.seek(at)
        size, kind = struct.unpack(">I4s", f.read(8))
        header = 8
        if size == 1:
            size = struct.unpack(">Q", f.read(8))[0]
            header = 16
        elif size == 0:
            size = end - at
        kind = kind.decode("latin1")
        if size < header or at + size > end:
            raise UnreadableError(f"a {kind!r} box at byte {at} runs past its parent")
        yield kind, at + header, at + size
        at += size


def read_length(clip):
    try:
        with open(clip, "rb") as f:
            end = f.seek(0, 2)
            moov = next(((s, e) for k, s, e in boxes(f, 0, end) if k == "moov"), None)
            if moov is None:
                raise UnreadableError(f"{clip} has no moov box: not an MP4 clip")
            mvhd = next(((s, e) for k, s, e in boxes(f, *moov) if k == "mvhd"), None)
            if mvhd is None:
                raise UnreadableError(f"{clip} has no mvhd box in its moov")
            f.seek(mvhd[0])
            body = f.read(mvhd[1] - mvhd[0])
    except OSError as err:
        raise UnreadableError(f"cannot read {clip}: {err.strerror}") from err
    except struct.error as err:
        raise UnreadableError(f"{clip} ends inside a box header") from err
    version = body[0] if body else None
    layout = {0: (">IIII", 0xFFFFFFFF), 1: (">QQIQ", 0xFFFFFFFFFFFFFFFF)}.get(version)
    if layout is None:
        raise UnreadableError(f"{clip}'s mvhd is version {version}, not 0 or 1")
    form, unknown = layout
    try:
        _, _, timescale, duration = struct.unpack_from(form, body, 4)
    except struct.error as err:
        raise UnreadableError(
            f"{clip}'s mvhd is too short for version {version}"
        ) from err
    if timescale == 0 or duration in (0, unknown):
        return None
    return duration / timescale


def check_length(length, span):
    if length is None:
        return UNJUDGED, "the header gives no duration (a fragmented clip?)"
    figure = f"{length:.3f} s"
    if span is None:
        return UNJUDGED, f"{figure}; no range: give --range from the motion brief"
    low, high = span
    if low <= length <= high:
        return PASS, f"{figure}, inside {low:g}-{high:g} s"
    side = "shorter" if length < low else "longer"
    return FAIL, (
        f"{figure}, {side} than the brief's {low:g}-{high:g} s: render it again "
        "with a duration inside the range"
    )


def check_loop(entry, where, fields):
    if entry is None:
        return UNJUDGED, where
    model = entry.get("model")
    if model not in fields:
        return (
            UNJUDGED,
            f"{model or 'no model'} has no row in loop-fields.json",
        )
    start_field, end_field = fields[model]["start"], fields[model]["end"]
    given = entry.get("input") if isinstance(entry.get("input"), dict) else {}
    start, end = given.get(start_field), given.get(end_field)
    if not start:
        return (
            FAIL,
            f"the request sent no start frame, {start_field}: render it again with the still as both {start_field} and {end_field}",
        )
    if not end:
        return (
            FAIL,
            f"the request sent no end frame, {end_field}: render it again with {end_field} set to {start_field}'s still",
        )
    if start != end:
        return (
            FAIL,
            f"{start_field} {start} and {end_field} {end} differ: render it again with one still as both",
        )
    return PASS, f"{start_field} and {end_field} both send {start}"


def read_range(text):
    match = RANGE.fullmatch(text.replace(" ", ""))
    if not match or float(match[1]) > float(match[2]):
        raise argparse.ArgumentTypeError(
            f"{text} is not MIN-MAX seconds, MIN no more than MAX"
        )
    return float(match[1]), float(match[2])


def main(argv):
    parser = argparse.ArgumentParser(
        prog="check-clip.py",
        description="Check generated clips: the length against the brief's range, and that the request sent one still as start and end frame.",
    )
    parser.add_argument("clips", nargs="+", metavar="clip")
    parser.add_argument(
        "--range",
        type=read_range,
        help="the motion brief's length range, MIN-MAX seconds",
    )
    parser.add_argument(
        "--log",
        help=f"the round's spend log; default the {spend_log.LOG_NAME} beside each clip",
    )
    args = parser.parse_args(argv)

    try:
        fields = read_fields()
    except UnreadableError as err:
        print(f"check-clip: {err}", file=sys.stderr)
        return 2
    logs = {}
    results = []
    for clip in args.clips:
        try:
            length = read_length(clip)
            entry, where = spend_log.find_line(clip, args.log, logs)
        except UnreadableError as err:
            print(f"check-clip: {err}", file=sys.stderr)
            return 2
        model = entry.get("model") if entry else None
        print(f"{clip} — {model or 'model unknown'} ({where})")
        for name, (verdict, detail) in (
            ("length", check_length(length, args.range)),
            ("loop", check_loop(entry, where, fields)),
        ):
            results.append(verdict)
            print(f"  {name}: {verdict} — {detail}")

    if FAIL in results:
        return 1
    return 6 if UNJUDGED in results else 0


if __name__ == "__main__":
    run_main(main)
