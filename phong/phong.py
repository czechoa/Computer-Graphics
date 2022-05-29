import math
import time
import tkinter
import itertools

import numpy as np
import pygame
from numpy import multiply, subtract, dot

WIDTH = 400
HEIGHT = 400
MOVE_STEP = 100

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Phong')

pygame.font.init()  # you have to call this at the start,

OBSERVER = np.array([200, 200, 0])
CENTER = np.array([200, 200, 200])
SOURCE = np.array([200, 200, 0])
# OBSERVER = (200, 200, 0)
# CENTER = (200, 200, 200)
# SOURCE = (400, 400, 0)

RADIUS = 100
Parametrs = {
    'IA': 1,
    'KA': 0.05,  # otoczenia
    'IP': 1,
    'KD': 0.5,  # rozproszonego
    'KS': 0.5,  # odbitego
    'N': 5
}
basic_color = [0, 0, 1]


def z_coord_vectoring():
    # a = 1 so it can be skipped
    # if not draw_cycle(x,y):
    #     return False
    points = np.array(list(itertools.product(range(WIDTH), range(HEIGHT))))
    x = points[:, 0]
    y = points[:, 1]

    z_coord = np.zeros(len(x))

    b = -2 * CENTER[2]
    # (x - CENTER[0])**2 + (y - CENTER[1])**2  + z**2  - 2*z_0* *z + z_)**2

    c = CENTER[2] ** 2 + (x - CENTER[0]) ** 2 + (y - CENTER[1]) ** 2 - RADIUS ** 2
    delta = b ** 2 - 4 * c

    # index_delta_0 = np.where(delta == 0)
    # z_coord[index_delta_0] = -b / 2

    index_delta_bigger_0 = np.where(delta >= 0)
    delta_sqrt = np.sqrt(delta[index_delta_bigger_0])
    z1 = (-b - delta_sqrt) / 2
    # z2 = (-b + delta_sqrt) / 2

    z_coord[index_delta_bigger_0] = z1

    return np.vstack((x[index_delta_bigger_0], y[index_delta_bigger_0], z_coord[index_delta_bigger_0])).T.astype(int)


def vector(start_point, end_point):
    return np.array([end_point[0] - start_point[0],
                     end_point[1] - start_point[1],
                     end_point[2] - start_point[2]])


def norm(vector: np.array):
    return np.sqrt(np.sum(vector ** 2, axis=1))


def versor(vector):
    n = norm(vector)
    return vector / n.reshape(-1, 1)


def illumination(point):
    n = versor(CENTER - point)
    l = versor(point - SOURCE)
    v = versor(point - OBSERVER)

    r = versor((n * 2 * n * l) - l)

    n_l = np.max(np.vstack((np.sum(np.multiply(n, l), axis=1), np.zeros(len(n)))), axis=0)

    r_v = np.max(np.vstack((np.sum(np.multiply(r, v), axis=1), np.zeros(len(n)))), axis=0)

    return Parametrs['IA'] * Parametrs['KA'] + Parametrs['IP'] * (
                Parametrs['KD'] * n_l + Parametrs['KS'] * r_v ** Parametrs['N'])


def render():
    start = time.time()
    # print(x,y,z)
    points = z_coord_vectoring()

    intensity = np.min(np.vstack((illumination(points) * 255, np.ones((len(points))) * 255)), axis=0)
    # print(intensity)

    color = (intensity * np.array([0, 0, 1]).reshape(3, 1)).T
    for i, point in enumerate(points):
        pygame.draw.circle(screen, color[i], (point[0], HEIGHT - point[1]), 1, 0)

    print(time.time() - start, SOURCE, Parametrs)


def move(step, coord):
    global SOURCE
    # SOURCE = list(SOURCE)
    SOURCE[coord] += step
    # SOURCE = tuple(SOURCE)


def update_parameters(pametr, step):
    Parametrs[pametr] *= step
    if Parametrs[pametr] < 0:
        Parametrs[pametr] = 0
    elif pametr !='N' and Parametrs[pametr] > 1:
        Parametrs[pametr] = 1



key_to_function = {
    pygame.K_q: lambda: move(MOVE_STEP, 1),
    pygame.K_e: lambda: move(-MOVE_STEP, 1),
    pygame.K_a: lambda: move(-MOVE_STEP, 0),
    pygame.K_d: lambda: move(MOVE_STEP, 0),
    pygame.K_w: lambda: move(MOVE_STEP, 2),
    pygame.K_s: lambda: move(-MOVE_STEP, 2),
    pygame.K_n: lambda: update_parameters('N',2),
    pygame.K_m: lambda: update_parameters('N', 1/2),
    pygame.K_k: lambda: update_parameters('KA', 1.25),
    pygame.K_l: lambda: update_parameters('KA', 0.75),
    pygame.K_o: lambda: update_parameters('KD', 1.25),
    pygame.K_p: lambda: update_parameters('KD', 0.75),
    pygame.K_u: lambda: update_parameters('KS', 1.25),
    pygame.K_i: lambda: update_parameters('KS', 0.75),
}

running = True
render()
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key in key_to_function:
                key_to_function[event.key]()
                render()
    # for i, text in enumerate(self.texts):
    #     self.screen.blit(text, (0, self.font_size * i))

    pygame.display.flip()
