import unittest

from takeoff.main import main


class TestMain(unittest.TestCase):

    def test_help(self):
        self.assertRaises(SystemExit, main, ["--help"])
