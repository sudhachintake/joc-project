import pygame as pg
from setup import GameSettings as Settings
from menus import *

class SceneManager(object):
    def __init__(self,firstScene):
        self.go_to(firstScene)

    def go_to(self,scene):
        self.scene=scene
        self.scene.manager=self

def main():
    pg.init()
    screen=pg.display.set_mode([Settings.SCREEN_WIDTH,Settings.SCREEN_HEIGHT])
    pg.display.set_caption("GAME WINDOW")
    timer=pg.time.Clock()
    running=True

    manager=SceneManager(TitleScene())

    while running:
        timer.tick(Settings.FPS)

        if pg.event.get(QUIT):
            running=False
            return
        
        manager.scene.handleEvents(pg.event.get())
        manager.scene.update()
        manager.scene.render(screen)
        pg.display.flip()


if __name__=='__main__':
    main()
