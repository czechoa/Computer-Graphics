import numpy as np
from matrix import projection_2d_matrix, normalization_2d_matrix, rotateXMatrix, rotateYMatrix, rotateZMatrix
from equation_of_plane import calculate_equation_of_plane, calculate_points_behind, calculate_points_forward


class Wireframe:
    def __init__(self):
        self.nodes = np.zeros((0, 4))
        self.nodes_2d_throw = np.zeros((0, 2))
        self.edges = []
        self.walls = np.zeros((0, 4))
        self.walls_z = np.zeros((0, 4))
        self.walls_colors = np.zeros((0, 3))

    def addNodes(self, node_array):
        ones_column = np.ones((len(node_array), 1))
        ones_added = np.hstack((node_array, ones_column))
        self.nodes = np.vstack((self.nodes, ones_added))
        self.nodes_2d_throw = self.nodes[:, :2].copy()

    def addEdges(self, edgeList):
        self.edges += edgeList

    def update_wall_z(self):
        self.walls_z = self.nodes[self.walls, 2]

    def add_walls(self, wallList, colors):
        self.walls = np.array(wallList)
        self.update_wall_z()
        self.walls_colors = np.array(colors)

    def painter_algorithm(self):


        self.walls_z = np.sort(self.walls_z, axis=1, kind='stable')
        #
        planes = np.array([calculate_equation_of_plane(*x) for x in self.nodes[self.walls[:, :3]][:, :, :3]], ).reshape(
            (len(self.walls), 4))
        #
        points_behind_wall =  -1*np.array(
            [calculate_points_behind(plane.reshape(1, 4), self.nodes).sum() if calculate_points_forward(plane, np.array(
                (0, 0, 0, 1)))
             else calculate_points_forward(plane.reshape(1, 4), self.nodes).sum() for plane in planes])


        #
        # check_calculate_equation_of_plane(planes, self.nodes)
        #
        to_sort = np.hstack((self.walls_z, points_behind_wall.reshape(-1, 1)))
        # to_sort = self.walls_z

        sorted_index = np.lexsort([to_sort[:, -i] for i in reversed(range(1, to_sort.shape[1] + 1))])[::-1]
        #
        self.order_walls(sorted_index)
        self.bubble_sort(points_behind_wall[sorted_index])

    def order_walls(self, sorted_index):
        self.walls = self.walls[sorted_index]
        self.walls_z = self.walls_z[sorted_index]
        self.walls_colors = self.walls_colors[sorted_index]

    def outputNodes(self):

        for i in range(self.nodes.shape[0]):
            x, y, z, _ = self.nodes[i]
            print("Node %d: (%.3f, %.3f, %.3f)" % (i, x, y, z))

    def outputEdges(self):
        for i, (start, stop) in enumerate(self.edges):
            node1 = self.nodes[start]
            node2 = self.nodes[stop]
            print("Edge %d: (%.3f, %.3f, %.3f)" % (i, node1[0], node1[1], node1[2]))
            print("to (%.3f, %.3f, %.3f)" % (node2[0], node2[1], node2[2]))

    def projection_2d(self, d):
        mrp2 = projection_2d_matrix(d)
        vector_2d = np.dot(self.nodes, mrp2)

        normalization_matrix = normalization_2d_matrix(d, self.nodes[2])

        self.nodes_2d_throw = np.dot(vector_2d, normalization_matrix)


    def transform(self, matrix):
        self.nodes = np.dot(self.nodes, matrix)

        self.update_wall_z()
        self.painter_algorithm()

    def transform_throw(self, matrix):
        self.nodes_2d_throw = np.dot(self.nodes_2d_throw, matrix)

    def rotateX(self, theta=1):
        self.transform(rotateXMatrix(theta))

    def rotateY(self, theta=1):
        self.transform(rotateYMatrix(theta))

    def rotateZ(self, theta=1):
        self.transform(rotateZMatrix(theta))

    def wall_order(self):
        for i in range(len(self.walls) - 1):
            wall = self.walls[i]
            print(i, wall)

            for z in range(i+1,len(self.walls)):
                wall_next = self.walls[z].copy()

                plane = np.array(calculate_equation_of_plane(*self.nodes[wall[:3]][:, :3]))
                plane_next = np.array(calculate_equation_of_plane(*self.nodes[wall_next[:3]][:, :3]))
                if calculate_points_forward(plane, np.array((0, 0, 0, 1))):
                    points_behind = calculate_points_behind(plane.reshape(1, 4) ,self.nodes[wall_next]).sum()
                else:
                    points_behind = calculate_points_forward(plane.reshape(1, 4), self.nodes[wall_next]).sum()
                print(points_behind)
                if points_behind > 0:
                    self.walls[z] = self.walls[i]
                    self.walls[i] = wall_next
                    tmp_color = self.walls_colors[i].copy()
                    self.walls_colors[i] = self.walls_colors[z]
                    self.walls_colors[z] = tmp_color
                    break


    def bubble_sort(self,points_behind_wall):
        n = len(self.walls)
        for i in range(n):

            already_sorted = True

            for j in range(n - i - 1):

                wall = self.walls[j]
                wall_next = self.walls[j+1].copy()
                plane = np.array(calculate_equation_of_plane(*self.nodes[wall[:3]][:, :3]))

                if calculate_points_forward(plane, np.array((0, 0, 0, 1))):
                    points_behind = calculate_points_behind(plane.reshape(1, 4) ,self.nodes[wall_next]).sum()
                else:
                    points_behind = calculate_points_forward(plane.reshape(1, 4), self.nodes[wall_next]).sum()

                if points_behind > 0:
                    self.walls[j], self.walls[j + 1] = self.walls[j + 1].copy(), self.walls[j].copy()
                    self.walls_colors[j], self.walls_colors[j + 1] = self.walls_colors[j + 1].copy(), self.walls_colors[j].copy()
                    already_sorted = False

            if already_sorted:
                break

    # def counter_walls_behind(self, ):
    #     _

if __name__ == "__main__":
    cube = Wireframe()
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
    walls = np.vstack((walls_0, walls_1))

    cube.add_walls(
        walls,
        colors=[(x, z, y) for x in (0, 125, 250) for y in (125, 250) for z in (0, 250)]
    )
    # planes = np.array([calculate_equation_of_plane(*x) for x in cube.nodes[cube.walls[:, :3]][:, :, :3]], ).reshape(
    #     (len(cube.walls), 4))

    # for i,plane in enumerate(planes):
    #     wall = cube.walls[i]
    #     wall_next = cube.walls[i+1]
    #     if plane
    # for i in range(len(walls) -1):
    #     # print(walls)
    #     # print('\n')
    #     wall = walls[i]
    #     plane = np.array(calculate_equation_of_plane( *cube.nodes[wall[:3]][:,:3]))
    #
    #     wall_next = walls[i+1].copy()
    #     if calculate_points_forward(plane, np.array(( 0, 0, 0,1))):
    #         points_behind = calculate_points_behind(plane.reshape(1, 4), cube.nodes[wall_next]).sum()
    #     else:
    #         points_behind = calculate_points_forward(plane.reshape(1, 4), cube.nodes).sum()
    #     if points_behind > 0:
    #         walls[i+1] = walls[i]
    #         walls[i] = wall_next


