import copy
import json
import os
import re
import shutil
import struct
import sys
import tempfile
import unittest

HERE = os.path.dirname(__file__)
sys.path.insert(0, HERE)
import child  # noqa: E402 - imported after the sys.path.insert above puts test/ on the path

SCRIPTS = os.path.join(HERE, "..", "plugin", "skills", "design-round", "scripts")
SCRIPT = os.path.join(SCRIPTS, "check-load.py")
TABLE = os.path.join(SCRIPTS, "check-load.table")
FIXTURES = os.path.join(HERE, "fixtures", "load")
FAULT = os.path.join(FIXTURES, "net-tier01-fault.html")
CLEAN = os.path.join(FIXTURES, "net-tier01-clean.html")
PARTS = os.path.join(FIXTURES, "net-tier01-parts.json")
GOOD = os.path.join(FIXTURES, "good.woff2")
PLAIN = os.path.join(FIXTURES, "plain.ttf")
FLEX = os.path.join(FIXTURES, "flex.woff")


sys.path.insert(0, SCRIPTS)
import siblings  # noqa: E402

load = siblings.load(SCRIPTS, "check-load.py")
fontfile = load.fontfile


def run(page, out, *args):
    # guess, #501
    return child.run(
        [sys.executable, SCRIPT, page, "--files", "--out", out, *args],
        timeout=180,
    )


def table(*lines):
    return load.parse_table("\n".join(lines))


with open(TABLE, encoding="utf8") as fh:
    SHIPPED = load.parse_table(fh.read())


def line(check):
    return next(x for x in SHIPPED if x.check == check)


def _font(**over):
    base = dict(
        features=set(),
        chars=set(range(32, 127)),
        axes={},
        postscript="Good-Regular",
        family="Good",
        italic=False,
    )
    return fontfile.Font(**{**base, **over})


def _text(**over):
    base = dict(
        where="p",
        text="Hello",
        family="Good, serif",
        weight="400",
        style="normal",
        stretch="100%",
        size=16.0,
        caps="normal",
        synthesis="none",
        features="normal",
        variations="normal",
        numbers=False,
        fonts=[_used("Good", "Good-Regular", True, 5)],
    )
    return {**base, **over}


def _used(family, ps, custom, glyphs):
    return {
        "familyName": family,
        "postScriptName": ps,
        "isCustomFont": custom,
        "glyphCount": glyphs,
    }


def page(**over):
    base = dict(
        url="https://example.test/",
        faces=[
            {
                "family": "Good",
                "style": "normal",
                "src": ["https://example.test/good.woff2"],
            }
        ],
        fonts={
            "https://example.test/good.woff2": _font(features={"smcp", "c2sc", "ss01"})
        },
        texts=[_text()],
        distinct=[["Good", "400", "normal", {"Il": 0.4, "I1": 0.4, "l1": 0.4}]],
        images=[],
        stores=[],
        unread=[],
        scripts=[],
        styles=[],
        inline=[],
        bodies={},
        cookies=[],
        requested=[],
        footer=[["Cookies", "/cookies"]],
        banner=False,
    )
    return {**base, **copy.deepcopy(over)}


def judge(read, lines=SHIPPED, declared=None, undeclared=frozenset()):
    declared = {"cookie-banner": "#consent"} if declared is None else declared
    found = load.findings(lines, read, declared=declared, undeclared=undeclared)
    return {f["id"]: f for f in found}


def answer(read, record, **kw):
    return judge(read, **kw)[record]["answer"]


def misses(read, record, **kw):
    return [m["what"] for m in judge(read, **kw)[record]["misses"]]


