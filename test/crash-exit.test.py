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


def crashed(script):
    return subprocess.run(
        [sys.executable, "-c", CRASH, script, "page.html"],
        capture_output=True,
        text=True,
        timeout=RUN_S,
        check=False,
    )


class CrashExit(unittest.TestCase):
    def test_a_crash_exits_2_with_its_traceback_on_stderr_and_no_stdout(self):
        checks = sorted(glob.glob(os.path.join(SCRIPTS, "check-*.py")))
        self.assertEqual(len(checks), 17, checks)
        for script in checks:
            with self.subTest(os.path.basename(script)):
                proc = crashed(script)
                self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
                self.assertIn("Traceback", proc.stderr)
                self.assertIn("RuntimeError: planted crash", proc.stderr)
                self.assertEqual(proc.stdout, "")


if __name__ == "__main__":
    unittest.main()
