import importlib.util
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(
    HERE, "..", "plugin", "skills", "design-round", "scripts", "siblings.py"
)
# A guess, unmeasured: one bare Python start that loads two empty files (#558).
PROGRAM_RUN_S = 60
spec = importlib.util.spec_from_file_location("siblings_under_test", SCRIPT)
siblings = importlib.util.module_from_spec(spec)
spec.loader.exec_module(siblings)


class Load(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.addCleanup(self.forget)

    def forget(self):
        for key in [k for k in sys.modules if k.startswith(os.path.realpath(self.dir))]:
            del sys.modules[key]

    def write(self, name, text):
        with open(os.path.join(self.dir, name), "w", encoding="utf8") as fh:
            fh.write(text)

    def test_a_second_load_returns_the_first_module_without_running_it_again(self):
        self.write(
            "counted.py",
            "import sys\nsys.counted_runs = getattr(sys, 'counted_runs', 0) + 1\nclass Error(Exception): pass\n",
        )
        sys.counted_runs = 0
        self.addCleanup(delattr, sys, "counted_runs")
        first = siblings.load(self.dir, "counted.py")
        second = siblings.load(os.path.join(self.dir, "."), "counted.py")
        self.assertIs(first, second)
        self.assertIs(first.Error, second.Error)
        self.assertEqual(sys.counted_runs, 1)

    def test_two_spellings_of_one_file_share_its_module(self):
        self.write("one.py", "")
        os.mkdir(os.path.join(self.dir, "sub"))
        self.assertIs(
            siblings.load(self.dir, "one.py"),
            siblings.load(os.path.join(self.dir, "sub"), os.path.join("..", "one.py")),
        )

    def test_a_circular_load_gets_the_part_built_module(self):
        self.write(
            "a.py",
            "import sys\nsiblings = sys.modules['siblings_under_test']\nFIRST = 1\nb = siblings.load(%r, 'b.py')\n"
            % self.dir,
        )
        self.write(
            "b.py",
            "import sys\nsiblings = sys.modules['siblings_under_test']\na = siblings.load(%r, 'a.py')\nSEEN = a.FIRST\n"
            % self.dir,
        )
        sys.modules["siblings_under_test"] = siblings
        self.addCleanup(sys.modules.pop, "siblings_under_test")
        a = siblings.load(self.dir, "a.py")
        self.assertIs(a.b.a, a)
        self.assertEqual(a.b.SEEN, 1)

    def test_a_load_that_raises_is_not_cached_so_a_retry_runs_it_again(self):
        self.write(
            "broken.py",
            "import sys\nif not getattr(sys, 'broken_ok', False):\n    raise ImportError('no numpy')\nREADY = True\n",
        )
        with self.assertRaises(ImportError):
            siblings.load(self.dir, "broken.py")
        sys.broken_ok = True
        self.addCleanup(delattr, sys, "broken_ok")
        self.assertTrue(siblings.load(self.dir, "broken.py").READY)

    def test_the_script_run_as_the_program_is_its_own_files_module(self):
        self.write(
            "lib.py",
            "import sys\nsys.path.insert(0, %r)\nimport siblings\nmain = siblings.load(%r, 'prog.py')\n"
            % (os.path.dirname(SCRIPT), self.dir),
        )
        self.write(
            "prog.py",
            (
                "import sys\nsys.path.insert(0, %r)\nimport siblings\n"
                "class Error(Exception): pass\n"
                "lib = siblings.load(%r, 'lib.py')\n"
                "print(lib.main is sys.modules['__main__'], lib.main.Error is Error)\n"
            )
            % (os.path.dirname(SCRIPT), self.dir),
        )
        run = subprocess.run(
            [sys.executable, os.path.join(self.dir, "prog.py")],
            capture_output=True,
            text=True,
            timeout=PROGRAM_RUN_S,
        )
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(run.stdout.strip(), "True True")


if __name__ == "__main__":
    unittest.main()