class FixturePages(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp()
        cls.runs = {}
        for name, path in (("fault", FAULT), ("clean", CLEAN)):
            out = os.path.join(cls.tmp, name)
            proc = run(path, out, "--parts", PARTS)
            with open(os.path.join(out, "files.json"), encoding="utf8") as fh:
                cls.runs[name] = (proc, json.load(fh))

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp)

    def test_the_clean_page_meets_every_record_and_exits_0_313(self):
        proc, got = self.runs["clean"]
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertEqual(set(got["answers"].values()), {"pass"}, proc.stdout)
        self.assertEqual(set(got["answers"]), {x.id for x in SHIPPED})

    def test_the_fault_page_fails_each_marked_record_on_one_miss_and_exits_1(self):
        proc, got = self.runs["fault"]
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        with open(FAULT, encoding="utf8") as fh:
            marked = set(re.findall(r'data-fault="([^"]+)"', fh.read()))
        self.assertEqual(marked, {x.id for x in SHIPPED})
        token = {
            "vault.glyph-coverage": "Łódź",
            "vault.glyph-distinct": "Net Plain",
            "vault.small-caps": "font-synthesis-small-caps",
            "vault.font-features": "ss05",
            "vault.figure-face": "'204'",
            "vault.type-axes": "flex.woff",
            "vault.icon-vector": "icon.png",
            "vault.cookie-banner": "_ga",
        }
        self.assertEqual(set(token), marked)
        for f in got["findings"]:
            self.assertEqual(f["answer"], "fail", f)
            self.assertEqual(len(f["misses"]), 1, f)
            miss = f["misses"][0]
            self.assertIn(token[f["id"]], f"{miss['where']} {miss['what']}", f)

    def test_each_font_format_is_read_woff2_through_the_browser(self):
        _, got = self.runs["fault"]
        fonts = {os.path.basename(src): f for src, f in got["fonts"].items()}
        self.assertEqual(fonts["good.woff2"]["features"], ["c2sc", "smcp", "ss01"])
        self.assertEqual(fonts["plain.ttf"]["postscript"], "NetPlain-Regular")
        self.assertEqual(list(fonts["flex.woff"]["axes"]), ["wght", "opsz"])

    def test_without_a_declaration_the_cookie_banner_is_not_judged(self):
        with tempfile.TemporaryDirectory() as out:
            proc = run(CLEAN, out)
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            self.assertIn("vault.cookie-banner: not judged", proc.stdout)
            self.assertIn("no parts declaration names the cookie-banner", proc.stdout)


class Arguments(unittest.TestCase):
    def test_files_without_out_is_a_usage_error(self):
        # guess, #501
        proc = child.run([sys.executable, SCRIPT, CLEAN, "--files"], timeout=60)
        self.assertEqual(proc.returncode, 2)
        self.assertIn("--files wants --out DIR", proc.stderr)

    def test_a_bad_table_line_is_refused(self):
        for text, said in (
            ("vault.x | nothing", "no check 'nothing'"),
            ("vault.x | coverage | 3", "coverage reads no value"),
            ("vault.x | distinct | 2", "distinct wants a value"),
            ("vault.x | cookies-page | (", "cookies-page wants a regular expression"),
            ("# only a comment", "the table has no lines"),
        ):
            with (
                self.subTest(text=text),
                self.assertRaisesRegex(load.TableError, re.escape(said)),
            ):
                load.parse_table(text)

    def test_the_shipped_table_carries_each_records_value(self):
        self.assertEqual(line("distinct").value, 0.05)
        self.assertEqual(line("variable").value, 3)
        self.assertEqual(line("opsz").value, 20)
        self.assertEqual(line("vector").value, 48)
        self.assertIn("_ga", line("banner").value)
        self.assertTrue(line("cookies-page").value.search("Cookie policy"))


