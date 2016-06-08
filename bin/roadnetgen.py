#!/usr/bin/python2
import numpy
from numpy.random import random_integers as rand
import matplotlib.pyplot as pyplot
import networkx as nx
from toPBM import writePBM


def roadNetGen(roadnet):
    # TODO: This is pretty hacked together. Make this better
    try:
        # iterate over neighbors
        edg = numpy.zeros((len(roadnet.neighbors(0))))
        for n in roadnet.neighbors(0):
            edg[n-1] = roadnet.edge[0][n]['weight']
    except:
        print('roadnet must be a networkx graph type')
        raise

    try:
        homenode = roadnet.node[0]
    except:
        print('roadnet must have a node named "0"')
        raise

    # assume that the first and third elements are vertical
    # constrain dimensions by the max height and max width
    edg = 2*edg # make edges twice as long, so we can scale up the resolution
    sze = 2*max(edg)+1
    #height = 2* max(edg[2],edg[0]) + 1
    #width = 2* max(edg[3],edg[1]) + 1

    # Build actual maze
    #Z = numpy.ones((height,width), dtype=bool)
    Z = numpy.ones((sze,sze),dtype=bool)
    # Fill borders
    # Z[0, :] = Z[-1, :] = 1
    # Z[:, 0] = Z[:, -1] = 1

    #Z[height/2-edg[2]:height/2+edg[0],width/2]=0
    #Z[height/2, width/2-edg[3]:width/2+edg[1]]=0
    print(sze/2,sze/2+1)
    Z[sze/2-edg[2]:sze/2+edg[0],sze/2:sze/2+2]=0
    Z[sze/2:sze/2+2 , sze/2-edg[3]:sze/2+edg[1]]  = 0

    return Z

# Build a road network
RN = nx.Graph()
RN.add_edge(0, 1, weight=3)
RN.add_edge(0, 2, weight=2)
RN.add_edge(0, 3, weight=5)
RN.add_edge(0, 4, weight=3)

# Generate the occupancy grid
roadnet_mat = numpy.rot90(roadNetGen(RN))

pyplot.figure(figsize=(10, 5))
# pyplot.imshow(maze(80, 40), cmap=pyplot.cm.binary, interpolation='nearest')
# genMaze = maze(31,31, complexity=0.1, density=0.15)

writePBM(roadnet_mat,name="roadnet")

pyplot.imshow(roadnet_mat, cmap=pyplot.cm.binary, interpolation='nearest')
pyplot.xticks([]), pyplot.yticks([])
pyplot.show()
