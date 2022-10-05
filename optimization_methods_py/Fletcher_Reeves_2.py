import numpy as np
from numpy.linalg import norm


def ddx(x, y):
    return 2 * (2 * x * (x ** 2 + y - 11) + x + y ** 2 - 7)


def ddy(x, y):
    return 2 * (x ** 2 + 2 * y * (x + y ** 2 - 7) + y - 11)


def f(point):
    x, y = point
    return (x ** 2 + y - 11) ** 2 + (x + y ** 2 - 7) ** 2


def grad(point):
    x, y = point
    return ddx(x, y), ddy(x, y)


def arg_min(x, d):
    alpha = np.arange(0.0001, 0.9, 0.0001)
    func = [f((x + item * d).v) for item in alpha]
    return alpha[np.argmin(func)]


class Vector:
    def __init__(self, v):
        self.x, self.y = v

    def __repr__(self):
        return '(%.3f, %.3f)' % (self.x, self.y)

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector((x, y))

    def __rmul__(self, other):
        x = self.x * other
        y = self.y * other
        return Vector((x, y))

    def __neg__(self):
        return Vector((-self.x, -self.y))

    @property
    def v(self):
        return self.x, self.y

    @property
    def a(self):
        return [self.x, self.y]


def main():
    x = Vector((0, 0))
    d = -Vector(grad(x.v))

    k = 0
    n = 6

    while k < n:
        if n % (k + 1) == 0:
            print('#1', end=' ')
            alpha_k = arg_min(x, d)

            x_new = x + alpha_k * d
            d_new = -Vector(grad(x_new.v))

            x = x_new
            d = d_new

        else:
            print('#2', end=' ')
            alpha_k = arg_min(x, d)

            x_new = x + alpha_k * d

            f_1 = (norm(Vector(grad(x_new.v)).a)) ** 2
            f_2 = (norm(Vector(grad(x.v)).a)) ** 2
            beta_k = f_1 / f_2

            d_new = -Vector(grad(x_new.v)) + beta_k * d

            x = x_new
            d = d_new

        k += 1
        print(x, 'k =', k)

    print('Минимум: (%.3f, %.3f) = %.3f' % (x.x, x.y, f(x.v)))


if __name__ == "__main__":
    main()
