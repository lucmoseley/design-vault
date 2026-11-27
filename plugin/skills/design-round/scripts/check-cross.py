#!/usr/bin/env python3
"""USAGE
  python3 check-cross.py <home page> --out DIR [--flow URL]… [--form SELECTOR]
        [--table FILE] [--timeout MS]

The home page is a URL or a local HTML file. From it the probe follows every
link to a page on the same site, an http(s) page on the same origin or a
local file in the home page's folder or below it, and reads each page it
reaches. A page that will not load is listed and not read.

Each --flow names a flow's first step. The probe fills that step's form with
valid values (drive-form.py), submits it, and on the step it reaches reads
every field. It then presses the browser's Back button and reads the step it
left, presses Forward, and goes on, until a step has no form, a submit does
not move on, or a step comes round again. A submit that reaches a page with
no form ends the flow, and Back is not pressed after it. That submit is
really sent, so run the probe on a candidate, never a live site. --form
names the form on every step, by a CSS selector; without it each step's
first <form> is driven. A flow's steps are exempt from the multiple-ways
line.

THE TABLE, by default check-cross.table beside this script, gives each line
as fields split by " | ": the record id, the check, and the value it reads,
where it reads one. Blank lines and lines starting with # are skipped.

  phone <device>      each page loaded as Playwright's <device> ends on the
                      same URL as on a desktop, and names no separate mobile
                      page (a link rel=alternate with a media query)
  order               each navigation repeated on another page keeps the
                      items both share in the same relative order there, an
                      item being a link's text and target
  ways >= N           each page outside a flow is reached in N or more
                      ways: navigation (a link to it in a navigation
                      landmark, the header or the footer of another page),
                      links (a link to it anywhere else on another page),
                      search (the site has a search: role=search, <search>
                      or a search field)
  home-hub pages <= N on a site of N pages or fewer whose home page links
                      every other page, a page that links back to the home
                      page passes the ways line on the home-hub line's own
                      record however many ways it has; a home-hub line on a
                      record with no ways line is refused
  back                in a flow, Back from a step shows the step before at
                      its own URL with every value typed into it
  repeat              in a flow, a field whose autocomplete token an
                      earlier step's field was given arrives holding that
                      field's value; a bare on, off or detail word is no token

Each record id's finding is fail where any check misses, else not judged
where a check could not run (a flow that pressed Back after no step, or
reached no second step), else
pass, or no match where a check found nothing to compare. DIR/cross.json
holds every finding and what each page read; an earlier run's is deleted.

A family script loads it by path and calls the library:

    phone = cross.device("Pixel 7")
    pages, unread = cross.crawl(browser, home)     # {url: read}, [(url, why)]
    phones = cross.phone_urls(browser, list(pages), phone)
    walks = [cross.walk(browser, first_step)]
    found = cross.findings(table, pages, walks, phones=phones, home=home)

EXITS 0 no miss / 1 a miss (each printed) / 2 the arguments or the table are
wrong / 3 Playwright or its browser is missing / 4 a page did not render in time
/ 5 the browser refused the home page or a flow's first step / 7 a call hung that
would never return. Exits 0 and 1 print on stdout; the rest print on stderr.
An exception it does not handle once loaded exits 2, its traceback on stderr.
"""

import argparse
import collections
import difflib
import os
import re
import sys
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import siblings  # noqa: E402
from crash_exit import run_main  # noqa: E402
from fail_open import expected  # noqa: E402


runner = siblings.load(HERE, "runner.py")
answers_file = siblings.load(HERE, "answers-file.py")
form = siblings.load(HERE, "drive-form.py")
rule_table = siblings.load(HERE, "rule-table.py")

TABLE = os.path.join(HERE, "check-cross.table")
CHECKS = {
    "phone": re.compile(r"\S.*"),
    "order": None,
    "ways": re.compile(r">=\s*(\d+)"),
    "home-hub": re.compile(r"pages\s*<=\s*(\d+)"),
    "back": None,
    "repeat": None,
}
WAYS = ("navigation", "links", "search")

Step = collections.namedtuple("Step", "url typed arrived back")
Walk = collections.namedtuple("Walk", "start steps ended")
LAST_SUBMIT = "the last step's submit, after which Back is not pressed"


TableError = rule_table.TableError


