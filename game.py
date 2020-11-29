import pygame
from menu import *
import math
import random
import sys

sys.setrecursionlimit(1500)

class button():
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('PRIMETIME Regular', 60)
            text = font.render(self.text, 1, (218, 239, 244))
            win.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False

class Game():
    def __init__(self):
        pygame.init()
        self.hint_count = 0

        self.hint_btn = button((215, 203, 69),972, 417,200,90,'Hint')
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.MOUSE_CLICK = False, False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = 1200, 720
        self.display = pygame.Surface((self.DISPLAY_W,self.DISPLAY_H))
        self.window = pygame.display.set_mode(((self.DISPLAY_W,self.DISPLAY_H)))
        self.mposx, self.mposy = self.DISPLAY_W/2,self.DISPLAY_H/2
        self.RADIUS = 35
        self.GAP = 20
        self.letters = []
        self.startx = round((self.DISPLAY_W - (self.RADIUS * 2 + self.GAP) * 13) / 2)
        self.starty = 550
        self.A = 65
        for i in range(26):
            self.x = self.startx + self.GAP * 2 + ((self.RADIUS * 2 + self.GAP) * (i % 13))
            self.y = self.starty + ((i // 13) * (self.GAP + self.RADIUS * 2))
            self.letters.append([self.x, self.y, chr(self.A + i), True])
        self.LETTER_FONT = pygame.font.SysFont('PRIMETIME Regular', 50)
        self.WORD_FONT = pygame.font.SysFont('PRIMETIME Regular', 40)
        self.SCORE_FONT = pygame.font.SysFont('Broadway', 60)
        self.TITLE_FONT = pygame.font.SysFont('PRIMETIME Regular', 90)
        self.images = []
        for i in range(7):
            image = pygame.image.load("hangman" + str(i) + ".png")
            self.images.append(image)
        #INGAME vars
        self.score = 0
        #self.won = False
        #self.lose = False
        self.guessed_words = 0
        self.hangman_status = 0
        file = open('categ.txt', 'r')
        f = file.readlines()
        categ = []
        for ln in f:
            categ.append(ln.strip())
        print(categ)
        file.close()
        self.categories = categ
        self.word = ""
        self.category = ""
        file = open('animals.txt', 'r')
        f = file.readlines()
        anim = []
        for ln in f:
            anim.append(ln.strip())
        print(anim)
        file.close()
        self.words_animal = anim
        file = open('trees.txt', 'r')
        f = file.readlines()
        trees = []
        for ln in f:
            trees.append(ln.strip())
        print(trees)
        file.close()
        self.words_tree = trees
        file = open('countries.txt', 'r')
        f = file.readlines()
        countries = []
        for ln in f:
            countries.append(ln.strip())
        print(countries)
        file.close()
        self.words_countries = countries
        self.guessed = []
        self.font_name = pygame.font.get_default_font()
        self.BLACK, self.WHITE, self.BG = (0, 0, 0), (255, 255, 255),(70, 74, 86)
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.curr_menu = self.main_menu

    def randomize(self):
        sys.setrecursionlimit(1500)
        self.hangman_status = 0
        for letter in self.letters:
            x, y, ltr, visible = letter
            if visible == False:
                letter[3] = True
        self.category = random.choice(self.categories)
        print(self.category)
        if self.category == "Animals":
            self.word = random.choice(self.words_animal).upper()
        elif self.category == "Trees":
            self.word = random.choice(self.words_tree).upper()
        else:
            self.word = random.choice(self.words_countries).upper()
        print(self.word)


    def new_word(self):

        self.hint_btn.draw(self.display, None)
        self.display.blit(self.images[self.hangman_status], (15, 5))
        categ_text = self.TITLE_FONT.render(self.category, 1, (218, 239, 244))
        self.display.blit(categ_text, (self.DISPLAY_W / 2 - categ_text.get_width() / 2, 50))

        display_word = ""
        for letter in self.word:
            if letter in self.guessed:
                display_word += letter + " "
            else:
                display_word += "_ "
        text = self.WORD_FONT.render(display_word, 1, (218, 239, 244))
        self.display.blit(text, (600 - (text.get_width()/2), 200))

        scoreText = self.SCORE_FONT.render(str(self.score), 1, (218, 239, 244))
        self.display.blit(scoreText, (985, 35))

        for letter in self.letters:
            x, y, ltr, visible = letter
            if visible:
                pygame.draw.circle(self.display, (141, 165, 203), (x, y), self.RADIUS)
                text = self.LETTER_FONT.render(ltr, 1, (218, 239, 244))
                self.display.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))



    def game_loop(self):
        while self.playing:
            self.check_events()
            if self.BACK_KEY:
                self.playing= False

            bg = pygame.image.load('BG.jpg')
            self.display.blit(bg, (0, 0))
            self.new_word()
            self.window.blit(self.display, (0,0))
            pygame.display.update()
            self.reset_keys()


    def repeat_hint(self):
        sys.setrecursionlimit(1500)
        hint = random.choice(self.word)
        print(hint)
        checkHint = True
        while checkHint:
            if hint not in self.guessed:
                self.guessed.append(hint)
                print(hint)
                checkHint = False
            else:
                self.repeat_hint()

    def check_events(self):
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                if self.hint_btn.isOver(pos):
                    if self.hint_count == 0:
                        self.repeat_hint()
                        self.hint_count +=1
                    else:
                        print("hint used!")
                        self.display.fill(self.BG)
                        text = self.WORD_FONT.render("Hint for this round is used!",1,(218, 239, 244))
                        self.display.blit(text,(self.DISPLAY_W/2 - text.get_width()/2 , self.DISPLAY_H/2 - text.get_height()/2))
                        self.window.blit(self.display,(0,0))
                        pygame.display.update()
                        pygame.time.delay(1500)
                self.MOUSE_CLICK = True
                self.mposx, self.mposy = m_x, m_y
                print(m_x)
                print(m_y)
                for letter in self.letters:
                    x, y, ltr, visible = letter
                    if visible:
                        dis = math.sqrt((x - m_x) ** 2 + (y - m_y) ** 2)
                        if dis < self.RADIUS:
                            letter[3] = False
                            self.guessed.append(ltr)
                            if ltr not in self.word:
                                self.hangman_status += 1
                won = True
                for letter in self.word:
                    if letter not in self.guessed:
                        won = False
                        if self.hangman_status >= 7:
                            print("You lose!")
                            lose = "You lose! The mystery word is " + self.word
                            self.display.fill(self.BG)
                            text = self.WORD_FONT.render(lose, 1, (218, 239, 244))
                            self.display.blit(text, (
                                self.DISPLAY_W / 2 - text.get_width() / 2, self.DISPLAY_H / 2 - text.get_height() / 2))

                            self.playing = False
                            self.hint_count = 0
                            self.score = 0
                            self.guessed = []
                            self.hangman_status = 0

                            self.window.blit(self.display, (0, 0))
                            pygame.display.update()
                            self.randomize()
                            self.game_loop()
                            pygame.time.delay(2400)

                        break
                if won:
                    self.score+=1
                    self.guessed = []
                    self.hint_count = 0
                    self.randomize()
                    self.game_loop()

            if event.type == pygame.MOUSEMOTION:
                if self.hint_btn.isOver(pos):
                    self.hint_btn.color = (215, 180, 50)

                else:
                    self.hint_btn.color = (215, 203, 69)




    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.MOUSE_CLICK = False, False, False, False, False


    def draw_text(self, text, size, x, y ):
        font = pygame.font.SysFont('PRIMETIME Regular',size)
        text_surface = font.render(text, True, (218, 239, 244))
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface,text_rect)

    # TO ADD
    # *Leaderboard JSON

    #DONE
    # *hint
    # scoring