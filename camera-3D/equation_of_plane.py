import  numpy as np
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
