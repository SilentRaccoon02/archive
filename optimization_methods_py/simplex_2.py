import time
import numpy as np
import matplotlib.pyplot as plt

alpha = 1
beta = 0.5
gamma = 2
N_MAX = 30  # максимальное число шагов


def f(point):
    x, y = point
    return (x ** 2 + y - 11) ** 2 + (x + y ** 2 - 7) ** 2


def z(x, y):
    return (x ** 2 + y - 11) ** 2 + (x + y ** 2 - 7) ** 2


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return '(%.3f, %.3f)' % (self.x, self.y)

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x, y)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return Vector(x, y)

    def __rmul__(self, other):
        x = self.x * other
        y = self.y * other
        return Vector(x, y)

    def __truediv__(self, other):
        x = self.x / other
        y = self.y / other
        return Vector(x, y)

    def c(self):
        return self.x, self.y


def main():
    x = np.arange(-4, 4, 0.1)
    y = np.arange(-4, 4, 0.1)
    x_3d, y_3d = np.meshgrid(x, y)
    z_3d = z(x_3d, y_3d)

    plt.ion()
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, figsize=[10, 8])
    ax.plot_surface(x_3d, y_3d, z_3d, alpha=0.6)

    v1 = Vector(0, 0)
    v2 = Vector(0, 0.5)
    v3 = b = Vector(0.5, 0)

    point_1 = ax.scatter(v1.x, v1.y, f(v1.c()), color='red')
    point_2 = ax.scatter(v2.x, v2.y, f(v2.c()), color='red')
    point_3 = ax.scatter(v3.x, v3.y, f(v3.c()), color='red')

    n = 0
    for i in range(N_MAX):
        n += 1

        temp = {v1: f(v1.c()), v2: f(v2.c()), v3: f(v3.c())}
        points = sorted(temp.items(), key=lambda x: x[1])  # сортировка по значению функции

        point_1.remove()
        point_2.remove()
        point_3.remove()
        point_1 = ax.scatter(v1.x, v1.y, f(v1.c()), color='red')
        point_2 = ax.scatter(v2.x, v2.y, f(v2.c()), color='red')
        point_3 = ax.scatter(v3.x, v3.y, f(v3.c()), color='red')
        fig.canvas.draw()
        fig.canvas.flush_events()

        b = points[0][0]
        g = points[1][0]
        w = points[2][0]

        mid = (g + b) / 2

        # reflection
        xr = mid + alpha * (mid - w)
        if f(xr.c()) < f(g.c()):
            w = xr
        else:
            if f(xr.c()) < f(w.c()):
                w = xr
            c = (w + mid) / 2
            if f(c.c()) < f(w.c()):
                w = c
        if f(xr.c()) < f(b.c()):

            # expansion
            xe = mid + gamma * (xr - mid)
            if f(xe.c()) < f(xr.c()):
                w = xe
            else:
                w = xr
        if f(xr.c()) > f(g.c()):

            # contraction
            xc = mid + beta * (w - mid)
            if f(xc.c()) < f(w.c()):
                w = xc

        v1 = w
        v2 = g
        v3 = b

    print('Число шагов:', n)
    print('Минимум: (%.3f, %.3f) = %.3f' % (b.x, b.y, f(b.c())))

    plt.ioff()

    ax.scatter(b.x, b.y, f(b.c()), color='blue')
    plt.show()


if __name__ == "__main__":
    main()
