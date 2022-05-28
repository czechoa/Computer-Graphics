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
pygame.display.set_caption('Wireframe Display')

pygame.font.init()  # you have to call this at the start,
# if you want to use this module.


# OBSERVER = np.array([200, 200, 0])
# CENTER = np.array([200, 200, 200])
# SOURCE = np.array([400, 400, 0])
OBSERVER = (200, 200, 0)
CENTER = (200, 200, 200)
SOURCE = (400, 400, 0)

RADIUS = 100


def draw_cycle(x, y):
    if x > CENTER[0] + RADIUS or x < CENTER[0] - RADIUS:
        return False
    elif y > CENTER[1] + RADIUS or y < CENTER[1] - RADIUS:
        return False
    return True


def z_coord(x, y):
    # a = 1 so it can be skipped
    # if not draw_cycle(x,y):
    #     return False
    b = -2 * CENTER[2]
    # (x - CENTER[0])**2 + (y - CENTER[1])**2  + z**2  - 2*z_0* *z + z_)**2

    c = CENTER[2] ** 2 + (x - CENTER[0]) ** 2 + (y - CENTER[1]) ** 2 - RADIUS ** 2

    delta = b ** 2 - 4 * c
    if delta == 0:
        return -b / 2
    elif delta > 0:
        z1 = (-b - math.sqrt(delta)) / 2
        # z2 = (-b + math.sqrt(delta)) / 2
        return z1


def z_coord_vectoring():
    # a = 1 so it can be skipped
    # if not draw_cycle(x,y):
    #     return False
    points = np.array(list(itertools.product(range(WIDTH), range(HEIGHT))))
    x = points[:,0]
    y = points[:, 1]

    z_coord = np.zeros(len(x))

    b = -2 * CENTER[2]
    # (x - CENTER[0])**2 + (y - CENTER[1])**2  + z**2  - 2*z_0* *z + z_)**2

    c = CENTER[2] ** 2 + (x - CENTER[0]) ** 2 + (y - CENTER[1]) ** 2 - RADIUS ** 2
    delta = b ** 2 - 4 * c

    index_delta_0 = np.where(delta == 0)
    z_coord[index_delta_0] = -b / 2

    index_delta_bigger_0 = np.where(delta > 0)
    delta_sqrt = np.sqrt(delta[index_delta_bigger_0])
    z1 = (-b - delta_sqrt) / 2
    # z2 = (-b + delta_sqrt) / 2

    z_coord[index_delta_bigger_0] = z1

    # z2 = (-b + delta_sqrt) / 2
    # z_coord[index_delta_bigger_0] = np.min(np.vstack((z1, z2)), axis=0)
    return np.vstack( (x,y, z_coord)).T.astype(int)

def vector(start_point, end_point):
    return np.array([end_point[0] - start_point[0],
                     end_point[1] - start_point[1],
                     end_point[2] - start_point[2]])


def norm(vector: np.array):
    return math.sqrt(sum(vector ** 2))


def versor(vector):
    n = norm(vector)
    # n = np.linalg.norm(vector)
    return vector / n




def illumination(point):
    #
    IA = 1
    KA = 0.05  # otoczenia

    IP = 1
    KD = 0.5  # rozproszonego

    KS = 0.5  # odbitego
    N = 5

    n = versor(vector(CENTER, point))
    # n = versor(CENTER - point)

    l = versor(vector(point, SOURCE))
    # l = versor( point - SOURCE)

    v = versor(vector(point, OBSERVER))
    # v = versor( point - OBSERVER)

    r = versor(subtract(multiply(multiply(n, 2), multiply(n, l)), l))
    # r = versor( ( n * 2 * n * l) -  l)

    return IA * KA + IP * (KD * max(dot(n, l), 0) + KS * max(dot(r, v), 0) ** N)


def render():
    start = time.time()
    for  x, y, z  in z_coord_vectoring():
        # print(x,y,z)
        if  z !=0:
            intensity = min(  int(illumination([x, y, z]) * 255 ), 255)
            # print(intensity)
            color = multiply(intensity,(0,0,1))
            # print(color)
            # image.put('#{0:02x}{0:02x}{0:02x}'.format(intensity), coords)
            pygame.draw.circle(screen, color,  (x,HEIGHT - y), 1, 0)

    print(time.time() - start)




def move(step, coord):
    global SOURCE
    SOURCE = list(SOURCE)
    SOURCE[coord] += step
    SOURCE = tuple(SOURCE)


key_to_function = {
    pygame.K_q: lambda: move(MOVE_STEP, 1),
    pygame.K_e: lambda: move(-MOVE_STEP, 1),
    pygame.K_a: lambda: move(-MOVE_STEP, 0),
    pygame.K_d: lambda: move(MOVE_STEP, 0),
    pygame.K_w: lambda: move(MOVE_STEP, 2),
    pygame.K_s: lambda: move(-MOVE_STEP, 2)
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
