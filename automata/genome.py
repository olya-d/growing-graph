"""
Genome language:
C(P),c : command, where C is a current state, P is a previous state (() if there is no condition), c is a condition on the number of connections

Command language:
++X - grow and adjacent cell in X state
--X - remove adjacent cell in X state
+X  - connect to the closest cell in X state
-X  - disconnect from the closest cell in X state
X   - change state to X
"""
import re


class Operation:
    def __init__(self, c_state, p_state, c_condition, command):
        self.c_state = c_state
        self.p_state = p_state
        self.c_condition = c_condition.replace(' ', '')
        self.command = command.replace(' ', '')


class Genome:

    re_operation = re.compile(r'(\w+)\((\w*)\),(.+):(.+)')

    def __init__(self, text):
        self.operations = []
        for line in text.splitlines():
            current_state, previous_state, connection_condition, command = re.match(Genome.re_operation, line).groups()
            self.operations.append(Operation(current_state, previous_state, connection_condition, command))