class Coverage(unittest.TestCase):
    R = "vault.glyph-coverage"

    def test_a_glyph_falling_to_an_installed_face_misses_naming_the_characters(self):
        t = _text(
            text="Łódź",
            fonts=[
                _used("Good", "Good-Regular", True, 1),
                _used("DejaVu Sans", "DejaVuSans", False, 3),
            ],
        )
        got = misses(page(texts=[t]), self.R)
        self.assertEqual(len(got), 1)
        self.assertIn("(Łóź)", got[0])
        self.assertIn("the browser's installed fallback", got[0])

    def test_a_later_installed_family_in_the_stack_still_misses(self):
        t = _text(
            family='Good, "DejaVu Sans", serif',
            fonts=[
                _used("Good", "Good-Regular", True, 1),
                _used("DejaVu Sans", "DejaVuSans", False, 1),
            ],
        )
        self.assertIn("a later family", misses(page(texts=[t]), self.R)[0])

    def test_a_later_web_font_or_emoji_family_is_on_purpose(self):
        greek = {
            "family": "Greek",
            "style": "normal",
            "src": ["https://example.test/greek.woff2"],
        }
        fonts = {"https://example.test/greek.woff2": _font(postscript="Greek-Regular")}
        t = _text(
            family='Good, Greek, "Noto Color Emoji", serif',
            fonts=[
                _used("Good", "Good-Regular", True, 2),
                _used("Greek", "Greek-Regular", True, 2),
                _used("Noto Color Emoji", "NotoColorEmoji", False, 1),
            ],
        )
        read = page(texts=[t])
        read["faces"].append(greek)
        read["fonts"].update(fonts)
        self.assertEqual(answer(read, self.R), "pass")

    def test_a_first_family_that_draws_nothing_misses(self):
        t = _text(fonts=[_used("DejaVu Sans", "DejaVuSans", False, 5)])
        self.assertIn("Good draws none of", misses(page(texts=[t]), self.R)[0])

    def test_a_generic_first_family_counts_its_main_face(self):
        t = _text(
            family="sans-serif",
            fonts=[
                _used("DejaVu Sans", "DejaVuSans", False, 5),
                _used("Noto Sans", "NotoSans", False, 1),
            ],
        )
        got = misses(page(texts=[t]), self.R)
        self.assertEqual(len(got), 1)
        self.assertIn("Noto Sans", got[0])


class Distinct(unittest.TestCase):
    R = "vault.glyph-distinct"

    def _with(self, il):
        return page(
            distinct=[["Good", "400", "normal", {"Il": il, "I1": 0.4, "l1": 0.4}]]
        )

    def test_the_tables_least_difference_passes_and_less_misses(self):
        self.assertEqual(answer(self._with(0.05), self.R), "pass")
        self.assertIn("I and l differ by 0.049", misses(self._with(0.049), self.R)[0])

    def test_the_value_is_read_from_the_table(self):
        lines = table("vault.glyph-distinct | distinct | >= 0.5")
        self.assertEqual(answer(self._with(0.4), self.R, lines=lines), "fail")

    def test_a_face_with_no_such_glyph_is_not_judged(self):
        self.assertEqual(answer(self._with(None), self.R), "not judged")


class SmallCaps(unittest.TestCase):
    R = "vault.small-caps"

    def test_true_small_caps_with_synthesis_off_pass(self):
        self.assertEqual(answer(page(texts=[_text(caps="small-caps")]), self.R), "pass")

    def test_a_face_without_smcp_misses(self):
        read = page(texts=[_text(caps="small-caps")])
        read["fonts"]["https://example.test/good.woff2"] = _font()
        self.assertIn("no smcp", misses(read, self.R)[0])

    def test_all_small_caps_also_wants_c2sc(self):
        read = page(texts=[_text(caps="all-small-caps")])
        read["fonts"]["https://example.test/good.woff2"] = _font(features={"smcp"})
        self.assertEqual(
            misses(read, self.R),
            ["all-small-caps from a face with no c2sc: synthesised"],
        )

    def test_synthesis_left_on_misses(self):
        self.assertIn(
            "not none",
            misses(page(texts=[_text(caps="small-caps", synthesis="auto")]), self.R)[0],
        )

    def test_italic_small_caps_from_an_upright_file_miss_and_from_an_italic_file_pass(
        self,
    ):
        read = page(texts=[_text(caps="small-caps", style="italic")])
        self.assertIn("synthesised slant", misses(read, self.R)[0])
        read["faces"][0]["style"] = "italic"
        self.assertEqual(answer(read, self.R), "pass")

    def test_an_installed_face_is_not_judged(self):
        t = _text(
            caps="small-caps",
            family="Georgia",
            fonts=[_used("Georgia", "Georgia", False, 5)],
        )
        self.assertEqual(answer(page(texts=[t]), self.R), "not judged")


