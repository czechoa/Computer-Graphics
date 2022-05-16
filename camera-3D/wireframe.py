import numpy as np


class Wireframe:
    def __init__(self):
        self.nodes = np.zeros((0, 4))
        self.nodes_2d_throw = np.zeros((0, 2))
        self.edges = []
        self.walls = np.zeros((0, 4))
        self.walls_z = np.zeros((0, 4))
        self.walls_x_y_norm =  np.zeros((0, 4))
        self.walls_colors = np.zeros((0, 3))

    def addNodes(self, node_array):
        ones_column = np.ones((len(node_array), 1))
        ones_added = np.hstack((node_array, ones_column))
        self.nodes = np.vstack((self.nodes, ones_added))
        self.nodes_2d_throw = self.nodes[:, :2].copy()

    def addEdges(self, edgeList):
        self.edges += edgeList

    def update_wall_z_and_x_Y_norm(self):
        self.walls_z = self.nodes[self.walls, 2]
        self.walls_x_y_norm = np.linalg.norm(self.nodes[self.walls, :3], axis=2)

    def add_walls(self, wallList, colors):
        self.walls = np.array(wallList)
        self.update_wall_z_and_x_Y_norm()
        self.walls_colors = np.array(colors)

    def sort_by_z_walls(self):

        self.walls_z = np.sort(self.walls_z, axis=1,kind='stable')
        self.walls_x_y_norm = np.sort(self.walls_x_y_norm, axis=1,kind='stable')

        to_sort = np.hstack((self.walls_x_y_norm, self.walls_z))
        sorted_index = np.lexsort([to_sort[:, -i] for i in reversed(range(1,9))] )[::-1]

        self.walls = self.walls[sorted_index]
        self.walls_z = self.walls_z[sorted_index]
        self.walls_x_y_norm = self.walls_x_y_norm[sorted_index]
        self.walls_colors = self.walls_colors[sorted_index]
        # print('po sortowaniu')
        # print(sorted_index)
        # print(self.walls)
        # print(self.walls_z)
        # print(to_sort[sorted_index])

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

    def findCentre(self):
        meanX, meanY, meanZ, _ = self.nodes.mean(axis=0)
        return (meanX, meanY, meanZ)

    def transform(self, matrix):
        self.nodes = np.dot(self.nodes, matrix)
        self.update_wall_z_and_x_Y_norm()
        self.sort_by_z_walls()

    def transform_throw(self, matrix):
        self.nodes_2d_throw = np.dot(self.nodes_2d_throw, matrix)

    # def scale(self,scale):
    #
    #     matrix = scaleMatrix(scale)
    #     self.transform(matrix)

    def rotateX(self, theta=1):
        self.transform(rotateXMatrix(theta))

    def rotateY(self, theta=1):
        self.transform(rotateYMatrix(theta))

    def rotateZ(self, theta=1):
        self.transform(rotateZMatrix(theta))


if __name__ == "__main__":
    cube = Wireframe()
    cube_nodes = [(x, y, z) for x in (50, 250) for y in (50, 250) for z in (50, 250)]

    cube.addNodes(np.array(cube_nodes))

    cube.addEdges(
        [(n, n + 4) for n in range(0, 4)] + [(n, n + 1) for n in range(0, 8, 2)] + [(n, n + 2) for n in (0, 1, 4, 5)])

    cube.add_walls(
        [[0, 4, 6, 2],
         [1, 5, 7, 3],
         [7, 3, 2, 6],
         [0, 1, 5, 4],
         [1, 0, 2, 3],
         [7, 6, 4, 5]], colors= np.zeros((6,3))
    )
    cube.sort_by_z_walls()
    cube.sort_by_z_walls()

    # cube.outputNodes()
    # cube.outputEdges()


def translationMatrix(dx=0, dy=0, dz=0):
    return np.array([[1, 0, 0, 0],
                     [0, 1, 0, 0],
                     [0, 0, 1, 0],
                     [dx, dy, dz, 1]])


def rotateXMatrix(radians):
    c = np.cos(radians)
    s = np.sin(radians)
    return np.array([[1, 0, 0, 0],
                     [0, c, s, 0],
                     [0, -s, c, 0],
                     [0, 0, 0, 1]])


def rotateYMatrix(radians):
    c = np.cos(radians)
    s = np.sin(radians)
    return np.array([[c, 0, s, 0],
                     [0, 1, 0, 0],
                     [-s, 0, c, 0],
                     [0, 0, 0, 1]])


def rotateZMatrix(radians):
    c = np.cos(radians)
    s = np.sin(radians)
    return np.array([[c, -s, 0, 0],
                     [s, c, 0, 0],
                     [0, 0, 1, 0],
                     [0, 0, 0, 1]])

# def scaleMatrix(z):
#     zoom = 1 /(1-z)
#     zoom_1 = -z/(1-z)
#     return np.array([[1, 0, 0, 0],
#                      [0, 1, 0, 0],
#                      [0, 0, zoom,1],
#                      [0, 0, zoom_1, 0]]
#                     )
