"""
Genome language:
state|maximum number of adjacent edges|maximum number of parents|command|command state
The first cell will be created in the state of the first line of genome.
If maximum number of adjacent edges or parents is -1, it is ignored.

Example:
A|10|5|++|B will grow from a cell in state A an adjacent cell in state B, if A has no more than 10 edges and no more than 5 parents.

Command language:
++ - grow an adjacent cell
-- - remove adjacent cell
+  - connect to the closest cell
-  - disconnect from the closest cell
->  - change state
"""
import re
import automata.graph_operatations as go
import collections
import copy


class Command:
    def __init__(self, action, state):
        self.state = state
        self.text = text
        action, self.state = re.match(r'([+-]*)(\w+)', text).groups()
        self.function = {
            '++': self.plus_plus,
            '--': self.minus_minus,
            '+': self.plus,
            '-': self.minus,
            '->': self.change_state
        }[action]

    def plus_plus(self, c):
        new_cell = Cell(c.graph, self.state, parents=c.number_of_parents+1)
        new_cell.add_imediate_parent(c)
        go.add_vertex(c.graph, new_cell)
        go.add_edge(c.graph, new_cell, c, directed=False)

    def minus_minus(self, c):
        for v in c.graph[c]:
            if v.state == self.state:
                go.remove_vertex(c.graph, v)
                break

    def plus(self, c):
        closest = go.find_closest(c.graph, c, lambda x: x.state == self.state)
        if closest:
            go.add_edge(c.graph, closest, c, directed=False)
            closest.add_imediate_parent(c)

    def minus(self, c):
        for v in c.graph[c]:
            if v.state == self.state:
                go.remove_edge(c.graph, v, c)
                break

    def change_state(self, c):
        c.state = self.state


class Operation:

    parse_re = re.compile('([a-zA-Z])\|(-?\d+)\|(-?\d+)\|(\+\+|\-\-|\->|\+|-)\|([a-zA-Z])')

    def __init__(self, text):
        self.text = text.replace(' ', '')
        parsed = re.match(Operation.parse_re, self.text)
        self.state, max_edges, max_parents, action, command_state = parsed.groups()
        self.max_edges = int(max_edges)
        self.max_parents = int(max_parents)
        self.command = Command(action, command_state)

    def execute(self, cell):
        if cell.state == self.state:
            if self.max_edges == -1 or cell.number_of_connections <= self.max_edges:
                if self.max_parents == -1 or cell.number_of_parents <= self.max_parents:
                    self.command.function(cell)
                    return True
        return False

    def __str__(self):
        return self.text


class Genome:
    def __init__(self, text):
        self.text = text
        self.operations = []
        for line in text.splitlines():
            self.operations.append(Operation(line))

    def __str__(self):
        return self.text

    def states(self):
        return set([state for op in self.operations for state in [op.state, op.command.state]])


class Cell(object):
    def __init__(self, graph, state='', parents=1):
        self.graph = graph
        self.state = state
        self.previous_state = state
        self.number_of_parents = parents
        self.imediate_parents = []

    @property
    def number_of_connections(self):
        return len(self.graph[self])

    def add_imediate_parent(self, c):
        self.imediate_parents.append(c)

    def __str__(self):
        return self.state


class Organism(object):
    def __init__(self, genome):
        self.graph = {}
        self.genome = Genome(genome)
        c = Cell(self.graph, state=self.genome.operations[0].state, parents=0)
        go.add_vertex(self.graph, c)

    def iterate(self):
        changed = False
        graph = copy.copy(self.graph)
        for operation in self.genome.operations:
            for c in graph:
                if operation.execute(c):
                    changed = True
        return changed
