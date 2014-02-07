import random
import math
import itertools


class Vector:
    """2D dimensional vector.

    Available operations:
        addition, subtraction of vectors: v1 - v2, v1 + v2
        magnitude: abs(v)
        normalization: v.normalize()
        scalar multiplication: a*v

    Attributes:
        x: x coordinate
        y: y coordinate
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __rmul__(self, a):
        return Vector(self.x*a, self.y*a)

    def __sub__(self, v):
        return Vector(self.x - v.x, self.y - v.y)

    def __div__(self, a):
        if a != 0:
            return Vector(self.x/a, self.y/a)
        return self 

    def __add__(self, v):
        return Vector(self.x + v.x, self.y + v.y)

    def __abs__(self):
        return math.sqrt(self.x*self.x + self.y*self.y)

    def normalize(self):
        m = abs(self)
        if m != 0:
            return 1/m * self
        return self


def spring_layout(graph, width, height, iterations=1000, c=0.5):
    """Graph Drawing by Force-directed Placement using Fruchterman-Reingold algorithm.
    Original paper: http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.13.8444&rep=rep1&type=pdf
    Args:
        graph: adjacency list
        width: width of frame
        height: height of frame
        iterations: number of iterations in the algorithm
        c: constant in the formula for k (ideal distance between vertices)
    Returns:
        Graph with added to each vertex attribute .pos, that returns Vector
    """
    area = width*height
    k = math.sqrt(area/len(graph.keys()))*c

    def fr(x):
        return k*k/(x + 0.1)

    def fa(x):
        return x*x/k

    t = width*1.0/10
    dt = t/(iterations + 1)

    for v in graph:
        if not hasattr(v, 'pos'):
            x = random.randrange(-width/2, width/2)
            y = random.randrange(-height/2, height/2)
            v.pos = Vector(x, y)
        v.disp = Vector(0, 0)

    for i in xrange(iterations):
        for pair in itertools.combinations(graph.keys(), 2):
            v, u = pair[0], pair[1]
            diff = v.pos - u.pos
            mag = abs(diff)
            norm = diff/mag

            # repulsive force
            force = fr(mag)*norm

            # attractive force
            if v in graph[u]:
                force -= fa(mag)*norm

            v.disp += force
            u.disp -= force

        for v in graph:
            # limit the maximum displacement to the temperature t
            mag = abs(v.disp)
            v.pos = v.pos + min(mag, t)*v.disp/mag
            # prevent from being displaced outside frame
            v.pos.x = min(width/2, max(-width/2, v.pos.x))
            v.pos.y = min(height/2, max(-height/2, v.pos.y))
            v.disp = Vector(0, 0)

        t -= dt

    return graph
