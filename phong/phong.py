import math
import time
import tkinter
import itertools
from sklearn.preprocessing import normalize
import numpy as np
import pygame
from numpy import multiply, subtract, dot

WIDTH = 400
HEIGHT = 400
MOVE_STEP = 100

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Phong')

pygame.font.init()  #

OBSERVER = np.array([200, 200, 0])
CENTER = np.array([200, 200, 200])
SOURCE = np.array([200, 800, -500])

RADIUS = 100
Parametrs = {
    'IA': 1,
    'KA': 0.05,  # otoczenia
    'IP': 1,
    'KD': 0.5,  # rozproszonego
    'KS': 0.5,  # odbitego
    'N': 5
}
basic_color = [1, 1, 1]


def z_coord_vectoring():
    points = np.array(list(itertools.product(range(WIDTH), range(HEIGHT))))
    x = points[:, 0]
    y = points[:, 1]
    z_coord = np.zeros(len(x))

    b = -2 * CENTER[2]
    c = CENTER[2] ** 2 + (x - CENTER[0]) ** 2 + (y - CENTER[1]) ** 2 - RADIUS ** 2
    delta = b ** 2 - 4 * c

    index_delta_bigger_0 = np.where(delta >= 0)
    delta_sqrt = np.sqrt(delta[index_delta_bigger_0])
    z1 = (-b - delta_sqrt) / 2

    z_coord[index_delta_bigger_0] = z1

    return np.vstack((x[index_delta_bigger_0], y[index_delta_bigger_0], z_coord[index_delta_bigger_0])).T.astype(int)


def normalize_matrix(matrix):
    normed_matrix = normalize(matrix, axis=1, norm='l2')
    return normed_matrix


def illumination(point):
    n = normalize_matrix(point - CENTER)
    print(point[-1])
    v = normalize_matrix(OBSERVER - point)

    l = normalize_matrix(SOURCE - point)
    r = normalize_matrix(2 * np.sum(np.multiply(n, l), axis=1).reshape(-1, 1) * n - l)

    n_l = np.max(np.vstack((np.sum(np.multiply(n, l), axis=1), np.zeros(len(n)))), axis=0)

    r_v = np.max(np.vstack((np.sum(np.multiply(r, v), axis=1), np.zeros(len(n)))), axis=0)
    return Parametrs['IA'] * Parametrs['KA'] + Parametrs['IP'] * (
            Parametrs['KD'] * n_l + Parametrs['KS'] * r_v ** Parametrs['N'])


def render():
    start = time.time()
    points = z_coord_vectoring()

    intensity = np.min(np.vstack((illumination(points) * 255, np.ones((len(points))) * 255)), axis=0)

    color = (intensity * np.array(basic_color).reshape(3, 1)).T
    for i, point in enumerate(points):
        pygame.draw.circle(screen, color[i], (point[0], HEIGHT - point[1]), 1, 0)

    print(time.time() - start, SOURCE, Parametrs)


def move(step, coord):
    global SOURCE
    SOURCE[coord] += step


def update_parameters(pametr, step):
    Parametrs[pametr] *= step
    if Parametrs[pametr] < 0:
        Parametrs[pametr] = 0
    elif pametr != 'N' and Parametrs[pametr] > 1:
        Parametrs[pametr] = 1


key_to_function = {
    pygame.K_q: lambda: move(MOVE_STEP, 1),
    pygame.K_e: lambda: move(-MOVE_STEP, 1),
    pygame.K_a: lambda: move(-MOVE_STEP, 0),
    pygame.K_d: lambda: move(MOVE_STEP, 0),
    pygame.K_w: lambda: move(MOVE_STEP, 2),
    pygame.K_s: lambda: move(-MOVE_STEP, 2),
    pygame.K_n: lambda: update_parameters('N', 2),
    pygame.K_m: lambda: update_parameters('N', 1 / 2),
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

    pygame.display.flip()