class Features(unittest.TestCase):
    R = "vault.font-features"

    def test_a_feature_the_file_has_passes_and_one_it_lacks_misses(self):
        self.assertEqual(answer(page(texts=[_text(features='"ss01"')]), self.R), "pass")
        self.assertIn(
            "the face has no ss05",
            misses(page(texts=[_text(features='"ss05" 1')]), self.R)[0],
        )

    def test_a_feature_switched_off_is_not_read(self):
        self.assertEqual(
            answer(page(texts=[_text(features='"ss05" 0')]), self.R), "no match"
        )

    def test_a_feature_a_property_sets_misses(self):
        got = misses(page(texts=[_text(features='"tnum"')]), self.R)
        self.assertEqual(
            got,
            [
                'font-feature-settings switches on "tnum", which font-variant-numeric sets'
            ],
        )

    def test_a_feature_in_an_installed_face_is_not_judged(self):
        t = _text(
            features='"ss01"',
            family="Georgia",
            fonts=[_used("Georgia", "Georgia", False, 5)],
        )
        self.assertEqual(answer(page(texts=[t]), self.R), "not judged")

    def test_a_variant_before_the_font_shorthand_misses_and_after_it_passes(self):
        before = ".n { font-variant-numeric: tabular-nums; font: 16px Good }"
        after = "/* x { font: 1px a } */ .n { font: 16px Good; font-variant-numeric: tabular-nums }"
        self.assertIn(
            "comes before the font shorthand", misses(page(styles=[before]), self.R)[0]
        )
        self.assertEqual(answer(page(styles=[after]), self.R), "pass")
        sheet = {"https://example.test/a.css": ("stylesheet", before.encode())}
        self.assertEqual(answer(page(bodies=sheet), self.R), "fail")
        self.assertEqual(
            answer(
                page(inline=[["p", "font-feature-settings: 'ss01'; font: 12px a"]]),
                self.R,
            ),
            "fail",
        )
        unread = [["https://example.test/b.css", "stylesheet", "no body"]]
        self.assertEqual(
            answer(page(styles=[after], unread=unread), self.R), "not judged"
        )


class Tabular(unittest.TestCase):
    R = "vault.figure-face"

    def test_one_advance_passes_two_miss_and_other_text_is_not_read(self):
        same = _text(text="101", numbers=True, advances=[55.0] * 10)
        mixed = _text(text="101", numbers=True, advances=[55.0] * 9 + [30.0])
        self.assertEqual(answer(page(texts=[same]), self.R), "pass")
        self.assertIn("2 advances", misses(page(texts=[mixed]), self.R)[0])
        self.assertEqual(
            answer(page(texts=[_text(text="101", advances=[1, 2])]), self.R), "no match"
        )


def _flex(**over):
    face = {
        "family": "Flex",
        "style": "normal",
        "src": ["https://example.test/flex.woff2"],
    }
    font = _font(
        postscript="Flex-Regular", axes={"wght": (100, 400, 900), "opsz": (8, 14, 144)}
    )
    texts = [
        _text(
            family="Flex",
            fonts=[_used("Flex", "Flex-Regular", True, 4)],
            **{"size": 16.0, **t},
        )
        for t in over.pop("texts")
    ]
    read = page(texts=texts, **over)
    read["faces"].append(face)
    read["fonts"]["https://example.test/flex.woff2"] = font
    return read


class Axes(unittest.TestCase):
    R = "vault.type-axes"

    def test_three_weights_pay_for_a_variable_file_and_two_do_not(self):
        three = [
            {"weight": w, "size": s}
            for w, s in (("400", 16.0), ("500", 24.0), ("700", 32.0))
        ]
        self.assertEqual(answer(_flex(texts=three), self.R), "pass")
        got = misses(_flex(texts=three[:2]), self.R)
        self.assertEqual(len(got), 1)
        self.assertIn("drawing weight 400, 500 alone, under 3 weights", got[0])

    def test_an_in_between_weight_a_width_or_a_grade_pays(self):
        for t in ({"weight": "450"}, {"stretch": "87.5%"}, {"variations": '"GRAD" 50'}):
            with self.subTest(t=t):
                texts = [{"size": 16.0, **t}, {"size": 32.0}]
                self.assertEqual(answer(_flex(texts=texts), self.R), "pass")

    def test_opsz_wants_sizes_both_under_and_from_the_display_size(self):
        cases = (((16.0, 20.0), "pass"), ((16.0, 19.9), "fail"), ((20.0, 32.0), "fail"))
        for sizes, want in cases:
            with self.subTest(sizes=sizes):
                texts = [
                    {"weight": w, "size": s}
                    for w, s in zip(
                        ("400", "500", "700"), (*sizes, sizes[0]), strict=True
                    )
                ]
                self.assertEqual(answer(_flex(texts=texts), self.R), want)


