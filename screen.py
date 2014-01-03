import wx
import wx.grid

from automata.organism import Organism
from layout import spring_layout
import itertools


WIN_WIDTH = 800
WIN_HEIGHT = 800
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
BACKGROUND_COLOR = "#000000"


class GraphVisualizerFrame(wx.Frame):
    def __init__(self, parent, title, organism):
        self.organism = organism
        super(GraphVisualizerFrame, self).__init__(parent, title=title, size=(800, 600))
        self.InitUI()
        self.Show(True)

    def InitUI(self):
      self.panel = wx.Panel(self)
      self.SetMenuBar(wx.MenuBar())

      toolbar = self.CreateToolBar()
      toolbar.Realize()

      self.buffer = wx.EmptyBitmap(800, 600)
      self.draw(None)

    def draw(self, event):
        self.force_timer = wx.Timer(self)
        self.force_timer.Start(100)
        self.iterate_timer = wx.Timer(self)
        self.iterate_timer.Start(1000)

        self.Bind(wx.EVT_TIMER, self.update_layout, self.force_timer)
        self.Bind(wx.EVT_TIMER, self.update_organism, self.iterate_timer)

        dc = wx.BufferedDC(wx.ClientDC(self.panel), self.buffer)
        spring_layout(self.organism.graph, width=400, height=300, iterations=10)
        self.draw_graph(dc)

    def update_layout(self, event):
        if not spring_layout(self.organism.graph, width=400, height=300, iterations=10):
            self.force_timer.Destroy()
        self.update(event)

    def update_organism(self, event):
        if not self.organism.iterate():
            self.iterate_timer.Destroy()

    def update(self, event):
        if self.force_timer.IsRunning() or self.iterate_timer.IsRunning():
            dc = wx.BufferedDC(wx.ClientDC(self.panel), self.buffer)
            self.draw_graph(dc)

    def draw_graph(self, dc):
        dc.Clear()
        for pair in itertools.combinations(self.organism.graph.keys(), 2):
            if pair[0] in self.organism.graph[pair[1]]:
                x1 = int(pair[0].pos.x) + 200
                y1 = int(pair[0].pos.y) + 150
                x2 = int(pair[1].pos.x) + 200
                y2 = int(pair[1].pos.y) + 150

                dc.DrawLine(x1, y1, x2, y2)

app = wx.App()
code = 'A(A),c>=0,p==0 :++B \
\nB(),c >=0,p<2 :++B \nB(B),c>=0,p>=0 :C \nA(A),c>=0,p>=0 :G \nC(B), c==1,p>=0 :G \nG(G), c <=5,p>=0 :++H'
organism = Organism('A', code)
frame = GraphVisualizerFrame(None, 'Organism', organism)
frame.Show()

app.MainLoop()
app.Destroy()

