import numpy as np
import numpy.linalg as ln
import scipy as sp
import scipy.optimize

EPS = 10e-3
N_MAX = None


def f(x):
    return (x[0] ** 2 + x[1] - 11) ** 2 + (x[0] + x[1] ** 2 - 7) ** 2


def grad(x):
    ddx = 2 * (2 * x[0] * (x[0] ** 2 + x[1] - 11) + x[0] + x[1] ** 2 - 7)
    ddy = 2 * (x[0] ** 2 + 2 * x[1] * (x[0] + x[1] ** 2 - 7) + x[1] - 11)
    return np.array([ddx, ddy])


def main():
    x0 = np.array([0, 0])

    global N_MAX
    if N_MAX is None:
        N_MAX = len(x0) * 200

    k = 0
    gfk = grad(x0)
    n = len(x0)
    I = np.eye(n, dtype=int)
    hk = I
    xk = x0

    while ln.norm(gfk) > EPS and k < N_MAX:
        pk = -np.dot(hk, gfk)

        line_search = sp.optimize.line_search(f, grad, xk, pk)
        alpha_k = line_search[0]

        xkp1 = xk + alpha_k * pk
        sk = xkp1 - xk
        xk = xkp1

        gfkp1 = grad(xkp1)
        yk = gfkp1 - gfk
        gfk = gfkp1

        k += 1

        ro = 1.0 / (np.dot(yk, sk))
        a1 = I - ro * sk[:, np.newaxis] * yk[np.newaxis, :]
        a2 = I - ro * yk[:, np.newaxis] * sk[np.newaxis, :]
        hk = np.dot(a1, np.dot(hk, a2)) + (ro * sk[:, np.newaxis] *
                                           sk[np.newaxis, :])

        print('(%.3f, %.3f)' % (xk[0], xk[1]))

    print('Число шагов:', k)
    print('Минимум: (%.3f, %.3f) = %.3f' % (xk[0], xk[1], f(xk)))


if __name__ == "__main__":
    main()
