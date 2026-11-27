import collections
import contextlib
import glob
import hashlib
import http.server
import json
import os
import pathlib
import re
import sys
import tempfile
import threading
import unittest

HERE = os.path.dirname(__file__)
sys.path.insert(0, HERE)
import child  # noqa: E402 - imported after the sys.path.insert above puts test/ on the path

SCRIPTS = os.path.join(HERE, "..", "plugin", "skills", "design-round", "scripts")
RULES = os.path.join(HERE, "..", "plugin", "skills", "design-critique", "rules")


sys.path.insert(0, SCRIPTS)
import siblings  # noqa: E402

dom = siblings.load(SCRIPTS, "check-dom.py")
runner = siblings.load(SCRIPTS, "runner.py")
FIXTURES = pathlib.Path(HERE, "fixtures", "probe").resolve()
FAULT = FIXTURES / "dom-fault.html"
CLEAN = FIXTURES / "dom-clean.html"
FAULT_ONE = FIXTURES / "dom-fault-one.html"
CLEAN_ONE = FIXTURES / "dom-clean-one.html"
MISSING_FAULT = FIXTURES / "dom-missing-fault.html"
MISSING_CLEAN = FIXTURES / "dom-missing-clean.html"
PARTS_FILE = FIXTURES / "dom-parts.json"
with open(dom.TABLE, encoding="utf8") as fh:
    BLOCKS = dom.parse(fh.read())
with open(PARTS_FILE, encoding="utf8") as fh:
    PARTS, UNSET = dom.probe.declared_parts(fh.read())
RECORDS = list(dict.fromkeys(r.id for b in BLOCKS for r in b.rules))
MARKED = ("data-fault", "data-fault-absent")
OPEN = contextlib.ExitStack()
BROWSER = None
SITES = {}
SWEPT = {}
# measured: 5.1-5.3 s a fault-page run at load 9.9, #454
PROGRAM_S = 60


def site(page, missing, status):

    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k):
            super().__init__(*a, directory=str(FIXTURES), **k)

        def log_message(self, *a):
            pass

        def do_GET(self):
            path = self.path.split("?")[0]
            if path != "/" and (FIXTURES / path.lstrip("/")).is_file():
                return super().do_GET()
            body = (page if path == "/" else missing).read_bytes()
            self.send_response(200 if path == "/" else status)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(body)

    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    OPEN.callback(server.shutdown)
    return f"http://127.0.0.1:{server.server_port}/"


def setUpModule():
    global BROWSER
    BROWSER = OPEN.enter_context(runner.chromium())
    SITES["fault"] = site(FAULT, MISSING_FAULT, 200)
    SITES["clean"] = site(CLEAN, MISSING_CLEAN, 404)
    SITES["fault-one"] = site(FAULT_ONE, MISSING_CLEAN, 404)
    SITES["clean-one"] = site(CLEAN_ONE, MISSING_CLEAN, 404)


def tearDownModule():
    OPEN.close()


def found(url, blocks=BLOCKS, parts=PARTS, unset=UNSET):
    key = (url, id(blocks), tuple(sorted(parts.items())), tuple(sorted(unset)))
    if key not in SWEPT:
        swept = dom.run(
            BROWSER,
            url,
            blocks,
            parts=parts,
            unset=unset,
            timeout=runner.LOAD_TIMEOUT_MS,
        )
        rules = [r.rule for r in swept[0][1]]
        SWEPT[key] = {f["id"]: f for f in dom.probe.findings(rules, swept)}
    return SWEPT[key]


def faults(*pages):
    return collections.Counter(
        m for p in pages for m in re.findall(r"fault: (vault\.\S+?):", p.read_text())
    )


def own_tokens():
    nth = collections.Counter()
    out = {}
    for b in BLOCKS:
        for r in b.rules:
            nth[r.id] += 1
            out[dom.block_line(b, r).line] = (b, r, f"{r.id}:{nth[r.id]}")
    return out


LINES = own_tokens()


def tokens(*pages):
    return collections.Counter(
        token
        for p in pages
        for attr in MARKED
        for value in re.findall(rf'{attr}="([^"]*)"', p.read_text())
        for token in value.split()
    )


