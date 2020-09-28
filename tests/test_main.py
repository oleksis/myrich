import os, sys
from subprocess import PIPE, Popen
from unittest import TestCase, main as unittest_main

_path = os.path.realpath(os.path.abspath(__file__))
ROOT_PATH = os.path.dirname(os.path.dirname(_path))
sys.path.insert(0, ROOT_PATH)

from myrich import __version__ as version


class MainTest(TestCase):
    """Main test with subprocess
    NOTE: Rich package need be system-wide installed
    """

    def setUp(self) -> None:
        self.cwd = ROOT_PATH
        self.args = []
        self.command = ["python", "-m", "myrich"] + self.args
        self.process: Popen = None
        self.stdout = self.stderr = self.stdin = None
        self.return_code = None
        self.encoding = "utf-8"
        self.ENTER = "\n"

    def test_run_myrich(self, args: list = [], data: str = ""):
        if args:
            self.args = args

        self.command += self.args
        self.process = Popen(
            self.command,
            stdin=PIPE,
            stdout=PIPE,
            stderr=PIPE,
            cwd=self.cwd,
            encoding=self.encoding,
        )

        if data:
            self.stdin = data
            self.stdout, self.stderr = self.process.communicate(
                data + self.ENTER + "exit" + self.ENTER
            )
            self.assertTrue("(rich)" in self.stdout and "Bye" in self.stdout)
        else:
            # Sure exit the shell and read output and error
            self.stdout, self.stderr = self.process.communicate("exit" + self.ENTER)

        self.return_code = self.process.returncode

    def test_myrich_version(self):
        self.test_run_myrich(["--version"])
        output = self.stdout
        self.assertFalse(self.return_code)
        self.assertTrue(version in output)

    def test_myrich_hello(self):
        self.test_run_myrich(["echo Hello out there :waving_hand:"])
        expected = "Hello out there"
        output = self.stdout
        self.assertFalse(self.return_code)
        self.assertTrue(expected in output)

    def test_myrich_cd_tests(self):
        data = "cd tests"
        self.test_run_myrich([], data)
        output = self.stdout
        self.assertFalse(self.return_code)
        self.assertTrue("(rich)" in output and "tests" in output)

    def test_myrich_syntax(self):
        self.test_run_myrich(["-S", "-l", "--path", "setup.py"])
        expected = "setuptools"
        output = self.stdout
        self.assertFalse(self.return_code)
        self.assertTrue(expected in output)

    def test_myrich_syntax_error_color(self):
        self.test_run_myrich(["-S", "-b", "mycolor", "--path", "setup.py"])
        output = self.stdout
        self.assertTrue("ERROR:" in output and "mycolor" in output)

    def test_myrich_syntax_error_path(self):
        self.test_run_myrich(["-S", "-l", "setup.py"])
        output = self.stdout
        self.assertTrue("ERROR:" in output and "--path" in output)

    def test_myrich_markdown_file(self):
        self.test_run_myrich(["-M", "README.md"])
        link = "(https://rich.readthedocs.io/en/latest/)"
        output = self.stdout
        self.assertFalse(self.return_code)
        self.assertTrue(link in output)

    def test_myrich_markdown_string(self):
        self.test_run_myrich(["-M", "# Header text of file"])
        expected = "╔═"
        output = self.stdout
        self.assertFalse(self.return_code)
        self.assertTrue(expected in output and "Header text of file" in output)

    def test_myrich_markdown_hyperlinks(self):
        # If your Terminal support links
        self.test_run_myrich(["-M", "-y", "README.md"])
        link = "(https://rich.readthedocs.io/en/latest/)"
        output = self.stdout
        self.assertFalse(self.return_code)
        # No show in CMD
        self.assertFalse(link in output)

    def test_myrich_shell_syntax(self):
        data = "syntax -l --path setup.py"
        self.test_run_myrich([], data)
        output = self.stdout
        self.assertFalse(self.return_code)
        self.assertTrue(data == self.stdin)
        self.assertTrue("10" in output)
        self.assertTrue("Shell-like using Rich" in output)

    def test_myrich_shell_markdown(self):
        data = "markdown -t README.md"
        link = "(https://rich.readthedocs.io/en/latest/)"
        self.test_run_myrich([], data)
        self.assertTrue(data == self.stdin)
        output = self.stdout
        self.assertFalse(self.return_code)
        self.assertTrue(link in output)

    def test_myrich_shell_myrich(self):
        data = "myrich"
        expected = "WARNING: No action taken to avoid nested environments"
        self.test_run_myrich([], data)
        self.assertTrue(data == self.stdin)
        output = self.stdout
        self.assertFalse(self.return_code)
        self.assertTrue(expected in output)

    def tearDown(self) -> None:
        if self.process and isinstance(self.process, Popen):
            self.process.kill()


if __name__ == "__main__":
    unittest_main()
