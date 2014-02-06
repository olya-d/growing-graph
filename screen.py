import wx

from automata.organism import Organism
from layout import spring_layout
import itertools
import support


WIN_WIDTH = 800  # Main window width
WIN_HEIGHT = 800  # Main window height
FORCE_FQ = 100  # The frequency of a force-directed algorithm updates in ms
ITERATION_FQ = 1000  # The frequency of organism's iterations in ms
LAYOUT_ITERATIONS = 10  # The number of iterations in a force-directed algorithm per update


class GraphVisualizerFrame(wx.Frame):
    def __init__(self, parent, title, organism):
        self.organism = organism
        super(GraphVisualizerFrame, self).__init__(parent, title=title, size=(WIN_WIDTH, WIN_HEIGHT))
        self.InitUI()
        self.Show(True)

    def InitUI(self):
        """
        Initializes main UI elements: panel, toolbar, bitmap buffer.
        """
        self.panel = wx.Panel(self)
        self.SetMenuBar(wx.MenuBar())

        toolbar = self.CreateToolBar()
        toolbar.Realize()

        self.buffer = wx.EmptyBitmap(WIN_WIDTH, WIN_HEIGHT)
        self.draw(None)

    def draw(self, event):
        """
        Initializes timers related to displaying the organism.
        """
        self.force_timer = wx.Timer(self)
        self.force_timer.Start(FORCE_FQ)
        self.iterate_timer = wx.Timer(self)
        self.iterate_timer.Start(ITERATION_FQ)

        self.Bind(wx.EVT_TIMER, self.update_layout, self.force_timer)
        self.Bind(wx.EVT_TIMER, self.update_organism, self.iterate_timer)

        dc = wx.BufferedDC(wx.ClientDC(self.panel), self.buffer)
        spring_layout(self.organism.graph, width=WIN_WIDTH/2, height=WIN_HEIGHT/2, iterations=LAYOUT_ITERATIONS)

        # Generate a color for each state
        states = self.organism.genome.states()
        self.colors = dict(zip(states, support.distinct_colors(len(states))))

        self.draw_graph(dc)

    def update_layout(self, event):
        """
        Updates layout by calling force-directed algorithm.
        """
        if not spring_layout(self.organism.graph, width=WIN_WIDTH/2, height=WIN_HEIGHT/2, iterations=LAYOUT_ITERATIONS):
            self.force_timer.Destroy()
        self.update(event)

    def update_organism(self, event):
        """
        Updates organism by performing one iteration.
        """
        if not self.organism.iterate():
            self.iterate_timer.Destroy()

    def update(self, event):
        """
        Updates bitmap buffer.
        """
        if self.force_timer.IsRunning() or self.iterate_timer.IsRunning():
            dc = wx.BufferedDC(wx.ClientDC(self.panel), self.buffer)
            self.draw_graph(dc)

    def draw_graph(self, dc):
        """
        Draws graph in bitmap buffer, called by update()
        """
        dc.Clear()
        dc.SetBrush(wx.Brush('#000000'))
        dc.DrawRectangle(0, 0, WIN_WIDTH, WIN_HEIGHT)

        for pair in itertools.combinations(self.organism.graph.keys(), 2):
            edge_state = None
            if pair[0] in self.organism.graph[pair[1]]:
                if pair[0] in pair[1].imediate_parents:
                    edge_state = pair[0].state
                elif pair[1] == pair[0].imediate_parents:
                    edge_state = pair[1].state
                dc.SetPen(wx.Pen(self.colors[edge_state]))
                x1 = int(pair[0].pos.x) + WIN_WIDTH/2
                y1 = int(pair[0].pos.y) + WIN_HEIGHT/2
                x2 = int(pair[1].pos.x) + WIN_WIDTH/2
                y2 = int(pair[1].pos.y) + WIN_HEIGHT/2

                dc.DrawLine(x1, y1, x2, y2)

app = wx.App()
code = 'A(A),c>=0,p==0 :++B \
\nB(),c >=0,p<2 :++B \nB(B),c>=0,p>=0 :C \nA(A),c>=0,p>=0 :G \nC(B), c==1,p>=0 :G \nG(G), c <=5,p>=0 :++H'
organism = Organism('A', code)
frame = GraphVisualizerFrame(None, 'Organism', organism)
frame.Show()

app.MainLoop()
app.Destroy()

