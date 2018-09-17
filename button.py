import pygame
import sys
import random
from pygame.locals import *


class Button:
    def __init__(self, rect, command, **kwargs):
        self.process_kwargs(kwargs)
        self.rect = pygame.Rect(rect)
        self.image = pygame.Surface(self.rect.size).convert()
        self.function = command
        self.text = self.font.render(self.text, True, self.font_color)
        self.text_rect = self.text.get_rect(center=self.rect.center)

    def process_kwargs(self, kwargs):
        settings = {
            'color': pygame.Color('red'),
            'text': 'default',
            'font': pygame.font.Font("freesansbold.ttf", 24),
            'hover_color': (200, 0, 0),
            'font_color': pygame.Color('white'),
        }
        for kwarg in kwargs:
            if kwarg in settings:
                settings[kwarg] = kwargs[kwarg]
            else:
                raise AttributeError("{} has no keyword: {}".format(
                    self.__class__.__name__, kwarg))
        self.__dict__.update(settings)

    def on_click(self):
        if self.is_hovering():
            self.function()

    def is_hovering(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            return True

    def draw(self, surf):
        if self.is_hovering():
            self.image.fill(self.hover_color)
        else:
            self.image.fill(self.color)
        surf.blit(self.image, self.rect)
        surf.blit(self.text, self.text_rect)
