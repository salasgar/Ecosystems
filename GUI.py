import pygame
from pygame.locals import *


class GUI(object):
    def __init__(self):
        pygame.init()
        windowSurface = pygame.display.set_mode((500, 400), 0, 32)
        pygame.display.set_caption('Hello world!')

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

    def draw_ecosystem(self, ecosystem):
        pygame.display.update()

    def handle_events(self, ecosystem):
        pass  # Get events and modify Ecosystem accordingly

    def delete(self):
        pygame.quit()