def parse(text):
    lines = rule_table.parse(text, CHECKS, _line_value)
    first_by_check = {}
    for line in lines:
        first = first_by_check.setdefault(line.check, line)
        if first.value != line.value:
            raise TableError(
                f"{line.text!r}: {line.check} is already given a different value by "
                f"{first.text!r}, and the table gives each check one value"
            )
    ways = {line.id for line in lines if line.check == "ways"}
    for line in lines:
        if line.check == "home-hub" and line.id not in ways:
            raise TableError(
                f"{line.text!r}: home-hub relaxes its own record's ways line, and {line.id} has none"
            )
    return lines


def _line_value(n, check, m):
    if m is None:
        return None
    return int(m[1]) if m.groups() else m[0]


PAGE_JS = r"""
() => {
  const NAV = 'nav, [role="navigation"]';
  const CHROME = `${NAV}, header, footer, [role="banner"], [role="contentinfo"]`;
  const bare = (href) => { const u = new URL(href, location.href); u.hash = ""; return u.href; };
  const drawn = (el) => el.getClientRects().length > 0;
  const text = (el) => (el.innerText ?? el.textContent).replace(/\s+/g, " ").trim();
  const links = [...document.querySelectorAll("a[href], area[href]")]
    .filter((a) => drawn(a) && !/^(mailto|tel|javascript):/i.test(a.getAttribute("href")))
    .map((a) => ({ href: bare(a.href), nav: !!a.closest(CHROME) }));
  const navs = [...document.querySelectorAll(NAV)]
    .filter((n) => drawn(n) && !n.parentElement?.closest(NAV))
    .map((n) => [...n.querySelectorAll("a[href]")].filter(drawn)
      .map((a) => `${text(a)} -> ${bare(a.href)}`));
  const search = !!document.querySelector(
    '[role="search"], search, input[type="search"]');
  const mobile = [...document.querySelectorAll('link[rel~="alternate"][media][href]')]
    .map((l) => bare(l.href));
  return { url: bare(location.href), links, navs, search, mobile };
}
"""


def _bare(url):
    return urllib.parse.urldefrag(url)[0]


def on_site(home, url):
    h, u = urllib.parse.urlsplit(home), urllib.parse.urlsplit(url)
    if h.scheme == "file":
        folder = h.path.rsplit("/", 1)[0] + "/"
        return u.scheme == "file" and u.path.startswith(folder)
    return u.scheme in ("http", "https") and (u.scheme, u.netloc) == (
        h.scheme,
        h.netloc,
    )


def _open(page, url):
    form.after(page, lambda: page.goto(url))
    return page.evaluate(PAGE_JS)


def crawl(browser, home, read=None, **context):
    from playwright.sync_api import Error as PlaywrightError

    pages, unread, queue, seen = {}, [], [_bare(home)], {_bare(home)}
    ctx = browser.new_context(**context)
    try:
        page = ctx.new_page()
        while queue:
            url = queue.pop(0)
            try:
                got = _open(page, url)
            except PlaywrightError as exc:
                if url == _bare(home):
                    raise
                unread.append((url, runner.first_line(exc)))
                continue
            if read is not None:
                got["read"] = read(page)
            pages.setdefault(got["url"], got)
            for link in got["links"]:
                if link["href"] not in seen and on_site(home, link["href"]):
                    seen.add(link["href"])
                    queue.append(link["href"])
    finally:
        ctx.close()
    return pages, unread


def phone_urls(browser, urls, device):
    ctx = browser.new_context(**device)
    try:
        page = ctx.new_page()
        out = {}
        for url in urls:
            got = _open(page, url)
            out[url] = (got["url"], got["mobile"])
        return out
    finally:
        ctx.close()


def walk(browser, start, selector=None):
    ctx = browser.new_context()
    try:
        page = ctx.new_page()
        form.after(page, lambda: page.goto(start))
        steps, seen = [], set()
        while True:
            try:
                fields = form.fields(page, selector)
            except form.FormError as exc:
                expected(exc, "the walk ends")
                return Walk(start, steps, "a step with no form")
            url = _bare(page.url)
            if (url, tuple(f.key for f in fields)) in seen:
                return Walk(start, steps, "a step came round again")
            seen.add((url, tuple(f.key for f in fields)))
            arrived = [(f.key, f.token, f.value) for f in fields]
            filled = form.fill(page, selector)
            typed = {f.key: f.value for f in filled if f.value is not None}
            settled = form.submit(page, selector)
            if not settled.navigated and _bare(settled.url) == url:
                steps.append(Step(url, typed, arrived, None))
                return Walk(start, steps, "a submit that did not move on")
            if not _has_form(page, selector):
                steps.append(Step(url, typed, arrived, None))
                return Walk(start, steps, LAST_SUBMIT)
            back = form.after(page, page.go_back)
            steps.append(Step(url, typed, arrived, back))
            ahead = form.after(page, page.go_forward)
            if _bare(ahead["url"]) != _bare(settled.url):
                return Walk(
                    start,
                    steps,
                    f"Forward from {url} did not return to {_bare(settled.url)}",
                )
    finally:
        ctx.close()