def _image(**over):
    return {
        "where": "button > img",
        "src": ["https://example.test/i"],
        "width": 24,
        "height": 24,
        "action": True,
        "declared": False,
        **over,
    }


class Vector(unittest.TestCase):
    R = "vault.icon-vector"

    def _with(self, data, **over):
        return page(
            images=[_image(**over)], bodies={"https://example.test/i": ("image", data)}
        )

    def test_an_svg_icon_passes_and_each_raster_format_misses(self):
        self.assertEqual(
            answer(self._with(b'<?xml version="1.0"?>\n<svg/>'), self.R), "pass"
        )
        for data, name in (
            (b"\x89PNG\r\n\x1a\n...", "PNG"),
            (b"RIFF\0\0\0\0WEBPVP8", "WebP"),
            (b"\0\0\0\x1cftypavif", "AVIF"),
            (b"\xff\xd8\xff\xe0", "JPEG"),
        ):
            with self.subTest(name=name):
                self.assertIn(
                    f"a {name} file" if name != "AVIF" else "an AVIF file",
                    misses(self._with(data), self.R)[0],
                )

    def test_a_data_url_icon_is_read_from_its_bytes(self):
        read = page(images=[_image(src=["data:image/svg+xml,%3Csvg%2F%3E"])])
        self.assertEqual(answer(read, self.R), "pass")

    def test_the_size_limit_comes_from_the_table_and_bounds_what_counts_as_an_icon(
        self,
    ):
        png = b"\x89PNG\r\n\x1a\n"
        self.assertEqual(answer(self._with(png, width=48, height=48), self.R), "fail")
        self.assertEqual(
            answer(self._with(png, width=49, height=48), self.R), "no match"
        )
        self.assertEqual(answer(self._with(png, action=False), self.R), "no match")
        self.assertEqual(
            answer(
                self._with(png, width=300, height=300, action=False, declared=True),
                self.R,
            ),
            "fail",
        )

    def test_an_icon_whose_file_was_not_fetched_is_not_judged(self):
        self.assertEqual(answer(page(images=[_image()]), self.R), "not judged")


class Banner(unittest.TestCase):
    R = "vault.cookie-banner"

    def test_without_a_declared_banner_it_is_not_judged(self):
        self.assertEqual(answer(page(), self.R, declared={}), "not judged")
        found = judge(page(), declared={}, undeclared={"cookie-banner"})[self.R]
        self.assertIn("with no selector", found["unjudged"][0]["what"])

    def test_storage_needing_consent_with_no_banner_misses(self):
        for over in (
            {"cookies": [{"name": "_ga", "domain": "example.test"}]},
            {"cookies": [{"name": "id", "domain": ".ads.other"}]},
            {"stores": ["ajs_user_id"]},
            {"requested": ["https://www.googletagmanager.com/gtag/js"]},
            {"scripts": ["load('https://static.hotjar.com/c.js')"]},
            {
                "bodies": {
                    "https://example.test/a.js": (
                        "script",
                        b"//cdn.segment.com/analytics.js",
                    )
                }
            },
        ):
            with self.subTest(over=over):
                self.assertIn("no cookie-banner shows", misses(page(**over), self.R)[0])
                self.assertEqual(answer(page(banner=True, **over), self.R), "pass")

    def test_a_banner_over_strictly_necessary_storage_alone_misses(self):
        read = page(
            banner=True,
            cookies=[{"name": "session", "domain": "example.test"}],
            stores=["theme"],
        )
        self.assertIn("only strictly necessary", misses(read, self.R)[0])

    def test_storage_or_a_script_it_could_not_read_leaves_it_not_judged(self):
        unread = [["https://example.test/a.js", "script", "no body"]]
        self.assertEqual(answer(page(stores=None), self.R), "not judged")
        self.assertEqual(answer(page(banner=True, unread=unread), self.R), "not judged")
        self.assertEqual(answer(page(unread=unread, stores=["_ga"]), self.R), "fail")

    def test_the_footer_must_link_a_cookies_page(self):
        self.assertIn("no footer", misses(page(footer=None), self.R)[0])
        self.assertIn(
            "no footer link matches",
            misses(page(footer=[["Privacy", "/privacy"]]), self.R)[0],
        )
        self.assertEqual(
            answer(page(footer=[["Your data", "/legal/cookies"]]), self.R), "pass"
        )


