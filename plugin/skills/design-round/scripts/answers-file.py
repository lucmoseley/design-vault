import datetime
import json
import os
import pathlib


def start(out, name, *stale):
    os.makedirs(out, exist_ok=True)
    path = pathlib.Path(out, name)
    for old in [path, *(m for g in stale for m in pathlib.Path(out).glob(g))]:
        old.unlink(missing_ok=True)
    when = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
    return when, str(path)


def write(path, url, when, **fields):
    if "answers" not in fields:
        raise TypeError("write() needs an answers field")
    with open(path, "w", encoding="utf8") as fh:
        json.dump(
            {"url": url, "run_at": when.isoformat(), **fields},
            fh,
            indent=1,
            ensure_ascii=False,
        )
        fh.write("\n")
