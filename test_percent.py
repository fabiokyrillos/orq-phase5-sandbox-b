import unittest

from percent import percent


class PercentTest(unittest.TestCase):
    def test_percent(self) -> None:
        self.assertEqual(percent(1, 4), 25.0)

    def test_percent_zero_whole(self) -> None:
        with self.assertRaises(ValueError):
            percent(1, 0)


if __name__ == "__main__":
    unittest.main()
