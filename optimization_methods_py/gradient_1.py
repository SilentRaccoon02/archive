from numpy.linalg import norm

EPS = 0.0000000004  # точность
L = 0.1  # шаг
N_MAX = 9300  # максимальное число шагов


def ddx(x, y):
    return 2 * (200 * x ** 3 - 200 * x * y + x - 1)


def ddy(x, y):
    return 200 * (y - x ** 2)


def f(point):
    x, y = point
    return 100 * (y - x ** 2) ** 2 + (1 - x) ** 2


def grad(point):
    x, y = point
    return ddx(x, y), ddy(x, y)


class Vector:
    def __init__(self, v):
        self.x, self.y = v

    def __repr__(self):
        return '(%.3f, %.3f)' % (self.x, self.y)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return Vector((x, y))

    def __rmul__(self, other):
        x = self.x * other
        y = self.y * other
        return Vector((x, y))

    @property
    def v(self):
        return self.x, self.y

    @property
    def a(self):
        return [self.x, self.y]


def main():
    alpha = 0.4
    x = Vector((0, 0))

    n = 0
    for n in range(N_MAX):
        d = alpha * Vector(grad(x.v))
        nvs = (norm(d.a)) ** 2

        if nvs < EPS:
            break

        x_new = x - alpha * d
        f_x = f(x.v)
        f_new = f(x_new.v)

        if f_new - f_x <= -alpha * nvs:
            alpha_k = alpha
        else:
            alpha_k = alpha * L

        x = x_new
        alpha = alpha_k
        print(x)

    print('Число шагов:', n)
    print('Минимум: (%.3f, %.3f) = %.3f' % (x.x, x.y, f(x.v)))


if __name__ == "__main__":
    main()
