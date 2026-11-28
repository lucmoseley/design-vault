import glob
import os
import shutil
import subprocess
import sys
import tempfile
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
ABSENT = (
    "import runpy, sys\n"
    "names, error = sys.argv[1].split(','), getattr(__builtins__, sys.argv[2])\n"
    "class Absent:\n"
    "    def find_spec(self, name, path=None, target=None):\n"
    "        if name.split('.')[0] in names:\n"
    "            raise error(f'planted: no {name}', name=name)\n"
    "sys.meta_path.insert(0, Absent())\n"
    "sys.argv = sys.argv[3:]\n"
    "runpy.run_path(sys.argv[0], run_name='__main__')\n"
)
PLANT = "raise RuntimeError('planted load crash')\n"
UNPLANTED = {"siblings.py", "crash_exit.py"}


def checks(scripts=SCRIPTS):
    found = sorted(glob.glob(os.path.join(scripts, "check-*.py")))
    assert len(found) == 17, found
    return found


def run(*argv):
    return subprocess.run(
        [sys.executable, *argv],
        capture_output=True,
        text=True,
        timeout=RUN_S,
        check=False,
    )


def crashed(script):
    return run("-c", CRASH, script, "page.html")


def without(names, script, error="ModuleNotFoundError"):
    return run("-c", ABSENT, names, error, script, "page.html")


class CrashExit(unittest.TestCase):
    def test_a_crash_exits_2_with_its_traceback_on_stderr_and_no_stdout(self):
        for script in checks():
            with self.subTest(os.path.basename(script)):
                proc = crashed(script)
                self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
                self.assertIn("Traceback", proc.stderr)
                self.assertIn("RuntimeError: planted crash", proc.stderr)
                self.assertEqual(proc.stdout, "")

    def test_a_sibling_that_fails_to_load_exits_2_with_its_traceback(self):
        with tempfile.TemporaryDirectory() as tmp:
            scripts = os.path.join(tmp, "scripts")
            shutil.copytree(SCRIPTS, scripts)
            for path in glob.glob(os.path.join(scripts, "*.py")):
                name = os.path.basename(path)
                if name in UNPLANTED or name.startswith("check-"):
                    continue
                with open(path, encoding="utf-8") as handle:
                    body = handle.read()
                with open(path, "w", encoding="utf-8") as handle:
                    handle.write(PLANT + body)
            for script in checks(scripts):
                with self.subTest(os.path.basename(script)):
                    proc = run(script, "page.html")
                    self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
                    self.assertIn("RuntimeError: planted load crash", proc.stderr)
                    self.assertEqual(proc.stdout, "")

    def test_a_module_the_plugin_does_not_pin_missing_exits_2_not_3(self):
        for module in ["argparse", "siblings"]:
            for script in checks():
                with self.subTest(module, script=os.path.basename(script)):
                    proc = without(module, script)
                    self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
                    self.assertIn(f"planted: no {module}", proc.stderr)
                    self.assertEqual(proc.stdout, "")

    def test_a_pinned_package_missing_while_loading_exits_3_naming_it(self):
        for name in ["dom", "access", "overlay", "seams"]:
            with self.subTest(name):
                proc = without("numpy", os.path.join(SCRIPTS, f"check-{name}.py"))
                self.assertEqual(proc.returncode, 3, proc.stdout + proc.stderr)
                self.assertIn(f"check-{name}.py: numpy is missing", proc.stderr)
                self.assertIn("pip install", proc.stderr)
                self.assertEqual(proc.stdout, "")

    def test_a_broken_pinned_package_exits_3_naming_it(self):
        proc = without("PIL", os.path.join(SCRIPTS, "check-access.py"), "ImportError")
        self.assertEqual(proc.returncode, 3, proc.stdout + proc.stderr)
        self.assertIn("check-access.py: PIL is missing", proc.stderr)

    def test_a_pinned_package_main_imports_missing_exits_3_naming_it(self):
        proc = without("PIL", os.path.join(SCRIPTS, "check-render.py"))
        self.assertEqual(proc.returncode, 3, proc.stdout + proc.stderr)
        self.assertIn("check-render.py: PIL is missing", proc.stderr)
        self.assertEqual(proc.stdout, "")


if __name__ == "__main__":
    unittest.main()