def landings(url):
    (as_mark,) = table("vault.marked | css:html | attr:data-fault | absent")[0].rules
    picks = [
        dom.Block(
            b.load,
            b.when,
            [r._replace(read=as_mark.read, must=as_mark.must) for r in b.rules],
        )
        for b in BLOCKS
    ]
    inventory = {}
    for load in dict.fromkeys(b.load for b in BLOCKS):
        for attr in MARKED:
            block = dom.Block(
                load,
                None,
                table(f"vault.{attr} | all css:[{attr}] | attr:{attr} | absent")[
                    0
                ].rules,
            )
            inventory[dom.block_line(block, block.rules[0]).line] = (block, attr)
    swept = dom.run(
        BROWSER,
        url,
        picks + [block for block, _ in inventory.values()],
        parts=PARTS,
        unset=UNSET,
        timeout=runner.LOAD_TIMEOUT_MS,
    )
    carried = collections.defaultdict(set)
    marked_picks = collections.defaultdict(set)
    lines_picking = set()
    for _, results in swept:
        for result in results:
            line = result.rule.line
            if line in inventory:
                block, attr = inventory[line]
                for s in result.subjects:
                    carried[block.load, attr, s.subject] |= set(s.value.split())
                continue
            if result.subjects:
                lines_picking.add(line)
            marked_picks[line] |= {
                s.subject for s in result.subjects if s.verdict == "miss"
            }
    out = collections.defaultdict(set)
    for f in found(url).values():
        for m in f["misses"]:
            line = m["line"]
            block, rule, _ = LINES[line]
            if m["subject"] != rule.select.text:
                attr, elements = "data-fault", {m["subject"]}
            elif line in lines_picking:
                attr, elements = "data-fault", marked_picks[line]
            else:
                attr = "data-fault-absent"
                elements = {e for at, a, e in carried if (at, a) == (block.load, attr)}
            for e in elements:
                out[line] |= carried[block.load, attr, e]
    return out


def local(folder, body, head=""):
    html = (
        '<!doctype html><html lang="en"><head><meta charset="utf-8"><title>t</title>'
        f"{head}</head><body>{body}</body></html>"
    )
    path = pathlib.Path(folder, hashlib.sha1(html.encode()).hexdigest() + ".html")
    path.write_text(html)
    return path.as_uri()


def table(text):
    return dom.parse(text)


def stamped(body, parts=None, head=""):
    with tempfile.TemporaryDirectory() as d:
        url = local(d, body, head)
        with dom.conditions.open_page(
            BROWSER, url, init_scripts=(dom.LISTEN_JS,)
        ) as page:
            dom.layout.load(
                page, url, dom.conditions.PHONE_WIDTH, dom.conditions.HEIGHTS
            )
            dom.stamp(page, parts or {})
            return page.evaluate(
                """() => Object.fromEntries([...document.querySelectorAll('[id]'), document.documentElement].map((el) => [
                  el.id || 'root',
                  Object.fromEntries([...el.attributes].filter((a) => a.name.startsWith('data-vault-')).map((a) => [a.name.slice(11), a.value])),
                ]))"""
            )


def records_naming(script):
    out = {}
    for path in glob.glob(os.path.join(RULES, "*.md")):
        text = pathlib.Path(path).read_text(encoding="utf8")
        for m in re.finditer(r"^### (\S+)\n((?:- .*\n?)*)", text, re.M):
            fields = dict(re.findall(r"^- ([\w-]+): (.*)$", m.group(2), re.M))
            if fields.get("script", "").split(" ")[0] == script:
                out[m.group(1)] = fields["answered-by"]
    return out


def program(*argv):
    return child.run(
        [sys.executable, os.path.join(SCRIPTS, "check-dom.py"), *argv],
        timeout=PROGRAM_S,
    )


