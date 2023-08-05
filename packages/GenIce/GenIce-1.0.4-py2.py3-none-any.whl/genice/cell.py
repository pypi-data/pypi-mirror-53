# parallelepiped cell


import numpy as np
import sys
import logging
from genice.valueparsers import put_in_array
from math import pi, sin, cos, sqrt, acos


def rel_wrap(relvec):
    return relvec - np.floor(relvec + 0.5)


def rel_wrapf(relvec):
    return relvec - np.floor(relvec)


def sincos(A):
    cA = cos(A)
    if abs(cA) < 1e-16:
        return 1.0, 0.0
    return sin(A), cA


# moved from GenIce/cif/CIF.py
def cellvectors(a,b,c,A=90,B=90,C=90):
    """
    Generate cell vectors from a,b,c and alpha, beta, gamma.
    """
    # probably same as six2nine in rigid.py
    logger = logging.getLogger()
    A *= pi/180
    B *= pi/180
    C *= pi/180
    sA, cA = sincos(A)
    sB, cB = sincos(B)
    sC, cC = sincos(C)
    ea = np.array([1.0, 0.0, 0.0])
    eb = np.array([cC, sC, 0])
    # ec.ea = ecx = cos(B)
    # ec.eb = ecx*ebx + ecy*eby = cos(A)
    ecx = cB
    ecy = (cA - ecx*eb[0]) / eb[1]
    ecz = sqrt(1-ecx**2-ecy**2)
    ec = np.array([ecx, ecy, ecz])
    # logger.info((cos(A), np.dot(eb, ec)))
    # logger.info((cos(B), np.dot(ec, ea)))
    # logger.info((cos(C), np.dot(ea, eb)))
    return np.vstack([ea*a, eb*b, ec*c])


class Cell():
    mat = np.zeros(9).reshape(3, 3)
    inv = None

    def __init__(self, desc=None):
        self.parse(desc)

    def abs2rel(self, absvecs):
        return np.dot(absvecs, self.inv)

    def rel2abs(self, relvec):
        return np.dot(relvec, self.mat)

    def abs_wrap(self, absvec):
        return self.rel2abs(rel_wrap(self.abs2rel(absvec)))

    def abs_wrapf(self, absvec):
        return self.rel2abs(rel_wrapf(self.abs2rel(absvec)))

    def volume(self):
        return np.linalg.det(self.mat)

    def scale(self, x):
        self.mat *= x
        self.inv = np.linalg.inv(self.mat)

    def scale2(self, x):
        for d in range(3):
            self.mat[d, :] = self.mat[d, :] * x[d]
        self.inv = np.linalg.inv(self.mat)

    def parse(self, mat):
        logger = logging.getLogger()
        logger.debug(("MAT:",mat))
        self.mat = mat.copy()
        La = np.linalg.norm(self.mat[0])
        Lb = np.linalg.norm(self.mat[1])
        Lc = np.linalg.norm(self.mat[2])
        alpha = acos((self.mat[1] @ self.mat[2]) / (Lb * Lc)) * 180 / pi
        beta = acos((self.mat[2] @ self.mat[0]) / (Lc * La)) * 180 / pi
        gamma = acos((self.mat[0] @ self.mat[1]) / (La * Lb)) * 180 / pi
        logging.info("Cell dimension:")
        logging.info("  a = {0}".format(La))
        logging.info("  b = {0}".format(Lb))
        logging.info("  c = {0}".format(Lc))
        logging.info("  A = {0}".format(alpha))
        logging.info("  B = {0}".format(beta))
        logging.info("  C = {0}".format(gamma))
        self.inv = np.linalg.inv(self.mat)

    def serialize_BOX9(self):
        s = "@BOX9\n"
        for d in range(3):
            s += "{0:.4f} {1:.4f} {2:.4f}\n".format(*self.mat[d] * 10)  # AA
        return s
