import json
import os
import pathlib
import re

LOG_NAME = "higgsfield-spend.jsonl"


class UnreadableError(Exception):
    pass


def read_log(path):
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
    p = pathlib.Path(file)
    own = f"{p.resolve().parent.name}/{p.stem}"
    first = re.sub(r"-\d+$", "", own)
    return [own] if first == own else [own, first]


def find_line(file, log, logs):
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
