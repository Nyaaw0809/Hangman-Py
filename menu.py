import pygame

class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = - 100

    def draw_cursor(self):
        self.game.draw_text('>', 15, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()

class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 30
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 60
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BG)
            icon = pygame.image.load('HiroLogo.png')

            self.up =  pygame.image.load('up.png')
            self.down =  pygame.image.load('down.png')
            self.enter = pygame.image.load('return.png')
            bg = pygame.image.load('BG.jpg')
            self.game.display.blit(bg,(0,0))
            self.game.display.blit(icon, ((self.game.DISPLAY_W / 2) - 285, (self.game.DISPLAY_H / 2 - 20) - 110))
            self.game.draw_text("Navigate: ", 20, 80, self.game.DISPLAY_H - 50)
            self.game.display.blit(self.up, (140, self.game.DISPLAY_H - 70))
            self.game.display.blit(self.enter, (280, self.game.DISPLAY_H - 70))
            self.game.display.blit(self.down, (210,self.game.DISPLAY_H - 70))
            self.game.draw_text('Hangman', 60, self.game.DISPLAY_W / 2, (self.game.DISPLAY_H / 2 - 20) - 50)

            self.game.draw_text("Start Game", 20, self.startx, self.starty)
            self.game.draw_text("How to Play", 20, self.optionsx, self.optionsy)
            self.game.draw_text("Credits", 20, self.creditsx, self.creditsy)
            self.draw_cursor()
            self.blit_screen()


    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
        elif self.game.UP_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'
        elif self.game.MOUSE_CLICK:
            if self.state == 'Start':
                self.game.playing = True
            elif self.state == 'Options':
                self.game.curr_menu = self.game.options
            elif self.state == 'Credits':
                self.game.curr_menu = self.game.credits
            self.run_display = False


    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Start':
                self.game.playing = True
                self.game.randomize()
                self.game.game_loop()
            elif self.state == 'Options':
                self.game.curr_menu = self.game.options
            elif self.state == 'Credits':
                self.game.curr_menu = self.game.credits
            self.run_display = False

class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.fill(self.game.BG)
            self.up = pygame.image.load('up.png')
            self.down = pygame.image.load('down.png')
            self.enter = pygame.image.load('return.png')
            bg = pygame.image.load('BG.jpg')
            self.game.display.blit(bg, (0, 0))
            self.game.draw_text('How to Play', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text('*Instructions', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 10)
            self.game.draw_text("Navigate: ", 20, 80, self.game.DISPLAY_H - 50)
            self.game.display.blit(self.up, (140, self.game.DISPLAY_H - 70))
            self.game.display.blit(self.enter, (280, self.game.DISPLAY_H - 70))
            self.game.display.blit(self.down, (210, self.game.DISPLAY_H - 70))
            self.blit_screen()

class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.fill(self.game.BG)
            self.up = pygame.image.load('up.png')
            self.down = pygame.image.load('down.png')
            self.enter = pygame.image.load('return.png')
            bg = pygame.image.load('BG.jpg')
            self.game.display.blit(bg, (0, 0))
            self.game.draw_text('Credits', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text('Ayn Clarisse Ranny', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 10)
            self.game.draw_text("Navigate: ", 20, 80, self.game.DISPLAY_H - 50)
            self.game.display.blit(self.up, (140, self.game.DISPLAY_H - 70))
            self.game.display.blit(self.enter, (280, self.game.DISPLAY_H - 70))
            self.game.display.blit(self.down, (210, self.game.DISPLAY_H - 70))
            self.blit_screen()
