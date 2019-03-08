#! /usr/local/bin/python3

import pygame
from plane_fighting import plane_objects

# don't define multiple single constants, but define one compound constant
# constants can also be defined by using methods
# SCREEN_WIDTH = 480
# SCREEN_HEIGHT = 700
SCREEN_RECT = pygame.Rect(0, 0, 480, 700)
FRAME_FREQ = 60


class PlaneGame(object):
    """main program module impl in OOP method"""

    def __init__(self):

        # 1. load pygame modules
        pygame.init()

        # 2. create clock object
        self.clock = pygame.time.Clock()

        # 3. create screen object
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)

        try:
            # 4. create game objects: bkg, hero, sprites
            self.__create_objects()
        except Exception as error:
            print("Something is wrong with game images: ", error)
            exit()

    def start_game(self):

        print("game start")

        while True:

            self.__set_frame_frequency()

            self.__event_handling()

            self.__check_collisions()

            self.__update_objects()

            self.__update_display()

    def __create_objects(self):
        """create bkg, hero, sprites using GameObjects class"""

        self.bkg = plane_objects.GameObjects("./images/background.png", 0)
        self.hero = plane_objects.GameObjects("./images/me1.png", speed=-1, init_x=150, init_y=300)
        self.sprite1 = plane_objects.GameObjects("./images/enemy1.png")
        self.sprite2 = plane_objects.GameObjects("./images/enemy1.png", 2, 50, 50)
        self.sprite_group = pygame.sprite.Group(self.bkg, self.hero, self.sprite1, self.sprite2)

    def __event_handling(self):
        """handling events from users"""

        # monitor events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__game_over()

    def __check_collisions(self):
        """checking collisions"""

        pass

    def __set_frame_frequency(self):
        """set fresh frequencies by setting clock ticking frequency"""

        self.clock.tick(FRAME_FREQ)

    def __update_objects(self):
        """redraw objects on the screen"""

        # The order of these two lines makes difference, if updating all elements
        # in sprites_group in __sprites_loc_update() instead of only updating element [2:]
        self.__hero_loc_update()
        self.__sprites_loc_update()

        self.sprite_group.update()

    def __update_display(self):
        """update display of objects on the screen"""

        self.sprite_group.draw(self.screen)
        pygame.display.update()

    def __hero_loc_update(self):
        """update hero's location whenever out of screen"""

        if self.hero.rect.centery + self.hero.rect.height // 2 <= 0:
            self.hero.rect.centery = SCREEN_RECT.height + self.hero.rect.height // 2

    def __sprites_loc_update(self):
        """update each sprite's location whenever out of screen"""

        enemy_list = self.sprite_group.sprites()
        for enemy in enemy_list[2:]:
            if enemy.rect.centery - enemy.rect.height // 2 >= SCREEN_RECT.height:
                enemy.rect.centery = 0 - enemy.rect.height // 2

    @staticmethod
    def __game_over():

        pygame.quit()
        exit()


if __name__ == '__main__':

    plane_game = PlaneGame()
    plane_game.start_game()
