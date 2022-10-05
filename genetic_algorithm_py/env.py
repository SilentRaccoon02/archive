import math
import numpy as np
import json

import algorithms

import pygame

pygame.init()


class Car:
    def __init__(self, x=75, y=375, from_file=False):
        if from_file:
            with open('data/car.json', 'r') as file:
                lst = json.load(file)

            self.x = lst[0]
            self.y = lst[1]

        else:
            self.x = x
            self.y = y

        self.A = [self.x - 10, self.y - 20]
        self.B = [self.x + 10, self.y - 20]
        self.C = [self.x + 10, self.y + 20]
        self.D = [self.x - 10, self.y + 20]

        self.speed = 0
        self.angle = 0
        self.angle_speed = math.pi / 80

        self.reward = 0
        self.total_reward = 0

        length = 400
        angle_1 = 7 * math.pi / 16
        angle_2 = math.pi / 4

        x_ang_1 = self.calc_x(angle_1, length)
        x_ang_2 = self.calc_x(angle_2, length)
        y_ang_1 = self.calc_y(angle_1, length)
        y_ang_2 = self.calc_y(angle_2, length)

        self.lines = [[self.x, self.y - 20, self.x, self.y - (length + 20)],
                      [self.x - 10, self.y - 20, self.x - (x_ang_1 + 10), self.y - (y_ang_1 + 20)],
                      [self.x + 10, self.y - 20, self.x + (x_ang_1 + 10), self.y - (y_ang_1 + 20)],
                      [self.x - 10, self.y - 20, self.x - (x_ang_2 + 10), self.y - (y_ang_2 + 20)],
                      [self.x + 10, self.y - 20, self.x + (x_ang_2 + 10), self.y - (y_ang_2 + 20)],
                      [self.x - 10, self.y - 20, self.x - (length / 2 + 10), self.y - 20],
                      [self.x + 10, self.y - 20, self.x + (length / 2 + 10), self.y - 20],
                      [self.x - 10, self.y + 20, self.x - (length / 2 + 10), self.y + 20],
                      [self.x + 10, self.y + 20, self.x + (length / 2 + 10), self.y + 20]]

    @staticmethod
    def calc_x(angle, length):
        return math.cos(angle) * length

    @staticmethod
    def calc_y(angle, length):
        return math.sin(angle) * length

    def rotate_point(self, point, angle):
        s = math.sin(angle)
        c = math.cos(angle)

        temp_x = point[0] - self.x
        temp_y = point[1] - self.y

        point[0] = self.x + c * temp_x - s * temp_y
        point[1] = self.y + s * temp_x + c * temp_y

        return point

    def rotate_car(self, direction):
        angle = direction * self.angle_speed
        self.angle += angle

        self.A = self.rotate_point(self.A, angle)
        self.B = self.rotate_point(self.B, angle)
        self.C = self.rotate_point(self.C, angle)
        self.D = self.rotate_point(self.D, angle)

        for i in range(len(self.lines)):
            self.lines[i][:2] = self.rotate_point(self.lines[i][:2], angle)
            self.lines[i][2:] = self.rotate_point(self.lines[i][2:], angle)

    @staticmethod
    def move_point(point, x, y):
        point[0] += x
        point[1] += y

        return point

    def move_car(self):
        x = math.cos(self.angle - math.pi / 2) * self.speed
        y = math.sin(self.angle - math.pi / 2) * self.speed

        self.x += x
        self.y += y

        self.A = self.move_point(self.A, x, y)
        self.B = self.move_point(self.B, x, y)
        self.C = self.move_point(self.C, x, y)
        self.D = self.move_point(self.D, x, y)

        for i in range(len(self.lines)):
            self.lines[i][:2] = self.move_point(self.lines[i][:2], x, y)
            self.lines[i][2:] = self.move_point(self.lines[i][2:], x, y)


