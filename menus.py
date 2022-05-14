import pygame as pg
from pygame.locals import *
from utils import *
from spaceships import *
from narratives import Narratives
import pickle

#logo
class TitleScene(Scene):

    def __init__(self):
        super(TitleScene, self).__init__()
        self.sfont = pg.font.SysFont('Cursive', 32)
        self.state = {"level_progress": 0, "num_levels": 0}
        self.state["num_levels"] = len(pickle.load(open("JOCProject\spacegem-python\levels", "rb")))

    def render(self, screen):
        screen.fill('black')
        logo = get_image("JOCProject\spacegem-python\images\logo.png")
        screen.blit(logo, (250,100))
        text = self.sfont.render('Click anywhere to begin', True, (255, 255, 255))
        screen.blit(text, (180, 450))

    def update(self):
        pass

    def handle_events(self, events):

        #when clicked anywhere goto welcome narrative
        for e in events:
            if e.type == MOUSEBUTTONUP:
                scene = GameScene(self.state) #passing number of levels
                self.manager.go_to(NarrativeScene(Narratives.intro, self.state, scene))
            #if '0'-cheatcode is pressed unlock all levels
            if e.type == KEYDOWN:
                if e.key == K_0:
                    self.state["level_progress"] = self.state["num_levels"]

# Display level menu
class GameScene(Scene):

    def __init__(self, state):
        self.state = state
        self.font = pg.font.SysFont('Cursive', 70)
        #backbutton
        self.back = BackButton()
        #group of level sq.
        self.levelsquares = pg.sprite.Group()

        #adding level sq.
        for i in range(self.state["num_levels"]):
            available = (i <= self.state["level_progress"])
            self.levelsquares.add(LevelSquare(50+150*i, 300, i, available))

    def render(self, screen):

        screen.fill('black')
        pg.draw.rect(screen, 'white', Rect(250,100,300,100), 5)
        text = self.font.render("Levels", True, 'white')
        screen.blit(text, (275,110))
        self.back.draw(screen)

        #drawing level squares
        for ls in self.levelsquares:
            ls.draw(screen)

    def update(self):
        pass

    def handle_events(self, events):
        for e in events:
            if e.type == MOUSEBUTTONUP:
                pos = pg.mouse.get_pos()

                #when clicked on any level square
                lvl = [l for l in self.levelsquares if l.rect.collidepoint(pos)]
                if len(lvl) > 0 and lvl[0].available:
                    #creating dictionary for its state
                    level_state = {
                                "level": lvl[0].level,
                                "ship_num": None,
                                "ships": None,
                                "start_time": pg.time.get_ticks(),
                                "curr_time": pg.time.get_ticks()
                                }
                    
                    # adding these key value pair to state
                    state = {**self.state, **level_state}
                    scene = SpaceshipScene(state)

                    #if narratives, display it
                    if len(Narratives.levels[lvl[0].level]) > 0:
                        self.manager.go_to(NarrativeScene(Narratives.levels[lvl[0].level], state, scene))
                    else: #goto next scene
                        self.manager.go_to(scene)
                
                #if backbutton pressed go back 1 scene
                elif self.back.rect.collidepoint(pos):
                    scene = GameScene(self.state)
                    self.manager.go_to(NarrativeScene(Narratives.intro, self.state, scene))

#parent class of win and lose between levels
class TransitionScene(Scene):
    def __init__(self, message, color, state):
        super(TransitionScene, self).__init__()
        self.font = pg.font.SysFont('Cursive', 36)
        self.sfont = pg.font.SysFont('Cursive', 30)
        self.message = message
        self.color = color
        self.state = state

    def render(self, screen):
        screen.fill(self.color)
        text1 = self.font.render(self.message, True, 'white')
        text2 = self.sfont.render('Click anywhere to continue', True, 'white')
        screen.blit(text1, (200, 50))
        screen.blit(text2, (200, 350))

    def update(self):
        pass

    def handle_events(self, events):
        #continue when clicked
        for e in events:
            if e.type == MOUSEBUTTONUP:
                self.manager.go_to(GameScene(self.state))
                
#if win
class WinScene(TransitionScene):
    def __init__(self, state):
        super(WinScene, self).__init__('You\'ve won this level', (50, 100, 50), state)

# if lose
class LoseScene(TransitionScene):
    def __init__(self, state):
        super(LoseScene, self).__init__('You\'ve lost this level', (120, 30, 30), state)

#generating levelSquare
class LevelSquare(pg.sprite.Sprite):

    def __init__(self, x, y, level, available):
        super().__init__()
        self.font = pg.font.SysFont('Cursive', 80)
        self.image = pg.Surface([100, 100])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.level = level

        #decide availability on level progress
        self.available = available
        if self.available:
            self.color = 'white'
        else:
            self.color = 'dimgray'

    #draw level squares
    def draw(self, screen):
        pg.draw.rect(screen, self.color, self.rect, 5)
        text = self.font.render(str(self.level), True, self.color)
        screen.blit(text, (self.rect.x+25,self.rect.y+5))

#narratives of game
class NarrativeScene(Scene):
    def __init__(self, texts, state, scene):
        super(NarrativeScene, self).__init__()
        self.font = pg.font.SysFont('Cursive', 32)
        self.texts = texts
        self.text_num = 0
        self.state = state
        self.scene = scene
        self.bg = pg.image.load("JOCProject\spacegem-python\images\\narrative-background.jpg")

    def render(self, screen):
        screen.blit(self.bg, (0,0))
        self.drawText(screen, self.texts[self.text_num])

    def update(self):
        pass

    def handle_events(self, events):
        for e in events:
            if e.type == MOUSEBUTTONUP:
                pos = pg.mouse.get_pos()
                #if pressed on next
                if pg.Rect(380, 500, 120, 50).collidepoint(pos):
                    self.manager.go_to(self.scene)

    #displaying text
    def drawText(self, screen, text):
        rect = pg.Rect(50,70,700,450)
        y = rect.top
        lineSpacing = -2
        fontHeight = self.font.size("Tg")[1]

        while text:
            i = 1
            while self.font.size(text[:i])[0] < rect.width and i < len(text):
                i += 1
            if i < len(text):
                i = text.rfind(" ", 0, i) + 1
            image = self.font.render(text[:i], True, 'white')
            screen.blit(image, (rect.left, y))
            y += fontHeight + lineSpacing
            text = text[i:]
        return text