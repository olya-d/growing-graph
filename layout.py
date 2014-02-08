import random
import math
import itertools


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

    half_width = width/2
    half_height = height/2

    for v in graph:
        if not hasattr(v, 'pos'):
            x = random.randrange(-half_width, half_width)
            y = random.randrange(-half_height, half_height)
            v.pos = {'x': x, 'y': y}
        v.disp = {'x': 0, 'y': 0}

    for i in xrange(iterations):
        for pair in itertools.combinations(graph.keys(), 2):
            v, u = pair[0], pair[1]
            dx = v.pos['x'] - u.pos['x']
            dy = v.pos['y'] - u.pos['y']
            mag = math.sqrt(dx*dx + dy*dy)
            if mag != 0:
                normx = dx/mag
                normy = dy/mag
            else:
                normx = dx
                normy = dy

            # repulsive force
            forcex = fr(mag)*normx
            forcey = fr(mag)*normy

            # attractive force
            if v in graph[u]:
                forcex -= fa(mag)*normx
                forcey -= fa(mag)*normy

            v.disp['x'] += forcex
            v.disp['y'] += forcey
            u.disp['x'] -= forcex
            u.disp['y'] -= forcey

        for v in graph:
            # limit the maximum displacement to the temperature t
            mag = math.sqrt(v.disp['x']**2 + v.disp['y']**2)
            if mag != 0:
                posx = v.pos['x'] + min(mag, t)*v.disp['x']/mag
                posy = v.pos['y'] + min(mag, t)*v.disp['y']/mag
            else:
                posx = v.pos['x'] + min(mag, t)*v.disp['x']
                posy = v.pos['y'] + min(mag, t)*v.disp['y']               
            # prevent from being displaced outside frame
            v.pos['x'] = min(half_width, max(-half_width, posx))
            v.pos['y'] = min(half_height, max(-half_height, posy))
            v.disp = {'x': 0, 'y': 0}

        t -= dt

    return graph
