from game import Game

g = Game()
g.randomize()
while g.running:
    g.curr_menu.display_menu()
    g.game_loop()