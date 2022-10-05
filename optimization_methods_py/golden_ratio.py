import time
import math
import numpy as np
import matplotlib.pyplot as plt

EPS = 0.1  # точность
N_MAX = 20  # максимальное число шагов
F = 1.618  # пропорция золотого сечения


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

        x_1 = b - (b - a) / F
        x_2 = a + (b - a) / F

        f_1 = f(x_1)
        f_2 = f(x_2)

        if f_1 > f_2:
            a = x_1
        else:
            b = x_2

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
