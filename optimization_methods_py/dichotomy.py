import time
import math
import numpy as np
import matplotlib.pyplot as plt

L = 0.1  # шаг
EPS = 2.1 * L  # точность
N_MAX = 20  # максимальное число шагов


def f(x):
    a = 1
    b = 2
    return a / math.exp(x) + b * x


def main():
    a = -1.0  # [a, b]
    b = 2.0

    x_plt = np.arange(-1.0, 1.0, 0.1)
    f_plt = [f(x) for x in x_plt]

    plt.ion()
    fig, ax = plt.subplots()
    ax.grid(True)
    ax.plot(x_plt, f_plt)

    x = (a + b) / 2
    point = ax.scatter(x, f(x), c='red')

    n = 0
    while abs(b - a) >= EPS and n < N_MAX:
        n += 1

        f_1 = f(x - L)
        f_2 = f(x + L)

        if f_1 > f_2:
            a = x - L
        else:
            b = x + L

        x = (a + b) / 2

        print('(%.2f, %.2f)' % (a, b))

        point.set_offsets([x, f(x)])
        fig.canvas.draw()
        fig.canvas.flush_events()
        time.sleep(0.2)

    print('Число шагов:', n)
    print('Минимум: (%.2f, %.2f)' % (x, f(x)))

    plt.ioff()
    point.remove()
    ax.scatter(x, f(x), c='blue')
    plt.show()


if __name__ == "__main__":
    main()
