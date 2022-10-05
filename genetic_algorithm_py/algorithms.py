import numpy as np
import json


def ccw(a, b, c):
    return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])


def intersect(a, b, c, d):
    return ccw(a, c, d) != ccw(b, c, d) and ccw(a, b, c) != ccw(a, b, d)


def perpendicular(a):
    b = np.empty_like(a)
    b[0] = -a[1]
    b[1] = a[0]
    return b


def seg_intersect(a1, a2, b1, b2):
    da = a2 - a1
    db = b2 - b1
    dp = a1 - b1
    dap = perpendicular(da)
    d = np.dot(dap, db)
    num = np.dot(dap, dp)
    return (num / d.astype(float)) * db + b1


def normalize_data(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))


def softmax(x):
    return np.exp(x) / np.sum(np.exp(x), axis=0)


def split_predictions(x):
    pred_1 = softmax(x[:3])
    pred_2 = softmax(x[3:])
    return pred_1, pred_2


def import_population():
    with open('data/population_0.json') as file:
        lst_1 = json.load(file)
    with open('data/population_1.json') as file:
        lst_2 = json.load(file)

    lst = lst_1[:25] + lst_2[25:]
    print(len(lst), len(lst[0]))

    with open('data/population_mix.json', 'w') as file:
        file.write(json.dumps(lst))
