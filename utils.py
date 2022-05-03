from abc import ABC,abstractmethod
from collections import namedtuple
from numbers import Number
import pygame.draw
import pygame.font
from pygame import Rect,Surface
 

class Scene(ABC):
    @abstractmethod
    def update(self):
        pass
    @abstractmethod
    def handleEvents(self,events):
        pass
    @abstractmethod
    def render(self,screen):
        pass

class Vector(namedtuple('Vector', ['x','y'])):
    def __neg__(self):
        return Vector(-self.x,-self.y)
    
    def __abs__(self):
        pass

    def add(self,other):
        if not isinstance(other, Vector):
            raise TypeError(f"{other} is not a Vector")
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x,y)
    
    def mult(self,other):
        if not isinstance(other, Vector):
            raise TypeError(f"{other} is not a Vector")
        x = self.x * other.x
        y = self.y * other.y
        return Vector(x,y)

class Button:
    def __init__(self,text,position,padding):
        font=pygame.font.SysFont('cursive', 13)
        size=Vector(*font.size(text)) + 2*Vector(*padding)
        self.text=font.render(text, True, white)
        self.rect=Rect(position,size)
        self.text_pos=Vector(*position) + Vector(*padding)

    def draw(self,screen):
        pygame.draw.rect(screen, white, self.rect,3)
        screen.blit(self.text,self.text_pos)

class BackButton(Button):
    def __init__(self):
        super.__init__("Back", Vector(50, 50),Vector(10, 5))

class TextBox:
    pass

def getImage(file):
    image=pygame.image.load(file).convert_alpha()
    return image

