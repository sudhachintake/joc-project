from abc import ABC, abstractmethod
from collections import namedtuple
from numbers import Number
import pygame.draw
import pygame.font
from pygame import Rect

#Abstract parent class for all Scenes
class Scene(ABC):
    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def handle_events(self, events):
        pass

    @abstractmethod
    def render(self, screen):
        pass

class Button:
    def __init__(self, text, position, padding):
        font = pygame.font.SysFont('cursive', 30)
        p2 =  tuple(2 * x for x in padding)
        size = font.size(text) 
        size = tuple((size[0]+p2[0], size[1]+p2[1]))
        self.text = font.render(text, True, 'white')
        (x, y) = position
        (a, b) = size
        self.rect = Rect(x, y, a, b)
        self.text_pos = position
        self.text_pos = tuple((self.text_pos[0]+ padding[0], self.text_pos[1]+ padding[1]))
        
    #draw rectangle around button
    def draw(self, screen):
        pygame.draw.rect(screen, 'white', self.rect, 3)
        screen.blit(self.text, self.text_pos)

class BackButton(Button):
    def __init__(self):
        super().__init__("Back", (50, 50), (10, 5))

#load images
def get_image(file):
    image = pygame.image.load(file).convert_alpha()
    return image
