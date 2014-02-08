"""
Genome language:
C(P),c : command, where C is a current state, P is a previous state (() if there is no condition),
c is a condition on the number of connections

Command language:
++X - grow an adjacent cell in X state
--X - remove adjacent cell in X state
+X  - connect to the closest cell in X state
-X  - disconnect from a cell in X state
X   - change state to X
"""
import re
import automata.graph_operatations as go


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
        new_cell = Cell(c.graph, self.state)
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
    def __init__(self, c_state, p_state, c_condition, command):
        self.c_state = c_state
        self.p_state = p_state
        self.c_condition = c_condition.replace(' ', '')
        self.command = Command(command.replace(' ', ''))

    def execute(self, cell):
        if cell.state == self.c_state and cell.previous_state == self.p_state:
            if self.connection_condition_satisfied(cell.number_of_connections):
                self.command.function(cell)

    def connection_condition_satisfied(self, c):
        return eval(self.c_condition)


class Genome:

    re_operation = re.compile(r'(\w+)\((\w*)\),(.+):(.+)')

    def __init__(self, text):
        self.operations = []
        self.lines = []
        for line in text.splitlines():
            self.lines.append(line)
            current_state, previous_state, connection_condition, command = re.match(Genome.re_operation, line).groups()
            self.operations.append(Operation(current_state, previous_state, connection_condition, command))