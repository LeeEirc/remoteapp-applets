import json
import os
import unittest
import base64
from .main import parse_base64_str


class TestMySQLWorkBench8(unittest.TestCase):

    def setUp(self) -> None:
        self.args = os.environ.get("test_data")

    def test_parse_base64_str(self):
        d = parse_base64_str(self.args)
        print(d)


if __name__ == '__main__':
    unittest.main()
