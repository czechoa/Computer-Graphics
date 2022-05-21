import numpy as np
from matrix import projection_2d_matrix, normalization_2d_matrix, rotateXMatrix, rotateYMatrix, rotateZMatrix


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

        planes = np.array([calculate_equation_of_plane(*x) for x in self.nodes[self.walls[:, :3]][:, :, :3]], ).reshape(
            (len(self.walls), 4))

        points_behind_wall = -1 * np.array(
            [calculate_points_behind(plane.reshape(1, 4), self.nodes).sum() if calculate_points_forward(plane, np.array(
                (0, 0, 0, 1)))
             else calculate_points_forward(plane.reshape(1, 4), self.nodes).sum() for plane in planes])

        # check_calculate_equation_of_plane(planes, self.nodes)

        to_sort = np.hstack((self.walls_z, points_behind_wall.reshape(-1, 1)))
        sorted_index = np.lexsort([to_sort[:, -i] for i in reversed(range(1, to_sort.shape[1] + 1))])[::-1]

        self.order_walls(sorted_index)
        print(to_sort[sorted_index])

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

if __name__ == "__main__":
    cube = Wireframe()
    cube_nodes = [(x * 2, y * 3, z / 2) for x in (50, 250) for y in (50, 250) for z in (50, 250)]

    cube.addNodes(np.array(cube_nodes))

    cube.addEdges(
        [(n, n + 4) for n in range(0, 4)] + [(n, n + 1) for n in range(0, 8, 2)] + [(n, n + 2) for n in (0, 1, 4, 5)])

    cube.add_walls(
        [[0, 2, 6, 4],  # PRZEDNIA
         [1, 3, 7, 5],  # TYLNIA

         [2, 6, 7, 3],  # DOLNA
         [0, 4, 5, 1],  # GORNA

         [1, 3, 2, 0],  # LEWA
         [7, 6, 4, 5]  # PRAWA
         ], colors=np.zeros((6, 3))
    )
    mt = projection_2d_matrix(2)
    print(cube.nodes)
    nodes_throw = np.dot(cube.nodes,mt)
    print(nodes_throw)

    d = 500
    mrp2 = projection_2d_matrix(d)
    vector_2d = np.dot(cube.nodes[:], mrp2)
    print(vector_2d)
    normalization_matrix = normalization_2d_matrix(d, cube.nodes[:][2])

    nodes_2d_throw = np.dot(vector_2d, normalization_matrix)
    print( d* cube.nodes[0][0]/cube.nodes[0][2] , d* cube.nodes[0][1]/cube.nodes[0][2])
    print(nodes_2d_throw)

def PolyArea(x, y):
    return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))


def check_calculate_equation_of_plane(plane, points):
    point_in_plane = np.around(np.dot(plane, points.T)) == 0
    print(point_in_plane.sum(axis=1))


def calculate_equation_of_plane(p1, p2, p3):
    v1 = p3 - p1
    v2 = p2 - p1

    cp = np.cross(v1, v2)

    a, b, c = cp
    d = -np.dot(cp, p3)

    return a, b, c, d


def calculate_points_behind(plane, points):
    return np.around(np.dot(plane, points.T)) > 0

def calculate_points_forward(plane, points):
    return np.around(np.dot(plane, points.T)) < 0
