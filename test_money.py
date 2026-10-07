import unittest

from money import format_brl, parse_brl, split_bill


def cents(shares: list[float]) -> int:
    """Sum shares in integer cents, so float noise cannot hide a lost cent."""
    return sum(round(share * 100) for share in shares)


class FormatBrlTest(unittest.TestCase):
    def test_format_grouped_amount(self) -> None:
        self.assertEqual(format_brl(1234.56), "R$ 1.234,56")

    def test_format_negative_uses_sign_before_symbol(self) -> None:
        self.assertEqual(format_brl(-5), "-R$ 5,00")

    def test_format_zero(self) -> None:
        self.assertEqual(format_brl(0), "R$ 0,00")

    def test_format_small_and_large_amounts(self) -> None:
        self.assertEqual(format_brl(0.5), "R$ 0,50")
        self.assertEqual(format_brl(999.99), "R$ 999,99")
        self.assertEqual(format_brl(1000), "R$ 1.000,00")
        self.assertEqual(format_brl(1234567.89), "R$ 1.234.567,89")

    def test_format_rounds_half_up(self) -> None:
        self.assertEqual(format_brl(1.005), "R$ 1,01")
        self.assertEqual(format_brl(2.344), "R$ 2,34")
        self.assertEqual(format_brl(-1.005), "-R$ 1,01")

    def test_format_amount_rounding_to_zero_has_no_sign(self) -> None:
        self.assertEqual(format_brl(-0.001), "R$ 0,00")

    def test_format_rejects_non_finite(self) -> None:
        for value in (float("nan"), float("inf"), float("-inf")):
            with self.subTest(value=value), self.assertRaises(ValueError):
                format_brl(value)

    def test_format_rejects_non_number(self) -> None:
        with self.assertRaises(TypeError):
            format_brl("1234.56")


class ParseBrlTest(unittest.TestCase):
    def test_parse_grouped_amount(self) -> None:
        self.assertEqual(parse_brl("R$ 1.234,56"), 1234.56)

    def test_parse_negative_and_zero(self) -> None:
        self.assertEqual(parse_brl("-R$ 5,00"), -5.0)
        self.assertEqual(parse_brl("R$ 0,00"), 0.0)

    def test_parse_accepts_surrounding_whitespace_and_missing_space(self) -> None:
        self.assertEqual(parse_brl("  R$ 7,25  "), 7.25)
        self.assertEqual(parse_brl("R$7,25"), 7.25)

    def test_parse_round_trips_format(self) -> None:
        for value in (0.0, 0.5, -5.0, 1234.56, 1234567.89):
            with self.subTest(value=value):
                self.assertEqual(parse_brl(format_brl(value)), value)

    def test_parse_rejects_malformed_text(self) -> None:
        malformed = [
            "",
            "1234,56",            # no symbol
            "R$ 1234,56",         # thousands not grouped
            "R$ 1.23,56",         # wrong group size
            "R$ 1.234.5,67",      # wrong group size
            "R$ 1,234.56",        # en-US separators
            "R$ 1.234,5",         # only one decimal
            "R$ 1.234,567",       # three decimals
            "R$ 1.234",           # no decimals
            "R$ -5,00",           # sign in the wrong place
            "R$ abc,00",
            "R$ 1.234,56 reais",  # trailing text
            "US$ 1.234,56",
        ]
        for text in malformed:
            with self.subTest(text=text), self.assertRaises(ValueError):
                parse_brl(text)

    def test_parse_rejects_non_string(self) -> None:
        with self.assertRaises(TypeError):
            parse_brl(1234.56)


class SplitBillTest(unittest.TestCase):
    def test_split_leftover_cents_go_to_the_first_people(self) -> None:
        self.assertEqual(split_bill(100, 3), [33.34, 33.33, 33.33])
        self.assertEqual(cents(split_bill(100, 3)), 10000)

    def test_split_small_amount_with_one_leftover_cent(self) -> None:
        self.assertEqual(split_bill(0.29, 2), [0.15, 0.14])
        self.assertEqual(cents(split_bill(0.29, 2)), 29)

    def test_split_exact_division(self) -> None:
        self.assertEqual(split_bill(90, 3), [30.0, 30.0, 30.0])
        self.assertEqual(cents(split_bill(90, 3)), 9000)

    def test_split_between_one_person(self) -> None:
        self.assertEqual(split_bill(12.34, 1), [12.34])
        self.assertEqual(cents(split_bill(12.34, 1)), 1234)

    def test_split_total_smaller_than_people(self) -> None:
        shares = split_bill(0.02, 3)
        self.assertEqual(shares, [0.01, 0.01, 0.0])
        self.assertEqual(cents(shares), 2)

    def test_split_zero_total(self) -> None:
        self.assertEqual(split_bill(0, 4), [0.0, 0.0, 0.0, 0.0])

    def test_split_negative_total(self) -> None:
        shares = split_bill(-100, 3)
        self.assertEqual(shares, [-33.34, -33.33, -33.33])
        self.assertEqual(cents(shares), -10000)

    def test_split_conserves_cents_over_many_sizes(self) -> None:
        for people in range(1, 13):
            for total in (0.07, 1.0, 12.34, 100.0, 9999.99):
                with self.subTest(total=total, people=people):
                    shares = split_bill(total, people)
                    self.assertEqual(len(shares), people)
                    self.assertEqual(cents(shares), round(total * 100))
                    self.assertEqual(shares, sorted(shares, reverse=True))

    def test_split_rejects_bad_people_count(self) -> None:
        for people in (0, -1):
            with self.subTest(people=people), self.assertRaises(ValueError):
                split_bill(10, people)
        for people in (2.0, "2", None, True):
            with self.subTest(people=people), self.assertRaises(TypeError):
                split_bill(10, people)

    def test_split_rejects_fractions_of_a_cent(self) -> None:
        for total in (0.001, 10.005, 1 / 3):
            with self.subTest(total=total), self.assertRaises(ValueError):
                split_bill(total, 2)

    def test_split_rejects_non_finite_total(self) -> None:
        for total in (float("nan"), float("inf")):
            with self.subTest(total=total), self.assertRaises(ValueError):
                split_bill(total, 2)


if __name__ == "__main__":
    unittest.main()
