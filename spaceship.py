from utils import *
import menus
import pygame as pg
from pygame.locals import *
import pickle
from setup import GameSettings as Settings
import interval

LEVELS=pickle.load(open(r'joc project\\levels','rb'))

class SpaceShipScene(Scene):
    def __init__(self,state):
        super(SpaceShipScene, self).__init__()
        self.state=state
        self.back=BackButton()
        self.levels=LEVELS[state['level']]
        
        if self.state['ship']==None:
            self.state['ship']=[True]*len(self.levels)

        self.space_ship=pg.sprite.Group()
        time=self.state['curr_time']-self.state['start_time']
        for i in range(len(self.levels)):
            if self.state['ship'][i]:
                disrupt='disrupt' in self.levels[i]
                broken=self.levels[i]['broken'] if 'broken' in self.levels[i] else {}
                self.space_ship.add(SpaceShip(self.levels[i],time,i,disrupt,broken))
        
        self.bg=pg.image.load(r'joc project\\images\\space-background.png')

    def render(self,scene):
        lose=[s for s in self.space_ship if s.rect.x<100 ]
        if len(lose)>0:
            self.manager.go_to(menus.LoseScene(self.state))
        
        if sum(self.state['ship'])==0:
            self.state['level_progress']=self.state['level']+1
            self.manager.go_to(menus.WinScene(self.state))
        screen.blit(self.bg,(0,0))
        self.back.draw(screen)
        self.space_ship.draw(screen)

    def update(self):
        self.space_ship.update()

    def handleEvents(self, events):
        for e in events:
            if e.type==MOUSEBUTTONUP:
                pos=pg.mouse.get_pos()
                ship=[s for s in self.space_ship in s.rect.collidepoint(pos)]
                if len(ship)>0:
                    self.state['ship_num']=ship[0].num
                    self.state['curr_time']=pg.time.get_ticks()
                    self.state['disrupt']=ship[0].disrupt
                    self.state['broken']=ship[0].broken
                    self.manager.go_to(interval.IntervalScene(ship[0].signals,ship[0].lose_time(),self.state))
                elif self.back.rect.collidepoint(pos):
                    self.manager.go_to(menus.GameScene(self.state))


class SpaceShip(pg.sprite.Sprite):
    def __init__(self,ship,time,num,disrupt=False,broken={}):
        super().__init__()
        self.signals=ship['signals']
        self.num=num
        self.image=pg.Surface([40,40])
        self.image=getImage(r'joc project\\images\\enemy_in_ship.png')
        self.rect=self.image.get_rect()
        self.cycles=0
        self.limit=4
        self.rect.x=ship['x']-time/1000*Settings.FPS/self.limit
        self.rect.y=ship['y']
        self.disrupt=disrupt
        self.broken=broken

        if disrupt:
            pg.draw.rect(self.image, 'springgreen', pg.Rect(0, 0, 80, 56),3)
        
        if len(broken)>0:
            pg.draw.polygon(self.image, 'red', [(1,6),(20,12),(1,18)],3)

    def update(self):
        self.cycles+=1

        if self.cycles==self.limit:
            self.cycles=0
            self.rect.x-=1

    
    def lose_time(self):
        return (self.rect.x-100)/(Settings.FPS/self.limit/1000)


    







        
