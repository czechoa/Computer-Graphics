import numpy as np


class Wireframe:
    def __init__(self):
        self.nodes = np.zeros((0, 4))
        self.nodes_2d_throw = np.zeros((0, 2))
        self.edges = []
        self.walls = np.zeros((0, 4))
        self.walls_z = np.zeros((0, 4))
        # self.walls_x_y_norm =  np.zeros((0, 4))
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
        # self.walls_x_y_norm = np.linalg.norm(self.nodes[self.walls, :3], axis=2)
        # self.walls_x_y_norm = np.linalg.norm(self.nodes[self.walls, :3], axis=2)


    def add_walls(self, wallList, colors):
        self.walls = np.array(wallList)
        self.update_wall_z_and_x_Y_norm()
        self.walls_colors = np.array(colors)

    def sort_by_z_walls(self):

        self.walls_z = np.sort(self.walls_z, axis=1,kind='stable')
        # self.walls_x_y_norm = np.sort(self.walls_x_y_norm, axis=1,kind='stable')
        planes = [calculate_equation_of_plane(*x) for x in self.nodes[self.walls[:, :3]][:, :, :3]]

        # nodes_and_000_point = np.vstack((self.nodes,(0,0,0,1)))
        points_behind_wall = -1*calculate_points_behind(planes[:], self.nodes).sum(axis=1)
        points_behind_wall += calculate_points_behind(planes[:], np.array((0,0,0,1)) )

        to_sort = np.hstack((points_behind_wall.reshape(-1,1), self.walls_z))

        sorted_index = np.lexsort([to_sort[:, -i] for i in reversed(range(1,to_sort.shape[1] +1))] )[::-1]

        self.walls = self.walls[sorted_index]
        self.walls_z = self.walls_z[sorted_index]
        self.walls_colors = self.walls_colors[sorted_index]
        print(self.walls)
        print(to_sort[sorted_index])

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

    def rotateX(self, theta=1):
        self.transform(rotateXMatrix(theta))

    def rotateY(self, theta=1):
        self.transform(rotateYMatrix(theta))

    def rotateZ(self, theta=1):
        self.transform(rotateZMatrix(theta))



def calculate_equation_of_plane(p1,p2,p3):
    # These two vectors are in the plane
    v1 = p3 - p1
    v2 = p2 - p1

    # the cross product is a vector normal to the plane
    cp = np.cross(v1, v2)

    a, b, c = cp
    # This evaluates a * x3 + b * y3 + c * z3 which equals d
    d = -np.dot(cp, p3)
    return  a,b,c,d

def calculate_points_behind(plane, points):
    return  np.dot(plane,points.T) > 0

def calculate_points_forward(plane, points):
    return  np.dot(plane,points.T) < 0

if __name__ == "__main__":
    cube = Wireframe()
    cube_nodes = [(x, y, z) for x in (50, 250) for y in (50, 250) for z in (50, 250)]

    cube.addNodes(np.array(cube_nodes))

    cube.addEdges(
        [(n, n + 4) for n in range(0, 4)] + [(n, n + 1) for n in range(0, 8, 2)] + [(n, n + 2) for n in (0, 1, 4, 5)])

    cube.add_walls(
        [[0, 2, 6, 4],# PRZEDNIA
         [1, 3, 7, 5], # TYLNIA

         [2, 6, 7, 3], # DOLNA
         [0, 4, 5, 1], # GORNA

         [1, 3, 2, 0],  # LEWA
         [7, 6, 4, 5] # PRAWA
         ], colors= np.zeros((6,3))
    )
    # print(cube.nodes[cube.walls[0]][:3,:3])
    # print(cube.nodes[cube.walls[:5,:3]][:,:,1])

    # print(calculate_equation_of_plane(*cube.nodes[cube.walls[:5,:3]][:,:,:3]))
    # print('\n')
    print('sing')
    cube.sort_by_z_walls()
    # planes = [ calculate_equation_of_plane(*x) for x in cube.nodes[cube.walls[:,:3]][:,:,:3]]


    # points_behind  = calculate_points_behind(planes[:],cube.nodes[:]).sum(axis=1)
    # print(points_behind.reshape(-1,1))

    # cube.sort_by_z_walls()


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

def PolyArea(x,y):
    return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))


