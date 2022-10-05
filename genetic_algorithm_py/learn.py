import random
import numpy as np
import json
import matplotlib.pyplot as plt
from deap import base, creator, tools

import env
import elitism
import algorithms
from neuralnet import NNetwork

import pygame

pygame.init()

GAME = False


def get_score(individual):
    network.set_weights(individual)

    car = env.Car()
    road = env.Road()
    reward = env.Reward()

    alive = True
    action_counter = 0
    total_reward = 0
    total_speed = 0

    # pygame
    if GAME:
        clock = pygame.time.Clock()

    while alive and action_counter < 800:
        action_counter += 1
        alive, x, intersection_points = env.get_data(car, road, reward)

        if alive:
            x.append(car.speed)
            x_data = algorithms.normalize_data(x).tolist()

            pred = network.predict(x_data)
            pred_1, pred_2 = algorithms.split_predictions(pred)

            pred_1 = np.argmax(pred_1)
            pred_2 = np.argmax(pred_2)

            env.make_move(car, pred_1, pred_2)

            total_reward = car.total_reward
            total_speed += car.speed

        # pygame
        if GAME:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            sc.fill(BLACK)

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

            if SHOW_REWARD_LINES:
                for i in range(car.reward, len(reward.lines)):
                    pygame.draw.line(sc, WHITE, (reward.lines[i][0], reward.lines[i][1]),
                                     (reward.lines[i][2], reward.lines[i][3]))

            pygame.display.update()
            clock.tick(FPS)

    avg_speed = total_speed / action_counter
    total_reward *= avg_speed
    return total_reward,


def init_individual(icls, content):
    return icls(content)


def init_population(pcls, ind_init, filename):
    with open(filename, "r") as pop_file:
        contents = json.load(pop_file)
    return pcls(ind_init(c) for c in contents)


if __name__ == '__main__':
    NEURONS_IN_LAYERS = [10, 8, 6]

    network = NNetwork(*NEURONS_IN_LAYERS)

    LENGTH_CHROMOSOME = NNetwork.get_total_weights(*NEURONS_IN_LAYERS)
    LOW = -1
    UP = 1
    ETA = 0.5

    POPULATION_SIZE = 40  # количество индивидуумов в популяции
    P_CROSSOVER = 0.9  # вероятность скрещивания
    P_MUTATION = 0.1  # вероятность мутации индивидуума
    MAX_GENERATIONS = 40  # максимальное количество поколений
    HALL_OF_FAME_SIZE = 2

    hof = tools.HallOfFame(HALL_OF_FAME_SIZE)

    RANDOM_SEED = 7
    random.seed(RANDOM_SEED)

    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()

    toolbox.register("randomWeight", random.uniform, LOW, UP)
    toolbox.register("individualCreator", tools.initRepeat, creator.Individual, toolbox.randomWeight, LENGTH_CHROMOSOME)
    toolbox.register("populationCreator", tools.initRepeat, list, toolbox.individualCreator)

    toolbox.register("individual_guess", init_individual, creator.Individual)
    toolbox.register("population_guess", init_population, list, toolbox.individual_guess, "data/population_0.json")

    # не забыть указать путь mix/no mix
    X_TWO = False
    TR = True
    if X_TWO:
        algorithms.import_population()
        population = toolbox.population_guess()

    elif TR:
        population = toolbox.population_guess()

    else:
        population = toolbox.populationCreator(n=POPULATION_SIZE)

    # pygame
    if GAME:
        W, H = 800, 650
        FPS = 10000

        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)

        SHOW_CAR_LINES = False
        SHOW_ROAD_LINES = True
        SHOW_NAVIGATION_POINTS = True
        SHOW_REWARD_LINES = True

        sc = pygame.display.set_mode((W, H))
        pygame.display.set_caption('App')

    toolbox.register("evaluate", get_score)
    toolbox.register("select", tools.selTournament, tournsize=2)
    toolbox.register("mate", tools.cxSimulatedBinaryBounded, low=LOW, up=UP, eta=ETA)
    toolbox.register("mutate", tools.mutPolynomialBounded, low=LOW, up=UP, eta=ETA, indpb=1.0 / LENGTH_CHROMOSOME)

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("max", np.max)
    stats.register("avg", np.mean)

    population, logbook = elitism.ea_simple_elitism(population, toolbox,
                                                    cxpb=P_CROSSOVER,
                                                    mutpb=P_MUTATION,
                                                    ngen=MAX_GENERATIONS,
                                                    halloffame=hof,
                                                    stats=stats,
                                                    verbose=True)

    maxFitnessValues, meanFitnessValues = logbook.select("max", "avg")

    with open('data/hof[0].json', 'w') as file:
        file.write(json.dumps((hof[0])))

    with open('data/hof[1].json', 'w') as file:
        file.write(json.dumps((hof[1])))

    with open('data/population.json', 'w') as file:
        file.write(json.dumps(population))

    with open('data/logbook.json', 'w') as file:
        file.write(json.dumps(logbook))

    plt.plot(maxFitnessValues, color='red')
    plt.plot(meanFitnessValues, color='green')
    plt.xlabel('Поколение')
    plt.ylabel('Макс/средняя приспособленность')
    plt.title('Зависимость приспособленности от поколения')

    plt.savefig('data/plt.png')

    plt.show()