def _has_form(page, selector):
    try:
        form.fields(page, selector)
    except form.FormError as exc:
        expected(exc, "no form")
        return False
    return True


def _token(token):
    words = " ".join(token.lower().split())
    return words if form.name_of(words) else None


def findings(table, pages, walks, *, phones, home):
    answers = rule_table.Answers(table, "page")
    hubs = {line.id: line for line in table if line.check == "home-hub"}
    for line in {(line.id, line.check): line for line in table}.values():
        if line.check == "phone" and phones is not None:
            _phone(answers, line, phones)
        elif line.check == "order":
            _order(answers, line, pages)
        elif line.check == "ways":
            _ways(answers, line, hubs.get(line.id), pages=pages, walks=walks, home=home)
        elif line.check == "back":
            for w in walks:
                _back(answers, line, w)
        elif line.check == "repeat":
            for w in walks:
                _repeat(answers, line, w)
    return answers.done()


def _phone(answers, line, phones):
    for url, (ended, mobile) in phones.items():
        answers.met(line)
        if ended != url:
            answers.miss(line, url, f"as {line.value} it ends on {ended}")
        for m in mobile:
            answers.miss(line, url, f"names a separate mobile page, {m}")


def _order(answers, line, pages):
    urls = list(pages)
    for i, b in enumerate(urls):
        for nav in pages[b]["navs"]:
            for a in urls[:i]:
                best = max(
                    pages[a]["navs"],
                    key=lambda other: len(set(nav) & set(other)),
                    default=[],
                )
                shared = set(nav) & set(best)
                if len(shared) < 2:
                    continue
                answers.met(line)
                here = [h for h in dict.fromkeys(best) if h in shared]
                there = [h for h in dict.fromkeys(nav) if h in shared]
                if here != there:
                    answers.miss(
                        line,
                        b,
                        f"its navigation orders {_names(there)}; {a} orders {_names(here)}",
                    )
                break


def _names(items):
    return ", ".join(i.split(" -> ")[0] for i in items)


def _ways(answers, line, hub, *, pages, walks, home):
    steps = {s.url for w in walks for s in w.steps} | {_bare(w.start) for w in walks}
    search = any(p["search"] for p in pages.values())
    home = _bare(home)
    others = set(pages) - {home}
    hub_holds = (
        hub is not None
        and len(pages) <= hub.value
        and home in pages
        and others <= {a["href"] for a in pages[home]["links"]}
    )
    for url in pages:
        if url in steps:
            continue
        answers.met(line)
        ways = {"search"} if search else set()
        for other, read in pages.items():
            if other == url:
                continue
            for link in read["links"]:
                if link["href"] == url:
                    ways.add("navigation" if link["nav"] else "links")
        if len(ways) >= line.value:
            continue
        if (
            hub_holds
            and url != home
            and any(a["href"] == home for a in pages[url]["links"])
        ):
            continue
        found = ", ".join(w for w in WAYS if w in ways) or "none"
        answers.miss(
            line, url, f"reached {len(ways)} way(s) ({found}), wants {line.value}"
        )


def _back(answers, line, w):
    judged = [s for s in w.steps if s.back is not None]
    if not judged:
        answers.unjudged(line, w.start, f"Back was pressed after no step: {w.ended}")
    for s in judged:
        answers.met(line)
        if _bare(s.back["url"]) != s.url:
            answers.miss(
                line, s.url, f"Back went to {_bare(s.back['url'])}, not this step"
            )
            continue
        held = {f["key"]: f["value"] for f in s.back["fields"]}
        for key, value in s.typed.items():
            if held.get(key) != value:
                answers.miss(
                    line,
                    s.url,
                    f"Back shows {key} as {held.get(key)!r}, not the {value!r} typed",
                )