class TheFixtures(unittest.TestCase):
    def test_the_fault_pages_plant_and_mark_one_fault_for_each_table_line(self):
        self.assertEqual(
            faults(FAULT, FAULT_ONE, MISSING_FAULT),
            collections.Counter(r.id for b in BLOCKS for r in b.rules),
        )
        self.assertEqual(
            tokens(FAULT, FAULT_ONE, MISSING_FAULT),
            collections.Counter(token for _, _, token in LINES.values()),
        )
        self.assertEqual(faults(CLEAN, CLEAN_ONE, MISSING_CLEAN), {})
        self.assertEqual(tokens(CLEAN, CLEAN_ONE, MISSING_CLEAN), {})

    def test_every_table_line_misses_on_the_element_its_fault_marks(self):
        landed = collections.defaultdict(set)
        for site in ("fault", "fault-one"):
            for line, got in landings(SITES[site]).items():
                landed[line] |= got
        self.assertEqual(
            [
                line
                for line, (_, _, token) in LINES.items()
                if token not in landed[line]
            ],
            [],
        )

    def test_every_record_fails_on_the_fault_page_310(self):
        got = found(SITES["fault"])
        self.assertEqual(
            {r: f["answer"] for r, f in got.items()}, dict.fromkeys(RECORDS, "fail")
        )

    def test_the_clean_page_passes_every_record_and_reports_nothing(self):
        got = found(SITES["clean"])
        self.assertEqual(
            {r: f["answer"] for r, f in got.items()}, dict.fromkeys(RECORDS, "pass")
        )
        for f in got.values():
            self.assertEqual((f["misses"], f["unjudged"]), ([], []))

    def test_the_clean_one_question_page_reports_nothing(self):
        got = found(SITES["clean-one"])
        self.assertEqual({r for r, f in got.items() if f["answer"] == "fail"}, set())
        self.assertEqual(got["vault.question-heading"]["answer"], "pass")
        self.assertEqual(got["vault.favicon"]["answer"], "pass")
        for f in got.values():
            self.assertEqual((f["misses"], f["unjudged"]), ([], []))

    def test_a_miss_names_its_element_and_both_widths(self):
        miss = found(SITES["fault"])["vault.paste-allowed"]["misses"]
        self.assertEqual(
            [(m["subject"], m["from"], m["to"]) for m in miss],
            [("input#pass", *dom.WIDTHS)],
        )
        self.assertTrue(miss[0]["line"].startswith("[page] vault.paste-allowed |"))
        self.assertIn(
            "390 and 1920 px",
            dom.report("u", [found(SITES["fault"])["vault.paste-allowed"]]),
        )

    def test_the_program_exits_1_on_a_miss_and_writes_its_findings_over_the_last(self):
        with tempfile.TemporaryDirectory() as out:
            stale = os.path.join(out, "dom.json")
            with open(stale, "w") as fh:
                fh.write("{}")
            ran = program(str(FAULT), "--out", out, "--parts", str(PARTS_FILE))
            with open(stale, encoding="utf8") as fh:
                written = json.load(fh)
        self.assertEqual(ran.returncode, 1)
        self.assertEqual(written["answers"]["vault.paste-allowed"], "fail")
        self.assertIn("vault.paste-allowed: fail", ran.stdout)

    def test_the_program_exits_2_on_a_table_it_cannot_read(self):
        with tempfile.TemporaryDirectory() as d:
            bad = pathlib.Path(d, "t.table")
            bad.write_text("when nonsense\n")
            ran = program(str(CLEAN), "--out", d, "--table", str(bad))
        self.assertEqual(ran.returncode, 2)
        self.assertIn("when wants a SELECTS", ran.stderr)

    def test_each_record_the_table_answers_names_check_dom_and_is_answered_by_script(
        self,
    ):
        self.assertEqual(
            records_naming("check-dom.py"), dict.fromkeys(RECORDS, "script")
        )


