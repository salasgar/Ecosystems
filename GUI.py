import pygame
from Basic_tools import *
from Geology_settings import *
# from pygame.locals import *
# from random import random
# sfrom time import sleep  # To remove


class GUI(object):

    def __init__(self, parent_ecosystem):
        self.zoom = 4  # TODO: Redefine somewhere else
        self.parent_ecosystem = parent_ecosystem
        (self.size_x, self.size_y) = \
            parent_ecosystem.biotope['size']
        size_pixels_x = self.size_x * self.zoom
        size_pixels_y = self.size_y * self.zoom
        # Pygame initialization
        pygame.init()
        self.windowSurface = pygame.display.set_mode((size_pixels_x,
                                                      size_pixels_y),
                                                     0, 32)
        pygame.display.set_caption('Ecosystems')

    def draw_ecosystem(self):
        # Draw organisms
        self.windowSurface.fill((0, 0, 0))
        if draw_geology:
            for i in range(self.parent_ecosystem.biotope.size_x()):
                for j in range(self.parent_ecosystem.biotope.size_y()):
                    color = (
                        # RED:
                        make_color_component(
                            self.parent_ecosystem.biotope.biotope_features[
                                'altitude'].get_value(
                                float(i)/self.size_x,
                                float(j)/self.size_y,
                                )
                            - 0.2 *
                            self.parent_ecosystem.biotope.biotope_features[
                                'water depth'].get_value(
                                float(i)/self.size_x,
                                float(j)/self.size_y,
                                ),
                            factor=0.3
                            ),
                        # GREEN:
                        make_color_component(
                            rain(
                                float(i)/self.size_x,
                                float(j)/self.size_y,
                                self.parent_ecosystem.time
                                ),
                            factor=0.4
                            ),
                        # BLUE:
                        make_color_component(
                            self.parent_ecosystem.biotope.biotope_features[
                                'water depth'].get_value(
                                float(i)/self.size_x,
                                float(j)/self.size_y,
                                ),
                            factor=0.1
                            )
                    )
                    x = i * self.zoom
                    y = j * self.zoom
                    pygame.draw.polygon(
                        self.windowSurface,
                        color,
                        ((x, y),
                         (x + self.zoom, y),
                         (x + self.zoom, y + self.zoom),
                         (x, y + self.zoom))
                        )

        for organism in self.parent_ecosystem.organisms_list:
            # Get organism information
            # TODO: access by organism.get_x() or similar
            o_x = organism['location'][0] * self.zoom
            o_y = organism['location'][1] * self.zoom
            # Draw organism
            # TODO: Define proper color
            if 'color' in organism:
                o_color = organism['color']
                # print o_color
            elif 'speed' in organism and organism['speed'] == 0.0:
                o_color = (0, 150, 0)
            else:
                o_color = (200, 200, 200)
            px_begin = 1
            px_end = self.zoom - px_begin
            pygame.draw.polygon(
                self.windowSurface,
                o_color,
                ((o_x + px_begin, o_y + px_begin),
                 (o_x + px_end, o_y + px_begin),
                 (o_x + px_end, o_y + px_end),
                 (o_x + px_begin, o_y + px_end)))
        pygame.display.update()

    def draw_featuremap(self, featuremap_code):
        featuremap = self.parent_ecosystem.biotope.get_featuremap(
                featuremap_code)
        px_begin = 1
        px_end = self.zoom - 1
        for x in range(self.ecosystem.biotope.size_x):
            for y in range(self.ecosystem.biotope.size_y):
                s_x = x * self.zoom
                s_y = y * self.zoom
                # Lo del color esta todavia sin implementar
                pygame.draw.polygon(self.windowSurface,
                                    featuremap.color(x, y),
                                    ((s_x + px_begin, s_y + px_begin),
                                     (s_x + px_end, s_y + px_begin),
                                     (s_x + px_end, s_y + px_end),
                                     (s_x + px_begin, s_y + px_end)))
        pygame.display.update()

    def handle_events(self):
        """
        # Este metodo no deberia llamar a algun metodo como
        # pygame.handle_events o algo asi?
        """
        pass  # Get events and modify Ecosystem accordingly

    def delete(self):
        pygame.quit()
