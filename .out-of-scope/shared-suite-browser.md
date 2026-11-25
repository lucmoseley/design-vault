# One browser shared across a Python suite's cases

The Python gate suites do not share one Chromium across their cases: each script a case runs launches its own, through `check-flow.py`'s `chromium()` (#376).

## Why this is out of scope

A suite case runs a design-round script as its own Python process, through `test/child.py`. Every such process pays for its own Playwright driver, whether it then launches a browser or connects to one already running. Measured on this machine with Playwright 1.61.0, five runs each:

| Step in one process | Time |
| --- | --- |
| `sync_playwright()` starting the driver | 0.33–0.45 s |
| `chromium.launch()` then `close()` | 0.10–0.23 s |
| `connect_over_cdp()` to a running Chromium, then a context and close | 0.38–0.41 s |

Connecting to a shared browser costs more than launching a fresh one, so a browser handed to each process costs time rather than saving it.

The saving #376 counted, about 100 s, comes almost all from the driver start. Only removing the per-case process removes that, by running each case in the suite's own process against a browser it opens once. That rewrite also takes away the isolation each case gets now:

- `chromium()` watches for a hung call by the one new browser process it sees under its own pid (`CallWatch`). A browser that outlives the case leaves nothing to watch.
- `child.main()` reruns a test that crashed after earlyoom killed one of its renderers (#438). With a shared browser, one killed renderer or one crashed browser fails every case after it.
- Launch flags differ by script (`HASH_ARGS`, `--disable-threaded-animation`, `--allow-file-access-from-files`), so a shared browser would be one per flag set, each a second copy of state that today starts empty for every case.

The issue stated a shared browser that lets state leak between cases is a regression. The only form of sharing that saves time is the one that loses that isolation.

Running a script's logic in the test's own process is still the core-and-shell rule (lucmoseley/workflow-core#2186). It reaches design-vault only for new and changed code (lucmoseley/workflow-core#2243), one script at a time, with its own browser per case. That is not this request.
