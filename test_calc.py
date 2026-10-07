import unittest

from calc import add, multiply, subtract


class AddTest(unittest.TestCase):
    def test_add(self) -> None:
        self.assertEqual(add(2, 3), 5)


class SubtractTest(unittest.TestCase):
    def test_subtract(self) -> None:
        self.assertEqual(subtract(5, 3), 2)


class MultiplyTest(unittest.TestCase):
    def test_multiply(self) -> None:
        self.assertEqual(multiply(4, 2.5), 10.0)


if __name__ == "__main__":
    unittest.main()
