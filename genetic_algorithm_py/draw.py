import json

import pygame

pygame.init()

if __name__ == '__main__':
    W, H = 800, 650
    FPS = 60

    WHITE = (255, 255, 255)

    sc = pygame.display.set_mode((W, H))
    pygame.display.set_caption('App')

    clock = pygame.time.Clock()

    points_1 = []
    lines_1 = []
    points_2 = []
    lines_2 = []
    car = (0, 0)

    ext = False
    dot = False
    running = True

    all_lines = []
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                point = pygame.mouse.get_pos()

                if not ext and not dot:
                    if points_1:
                        line = points_1[-1][0], points_1[-1][1], point[0], point[1]
                        lines_1.append(list(line))

                    points_1.append(point)

                if not dot and ext:
                    if points_2:
                        line = points_2[-1][0], points_2[-1][1], point[0], point[1]
                        lines_2.append(list(line))

                    points_2.append(point)

                if dot:
                    car = point
                    running = False
                    pygame.quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if not dot and ext:
                        line = points_2[-1][0], points_2[-1][1], points_2[0][0], points_2[0][1]
                        lines_2.append(list(line))
                        dot = True

                    if not ext and not dot:
                        line = points_1[-1][0], points_1[-1][1], points_1[0][0], points_1[0][1]
                        lines_1.append(list(line))
                        ext = True

        all_lines = lines_1 + lines_2

        if running:
            for i in range(len(all_lines)):
                pygame.draw.line(sc, WHITE, (all_lines[i][0], all_lines[i][1]), (all_lines[i][2], all_lines[i][3]))

            pygame.display.update()
            clock.tick(FPS)

    with open('data/road.json', 'w') as file:
        file.write(json.dumps(all_lines))

    with open('data/car.json', 'w') as file:
        file.write(json.dumps(car))