class TheBlocks(unittest.TestCase):
    def test_a_local_file_leaves_the_missing_page_lines_not_judged(self):
        with tempfile.TemporaryDirectory() as d:
            url = local(d, "<p>Hi</p>")
            blocks = table(
                "on missing page\nvault.x | css:html | attr:data-vault-status | = 404"
            )
            f = found(url, blocks, {}, set())["vault.x"]
        self.assertEqual(f["answer"], "not judged")
        self.assertIn("no site", f["unjudged"][0]["why"])

    def test_a_when_that_finds_nothing_leaves_its_lines_unanswered(self):
        blocks = table(
            "when css:html where attr:data-vault-listens matches devicemotion\n"
            "vault.x | part:motion-control | count | >= 1"
        )
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(
                found(local(d, "<p>Hi</p>"), blocks, {}, set())["vault.x"]["answer"],
                "no match",
            )
            url = local(
                d, "<script>addEventListener('devicemotion', () => {})</script>"
            )
            self.assertEqual(found(url, blocks, {}, set())["vault.x"]["answer"], "fail")
            self.assertEqual(
                found(url, blocks, {}, {"motion-control"})["vault.x"]["answer"],
                "not judged",
            )

    def test_a_part_named_in_a_when_and_declared_with_no_selector_is_not_judged(self):
        blocks = table(
            "when part:pull-to-refresh\nvault.x | role:button | count | >= 1"
        )
        with tempfile.TemporaryDirectory() as d:
            f = found(local(d, "<p>Hi</p>"), blocks, {}, {"pull-to-refresh"})["vault.x"]
        self.assertEqual(f["answer"], "not judged")

    def test_under_rtl_reads_the_page_right_to_left(self):
        blocks = table("under rtl\nvault.x | css:html | attr:dir | = rtl")
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(
                found(local(d, "<p>Hi</p>"), blocks, {}, set())["vault.x"]["answer"],
                "pass",
            )

    def test_the_table_refuses_an_undefined_name_and_a_when_with_no_selects(self):
        with self.assertRaisesRegex(dom.TableError, r"\$nope is not defined"):
            table("vault.x | $nope | count | = 0")
        with self.assertRaisesRegex(dom.TableError, "when wants a SELECTS"):
            table("when nothing here\nvault.x | css:p | count | = 0")


