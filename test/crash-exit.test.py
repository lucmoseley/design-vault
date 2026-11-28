import glob
import os
import subprocess
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.join(HERE, "..", "plugin", "skills", "design-round", "scripts")
# guess, #543
RUN_S = 60
# #543
CRASH = (
    "import argparse, runpy, sys\n"
    "def crash(*args, **kwargs):\n"
    "    raise RuntimeError('planted crash')\n"
    "argparse.ArgumentParser.parse_args = crash\n"
    "sys.argv = sys.argv[1:]\n"
    "runpy.run_path(sys.argv[0], run_name='__main__')\n"
)


# #649
LOAD_CRASH = (
    "import os, runpy, sys\n"
    "sys.path.insert(0, os.path.dirname(os.path.abspath(sys.argv[1])))\n"
    "import siblings\n"
    "def crash(*args, **kwargs):\n"
    "    raise RuntimeError('planted load crash')\n"
    "siblings.load = crash\n"
    "sys.argv = sys.argv[1:]\n"
    "runpy.run_path(sys.argv[0], run_name='__main__')\n"
)
# #649
NO_NUMPY = (
    "import runpy, sys\n"
    "class Absent:\n"
    "    def find_spec(self, name, path=None, target=None):\n"
    "        if name.split('.')[0] == 'numpy':\n"
    "            raise ModuleNotFoundError(f'No module named {name!r}', name=name)\n"
    "sys.meta_path.insert(0, Absent())\n"
    "sys.argv = sys.argv[1:]\n"
    "runpy.run_path(sys.argv[0], run_name='__main__')\n"
)


def checks():
    found = sorted(glob.glob(os.path.join(SCRIPTS, "check-*.py")))
    assert len(found) == 17, found
    return found


def crashed(script, plant=CRASH):
    return subprocess.run(
        [sys.executable, "-c", plant, script, "page.html"],
        capture_output=True,
        text=True,
        timeout=RUN_S,
        check=False,
    )


class CrashExit(unittest.TestCase):
    def test_a_crash_exits_2_with_its_traceback_on_stderr_and_no_stdout(self):
        for script in checks():
            with self.subTest(os.path.basename(script)):
                proc = crashed(script)
                self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
                self.assertIn("Traceback", proc.stderr)
                self.assertIn("RuntimeError: planted crash", proc.stderr)
                self.assertEqual(proc.stdout, "")

    def test_a_crash_while_loading_exits_2_with_its_traceback(self):
        for script in checks():
            with self.subTest(os.path.basename(script)):
                proc = crashed(script, LOAD_CRASH)
                self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
                self.assertIn("RuntimeError: planted load crash", proc.stderr)
                self.assertEqual(proc.stdout, "")

    def test_a_package_missing_while_loading_exits_3_naming_it(self):
        proc = crashed(os.path.join(SCRIPTS, "check-dom.py"), NO_NUMPY)
        self.assertEqual(proc.returncode, 3, proc.stdout + proc.stderr)
        self.assertIn("check-dom.py: numpy is missing", proc.stderr)
        self.assertEqual(proc.stdout, "")


if __name__ == "__main__":
    unittest.main()
