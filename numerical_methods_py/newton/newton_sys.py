import math
from typing import Tuple
from taylor import sin, cos

# cos(y + 0.5) - x = 2
# sin(x) - 2y =1
EPS = 0.0001
SIGNS = 4
N = 10


def solve(a11: float, a12: float, a1: float, a21: float, a22: float, a2: float) -> Tuple[float, float]:
    a22 = a22 * (a11 / a21) - a12
    a2 = a2 * (a11 / a21) - a1
    x2 = a2 / a22
    x1 = (a1 - a12 * x2) / a11

    return x1, x2


def f(x: float, y: float, der: str, const=1.0) -> float:
    if der == '1':
        return const * cos(y + 0.5, EPS) - x - 2

    elif der == '2':
        return const * sin(x, EPS) - 2 * y - 1

    elif der == '1x':
        return -1

    elif der == '1y':
        return -const * sin(y + 0.5, EPS)

    elif der == '2x':
        return const * cos(x, EPS)

    elif der == '2y':
        return -2

    else:
        raise ValueError('Invalid data')


def approx() -> Tuple[float, float]:
    x = -2
    y = -1 / 2

    for i in range(1, N + 1):
        const = i / N

        a11 = f(x, y, '1x', const)
        a12 = f(x, y, '1y', const)
        a1 = -f(x, y, '1', const)

        a21 = f(x, y, '2x', const)
        a22 = f(x, y, '2y', const)
        a2 = -f(x, y, '2', const)

        g, h = solve(a11, a12, a1, a21, a22, a2)
        x = x + g
        y = y + h

    return x, y


def newton(x: float, y: float) -> Tuple[float, float, int]:
    k = 0
    while True:
        k += 1

        a11 = f(x, y, '1x')
        a12 = f(x, y, '1y')
        a1 = -f(x, y, '1')

        a21 = f(x, y, '2x')
        a22 = f(x, y, '2y')
        a2 = -f(x, y, '2')

        g, h = solve(a11, a12, a1, a21, a22, a2)
        x_new = x + g
        y_new = y + h

        if math.sqrt((x_new - x) ** 2 + (y_new - y) ** 2) < EPS:
            return x_new, y_new, k

        x = x_new
        y = y_new


def plot():
    import numpy as np
    import matplotlib.pyplot as plt

    x1 = np.arange(-4, 4, 0.01)
    y2 = np.arange(-4, 4, 0.01)

    x2 = [cos(y + 0.5, EPS) - 2 for y in y2]
    y1 = [(sin(x, EPS) - 1) / 2 for x in x2]

    plt.plot(x1, y1, x2, y2)
    plt.grid()
    plt.show()


def main():
    x, y = approx()
    x, y, k = newton(x, y)
    print(f'x = {x:.{SIGNS}f}\ny = {y:.{SIGNS}f}\nk = {k}')


if __name__ == '__main__':
    # plot()
    main()