class TheStamps(unittest.TestCase):
    def test_listeners_by_add_event_listener_and_by_handler_property(self):
        got = stamped(
            '<div id="a"></div><div id="b"></div><script>'
            "a.addEventListener('drop', () => {}); b.ondragover = () => {}; window.addEventListener('deviceorientation', () => {});"
            "</script>"
        )
        self.assertEqual(got["a"]["listens"], "drop")
        self.assertEqual(got["b"]["listens"], "dragover")
        self.assertIn("deviceorientation", got["root"]["listens"].split())

    def test_a_cancelled_paste_a_set_value_and_a_link_address_are_stamped(self):
        got = stamped(
            '<input id="p" type="password" onpaste="event.preventDefault()"><input id="q" type="password">'
            '<input id="v"><script>v.value = "set by script"</script><a id="l" href="/x">x</a>'
        )
        self.assertEqual(got["p"].get("paste"), "blocked")
        self.assertNotIn("paste", got["q"])
        self.assertEqual(got["v"]["value"], "set by script")
        self.assertTrue(got["l"]["href"].endswith("/x"))

    def test_each_form_field_says_next_or_last_and_the_root_counts_its_questions(self):
        got = stamped(
            '<form><input id="a"><select id="s"><option>1</option></select><input id="b" type="email">'
            '<fieldset><legend>When</legend><input name="d"><input id="m" name="m"></fieldset>'
            '<input type="radio" name="r"><input type="radio" name="r"><input type="hidden" name="h"><button>Go</button></form>'
            '<form role="search"><input type="search"><input></form>'
            '<form><input type="search"></form>'
        )
        self.assertEqual(
            (got["a"]["field"], got["b"]["field"], got["m"]["field"]),
            ("next", "next", "last"),
        )
        self.assertEqual(got["root"]["questions"], "5")

    def test_an_icon_gets_its_name_whether_it_is_mirrored_and_its_stroke_scale(self):
        got = stamped(
            '<button id="b"><svg id="i" class="icon arrow-right" viewBox="0 0 24 24" width="48" height="48">'
            '<line x1="2" y1="12" x2="22" y2="12" stroke="black" stroke-width="2"/></svg>Next</button>'
            '<span style="scale: -1 1; display: inline-block"><svg id="m" viewBox="0 0 24 24" width="48" height="48">'
            '<line x1="2" y1="12" x2="22" y2="12" stroke="black" stroke-width="2" vector-effect="non-scaling-stroke"/></svg></span>'
            '<svg id="t" viewBox="0 0 24 24" width="24" height="24" style="transform: scaleX(-1)"><title>Clock</title><circle cx="12" cy="12" r="8" fill="black"/></svg>'
        )
        self.assertEqual(got["i"]["icon-name"], "icon arrow right")
        self.assertEqual(got["i"]["stroke-scale"], "2")
        self.assertEqual(got["m"]["stroke-scale"], "1")
        self.assertEqual(
            (got["i"]["mirrored"], got["m"]["mirrored"], got["t"]["mirrored"]),
            ("0", "1", "1"),
        )
        self.assertEqual(got["t"]["icon-name"], "clock")
        self.assertNotIn("stroke-scale", got["t"])
        self.assertEqual(
            (got["b"]["side"], got["b"]["side-icon"]), ("before", "icon arrow right")
        )

    def test_the_icon_side_follows_the_reading_direction(self):
        got = stamped(
            '<button id="l"><svg viewBox="0 0 24 24" width="24" height="24"><circle cx="12" cy="12" r="8"/></svg>Save</button>'
            '<button id="r" dir="rtl"><svg viewBox="0 0 24 24" width="24" height="24"><circle cx="12" cy="12" r="8"/></svg>Save</button>'
        )
        self.assertEqual((got["l"]["side"], got["r"]["side"]), ("before", "before"))

    def test_ink_lead_compares_the_current_icon_with_its_set(self):
        icon = '<svg viewBox="0 0 24 24" width="24" height="24"><circle cx="12" cy="12" r="8" {}/></svg>'
        ring = icon.format('fill="none" stroke="black" stroke-width="2"')
        got = stamped(
            f'<nav><a id="c" aria-current="page" href="/">{icon.format('fill="black"').replace("<svg", '<svg id="f"')}Home</a>'
            f'<a href="/a"><svg id="r"{ring[4:]}A</a></nav>'
        )
        self.assertGreater(float(got["f"]["ink-lead"]), 1.5)
        self.assertEqual(
            float(got["f"]["ink-lead"]),
            round(float(got["f"]["ink"]) / float(got["r"]["ink"]), 4),
        )
        self.assertNotIn("ink-lead", got["c"])

    def test_declared_parts_count_buttons_and_find_the_top_control(self):
        got = stamped(
            '<div id="s"><button style="width:30px;height:5px"></button><h2>Filters</h2><button>Apply</button></div>'
            '<div id="u"><h2>Filters</h2><button>Close</button></div><button hidden>Hidden</button>',
            {"sheet": "#s, #u"},
        )
        self.assertEqual((got["s"]["buttons"], got["s"]["top-control"]), ("2", "1"))
        self.assertEqual((got["u"]["buttons"], got["u"]["top-control"]), ("1", "0"))
        self.assertEqual(got["root"]["button-names"], " / Apply / Close")

    def test_icon_files_load_and_give_their_size(self):
        png = str(FIXTURES / "dom-icons" / "touch-180.png")
        with tempfile.TemporaryDirectory() as d:
            os.symlink(png, os.path.join(d, "t.png"))
            url = local(
                d,
                "",
                '<link id="t" rel="apple-touch-icon" href="t.png"><link id="g" rel="icon" href="gone.png">',
            )
            with dom.conditions.open_page(BROWSER, url) as page:
                dom.stamp(page, {})
                got = page.evaluate(
                    "[t.dataset.vaultLoaded, t.dataset.vaultSize, g.dataset.vaultLoaded]"
                )
        self.assertEqual(got, ["1", "180x180", "0"])

    def test_names_said_by_a_part_and_its_home_link(self):
        got = stamped(
            '<a id="h" href="/"><img id="l" class="logo" alt="Sea Hostel home" src="x.png" width="9" height="9"></a>'
            '<a href="/inbox"><svg aria-hidden="true" width="9" height="9"><title>Bell</title></svg>'
            '<span id="b" class="badge">4</span><span class="vh"> unread</span></a>'
            '<span id="n" class="badge" aria-label="Nine new">9</span>'
            '<a href="/" aria-labelledby="t"><span id="o" class="logo">Logo</span></a><p id="t">Home page</p>',
            {"logo": ".logo", "badge": ".badge"},
            head="<title>Sea Hostel: rooms</title>",
        )
        self.assertEqual(
            (got["l"]["link-name"], got["l"]["link-site"]), ("Sea Hostel home", "1")
        )
        self.assertTrue(got["l"]["link-href"].endswith("/"))
        self.assertEqual((got["b"]["said"], got["n"]["said"]), ("4 unread", "Nine new"))
        self.assertEqual(
            (got["o"]["link-name"], got["o"]["link-site"]), ("Home page", "0")
        )

    def test_a_declared_table_counts_its_loose_header_cells(self):
        got = stamped(
            '<table id="a" class="t"><thead><tr><th scope="col">A</th><td>B</td><th>C</th></tr></thead>'
            '<tbody><tr><th scope="row">r</th><td>1</td></tr><tr><th>s</th><td>2</td></tr></tbody></table>'
            '<table id="b" class="t"><tr><td>1</td></tr></table>',
            {"table": ".t"},
        )
        a, b = got["a"], got["b"]
        self.assertEqual(
            (a["head-cols"], a["head-loose"], a["row-loose"]), ("1", "2", "1")
        )
        self.assertEqual(
            (b["head-cols"], b["head-loose"], b["row-loose"]), ("0", "0", "0")
        )

    def test_a_progress_label_and_a_line_number_a_screen_reader_announces_are_stamped(
        self,
    ):
        got = stamped(
            '<style>.c span::before { content: counter(x); } .q span::before { content: counter(x) / ""; } .d::after { content: "x"; }</style>'
            '<label for="p">Upload progress</label><progress id="p"></progress><progress id="u">40%</progress>'
            '<pre class="c"><span id="c1">a</span></pre><pre class="q"><span id="c2">a</span></pre>'
            '<pre class="c" aria-hidden="true"><span id="c3">a</span></pre><pre><code id="d" class="d">a</code></pre>'
        )
        self.assertEqual(
            (got["p"]["label"], "label" in got["u"]), ("Upload progress", False)
        )
        self.assertEqual(got["c1"]["counter"], "counter(x)")
        self.assertRegex(got["c2"]["counter"], r'/\s*""$')
        self.assertNotIn("counter", got["c3"])
        self.assertNotIn("counter", got["d"])

    def test_a_block_drawn_as_a_heading_and_text_whose_spaces_are_kept_are_stamped(
        self,
    ):
        got = stamped(
            '<div id="h" style="font-size: 24px; font-weight: 700">Rooms</div><p style="font-style: italic">Bright.</p>'
            '<div id="x"><p>holds a block</p></div><p>after</p>'
            '<div id="r" role="note">Note</div><p>after</p>'
            '<pre id="s">a  b\tc\nd</pre><div id="w" style="white-space: pre-wrap"><span id="i">x  y</span></div>'
            '<div id="z">Over a rule</div><hr>'
            '<div id="e">Last</div>'
        )
        h = got["h"]
        self.assertEqual(
            (h["heads"], h["size-ratio"], h["next-weight"], h["next-style"]),
            ("1", "1.5", "400", "italic"),
        )
        for el in ("x", "r", "z", "e"):
            self.assertNotIn("heads", got[el], el)
        self.assertEqual(got["s"]["spaced-text"], "a\u2420\u2420b\u2409c\u2424d")
        self.assertEqual(got["w"]["spaced-text"], "x\u2420\u2420y")
        self.assertNotIn("spaced-text", got["i"])

    def test_ink_is_the_drawn_share_of_the_shot(self):
        from PIL import Image
        import io

        im = Image.new("RGB", (10, 10), "white")
        for x in range(10):
            im.putpixel((x, 0), (0, 0, 0))
        buf = io.BytesIO()
        im.save(buf, "PNG")
        self.assertEqual(dom.ink(buf.getvalue()), 0.1)


if __name__ == "__main__":
    child.main()
