from numpy.linalg import norm

EPS = 0.000001  # точность
L = 0.1  # шаг
N_MAX = 1000  # максимальное число шагов


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
