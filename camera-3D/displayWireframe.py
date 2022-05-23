import math
import time
import wireframe as wf
import pygame
import numpy as np
from matrix import translationMatrix
from pprint import pprint

key_to_function = {
    pygame.K_LEFT: (lambda x: x.translateAll([10, 0, 0])),
    pygame.K_RIGHT: (lambda x: x.translateAll([-10, 0, 0])),
    pygame.K_DOWN: (lambda x: x.translateAll([0, -10, 0])),
    pygame.K_UP: (lambda x: x.translateAll([0, 10, 0])),
    pygame.K_k: (lambda x: x.translateAll([0, 0, 10])),
    pygame.K_l: (lambda x: x.translateAll([0, 0, -10])),

    pygame.K_EQUALS: (lambda x: x.scaleAll(1.5)),
    pygame.K_MINUS: (lambda x: x.scaleAll(1 / 1.5)),
    pygame.K_q: (lambda x: x.rotateAll('X', 0.05)),
    pygame.K_w: (lambda x: x.rotateAll('X', -0.05)),
    pygame.K_a: (lambda x: x.rotateAll('Y', -0.05)),
    pygame.K_s: (lambda x: x.rotateAll('Y', 0.05)),
    pygame.K_z: (lambda x: x.rotateAll('Z', 0.05)),
    pygame.K_x: (lambda x: x.rotateAll('Z', -0.05))}


class ProjectionViewer:
    """ Displays 3D objects on a Pygame screen """

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Wireframe Display')

        pygame.font.init()  # you have to call this at the start,
        # if you want to use this module.
        self.font_size = 24
        self.my_font = pygame.font.SysFont('Comic Sans MS', self.font_size)
        self.texts = [self.my_font.render(x, False, (200, 0, 0)) for x in
                      ['l k move forward backward', 'q w rotate X-axis', 'a s rotate Y-axis', 'z x rotate Z-axis']]

        self.background = (10, 10, 50)
        self.d = 500
        self.wireframes = {}
        self.displayNodes = True
        self.displayEdges = True
        self.displayWalls = True
        self.nodeColour = (255, 255, 255)
        self.edgeColour = (200, 200, 200)
        self.wallColours = [(0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255),
                            (255, 0, 255), (0, 128, 128), (128, 0, 128)]

        self.nodeRadius = 4
        self.zoom = 1

    def addWireframe(self, name, wireframe):
        """ Add a named wireframe object. """

        self.wireframes[name] = wireframe

    def run(self):
        """ Create a pygame screen until it is closed. """

        running = True
        while running:
            start =time.time()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in key_to_function:
                        key_to_function[event.key](self)

                        # print(self.wireframes['cube'].nodes)
            self.display()
            # for i, text in enumerate(self.texts):
            #     self.screen.blit(text, (0, self.font_size * i))

            pygame.display.flip()
            # print('time display', time.time() -start)

    def display(self):
        """ Draw the wireframes on the screen. """

        self.screen.fill(self.background)
        self.displayEdges = False
        self.displayNodes = False
        self.displayWalls = True

        for wireframe in self.wireframes.values():
            for i, node in enumerate(wireframe.nodes):
                if node[2] > 0:
                    point_x = int(node[0] * self.d / node[2]) + self.width / 2
                    point_y = int(node[1] * self.d / node[2]) + self.height / 2
                else:
                    point_x = int(node[0] * self.d) + self.width / 2
                    point_y = int(node[1] * self.d) + self.height / 2

                point_x,point_y = self.set_max_x_y_values(point_x,point_y)

                wireframe.nodes_2d_throw[i] = (point_x, point_y)

                if self.displayNodes:
                    pygame.draw.circle(self.screen, self.nodeColour, (point_x, point_y), self.nodeRadius, 0)

            if self.displayEdges:
                for n1, n2 in wireframe.edges:
                    pygame.draw.aaline(self.screen, self.edgeColour, wireframe.nodes_2d_throw[n1][:2],
                                       wireframe.nodes_2d_throw[n2][:2], 1)

                    self.screen.blit(self.my_font.render(str(n1), False, (200, 0, 0)),
                                     (wireframe.nodes_2d_throw[n1][:2]))
                    self.screen.blit(self.my_font.render(str(n2), False, (200, 0, 0)),
                                     (wireframe.nodes_2d_throw[n2][:2]))

            if self.displayWalls:
                # new = time.time()
                displays_walls = 0
                for id_color, wall in enumerate(wireframe.walls):
                    if self.check_to_display_wall( wireframe.walls_z[id_color],wireframe.nodes_2d_throw[wall]):
                        displays_walls +=1
                        pygame.draw.polygon(self.screen, wireframe.walls_colors[id_color],
                                                wireframe.nodes_2d_throw[wall])
                # print(time.time() - new, displays_walls)

                # pygame.draw.polygon(self.screen, self.wallColour,
                #                     [wireframe.nodes_2d_throw[i][:2] for i in wall])
        pygame.draw.circle(self.screen, (255, 255, 255), (self.width / 2, self.height / 2), self.nodeRadius, 0)


    def check_to_display_wall(self,wall_z, nodes_2d):
        if np.all(wall_z < 0):
            return False
        if np.all(nodes_2d[:, 0] > self.width) or np.all(nodes_2d[:, 0] < 0):
            return False
        elif np.all(nodes_2d[:, 1] > self.height) or np.all(nodes_2d[:, 1] < 0):
            return False
        return True

    def set_max_x_y_values(self,point_x,point_y):
        if point_x > self.width * 2:
            point_x = self.width * 2
        elif point_x < -self.width :
            point_x = -self.width

        if point_y > self.height * 2:
            point_y = self.height *2
        elif point_y < -self.height:
            point_y = -self.height
        return point_x,point_y

    def translateAll(self, vector):
        matrix = translationMatrix(*vector)

        for wireframe in self.wireframes.values():
            wireframe.transform(matrix)

    def scaleAll(self, scale):
        self.d *= scale

    def rotateAll(self, axis, theta):
        rotateFunction = 'rotate' + axis

        for wireframe in self.wireframes.values():
            getattr(wireframe, rotateFunction)(theta)


