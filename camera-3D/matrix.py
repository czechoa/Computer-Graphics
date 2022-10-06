import numpy as np


def translationMatrix(dx=0, dy=0, dz=0):
    return np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [dx, dy, dz, 1]])


def rotateXMatrix(radians):
    c = np.cos(radians)
    s = np.sin(radians)
    return np.array([[1, 0, 0, 0], [0, c, s, 0], [0, -s, c, 0], [0, 0, 0, 1]])


def rotateYMatrix(radians):
    c = np.cos(radians)
    s = np.sin(radians)
    return np.array([[c, 0, s, 0], [0, 1, 0, 0], [-s, 0, c, 0], [0, 0, 0, 1]])


def rotateZMatrix(radians):
    c = np.cos(radians)
    s = np.sin(radians)
    return np.array([[c, -s, 0, 0], [s, c, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])


def normalization_2d_matrix(d, z):
    return np.array([[d / z, 0, 0, 0], [0, d / z, 0, 0], [0, 0, d / z, 0], [0, 0, 0, d / z]])


def projection_2d_matrix(d):
    return np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 1 / d], [0, 0, 0, 0]])