def _repeat(answers, line, w):
    if len(w.steps) < 2:
        answers.unjudged(line, w.start, f"the flow reached no second step: {w.ended}")
        return
    given = {}
    for s in w.steps:
        for key, token, value in s.arrived:
            t = _token(token)
            if t in given:
                answers.met(line)
                was_key, was = given[t]
                if value != was:
                    answers.miss(
                        line,
                        s.url,
                        f"{key} ({t}) arrives as {value!r}, though {was_key} was given {was!r}",
                    )
        tokens = {k: _token(t) for k, t, _ in s.arrived}
        for key, value in s.typed.items():
            if tokens.get(key) and isinstance(value, str):
                given[tokens[key]] = (key, value)


def device(name):
    from playwright.sync_api import sync_playwright

    with sync_playwright() as play:
        if name not in play.devices:
            near = difflib.get_close_matches(name, list(play.devices), n=3, cutoff=0)
            raise TableError(
                f"Playwright knows no device {name!r}; the nearest it knows: {', '.join(near)}"
            )
        return dict(play.devices[name])


def report(at, found, unread, walks):
    lines = [f"check-cross: {at.url}"]
    for url, why in unread:
        lines.append(f"  not read: {url}: {why}")
    for w in walks:
        lines.append(f"  flow {w.start}: {len(w.steps)} step(s), ended at {w.ended}")
    for f in found:
        lines.append(f"{f['id']}: {f['answer']}")
        for m in f["misses"]:
            lines.append(f"  - [{m['check']}] {m['page']}: {m['what']}")
        for m in f["unjudged"]:
            lines.append(f"  ? [{m['check']}] {m['page']}: {m['what']}")
    return "\n".join(lines)


def parse_args(argv):
    p = argparse.ArgumentParser(
        prog="check-cross.py",
        description="Open every page of a site, and walk each flow, and answer the rule records that compare pages.",
    )
    p.add_argument("url", help="the home page: an http(s) URL, or a local HTML file")
    p.add_argument("--out", required=True, metavar="DIR", help="where cross.json goes")
    p.add_argument(
        "--flow", action="append", default=[], metavar="URL", help="a flow's first step"
    )
    p.add_argument("--form", metavar="SELECTOR", help="the form on every flow step")
    p.add_argument("--table", default=TABLE, metavar="FILE", help="the check table")
    p.add_argument(
        "--timeout",
        type=int,
        default=runner.LOAD_TIMEOUT_MS,
        metavar="MS",
        help="for each load",
    )
    at = p.parse_args(argv)
    try:
        with open(at.table, encoding="utf8") as fh:
            at.lines = parse(fh.read())
    except OSError as exc:
        p.error(f"cannot read --table {at.table}: {exc.strerror}")
    except TableError as exc:
        p.error(f"--table {at.table}: {exc}")
    at.url = runner.page_url(p, at.url)
    at.flow = [runner.page_url(p, f) for f in at.flow]
    return p, at


def main(argv):
    p, at = parse_args(argv)
    when, json_path = answers_file.start(at.out, "cross.json")
    phone_line = next((line for line in at.lines if line.check == "phone"), None)

    def run():
        phone = device(phone_line.value) if phone_line else None
        with runner.chromium() as browser:
            pages, unread = crawl(browser, at.url)
            walks = []
            for start in at.flow:
                walks.append(walk(browser, start, at.form))
            phones = phone_urls(browser, list(pages), phone) if phone else None
            return pages, unread, walks, phones

    try:
        got, code = runner.run_browser(run, at.timeout, at.url)
    except TableError as exc:
        p.print_usage(sys.stderr)
        print(f"check-cross.py: error: --table {at.table}: {exc}", file=sys.stderr)
        return 2
    except form.FormError as exc:
        print(f"check-cross.py: a flow's form: {exc}", file=sys.stderr)
        return 2
    if code:
        return code
    pages, unread, walks, phones = got
    found = findings(at.lines, pages, walks, phones=phones, home=at.url)
    answers_file.write(
        json_path,
        at.url,
        when,
        answers={f["id"]: f["answer"] for f in found},
        findings=found,
        pages=pages,
        unread=[{"url": u, "why": w} for u, w in unread],
        flows=[
            {
                "start": w.start,
                "ended": w.ended,
                "steps": [s._asdict() for s in w.steps],
            }
            for w in walks
        ],
    )
    print(report(at, found, unread, walks))
    return 1 if any(f["misses"] for f in found) else 0


if __name__ == "__main__":
    run_main(main)
