import sys
import pygame
from pygame import *
from automata.organism import Organism
from layout import spring_layout
import itertools


WIN_WIDTH = 800
WIN_HEIGHT = 800
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
BACKGROUND_COLOR = "#000000"

def draw_graph(surface, graph):
    for pair in itertools.combinations(graph.keys(), 2):
        if pair[0] in graph[pair[1]]:
            start_x = int(pair[0].pos.x) + WIN_WIDTH/2
            start_y = int(pair[0].pos.y) + WIN_HEIGHT/2
            end_x = int(pair[1].pos.x) + WIN_WIDTH/2
            end_y = int(pair[1].pos.y) + WIN_HEIGHT/2
            pygame.draw.line(surface, Color('#ffffff'), (start_x, start_y), (end_x, end_y)) 

def main():
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY)
    pygame.display.set_caption("Story of life")
    bg = Surface(DISPLAY)

    bg.fill(Color(BACKGROUND_COLOR))

    fps_per_iteration = 20
    i = 0

    creature = Organism('A', 'A(A),c>=0,p==0 :++B \nB(), c >=0,p<2 :++B \nB(B),c>=0,p>=0 :C \nA(A),c>=0,p>=0 :G \nC(B), c==1,p>=0 :G \nG(G), c <=5,p>=0 :++H')
    while 1:
        bg.fill((0, 0, 0))
        # if changed:
        spring_layout(creature.graph, WIN_WIDTH - 300, WIN_HEIGHT - 300, iterations=100)
        draw_graph(bg, creature.graph)
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                sys.exit()
        screen.blit(bg, (0, 0))
        pygame.display.update()

        if i >= fps_per_iteration:
            if creature.iterate():
                i = 0
        i += 1
        

if __name__ == "__main__":
    main()