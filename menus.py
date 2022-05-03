import pygame as pg
from utils import *
from pygame.locals import *
from narratives import Narratives
import pickle

class TitleScene(Scene):


    def __init__(self):
        super(TitleScene,self).__init__()
        self.sfont=pg.font.SysFont('cursive', 32)
        self.state={"level_progress":0,"num_levels":0}
        self.state[num_levels]=len(pickle.load(open(r"joc project\\levels",encoding='UTF8')))



   
    def update(self):
        pass


   
    def handleEvents(self,events):
        for e in events:
            if e.type==MOUSEBUTTONUP:
                scene=GameScene(self.state)
                self.manager.go_to(NarrativeScene(Narratives.intro,self.state,scene))
            if e.type==KEYDOWN:
                if e.key==K_0:
                    self.state["level_progress"]=self.state["num_levels"]
            
        


   
    def render(self,screen):
        screen.fill("black")
        logo=getImage(r"joc project\images\logo.png")
        screen.blit(logo,(250,100))
        text=self.sfont.render("Click anywhere to Begin",True,"white")
        screen.blit(text,(180,450))

        
class GameScene(Scene):
    def __init__(self,state):
        self.state=state
        self.font=pg.font.SysFont('cursive', 70)
        self.back=BackButton()
        self.level_squares=pg.sprite.Group()

        for i in range(self.state['num_levels']):
            available=(i<=self.state['level_progress'])
            self.level_squares.add(LevelSquare(50+150*i,300,i,available))
    
    def render(self,screen):
        screen.fill("black")
        pg.draw.rect(screen, 'white', Rect(250, 100, 300, 100),5)
        text=self.font.render('levels', True, 'white')
        screen.blit(text,(275,110))
        self.back.draw(screen)

        for ls in self.level_squares:
            ls.draw(screen)

    def update(self):
        pass

    def handleEvents(self, events):
        for e in events:
            if e.type==MOUSEBUTTONUP:
                pos=pg.mouse.get_pos()
                lvl=[l for l in self.level_squares if l.rect.collidepoint(pos)]
                if len(lvl)>0 and lvl[0].available:
                    level_state={'level':lvl[0].level,'ship_num':None,'ship':None,'start_time':pg.time.get_ticks(),'curr_time':pg.time.get_ticks()}
                    state={**self.state,**level_state}
                    scene=SpaceShip(state)
                    if len(Narratives.levels[lvl[0].level])>0:
                        self.manager.go_to(Narratives.levels[lvl[0].level],state,scene)
                    else:
                        self.manager.go_to(scene)

                elif self.back.rect.collidepoint(pos):
                    scene=GameScene(self.state)
                    self.manager.go_to(NarrativeScene(Narratives.intro,self.state,scene))
                 

class TrasitionScene(Scene):
    def __init__(self,msg,color,state):
        super(TrasitionScene,self).__init__()
        self.font=pg.font.SysFont('cursive', 36)
        self.sfont=pg.font.SysFont('cursive', 30)
        self.msg=msg
        self.color=color
        self.state=state

    def render(self, screen):
        screen.fill(self.color)
        text1=self.font.render(self.msg, True, 'white')
        text2=self.sfont.render('click anyware to continue', True, 'white')
        screen.blit(text1,(200,50))
        screen.blit(text2,(200,350))

    def update(self):
        pass

    def handleEvents(self, events):
        for e in events:
            if e.type==MOUSEBUTTONUP:
                self.manager.go_to(GameScene(self.state))


class WinScene(TrasitionScene):
    def __init__(self,state):
        super(WinScene,self).__init__('you have won this level',(50,100,50),state)

class LoseScene(TrasitionScene):
    def __init__(self,state):
        super(LoseScene,self).__init__('you have Lost this level',(120,30,30),state)
    

class NarrativeScene(Scene):
    pass

class LevelSquare(pg.sprite.Sprite):
    def __init__(self,x,y,level,available):
        super().__init__()
        self.font=pg.font.SysFont('cursive', 80)
        self.image=pg.Surface([100,100])
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.level=level
        self.available=available

        if self.available:
            self.color='white'
        else:
            self.color='gray'
        
    def draw(self,screen):
        pg.draw.rect(screen, self.color, self.rect,5)
        text=self.font.render(str(self.level+1), True, self.color)
        screen.blit(text,(self.rect.x+25,self.rect.y+5))


