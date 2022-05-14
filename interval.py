import pygame as pg
from utils import *
import menus

#approx difference between notes
SEMITONE_MAP = [0, 2, 4, 5, 7, 9, 11, 12]

# Gems displayed (notes of music)
class Gem(pg.sprite.Sprite):

    def __init__(self, x, y, tone):
        super().__init__()
        self.image = get_image("JOCProject\spacegem-python\images\gem"+ str(tone) +".png").subsurface(pg.Rect(0,0,56,58))

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.tone = tone

# interval scene (freq of notes)
class IntervalScene(Scene):
    
    def __init__(self, signals, lose_time, state):
        super(IntervalScene, self).__init__()

        self.sprites = pg.sprite.Group() #hold and manage multiple sprites
        self.flag = ErrorFlag() #success or failure in guessing the tone...sq on right bottom corner
        self.timeremaining = TimeRemaining(lose_time)
        self.sprites.add(self.flag)
        self.sound = SoundDisplay(self.flag)
        self.gems = pg.sprite.Group()

        #adding gems
        for i in range(8):
            if i not in state["broken"]:
                self.gems.add(Gem(52 + i*60, 440, i))

        #given notes
        self.signals = signals
        self.sound.signal = signals[0]

        #variable for sublevels of that specific ship
        self.interval_num = 0

        self.lose_time = lose_time
        self.state = state

        #for playing audio
        pg.mixer.init()
        #playing initial sound
        self.gem_channel = pg.mixer.find_channel()
        self.sig_channel = pg.mixer.find_channel()
        self.play_notes(self.sig_channel,self.sound.signal)

        self.new_mouse_gem = False
        self.mouseover = 0

        self.bg = pg.image.load("JOCProject\spacegem-python\images\\transmission-background.png")

    #elements on screen
    def render(self, screen):

        #if time up
        if pg.time.get_ticks() - self.state["curr_time"] > self.lose_time:
            self.manager.go_to(menus.LoseScene(self.state))

        #putting all the sprites on screen
        screen.blit(self.bg, (0,0)) #background
        self.gems.draw(screen) # 8 gems
        self.sound.draw(screen, self.state["disrupt"]) # sound peaks
        self.sprites.draw(screen) # flag
        self.timeremaining.draw(screen, self.lose_time-(pg.time.get_ticks() - self.state["curr_time"])) #time bar

        #playing sound when mouse pointer is on some gem
        gem = self.mouse_gem()

        if len(gem) > 0 and (self.mouseover != gem[0].tone):
            self.mouseover = gem[0].tone
            self.new_mouse_gem = True

        elif len(gem) == 0 and self.mouseover >= 0:
            self.mouseover = -1
            self.gem_channel.stop()

        if self.new_mouse_gem:
            self.play_notes(self.gem_channel,[self.mouseover], long_note = True)
            self.new_mouse_gem = False

    def update(self):
        pass

    # handling mouse clicks
    def handle_events(self, events):
        for e in events:
            if e.type == pg.MOUSEBUTTONUP:
                pos = pg.mouse.get_pos()
                gem = self.mouse_gem()

                #if clicked on gem
                if len(gem) > 0:
                    correct = self.sound.update_text(gem[0].tone)

                    if correct:
                        self.interval_num += 1
                        
                        #if still signal (notes) is there, continuing
                        if self.interval_num < len(self.signals):
                            self.sound.signal = self.signals[self.interval_num]

                            
                        else: #returning to spaceship screen
                            self.state["ships"][self.state["ship_num"]] = False
                            self.state["curr_time"] = pg.time.get_ticks()
                            from spaceships import SpaceshipScene
                            self.manager.go_to(SpaceshipScene(self.state))

                        #playing next given notes
                        self.play_notes(self.sig_channel,self.sound.signal)

                #listen again (given notes)
                elif pg.Rect(160, 340, 190, 38).collidepoint(pos):
                    self.play_notes(self.sig_channel,self.sound.signal)

    #get gem on which move is hovered
    def mouse_gem(self):
        pos = pg.mouse.get_pos()
        gem = [g for g in self.gems if g.rect.collidepoint(pos)]
        return gem

    #can only take up to 2 notes
    def play_notes(self, channel, notes, long_note = False):
        if long_note:
            path = "JOCProject\spacegem-python\sounds\long\\"
        else:
            path = "JOCProject\spacegem-python\sounds\short\\"

        channel.play(pg.mixer.Sound(path+str(notes[0])+".wav"))

        if len(notes) > 1:
            channel.queue(pg.mixer.Sound(path+str(notes[1])+".wav"))

class SoundDisplay:

    def __init__(self, flag):
        self.notes = []
        self.flag = flag
        self.signal = [0,0]

    #draw feq. peak
    def draw_peaks(self, note, signal_number, color, screen):
        peak = SEMITONE_MAP[note]
        pointlist = [(75+100*signal_number, 320),
            (125+100*signal_number, 305-peak*15),
            (175+100*signal_number, 320)]
        pg.draw.polygon(screen, color, pointlist, 3)

    # checking notes selected are correct or not
    def update_text(self, note):
        correct = False

        #when nothing selected, or both selected is incorrect
        if len(self.notes) == 0 or len(self.notes) == 2:
            self.flag.update_status('black')
            self.notes = [note]

        # when 1st is selected, check for next
        elif len(self.notes) == 1:
            diff = abs(SEMITONE_MAP[note] - SEMITONE_MAP[self.notes[0]])

            #when correct
            if diff == SEMITONE_MAP[self.signal[1]]-SEMITONE_MAP[self.signal[0]]:
                self.flag.update_status('green') #updating flag
                correct = True

            #when wrong
            else:
                self.flag.update_status('red') #updating flag

            #appending 2nd note
            self.notes.append(note)

            #2nd peak should stay awhile, variable to do so.
            self.complete_time = pg.time.get_ticks()
        return correct

    #drawing peaks
    def draw(self, screen, disrupt):

        #when nothing selected, or both selected is incorrect
        if len(self.notes) == 2 and pg.time.get_ticks() - self.complete_time > 1000:
            self.flag.update_status('black')
            self.notes = []

        if not disrupt:
            self.draw_peaks(self.signal[0], 0, 'blue', screen)
            self.draw_peaks(self.signal[1], 1.5, 'blue', screen)

        #peaks for selected notes
        if len(self.notes) > 0:
            self.draw_peaks(self.notes[0], 4, 'blue', screen)
        if len(self.notes) > 1:
            self.draw_peaks(self.notes[1], 5.5, 'blue', screen)

#Error flag for success or failure
class ErrorFlag(pg.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pg.Surface([76, 76])
        
        self.rect = self.image.get_rect()
        self.rect.y = 432
        self.rect.x = 612

    def update_status(self, color):
        self.image.fill(color)

#remaining time
class TimeRemaining:
    def __init__(self, total_time):
        self.total_time = total_time
        self.remaining_time = total_time

    #drawing time bar
    def draw(self, screen, remaining_time):
        width = (remaining_time/self.total_time)*370
        if width > 74:
            color = 'green'
        else:
            color = 'red'
        pg.draw.rect(screen, color, pg.Rect(310, 540, width, 20))

