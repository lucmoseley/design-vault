"""access-pointer.py — check-access.py's --pointer mode (#317): answers
vault.coarse-target, whether targets are sized for the pointer in use. Its
only I/O is the browser and conditions.py its caller hands run().

At each of check-access.py's widths the page is opened twice through
conditions.py, once under a coarse pointer and once under a fine one:

- coarse: every target check-access.py's vault.target-size measures must
  measure THE COARSE FLOOR or more each way. Exempt are links set in running
  text and a Tab stop hidden at rest, as there; WCAG 2.5.8's spacing and
  user-agent exceptions do not apply. A
  control inside its own label is measured by the label's box, which a tap
  on works it too;
- fine: no target may be smaller than it is with every pointer and hover media
  rule switched off, `(pointer)`, `(any-pointer)`, `(hover)` and
  `(any-hover)` in an @media rule, an @import or a <link> media, read with
  transitions off. A style sheet from another
  site cannot be read, so its rules stay on, and a note names it. A size a
  script sets by matchMedia is not seen. The fine pointer's floor itself is
  vault.target-size's, which check-access.py's own run answers.

THE COARSE FLOOR is read from the table, check-access-pointer.table beside
this script or check-access.py's --pointer-table FILE: the line `vault.coarse-target | coarse |
<n>px`. A project's rules file may set its own, never under vault.target-size's
floor.
"""

import json
import os
import re

# The --pointer coarse floor, from vault.coarse-target's record.
TABLE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "check-access-pointer.table"
)
SEP = " | "
FLOOR = re.compile(r"(\d+(?:\.\d+)?)px")
QUESTION = (
    "vault.coarse-target",
    "targets sized for the pointer (WCAG 2.5.5, web.dev)",
)


class TableError(Exception):
    """A table line --pointer cannot run: exit 2."""


def parse_table(text, least):
    """The coarse floor in px from the table's one line, vault.coarse-target's,
    `least` px or more."""
    found = None
    for n, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        fields = [f.strip() for f in line.split(SEP)]
        if len(fields) != 3 or fields[:2] != [QUESTION[0], "coarse"]:
            raise TableError(
                f"line {n}: want {QUESTION[0]} | coarse | <n>px, got {line!r}"
            )
        m = FLOOR.fullmatch(fields[2])
        if not m:
            raise TableError(
                f"line {n}: coarse wants a value like 44px, got {fields[2]!r}"
            )
        if found is not None:
            raise TableError(f"line {n}: a second coarse line")
        floor = float(m.group(1))
        if floor < least:
            raise TableError(
                f"line {n}: coarse may not be under vault.target-size's {least:g}px, got {fields[2]!r}"
            )
        found = floor
    if found is None:
        raise TableError("no coarse line")
    return found


TARGETS_JS = r"""
const resting = restingStops();
const targets = () => pointerTargets((el) => resting.some((r) => r.contains(el)));
const tapBox = (el) => {
  const wrap = [...(el.labels || [])].find((l) => l.contains(el));
  return (wrap || el).getBoundingClientRect();
};
const sized = (r) => `${Math.round(r.width)}x${Math.round(r.height)}`;
"""

COARSE_JS = (
    TARGETS_JS
    + r"""
return targets().filter((el) => !inText(el)).flatMap((el) => {
  const r = tapBox(el);
  return r.width < FLOOR - PX_SLACK || r.height < FLOOR - PX_SLACK
    ? [{ subject: label(el), detail: `is ${sized(r)} px under a coarse pointer; ${FLOOR}x${FLOOR} px needed` }] : [];
});
"""
)

FINE_JS = (
    TARGETS_JS
    + r"""
const POINTER_MEDIA = /\b(any-)?(pointer|hover)\b/;
const els = targets();
const before = els.map(tapBox);
const still = document.createElement('style');
still.textContent = '*, *::before, *::after { transition: none !important }';
document.head.append(still);
const unread = [];
const off = (media) => { if (media && POINTER_MEDIA.test(media.mediaText)) media.mediaText = 'not all'; };
const walkRules = (rules) => {
  for (const rule of rules) {
    if (rule instanceof CSSImportRule) {
      off(rule.media);
      if (rule.styleSheet) walkSheet(rule.styleSheet);
      continue;
    }
    if (rule instanceof CSSMediaRule) off(rule.media);
    if (rule.cssRules) walkRules(rule.cssRules);
  }
};
const walkSheet = (sheet) => {
  off(sheet.media);
  let rules;
  try { rules = sheet.cssRules; } catch (e) { unread.push(sheet.href); return; }
  walkRules(rules);
};
for (const sheet of [...document.styleSheets, ...document.adoptedStyleSheets]) walkSheet(sheet);
const faults = [];
els.forEach((el, i) => {
  const was = before[i], now = tapBox(el);
  if (was.width < now.width - PX_SLACK || was.height < now.height - PX_SLACK) {
    faults.push({ subject: label(el), detail: `is ${sized(was)} px under a fine pointer, smaller than the ${sized(now)} px it is given with its pointer and hover media rules off` });
  }
});
return { faults, unread };
"""
)


def judged(page, pointer, script, answering):
    """One page's Judged for vault.coarse-target under `pointer`, `script`
    making a page function of a body."""
    if pointer == "coarse":
        return answering.Judged(page.evaluate(script(COARSE_JS)), [], [], [])
    got = page.evaluate(script(FINE_JS))
    notes = [
        f"the style sheet {href} cannot be read, as another site's cannot without CORS, so its pointer and hover rules were left on"
        for href in got["unread"]
    ]
    return answering.Judged(got["faults"], [], [], notes)


def run(browser, at, viewports, *, conditions, layout, page_js, answering):
    """[(width name, {question id: Judged})], each width's two pointers
    merged, and how many looping animations never finished."""
    consts = f"const FLOOR = {json.dumps(at.pointer_floor)};\n"

    def script(body):
        return page_js(layout.flow.LABEL_JS + consts + f"() => {{\n{body}\n}}")

    found, looping = [], 0
    for name, width, height in viewports:
        mine = answering.unjudged()
        for pointer in conditions.POINTERS:
            with conditions.open_page(
                browser,
                at.url,
                pointer=pointer,
                viewport={"width": width, "height": height},
            ) as page:
                page.set_default_timeout(at.timeout)
                looping = max(looping, page.evaluate(layout.SETTLE_JS))
                for into, got in zip(
                    mine, judged(page, pointer, script, answering), strict=True
                ):
                    into.extend(got)
        found.append((name, {QUESTION[0]: mine}))
    return found, looping
