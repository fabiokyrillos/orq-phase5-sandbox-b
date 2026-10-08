def add(a: float, b: float) -> float:
    return a + b


def subtract(a: float, b: float) -> float:
    return a - b


def multiply(a: float, b: float) -> float:
    return a * b


def clamp(value: float, low: float, high: float) -> float:
    if low > high:
        raise ValueError("low must not be greater than high")
    if value < low:
        return low
    if value > high:
        return high
    return value


def sign(value: float) -> int:
    if value < 0:
        return -1
    if value > 0:
        return 1
    return 0