def _sfnt(tables):
    head = struct.pack(">4sHHHH", b"\x00\x01\x00\x00", len(tables), 0, 0, 0)
    offset = 12 + 16 * len(tables)
    directory, body = b"", b""
    for tag, data in tables.items():
        directory += struct.pack(
            ">4sIII", tag.encode(), 0, offset + len(body), len(data)
        )
        body += data + bytes(-len(data) % 4)
    return head + directory + body


class FontFile(unittest.TestCase):
    def _read(self, path):
        with open(path, "rb") as fh:
            return fh.read()

    def test_a_truetype_and_a_woff_file_are_read(self):
        plain = fontfile.read(self._read(PLAIN))
        self.assertEqual(
            (plain.postscript, plain.family, plain.features, plain.axes, plain.italic),
            ("NetPlain-Regular", "Net Plain", set(), {}, False),
        )
        self.assertTrue({ord(c) for c in "Il1 az"} <= plain.chars)
        self.assertNotIn(ord("é"), plain.chars)
        flex = fontfile.read(self._read(FLEX))
        self.assertEqual(flex.axes, {"wght": (100, 400, 900), "opsz": (8, 14, 144)})
        self.assertIn(ord("é"), flex.chars)

    def test_each_format_is_told_by_its_signature(self):
        self.assertEqual(
            [fontfile.kind(self._read(p)) for p in (PLAIN, FLEX, GOOD)],
            ["sfnt", "woff", "woff2"],
        )
        self.assertIsNone(fontfile.kind(b"\x89PNG"))

    def test_what_it_cannot_open_is_a_font_error(self):
        for data, said in (
            (self._read(GOOD), "no Brotli decoder"),
            (b"ttcf\0\1\0\0", "font collection"),
            (b"\x89PNG\r\n\x1a\n", "no font signature"),
            (self._read(PLAIN)[:40], "cut short"),
        ):
            with (
                self.subTest(said=said),
                self.assertRaisesRegex(fontfile.FontError, said),
            ):
                fontfile.read(data)

    def test_gpos_features_and_a_format_12_cmap_are_read(self):
        feature_list = struct.pack(">H4sH", 1, b"kern", 8)
        gpos = struct.pack(">HHHHH", 1, 0, 0, 10, 0) + feature_list
        group = struct.pack(">III", 0x1F600, 0x1F602, 5)
        sub = struct.pack(">HHIII", 12, 0, 16 + len(group), 0, 1) + group
        cmap = struct.pack(">HHHHI", 0, 1, 3, 10, 12) + sub
        font = fontfile.read(_sfnt({"GPOS": gpos, "cmap": cmap}))
        self.assertEqual(font.features, {"kern"})
        self.assertEqual(font.chars, {0x1F600, 0x1F601, 0x1F602})

    def test_a_woff2_base128_with_a_leading_zero_is_refused(self):
        head = b"wOF2" + b"\0\1\0\0" + struct.pack(">IHH", 0, 1, 0) + bytes(32)
        data = head + bytes([0x3F]) + b"abcd" + bytes([0x80, 0x01])
        with self.assertRaisesRegex(fontfile.FontError, "leading zero"):
            fontfile.read(data, lambda b: b"")

    def test_a_woff2_whose_tables_overrun_the_stream_is_refused(self):
        head = b"wOF2" + b"\0\1\0\0" + struct.pack(">IHH", 0, 1, 0) + bytes(32)
        data = head + bytes([0x00, 0x10])
        with self.assertRaisesRegex(fontfile.FontError, "do not fill"):
            fontfile.read(data, lambda b: b"short")


if __name__ == "__main__":
    child.main()
