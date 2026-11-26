"""#139's loop: #136's stalled screenshot pointed at check-frames, contact-sheet and check-layout.
Run by hand, never by the gate:
    python3 test/load/sibling-shots.py <frames-last|frames-hash|sheet|layout> [runs=30] [busy=16]

Runs the script's own main() in-process on a fixture from its suite, beside <busy> CPU busy loops at the
lowest priority, with check-overlay-shot.py's stall on every page.screenshot() call. Prints the exit counts
and each screenshot line's outcomes. An exit 5 with "Unable to capture screenshot" means that script needs
check-overlay's SHOTS retry; none, over the stalled first shots the counts show, means it is not exposed.
#139 has the counts, taken with the loops at normal priority; #147 has check-overlay's at the lowest.
"""

import importlib.util
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.join(HERE, "..", "..", "plugin", "skills", "design-round", "scripts")
FIXTURES = os.path.join(HERE, "..", "fixtures")
sys.path.insert(0, SCRIPTS)
import siblings  # noqa: E402


# Private: a harness, which no design-round script loads back, so siblings.load's one copy is not owed (#606).
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


shot = load("check_overlay_shot", os.path.join(HERE, "check-overlay-shot.py"))

# name: (script, its arguments before --out, the exit its suite expects). layout is check-layout.test.py's
# "shots", the one case that reaches all six screenshot widths at a quick step.
TARGETS = {
    "frames-last": (
        "check-frames.py",
        [
            "last",
            os.path.join(FIXTURES, "frames", "twice.html"),
            "--at",
            "#logo",
            "--asset",
            os.path.join(FIXTURES, "frames", "mark.svg"),
        ],
        1,
    ),
    "frames-hash": (
        "check-frames.py",
        ["hash", os.path.join(FIXTURES, "frames", "draft", "index.html")],
        0,
    ),
    "sheet": ("contact-sheet.py", [os.path.join(FIXTURES, "sheet", "ramp.html")], 0),
    "layout": (
        "check-layout.py",
        [os.path.join(FIXTURES, "layout", "clean.html"), "--step", "400"],
        0,
    ),
}


def main(target, runs=shot.RUNS, busy=shot.BUSY):
    script, args, expected = TARGETS[target]
    module = siblings.load(SCRIPTS, script)

    def call():
        with tempfile.TemporaryDirectory() as out:
            return module.main([*args, "--out", out])

    print(target, flush=True)
    return shot.loop(call, expected, runs, busy)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], *(int(a) for a in sys.argv[2:4])))
