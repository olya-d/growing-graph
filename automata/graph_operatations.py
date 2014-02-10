def add_vertex(graph, vertex):
    if not vertex in graph.keys():
        graph[vertex] = []
    return graph


def add_edge(graph, vertex1, vertex2, directed=True):
    graph[vertex1].append(vertex2)
    if not directed:
        graph[vertex2].append(vertex1)
    return graph


def remove_edge(graph, vertex1, vertex2):
    if vertex2 in graph[vertex1]:
        graph[vertex1].remove(vertex2)
    if vertex1 in graph[vertex2]:
        graph[vertex2].remove(vertex1)
    return graph


def remove_vertex(graph, vertex):
    graph.pop(vertex, None)
    for v in graph.keys():
        if vertex in graph[v]:
            graph[v].remove(vertex)
    return graph


def find_closest(graph, vertex, condition):
    q = [vertex]
    v = {vertex}
    while q:
        t = q.pop()
        if condition(t):
            return t
        for u in graph[t]:
            if not u in v:
                v.add(u)
                q.append(u)
