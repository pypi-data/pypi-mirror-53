# coding: utf-8
"""
Show rings in Yaplot format, defined in https://github.com/vitroid/Yaplot

Usage:
    genice III -f rings > 3.rings.yap
    genice III -f rings[5] > output.yap    # up to 5-membered rings.
"""

import sys
from collections import defaultdict
import numpy as np
import networkx as nx
import yaplotlib as yp

from genice import rigid
from countrings import countrings_nx as cr



def face(center, rpos):
    pos = rpos + center
    n = rpos.shape[0]
    s = yp.Color(n)
    s += yp.Layer(n)
    s += yp.Polygon(pos)
    return s



def hook2(lattice):
    lattice.logger.info("Hook2: Show rings in Yaplot format.")
    # copied from svg_poly
    graph = nx.Graph(lattice.graph) #undirected
    cellmat = lattice.repcell.mat
    s = ""
    s += yp.Layer(2)
    s += yp.Color(0)
    for i,j in graph.edges():
        pi, pj = lattice.reppositions[i], lattice.reppositions[j]
        d = pj - pi
        d -= np.floor(d+0.5)
        s += yp.Line(pi @ cellmat, (pi+d) @ cellmat)
    for ring in cr.CountRings(graph).rings_iter(lattice.largestring):
        deltas = np.zeros((len(ring),3))
        d2 = np.zeros(3)
        for k,i in enumerate(ring):
            d = lattice.reppositions[i] - lattice.reppositions[ring[0]]
            d -= np.floor(d+0.5)
            deltas[k] = d
            dd = lattice.reppositions[ring[k]] - lattice.reppositions[ring[k-1]]
            dd -= np.floor(dd+0.5)
            d2 += dd
        # d2 must be zeros
        if np.all(np.absolute(d2) < 1e-5):
            comofs = np.sum(deltas, axis=0) / len(ring)
            deltas -= comofs
            com = lattice.reppositions[ring[0]] + comofs
            com -= np.floor(com)
            # rel to abs
            com    = np.dot(com,    cellmat)
            deltas = np.dot(deltas, cellmat)
            s += face(com,deltas)
    print(s)
    lattice.logger.info("Hook2: end.")


    
# argparser
def hook0(lattice, arg):
    lattice.logger.info("Hook0: ArgParser.")

    if arg == "":
        lattice.largestring=8
    else:
        try:
            lattice.largestring=int(arg)
        except:
            lattice.logger.error("Argument must be a positive integer.")
            sys.exit(1)

    lattice.logger.info("  Largest ring: {0}.".format(lattice.largestring))
    lattice.logger.info("Hook0: end.")



hooks = {2:hook2, 0:hook0}
