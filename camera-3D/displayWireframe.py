import math

import wireframe as wf
import pygame
import numpy as np
from pprint import pprint

key_to_function = {
    # pygame.K_LEFT:   (lambda x: x.translateAll('x', -10)),
    # pygame.K_RIGHT:  (lambda x: x.translateAll('x',  10)),
    # pygame.K_DOWN:   (lambda x: x.translateAll('y',  10)),
    # pygame.K_UP:     (lambda x: x.translateAll('y', -10)),

    pygame.K_LEFT: (lambda x: x.translateAll([10, 0, 0])),
    pygame.K_RIGHT: (lambda x: x.translateAll([-10, 0, 0])),
    pygame.K_DOWN: (lambda x: x.translateAll([0, -10, 0])),
    pygame.K_UP: (lambda x: x.translateAll([0, 10, 0])),
    pygame.K_k: (lambda x: x.translateAll([0, 0, 10])),
    pygame.K_l: (lambda x: x.translateAll([0, 0, -10])),

    pygame.K_EQUALS: (lambda x: x.scaleAll(1.5)),
    pygame.K_MINUS: (lambda x: x.scaleAll(1/1.5)),
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
        self.texts = [self.my_font.render(x,False, (200, 0, 0)) for x in ['l k move forward backward','q w rotate X-axis','a s rotate Y-axis','z x rotate Z-axis']]


        self.background = (10, 10, 50)
        self.d = 500
        self.wireframes = {}
        self.displayNodes = True
        self.displayEdges = True
        self.nodeColour = (255, 255, 255)
        self.edgeColour = (200, 200, 200)
        self.nodeRadius = 4
        self.zoom = 1

    def addWireframe(self, name, wireframe):
        """ Add a named wireframe object. """

        self.wireframes[name] = wireframe

    def run(self):
        """ Create a pygame screen until it is closed. """

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in key_to_function:
                        key_to_function[event.key](self)
                        # print(self.wireframes['cube'].nodes)

            self.display()
            for i,text in enumerate(self.texts):
                self.screen.blit(text, (0, self.font_size *i))

            pygame.display.flip()

    def display(self):
        """ Draw the wireframes on the screen. """

        self.screen.fill(self.background)
        self.displayEdges = True
        for wireframe in self.wireframes.values():

            if self.displayNodes:
                for i,node in enumerate(wireframe.nodes):
                    # pygame.draw.circle(self.screen, self.nodeColour, (int(node[0]), int(node[1])), self.nodeRadius, 0)
                    if node[2] > 0:
                        point_x = (int(node[0] * self.d) / (node[2])*self.zoom +self.width/2)
                        point_y = (int(node[1] * self.d) / (node[2] )*self.zoom + self.height/2)
                        wireframe.nodes_2d_throw[i] = (point_x,point_y)
                        pygame.draw.circle(self.screen, self.nodeColour, (point_x,point_y)  , self.nodeRadius, 0)

                # matrix = wf.translationMatrix(*[self.width/2,self.height/2,0])
                # wireframe.transform_throw(matrix)
                if self.displayEdges:
                    for n1, n2 in wireframe.edges:
                        pygame.draw.aaline(self.screen, self.edgeColour, wireframe.nodes_2d_throw[n1][:2], wireframe.nodes_2d_throw[n2][:2],
                                           1)

    def translateAll(self, vector):
        matrix = wf.translationMatrix(*vector)

        for wireframe in self.wireframes.values():
            wireframe.transform(matrix)

    def scaleAll(self, scale):
        if scale > 1:
            self.zoom *= scale
        else:
            if self.zoom !=1:
                self.zoom *= scale

    def rotateAll(self, axis, theta):
        rotateFunction = 'rotate' + axis

        for wireframe in self.wireframes.values():
            # centre = wireframe.findCentre()
            getattr(wireframe, rotateFunction)(theta)
            # self.translateAll([self.width/2,self.height/2,0])

if __name__ == '__main__':
    height = 1920 / 2
    width = 1080 / 2

    pv = ProjectionViewer(height, width )
    for i  in range(1,6):
        cube = wf.Wireframe()

        modulo_i = i%2
        if i == 5:
            cube_nodes = [(x-200, y, z + 300 * 3) for x in (50, 250) for y in (50, 250) for z in (50, 250)]
        elif i %2 == 0:
            cube_nodes = [(x, y, z + 300 * i/2) for x in (50, 250) for y in (50, 250) for z in (50, 250)]
        else:
            cube_nodes = [(x-400, y, z + 300 * math.ceil(i/2)) for x in (50, 250) for y in (50, 250) for z in (50, 250)]

        cube.addNodes(np.array(cube_nodes))

        cube.addEdges(
            [(n, n + 4) for n in range(0, 4)] + [(n, n + 1) for n in range(0, 8, 2)] + [(n, n + 2) for n in (0, 1, 4, 5)])

        pv.addWireframe(f'cube_{i}', cube)


    pv.run()
