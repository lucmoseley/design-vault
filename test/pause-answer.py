import json
import os
import sys

from playwright.sync_api import sync_playwright

SCRIPTS = os.path.join(
    os.path.dirname(__file__), "..", "plugin", "skills", "design-round", "scripts"
)
sys.path.insert(0, SCRIPTS)
import siblings  # noqa: E402

if __name__ == "__main__":
    job = json.loads(sys.argv[1])
    access = siblings.load(SCRIPTS, "check-access.py")
    access.WATCH_MS = job["watch_ms"]
    logged = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        ctx = browser.new_context()
        ctx.on("console", lambda m: logged.append(m.text))
        if job["init"]:
            ctx.add_init_script(job["init"])
        faults, unmeasured = access.pause_answer(ctx, job["url"], job["carousels"], [])
        ctx.close()
        browser.close()
    json.dump(
        {"faults": faults, "unmeasured": unmeasured, "logged": logged}, sys.stdout
    )
