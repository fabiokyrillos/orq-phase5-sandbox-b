import unittest

from calc import add, clamp, multiply, sign, subtract


class AddTest(unittest.TestCase):
    def test_add(self) -> None:
        self.assertEqual(add(2, 3), 5)


class SubtractTest(unittest.TestCase):
    def test_subtract(self) -> None:
        self.assertEqual(subtract(5, 3), 2)


class MultiplyTest(unittest.TestCase):
    def test_multiply(self) -> None:
        self.assertEqual(multiply(4, 2.5), 10.0)


class ClampTest(unittest.TestCase):
    def test_clamp_within_range(self) -> None:
        self.assertEqual(clamp(5, 0, 10), 5)

    def test_clamp_below_range(self) -> None:
        self.assertEqual(clamp(-1, 0, 10), 0)

    def test_clamp_above_range(self) -> None:
        self.assertEqual(clamp(11, 0, 10), 10)

    def test_clamp_at_boundaries(self) -> None:
        self.assertEqual(clamp(0, 0, 10), 0)
        self.assertEqual(clamp(10, 0, 10), 10)

    def test_clamp_fractional_values(self) -> None:
        self.assertEqual(clamp(2.5, 0.5, 1.5), 1.5)
        self.assertEqual(clamp(0.25, 0.5, 1.5), 0.5)
        self.assertEqual(clamp(1.25, 0.5, 1.5), 1.25)

    def test_clamp_equal_bounds(self) -> None:
        self.assertEqual(clamp(7, 3, 3), 3)
        self.assertEqual(clamp(-7, 3, 3), 3)
        self.assertEqual(clamp(3, 3, 3), 3)

    def test_clamp_reversed_bounds(self) -> None:
        with self.assertRaises(ValueError):
            clamp(5, 10, 0)


class SignTest(unittest.TestCase):
    def test_sign_negative(self) -> None:
        result = sign(-3.5)
        self.assertEqual(result, -1)
        self.assertIsInstance(result, int)

    def test_sign_zero(self) -> None:
        result = sign(0)
        self.assertEqual(result, 0)
        self.assertIsInstance(result, int)

    def test_sign_positive(self) -> None:
        result = sign(2)
        self.assertEqual(result, 1)
        self.assertIsInstance(result, int)


if __name__ == "__main__":
    unittest.main()
