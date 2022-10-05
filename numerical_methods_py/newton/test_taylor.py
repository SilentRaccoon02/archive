import math
from taylor import sin, cos


def test_sin():
    print('__sin__')

    x = -10 + 0.1
    while x < 10 - 0.1:
        value = sin(x, 0.001)
        exact = math.sin(x)
        print('sign', value < 0 and exact < 0 or value > 0 and exact > 0, 'accuracy %.4f' % (value - exact))

        x += 0.1


def test_cos():
    print('__cos__')

    x = -10 + 0.1
    while x < 10 - 0.1:
        value = cos(x, 0.001)
        exact = math.cos(x)
        print('sign', value < 0 and exact < 0 or value > 0 and exact > 0, 'accuracy %.4f' % (value - exact))

        x += 0.1


if __name__ == '__main__':
    test_sin()
    test_cos()
