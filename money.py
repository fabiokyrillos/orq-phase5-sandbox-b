"""Helpers for Brazilian reais (BRL).

Amounts are handled through ``Decimal(str(value))`` so that the two decimal
places a user typed are the ones we work with, and allocation is done in
integer cents so that no float noise can create or destroy money.
"""

import math
import re
from decimal import ROUND_HALF_UP, Decimal

CENTS = Decimal("0.01")

# "R$ 1.234,56": optional minus sign, then "R$", then groups of three digits
# separated by "." (the first group may be shorter), then exactly two decimals.
_BRL_RE = re.compile(r"^(?P<sign>-?)R\$ ?(?P<integer>\d{1,3}(?:\.\d{3})*),(?P<cents>\d{2})$")


def _to_decimal(value: float) -> Decimal:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError("value must be an int or a float")
    if not math.isfinite(value):
        raise ValueError("value must be a finite number")
    return Decimal(str(value))


def format_brl(value: float) -> str:
    """Format ``value`` as Brazilian currency, e.g. ``R$ 1.234,56``.

    Values with more than two decimal places are rounded half up, so
    ``1.005`` becomes ``R$ 1,01``. Negative amounts put the sign before the
    symbol: ``-R$ 5,00``. An amount that rounds to zero never gets a sign.
    """
    amount = _to_decimal(value).quantize(CENTS, rounding=ROUND_HALF_UP)
    sign = "-" if amount < 0 else ""
    # Format in the en-US style the stdlib gives us, then swap the separators.
    digits = f"{abs(amount):,.2f}".translate(str.maketrans({",": ".", ".": ","}))
    return f"{sign}R$ {digits}"


def parse_brl(text: str) -> float:
    """Read a string produced by :func:`format_brl` back into a float.

    The whole string must match the Brazilian format: thousands grouped with
    ".", exactly two decimals after ",", and the sign before ``R$``. Anything
    else raises ``ValueError``; a non-string argument raises ``TypeError``.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    match = _BRL_RE.match(text.strip())
    if match is None:
        raise ValueError(f"not a Brazilian currency amount: {text!r}")
    integer = match["integer"].replace(".", "")
    return float(Decimal(f"{match['sign']}{integer}.{match['cents']}"))


def split_bill(total: float, people: int) -> list[float]:
    """Split ``total`` into ``people`` shares that add up to exactly ``total``.

    The shares have two decimal places each and their cents sum back to the
    cents of ``total``. When the division leaves a remainder, the leftover
    cents go to the first people in the list, so ``split_bill(100, 3)`` gives
    ``[33.34, 33.33, 33.33]``.

    ``people`` must be a positive integer and ``total`` must be a finite
    amount in whole cents; otherwise ``ValueError`` is raised.
    """
    if isinstance(people, bool) or not isinstance(people, int):
        raise TypeError("people must be an int")
    if people < 1:
        raise ValueError("people must be at least 1")

    amount = _to_decimal(total)
    if amount != amount.quantize(CENTS):
        raise ValueError("total must not contain fractions of a cent")

    cents = int(amount.scaleb(2))
    negative = cents < 0
    base, leftover = divmod(abs(cents), people)
    shares = [base + 1] * leftover + [base] * (people - leftover)
    # A zero share stays +0.0 even when the bill is negative.
    return [-(share / 100) if negative and share else share / 100 for share in shares]