if __name__ == '__main__':
    height = 1920 / 2
    width = 1080 / 2

    pv = ProjectionViewer(height, width)
    cube = wf.Wireframe()
    cube_nodes = [(x, y, z) for x in (50, 250) for y in (50, 250) for z in (50, 250)]
    cube_nodes.extend([(-x, y, z) for x in (50, 250) for y in (50, 250) for z in (50, 250)])
    cube.addNodes(np.array(cube_nodes))

    cube.addEdges(
        [(n, n + 4) for n in range(0, 4)] + [(n, n + 1) for n in range(0, 8, 2)] + [(n, n + 2) for n in (0, 1, 4, 5)]

    )

    walls_0 = np.array([[0, 2, 6, 4],  # PRZEDNIA
             [3, 1, 5, 7],  # TYLNIA

             [2, 6, 7, 3],  # DOLNA
             [0, 4, 5, 1],  # gORNA

             [1, 3, 2, 0],  # LEWA
             [6, 7, 5, 4]  # PRAWA
             ])
    walls_1 = walls_0 + 8
    walls = np.vstack( (walls_0,walls_1))

    cube.add_walls(
        # [[0, 2, 6, 4],  # PRZEDNIA
        #  [3, 1, 5, 7],  # TYLNIA
        #
        #  [2, 6, 7, 3],  # DOLNA
        #  [0, 4, 5, 1],  # gORNA
        #
        #  [1, 3, 2, 0],  # LEWA
        #  [6, 7, 5, 4]  # PRAWA
        #
        #  ],
        walls,
        # colors=[(255, 0, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255)]
        colors = [ (x,z,y) for x in (0,125, 250) for y in (125, 250) for z in (0, 250)]

    )

    pv.addWireframe(f'cube', cube)

    pv.run()

