import pygame
from pygame.locals import *
from random import random
from time import sleep  # To remove

class GUI(object):
    def __init__(self, ecosystem):
        self.size_organism = 4
        self.ecosystem = ecosystem
        size_pixels_x = ecosystem.biotope.size_x * self.size_organism
        size_pixels_y = ecosystem.biotope.size_y * self.size_organism
        pygame.init()
        self.windowSurface = pygame.display.set_mode((size_pixels_x,
                                                      size_pixels_y),
                                                     0, 32)
        pygame.display.set_caption('Ecosystems')
    def draw_ecosystem(self):
        ecosystem = self.ecosystem
        # Draw organisms
        self.windowSurface.fill((0, 0, 0))
        for organism in ecosystem.organisms:

            # Get organism information
            # TODO: access by organism.get_x() or similar
            o_x = organism['status']['coordinates']['x'] * self.size_organism
            o_y = organism['status']['coordinates']['y'] * self.size_organism

            # Draw organism
            # TODO: Define proper color
            if organism['genes']['speed'] == 0.0:
                o_color = (0, 150, 0)
            else:
                o_color = (200, 200, 200)

            px_begin = 1
            px_end = self.size_organism - 1
            pygame.draw.polygon(self.windowSurface,
                                o_color,
                                ((o_x + px_begin, o_y + px_begin),
                                 (o_x + px_end, o_y + px_begin),
                                 (o_x + px_end, o_y + px_end),
                                 (o_x + px_begin, o_y + px_end)))
        pygame.display.update()

    def draw_substance(self, substance_code):
        substance = self.ecosystem.biotope.substance(substance_code)
        px_begin = 1
        px_end = self.size_organism - 1
        for x in range(self.ecosystem.biotope.size_x):
            for y in range(self.ecosystem.biotope.size_y):
                s_x = x * self.size_organism
                s_y = y * self.size_organism
                pygame.draw.polygon(self.windowSurface,
                                substance.color(x, y),
                                ((s_x + px_begin, s_y + px_begin),
                                 (s_x + px_end, s_y + px_begin),
                                 (s_x + px_end, s_y + px_end),
                                 (s_x + px_begin, s_y + px_end)))
        pygame.display.update()
                

    def handle_events(self):
        pass  # Get events and modify Ecosystem accordingly

    def delete(self):
        pygame.quit()
