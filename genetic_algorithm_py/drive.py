import numpy as np
import json

import env
import algorithms
from neuralnet import NNetwork

import pygame

pygame.init()

if __name__ == '__main__':
    W, H = 800, 650
    FPS = 60

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)

    SHOW_CAR_LINES = False
    SHOW_ROAD_LINES = True
    SHOW_NAVIGATION_POINTS = False

    IMPORT_ROAD = False

    sc = pygame.display.set_mode((W, H))
    pygame.display.set_caption('App')

    with open('data/best.json') as file:
        individual = json.load(file)

    NEURONS_IN_LAYERS = [10, 8, 6]
    network = NNetwork(*NEURONS_IN_LAYERS)
    network.set_weights(individual)

    clock = pygame.time.Clock()

    if IMPORT_ROAD:
        car = env.Car(from_file=True)
        road = env.Road(from_file=True)

    else:
        car = env.Car()
        road = env.Road()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        intersection = False
        for i in range(len(road.lines)):
            line_1 = algorithms.intersect(road.lines[i][:2], road.lines[i][2:], car.A, car.B)
            line_2 = algorithms.intersect(road.lines[i][:2], road.lines[i][2:], car.B, car.C)
            line_3 = algorithms.intersect(road.lines[i][:2], road.lines[i][2:], car.C, car.D)
            line_4 = algorithms.intersect(road.lines[i][:2], road.lines[i][2:], car.D, car.A)

            if line_1 or line_2 or line_3 or line_4:
                intersection = True

        intersection_points = []
        intersection_distance = []
        for i in range(len(car.lines)):
            check = False
            for j in range(len(road.lines)):
                point_1 = np.array(road.lines[j][:2])
                point_2 = np.array(road.lines[j][2:])
                point_3 = np.array(car.lines[i][:2])
                point_4 = np.array(car.lines[i][2:])

                if algorithms.intersect(point_1, point_2, point_3, point_4):
                    point = algorithms.seg_intersect(point_1, point_2, point_3, point_4)
                    a = pygame.Vector2(point_3[:1], point_3[1:])
                    b = pygame.Vector2(point[:1], point[1:])
                    distance = a.distance_to(b)

                    if check:
                        if distance < intersection_distance[-1]:
                            intersection_points[-1] = point
                            intersection_distance[-1] = distance
                    else:
                        intersection_points.append(point)
                        intersection_distance.append(distance)
                        check = True

            if not check:
                intersection_points.append([1000, 1000])
                intersection_distance.append(200)

        x = intersection_distance
        x.append(car.speed)
        x_data = algorithms.normalize_data(x).tolist()

        pred = network.predict(x_data)
        pred_1, pred_2 = algorithms.split_predictions(pred)

        pred_1 = np.argmax(pred_1)
        pred_2 = np.argmax(pred_2)

        env.make_move(car, pred_1, pred_2)

        sc.fill(BLACK)

        if intersection:
            pygame.draw.polygon(sc, RED, [car.A, car.B, car.C, car.D])
        else:
            pygame.draw.polygon(sc, WHITE, [car.A, car.B, car.C, car.D])

        if SHOW_NAVIGATION_POINTS and intersection_points:
            for i in range(len(intersection_points)):
                pygame.draw.circle(sc, WHITE, intersection_points[i], 5)

        if SHOW_CAR_LINES:
            for i in range(len(car.lines)):
                pygame.draw.line(sc, WHITE, (car.lines[i][0], car.lines[i][1]),
                                 (car.lines[i][2], car.lines[i][3]))

        if SHOW_ROAD_LINES:
            for i in range(len(road.lines)):
                pygame.draw.line(sc, WHITE, (road.lines[i][0], road.lines[i][1]),
                                 (road.lines[i][2], road.lines[i][3]), 2)

        pygame.display.update()
        clock.tick(FPS)
