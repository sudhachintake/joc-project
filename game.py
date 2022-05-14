import pygame as pg
from menus import *
from setup import GameSettings as Settings

#for pygame 1st scene
class SceneManager:

    def __init__(self, firstScene):
        self.go_to(firstScene)
    
    #next scene it should go to
    def go_to(self, scene):
        self.scene = scene
        self.scene.manager = self

#main function
def main():

    #initialize pygame screen
    pg.init()

    #set parameters
    screen = pg.display.set_mode([Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT])

    #window name
    pg.display.set_caption('GAME WINDOW')

    #pygame timer
    timer = pg.time.Clock()

    #while game is continuing
    running = True

    #initialize manager
    manager = SceneManager(TitleScene())

    while running:

        #starting timer with decided freq
        timer.tick(Settings.FPS)

        #if clicked quit, the stop
        if pg.event.get(QUIT):
            running = False
            return

        # scenes managing 
        manager.scene.handle_events(pg.event.get())
        manager.scene.update()
        manager.scene.render(screen)

        #update contents of entire screen
        pg.display.flip()

if __name__ == "__main__":
    main()
