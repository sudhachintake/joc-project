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
    
    def __abs__(self):
        pass

    def add(self,other):
        if not isinstance(other, Vector):
            raise TypeError(f"{other} is not a Vector")
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x,y)
    
    def mult(self,other):
        if isinstance(other, Number):
            return Vector(other*self.x, other*self.y)
        else:
            TypeError("Can't multiply")

            


class Button:
    def __init__(self,text,position,padding):
        font=pygame.font.SysFont('cursive', 13)
        size=Vector(*font.size(text)) + 2*Vector(*padding)
        self.text=font.render(text, True, 'white')
        self.rect=Rect((50,50),(33,23))
        self.text_pos=Vector(*position) + Vector(*padding)

    def draw(self,screen):
        pygame.draw.rect(screen, white, self.rect,3)
        screen.blit(self.text,self.text_pos)

class BackButton(Button):
    def __init__(self):
        super().__init__("Back", Vector(50, 50),Vector(10, 5))

class TextBox:
    def __init__(self,text,bgColor,maxSize,style):
        font=pg.font.SysFont(style["font"]["family"],style["font"]["size"])
        fontHeight=font.size("Tg")[1]
        lineSpacing=style["paragraph"]["spacing"]
        color=style["font"]["color"]
        margin=style["text"]["margin"]
        width,maxHeight=maxSize
        paragraphs = text.split('\n')
        lines = []
        for p in paragraphs:
            p_lines, _ = self._split_text(
                p, font, width, font_height, line_spacing, max_height)
            lines.extend(p_lines)
            lines.append('')
        lines.pop()  # remove last extra line.

        height = len(lines) * (font_height + line_spacing) - line_spacing
        size = Vector(width, height)
        self.image = Surface(size + 2 * margin)
        self.image.fill(bgcolor)
        offset = Vector(*margin)
        for line in lines:
            text_image = font.render(line, True, color, bgcolor)
            text_image.set_colorkey(bgcolor)
            self.image.blit(text_image, offset)
            offset += Vector(0, font_height + line_spacing)

        self.rect = self.image.get_rect()

    def draw(self, screen, offset=None):
        if offset is None:
            offset = Vector(*screen.get_size()) / 2
            offset -= Vector(*self.image.get_size()) / 2
        screen.blit(self.image, offset)
        self.rect = self.image.get_rect()
        self.rect.move_ip(*offset)

    @staticmethod
    def _split_text(text, font, line_width, font_height, line_spacing,
                    max_height=float('inf')):
        lines = []
        height = 0
        while text:
            # Determine if the row of text will be outside our area
            if height + font_height > max_height:
                break

            # Determine last character that fits.
            for i in range(len(text)):
                if font.size(text[:i + 1])[0] > line_width:
                    break
            else:
                i += 1

            # Adjust to last word.
            if i < len(text):
                try:
                    # Wrap last word.
                    line_end = text.rindex(" ", 0, i)
                    next_start = line_end + 1
                except ValueError:
                    # Very long word overflowing line.
                    line_end = i
                    next_start = i
            else:
                # Remaining text shorter than line.
                line_end = i
                next_start = i

            # Remove this line.
            lines.append(text[:line_end])
            text = text[next_start:]

            height += font_height + line_spacing

        return lines, text

def getImage(file):
    image=pygame.image.load(file).convert_alpha()
    return image

