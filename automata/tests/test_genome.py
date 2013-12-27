import unittest
from automata.organism import Genome


class ParsersTest(unittest.TestCase):

    def test_parsing1(self):
        text = 'B(A),c > 2, p=0: ++D'
        g = Genome(text)
        op = g.operations[0]
        self.assertEqual(op.c_state, 'B')
        self.assertEqual(op.p_state, 'A')
        self.assertEqual(op.c_condition, 'c>2')
        self.assertEqual(op.p_condition, 'p=0')
        self.assertEqual(op.command.state, 'D')
        self.assertEqual(op.command.function.__name__, 'plus_plus')

    def test_parsing2(self):
        text = 'A(C), c<2,p>=0 :F'
        g = Genome(text)
        op = g.operations[0]
        self.assertEqual(op.c_state, 'A')
        self.assertEqual(op.p_state, 'C')
        self.assertEqual(op.c_condition, 'c<2')
        self.assertEqual(op.p_condition, 'p>=0')
        self.assertEqual(op.command.state, 'F')
        self.assertEqual(op.command.function.__name__, 'change_state')

    def test_parsing3(self):
        text = 'A(), c == 5,p!=1:  -E'
        g = Genome(text)
        op = g.operations[0]
        self.assertEqual(op.c_state, 'A')
        self.assertEqual(op.p_state, '')
        self.assertEqual(op.c_condition, 'c==5')
        self.assertEqual(op.p_condition, 'p!=1')
        self.assertEqual(op.command.state, 'E')
        self.assertEqual(op.command.function.__name__, 'minus')
