"""
Genome language:
C(P),c,p : command, where C is a current state, P is a previous state (() if there is no condition),
c is a condition on the number of connections, p is a conditoin on the number of parents

Command language:
++X - grow an adjacent cell in X state
--X - remove adjacent cell in X state
+X  - connect to the closest cell in X state
-X  - disconnect from a cell in X state
X   - change state to X
"""
import re
import automata.graph_operatations as go
import collections
import copy


class Command:
    def __init__(self, text):
        action, self.state = re.match(r'([+-]*)(\w+)', text).groups()
        self.function = {
            '++': self.plus_plus,
            '--': self.minus_minus,
            '+': self.plus,
            '-': self.minus,
            '': self.change_state
        }[action]

    def plus_plus(self, c):
        new_cell = Cell(c.graph, self.state, parents=c.number_of_parents+1)
        go.add_vertex(c.graph, new_cell)
        go.add_edge(c.graph, new_cell, c, directed=False)

    def minus_minus(self, c):
        for v in c.graph[c]:
            if v.state == self.state:
                go.remove_vertex(c.graph, v)
                break

    def plus(self, c):
        closest = go.find_closest(c.graph, c, lambda x: x.state == self.state and not x in c.graph[c])
        if closest:
            go.add_edge(c.graph, closest, c)

    def minus(self, c):
        for v in c.graph[c]:
            if v.state == self.state:
                go.remove_edge(c.graph, v, c)
                break

    def change_state(self, c):
        c.previous_state = c.state
        c.state = self.state


class Operation:
    def __init__(self, text, c_state, p_state, c_condition, p_condition, command):
        self.text = text
        self.c_state = c_state
        self.p_state = p_state
        self.c_condition = c_condition.replace(' ', '')
        self.p_condition = p_condition.replace(' ', '')
        self.command = Command(command.replace(' ', ''))

    def execute(self, cell):
        if cell.state == self.c_state:
            if not self.p_state or cell.previous_state == self.p_state:
                if self.conditions_satisfied(cell):
                    self.command.function(cell)
                    return True
        return False

    def conditions_satisfied(self, cell):
        c = cell.number_of_connections
        p = cell.number_of_parents
        return eval(self.c_condition) and eval(self.p_condition)

    def __str__(self):
        return self.text


class Genome:

    re_operation = re.compile(r'(\w+)\((\w*)\),(.+),(.+):(.+)')

    def __init__(self, text):
        self.text = text
        self.operations = []
        for line in text.splitlines():
            c_state, p_state, c_condition, p_condition, command = re.match(Genome.re_operation, line).groups()
            self.operations.append(Operation(line, c_state, p_state, c_condition, p_condition, command))

    def __str__(self):
        return self.text


class Cell(object):
    def __init__(self, graph, state='', parents=1):
        self.graph = graph
        self.state = state
        self.previous_state = state
        self.number_of_parents = parents

    @property
    def number_of_connections(self):
        return len(self.graph[self])

    def __str__(self):
        return "{}({})".format(self.state, self.previous_state)


class Organism(object):
    def __init__(self, state, genome):
        self.graph = collections.OrderedDict({})
        self.genome = Genome(genome)
        c = Cell(self.graph, state, parents=0)
        go.add_vertex(self.graph, c)

    def iterate(self):
        changed = False
        graph = copy.copy(self.graph)
        for c in graph:
            s = c.state
            for op in self.genome.operations:
                if op.execute(c):
                    changed = True
            if s == c.state:
                c.previous_state = s
        return changed
