from typing import Tuple
from taylor import sin, cos

# x^2 - sin(10x) = 0
EPS = 0.0001
SIGNS = 4
N = 100


def f(x: float, der=0) -> float:
    if der == 0:
        return x ** 2 - sin(10 * x, EPS)

    elif der == 1:
        return 2 * x - 10 * cos(10 * x, EPS)

    elif der == 2:
        return 100 * sin(10 * x, EPS) + 2

    else:
        raise ValueError('Unsupported value')


def seq_enum(a: float, b: float) -> Tuple[float, float]:
    if a >= b:
        raise ValueError('Invalid data')

    h = (b - a) / N
    x = a

    for k in range(1, N):
        x_new = a + k * h

        if f(x) * f(x_new) < 0:
            return x, x_new

        x = x_new

    raise Exception('Help...')


def interval(x: float, a: float, b: float) -> Tuple[float, float]:
    f_x = f(x)
    f_a = f(a)
    f_b = f(b)

    if f_a * f_x < 0:
        return a, x

    elif f_b * f_x < 0:
        return x, b

    else:
        raise Exception('Help...')


def newton(a: float, b: float) -> Tuple[float, int]:
    if a >= b:
        raise ValueError('Invalid data')

    a, b = seq_enum(a, b)
    x = a

    k = 0
    while True:
        k += 1

        x_new = x - f(x) / f(x, 1)

        if a < x_new < b:
            print('Условие выполнено -> метод ньютона')

        else:
            print('Условие не выполнено -> метод половинного деления')
            x_new = (a + b) / 2

        if abs(x_new - x) < EPS:
            return x_new, k

        a, b = interval(x_new, a, b)
        x = x_new


def main():
    x, k = newton(-10, 10)
    print(f'x = {x:.{SIGNS}f}\nk = {k}')
    print(f'{f(x):.{SIGNS}f}')


if __name__ == '__main__':
    main()
