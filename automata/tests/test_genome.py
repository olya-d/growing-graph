import unittest
from automata.genome import Genome


class ParsersTest(unittest.TestCase):

    def test_parsing1(self):
        text = 'B(A),c > 2: ++D'
        g = Genome(text)
        op = g.operations[0]
        self.assertEqual(op.c_state, 'B')
        self.assertEqual(op.p_state, 'A')
        self.assertEqual(op.c_condition, 'c>2')
        self.assertEqual(op.command, '++D')

    def test_parsing2(self):
        text = 'A(C), c<2:F'
        g = Genome(text)
        op = g.operations[0]
        self.assertEqual(op.c_state, 'A')
        self.assertEqual(op.p_state, 'C')
        self.assertEqual(op.c_condition, 'c<2')
        self.assertEqual(op.command, 'F')

    def test_parsing3(self):
        text = 'A(), c == 5:  -E'
        g = Genome(text)
        op = g.operations[0]
        self.assertEqual(op.c_state, 'A')
        self.assertEqual(op.p_state, '')
        self.assertEqual(op.c_condition, 'c==5')
        self.assertEqual(op.command, '-E')