class Road:
    def __init__(self, from_file=False):
        if from_file:
            with open('data/road.json', 'r') as file:
                lst = json.load(file)

            self.lines = lst

        else:
            self.lines = [[50, 475, 50, 150],
                          [125, 425, 125, 200],
                          [50, 150, 150, 50],
                          [125, 200, 200, 125],
                          [150, 50, 300, 50],
                          [200, 125, 250, 125],
                          [300, 50, 400, 150],
                          [250, 125, 325, 200],
                          [400, 150, 400, 200],
                          [325, 200, 325, 250],
                          [400, 200, 475, 275],
                          [325, 250, 425, 350],
                          [475, 275, 650, 275],
                          [425, 350, 600, 350],
                          [650, 275, 750, 375],
                          [600, 350, 675, 425],
                          [750, 375, 750, 475],
                          [750, 475, 650, 575],
                          [675, 425, 600, 500],
                          [650, 575, 150, 575],
                          [600, 500, 200, 500],
                          [150, 575, 50, 475],
                          [200, 500, 125, 425]]


class Reward:
    def __init__(self):
        self.lines = [[50, 350, 125, 350],
                      [50, 300, 125, 300],
                      [50, 250, 125, 250],
                      [50, 200, 125, 200],
                      [50, 150, 125, 200],
                      [150, 50, 200, 125],
                      [300, 50, 250, 125],
                      [400, 150, 325, 200],
                      [400, 200, 325, 250],
                      [475, 275, 425, 350],
                      [475, 350, 475, 275],
                      [525, 350, 525, 275],
                      [575, 350, 575, 275],
                      [650, 275, 600, 350],
                      [750, 375, 675, 425],
                      [675, 425, 750, 425],
                      [750, 475, 675, 425],
                      [675, 425, 700, 525],
                      [600, 500, 650, 575],
                      [550, 500, 550, 575],
                      [500, 500, 500, 575],
                      [450, 500, 450, 575],
                      [400, 500, 400, 575],
                      [350, 500, 350, 575],
                      [300, 500, 300, 575],
                      [250, 500, 250, 575],
                      [200, 500, 200, 575],
                      [150, 575, 200, 500],
                      [50, 475, 125, 425]]


def get_data(car, road, reward):
    for i in range(len(road.lines)):
        line_1 = algorithms.intersect(road.lines[i][:2], road.lines[i][2:], car.A, car.B)
        line_2 = algorithms.intersect(road.lines[i][:2], road.lines[i][2:], car.B, car.C)
        line_3 = algorithms.intersect(road.lines[i][:2], road.lines[i][2:], car.C, car.D)
        line_4 = algorithms.intersect(road.lines[i][:2], road.lines[i][2:], car.D, car.A)

        if line_1 or line_2 or line_3 or line_4:
            return False, [], []

    if car.reward < len(reward.lines):
        current = car.reward
        line_1 = algorithms.intersect(reward.lines[current][:2], reward.lines[current][2:], car.A, car.B)
        line_2 = algorithms.intersect(reward.lines[current][:2], reward.lines[current][2:], car.B, car.C)
        line_3 = algorithms.intersect(reward.lines[current][:2], reward.lines[current][2:], car.C, car.D)
        line_4 = algorithms.intersect(reward.lines[current][:2], reward.lines[current][2:], car.D, car.A)

        if line_1 or line_2 or line_3 or line_4:
            car.reward += 1
            car.total_reward += 1
            if car.reward == len(reward.lines):
                car.reward = 0

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
            intersection_distance.append(400)

    return True, intersection_distance, intersection_points


def make_move(car, pred_1, pred_2):
    if pred_1 == 1:
        car.rotate_car(1)
    if pred_1 == 2:
        car.rotate_car(-1)

    gas = False
    if pred_2 == 1:
        car.speed += 0.05
        gas = True
    if pred_2 == 2:
        car.speed -= 0.05

    if car.speed and not gas:
        car.speed -= 0.05

    if car.speed > 8:
        car.speed = 8

    if car.speed < 0:
        car.speed = 0

    car.move_car()
