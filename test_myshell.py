import os
import unittest   
from main_shell import MyShell

class TestMyShell(unittest.TestCase):
    def setUp(self):
        self.shell = MyShell()
        with open("test.txt", "w") as f:
            f.write("a\nb\nc\nd\ne\nf\n")
    
    def tearDown(self):
        if os.path.exists("text.txt"):
            os.remove("test.txt")
        if os.path.exists("copy.txt"):
            os.remove("copy.txt")

    def test_list_and_dirs(self):
        self.shell.run_command("list")
        self.shell.run_command("list __pycache__")
        self.shell.run_command("dir __pycache__")
        self.shell.run_command("dirs")

    def test_date_format(self):
        out = self.shell.run_command("date")
        self.assertIn("-", out)

    def test_time(self):
        out = self.shell.run_command("time")
        self.assertEqual(len(out.split(":")), 3)

    def test_time_flags(self):
        self.shell.run_command("time -hours -secs")
        self.shell.run_command("time -hours -mins")
        self.shell.run_command("time -hours")
        self.shell.run_command("time -mins")
        self.shell.run_command("time -secs")

    def test_cat(self):
        out = self.shell.run_command("cat test.txt")
        self.assertIn("a", out)

    def test_head(self):
        out = self.shell.run_command("head -3 test.txt")
        self.assertTrue(out.startswith("a"))

    def test_tail(self):
        out = self.shell.run_command("tail -2 test.txt")
        self.assertIn("f", out)

    def test_copy_and_remove(self):
        self.shell.run_command("copy_file test.txt copy.txt")
        self.assertTrue(os.path.exists("copy.txt"))
        self.shell.run_command("remove_file copy.txt")
        self.assertFalse(os.path.exists("copy.txt"))

    def test_empty_file(self):
        self.shell.run_command("empty_file test.txt")
        self.assertEqual(os.path.getsize("test.txt"), 0)

    def test_pwd(self):
        out = self.shell.run_command("pwd")
        self.assertTrue(os.path.isdir(out))

if __name__ == "__main__":
    unittest.main()