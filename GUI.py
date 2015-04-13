import pygame
from pygame.locals import *
from random import random


class GUI(object):
    def __init__(self):
        pygame.init()
        self.windowSurface = pygame.display.set_mode((400, 400), 0, 32)
        pygame.display.set_caption('Hello world!')
        """
        # set up fonts
        basicFont = pygame.font.SysFont(None, 48)

        # set up the text
        text = basicFont.render('Hello world!',
                                True,
                                (255, 255, 255),
                                (0, 0, 255))
        textRect = text.get_rect()
        textRect.centerx = windowSurface.get_rect().centerx
        textRect.centery = windowSurface.get_rect().centery
        # draw the text onto the surface
        windowSurface.blit(text, textRect)
        """
    def draw_ecosystem(self, ecosystem):
        # Draw organisms
        self.windowSurface.fill((0, 0, 0))
        for organism in ecosystem.organisms:
            o_attack_capacity = organism['genes']['attack_capacity']
            o_defense_capacity = organism['genes']['defense_capacity']
            o_photo_capacity = organism['genes']['do_photosynthesis']

            o_x = organism['status']['coordinates']['x'] * 4.0  # Temporary
            o_y = organism['status']['coordinates']['y'] * 4.0  # Temporary
            #o_color = (int(o_attack_capacity)%256, int(255 * o_photo_capacity)%256, int(o_defense_capacity)%256)
            o_color = (200, 200, 200)            
            pygame.draw.polygon(self.windowSurface,
                                o_color,
                                ((o_x + 1, o_y + 1),  # Temporary
                                 (o_x + 3, o_y + 1),
                                 (o_x + 3, o_y + 3),
                                 (o_x + 1, o_y + 3)))
            if random()<0.1:
                print "o_x, o_y", o_x/4, o_y/4
        print "printing"

        pygame.display.update()

    def handle_events(self, ecosystem):
        pass  # Get events and modify Ecosystem accordingly

    def delete(self):
        pygame.quit()
