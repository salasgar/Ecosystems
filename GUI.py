import pygame
# from pygame.locals import *
# from random import random
# sfrom time import sleep  # To remove


class GUI(object):

    def __init__(self, parent_ecosystem):
        self.zoom = 4  # TODO: Redefine somewhere else
        self.parent_ecosystem = parent_ecosystem
        (biotope_size_x, biotope_size_y) = \
            parent_ecosystem.biotope['dimensions']
        size_pixels_x = biotope_size_x * self.zoom
        size_pixels_y = biotope_size_y * self.zoom
        # Pygame initialization
        pygame.init()
        self.windowSurface = pygame.display.set_mode((size_pixels_x,
                                                      size_pixels_y),
                                                     0, 32)
        pygame.display.set_caption('Ecosystems')

    def draw_ecosystem(self):
        # Draw organisms
        self.windowSurface.fill((0, 0, 0))
        for organism in self.parent_ecosystem.organisms:
            # Get organism information
            # TODO: access by organism.get_x() or similar
            o_x = organism['location'][0] * self.zoom
            o_y = organism['location'][1] * self.zoom
            # Draw organism
            # TODO: Define proper color
            if organism['speed'] == 0.0:
                o_color = (0, 150, 0)
            else:
                o_color = (200, 200, 200)
            px_begin = 1
            px_end = self.zoom - 1
            pygame.draw.polygon(self.windowSurface,
                                o_color,
                                ((o_x + px_begin, o_y + px_begin),
                                 (o_x + px_end, o_y + px_begin),
                                 (o_x + px_end, o_y + px_end),
                                 (o_x + px_begin, o_y + px_end)))
        pygame.display.update()

    def draw_substance(self, substance_code):
        substance = self.parent_ecosystem.biotope.get_substance(
                substance_code)
        px_begin = 1
        px_end = self.zoom - 1
        for x in range(self.ecosystem.biotope.size_x):
            for y in range(self.ecosystem.biotope.size_y):
                s_x = x * self.zoom
                s_y = y * self.zoom
                # Lo del color esta todavia sin implementar
                pygame.draw.polygon(self.windowSurface,
                                    substance.color(x, y),
                                    ((s_x + px_begin, s_y + px_begin),
                                     (s_x + px_end, s_y + px_begin),
                                     (s_x + px_end, s_y + px_end),
                                     (s_x + px_begin, s_y + px_end)))
        pygame.display.update()

    def handle_events(self):
        """
        # Este metodo no deberia llamar a algun metodo como pygame.handle_events o algo asi?
        """
        pass  # Get events and modify Ecosystem accordingly

    def delete(self):
        pygame.quit()
