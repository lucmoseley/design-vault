import os
import sys
import re
import unittest

SCRIPT = os.path.join(
    os.path.dirname(__file__),
    "..",
    "plugin",
    "skills",
    "design-round",
    "scripts",
    "rule-table.py",
)
SCRIPTS = os.path.join(
    os.path.dirname(__file__), "..", "plugin", "skills", "design-round", "scripts"
)
sys.path.insert(0, SCRIPTS)
import siblings  # noqa: E402

rule_table = siblings.load(SCRIPTS, "rule-table.py")

CHECKS = {"order": None, "ways": r">=\s*(\d+)"}


def _value(n, check, m):
    return int(m[1]) if m else None


class Lines(unittest.TestCase):
    def test_numbers_rule_lines_and_skips_blanks_and_comments(self):
        text = "# head\n\n  a | order  \n   # indented note\nb | ways | >= 2\n"
        self.assertEqual(
            list(rule_table.lines(text)), [(3, "a | order"), (5, "b | ways | >= 2")]
        )


class Parse(unittest.TestCase):
    def test_gives_each_line_its_check_and_the_hooks_value(self):
        table = rule_table.parse("a | order\nb | ways | >= 3\n", CHECKS, _value)
        self.assertEqual(
            table,
            [
                rule_table.Line("a", "order", None, "a | order"),
                rule_table.Line("b", "ways", 3, "b | ways | >= 3"),
            ],
        )

    def test_refuses_a_bad_line_naming_it(self):
        for text, why in (
            ("a | ways | >= 2 | 3", "line 1: want ID | CHECK [| VALUE]"),
            ("# only\nb | sort", "line 2: no check 'sort'; the checks are order, ways"),
            ("a | order | 2", "line 1: order reads no value, got '2'"),
            (
                "a | ways | 2",
                "line 1: ways wants a value like '>=\\\\s*(\\\\d+)', got '2'",
            ),
            ("a | ways", "line 1: ways wants a value like"),
            ("# none\n", "the table has no lines"),
        ):
            with (
                self.subTest(text),
                self.assertRaisesRegex(rule_table.TableError, re.escape(why)),
            ):
                rule_table.parse(text, CHECKS, _value)


TABLE = [rule_table.Line(i, "order", None, i) for i in ("a", "b", "c", "d", "e")]


class Answers(unittest.TestCase):
    def test_a_miss_outranks_unjudged_which_outranks_a_met_line(self):
        ans = rule_table.Answers(TABLE, "page")
        a, b, c, d, _ = TABLE
        ans.unjudged(a, "/", "no read")
        ans.miss(a, "/x", "out of order")
        ans.met(b)
        ans.unjudged(b, "/", "no read")
        ans.met(c)
        ans.miss(d, "/", "out of order")
        ans.met(d)
        self.assertEqual(
            [f["answer"] for f in ans.done()],
            ["fail", "not judged", "pass", "fail", "no match"],
        )

    def test_answers_rank_so_the_strongest_of_two_is_their_joint_answer(self):
        cases = [
            {"misses": m, "unjudged": u, "judged": j}
            for m in (0, 1)
            for u in (0, 1)
            for j in (0, 1)
        ]
        for x in cases:
            for y in cases:
                joint = rule_table.answer(**{k: x[k] or y[k] for k in x})
                strongest = max(
                    rule_table.answer(**x),
                    rule_table.answer(**y),
                    key=rule_table.ANSWERS.index,
                )
                with self.subTest(x=x, y=y):
                    self.assertEqual(strongest, joint)

    def test_one_place_takes_its_value_and_several_take_a_dict(self):
        one = rule_table.Answers(TABLE[:1], "where")
        one.miss(TABLE[0], "/", "x")
        self.assertEqual(
            one.done()[0]["misses"], [{"check": "order", "where": "/", "what": "x"}]
        )
        two = rule_table.Answers(TABLE[:1], "where", "fault", review=True)
        two.review(TABLE[0], {"where": "/"}, "look")
        two.unjudged(TABLE[0], None, "no read")
        (f,) = two.done()
        self.assertEqual(
            f["review"],
            [{"check": "order", "where": "/", "fault": None, "what": "look"}],
        )
        self.assertEqual(
            f["unjudged"],
            [{"check": "order", "where": None, "fault": None, "what": "no read"}],
        )
        self.assertNotIn("review", one.found["a"])


if __name__ == "__main__":
    unittest.main()
