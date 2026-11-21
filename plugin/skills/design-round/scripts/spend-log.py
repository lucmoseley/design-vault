"""spend-log.py — reads a round's spend log, the `higgsfield-spend.jsonl`
higgsfield.js appends one line to per request, and finds a candidate's line in
it, for the checks that read what was asked of the model: check-render.py and
check-clip.py (design-vault#336).

A file's line is the last whose `candidate` is the file's folder and stem,
`r2/v3-grok` for `r2/v3-grok.png`, and for a request's later outputs,
`r2/v3-grok-2.png`, the line of the stem without its `-<n>`. The log is the one
the caller names, or else the `higgsfield-spend.jsonl` beside the file.
"""

import json
import os
import pathlib
import re

LOG_NAME = "higgsfield-spend.jsonl"


class UnreadableError(Exception):
    pass


def read_log(path):
    """The log's lines by candidate."""
    lines = {}
    try:
        text = pathlib.Path(path).read_text(encoding="utf8")
    except OSError as err:
        raise UnreadableError(f"cannot read {path}: {err.strerror}") from err
    for n, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError as err:
            raise UnreadableError(f"{path}:{n} is not JSON: {err.msg}") from err
        if isinstance(entry, dict) and isinstance(entry.get("candidate"), str):
            lines[entry["candidate"]] = entry
    return lines


def candidates(file):
    """The file's candidate, then, for a request's later output, its first's."""
    p = pathlib.Path(file)
    own = f"{p.resolve().parent.name}/{p.stem}"
    first = re.sub(r"-\d+$", "", own)
    return [own] if first == own else [own, first]


def find_line(file, log, logs):
    """(the file's log line or None, where it came from or why there is none).
    log is the caller's --log or None, and a --log that cannot be read raises;
    logs is the caller's cache of the spend logs read so far, filled here."""
    if log is None:
        log = os.path.join(os.path.dirname(file) or ".", LOG_NAME)
        if not os.path.exists(log):
            return None, "no spend log"
    if log not in logs:
        logs[log] = read_log(log)
    name = next((c for c in candidates(file) if c in logs[log]), None)
    if name is None:
        return None, f"no line for {candidates(file)[0]} in {log}"
    return logs[log][name], f"{log}, line for {name}"
