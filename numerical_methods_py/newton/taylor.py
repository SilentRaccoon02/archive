import math
from typing import Callable

PI = math.pi


def sin_n(x: float, n: int) -> float:
    return (-1) ** n * x ** (2 * n + 1) / math.factorial(2 * n + 1)


def cos_n(x: float, n: int) -> float:
    return (-1) ** n * x ** (2 * n) / math.factorial(2 * n)


def taylor(series: Callable, x: float, eps: float) -> float:
    if abs(x) > PI / 4:
        raise ValueError('Unsupported value')

    new_n = series(x, 0)
    result = new_n

    n = 1
    while abs(new_n) > eps:
        new_n = series(x, n)
        result += new_n

        n += 1

    return result


def sin(x: float, eps: float) -> float:
    abs_x = abs(x)

    if abs_x > 7 * PI / 4:
        return sin(x - 2 * PI, eps) if x > 0 else sin(x + 2 * PI, eps)

    elif abs_x < PI / 4:
        return taylor(sin_n, x, eps)

    elif abs_x < 3 * PI / 4:
        return taylor(cos_n, PI / 2 - x, eps) if x > 0 else -taylor(cos_n, PI / 2 + x, eps)

    elif abs_x < 5 * PI / 4:
        return taylor(sin_n, PI - x, eps) if x > 0 else -taylor(sin_n, PI + x, eps)

    elif abs_x < 7 * PI / 4:
        return -taylor(cos_n, 3 * PI / 2 - x, eps) if x > 0 else taylor(cos_n, 3 * PI / 2 + x, eps)

    else:
        raise Exception('Help...')


def cos(x: float, eps: float) -> float:
    abs_x = abs(x)

    if abs_x > 7 * PI / 4:
        return cos(x - 2 * PI, eps) if x > 0 else cos(x + 2 * PI, eps)

    elif abs_x < PI / 4:
        return taylor(cos_n, x, eps)

    elif abs_x < 3 * PI / 4:
        return taylor(sin_n, PI / 2 - abs_x, eps)

    elif abs_x < 5 * PI / 4:
        return -taylor(cos_n, PI - abs_x, eps)

    elif abs_x < 7 * PI / 4:
        return -taylor(sin_n, 3 * PI / 2 - abs_x, eps)

    else:
        raise Exception('Help...')
