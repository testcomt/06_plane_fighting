#! /usr/local/bin/python3

import pygame
from plane_fighting import plane_objects


class PlaneGame(object):
    """main program module impl in OOP method"""

    def __init__(self):

        # 1. load pygame modules
        pygame.init()

        # 2. create clock object
        self.clock = pygame.time.Clock()

        # 3. create screen object
        self.screen = pygame.display.set_mode(plane_objects.SCREEN_RECT.size)

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

        self.bkg = plane_objects.GameObjects("./images/background.png")
        self.bkg2 = plane_objects.GameObjects("./images/background.png", init_y=-plane_objects.SCREEN_RECT.height)

        self.hero = plane_objects.GameObjects("./images/me1.png", -1, 150, 300)

        self.sprite1 = plane_objects.GameObjects("./images/enemy1.png", 2)
        self.sprite2 = plane_objects.GameObjects("./images/enemy1.png", 3, 50, 50)

        # Attention: The Sprites in the Group are not ordered,
        # so drawing and iterating the Sprites is in no particular order.
        # Doubt: the actual iterating order in this Group depends on the order of def.
        self.sprite_group = pygame.sprite.Group(self.bkg, self.bkg2, self.hero, self.sprite1, self.sprite2)

    def __event_handling(self):
        """handling events from users"""

        # monitor events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # use class name to call for static method
                PlaneGame.__game_over()

    def __check_collisions(self):
        """checking collisions"""

        pass

    def __set_frame_frequency(self):
        """set fresh frequencies by setting clock ticking frequency"""

        self.clock.tick(plane_objects.FRAME_FREQ)

    def __update_objects(self):
        """redraw objects on the screen"""

        # The order of these two lines makes difference
        # If self.__hero_loc_update() happens 1st, its location will be further updated
        # when running sprites update
        self.__sprites_loc_update()
        self.__hero_loc_update()

        self.sprite_group.update()

    def __update_display(self):
        """update display of objects on the screen"""

        self.sprite_group.draw(self.screen)
        pygame.display.update()

    def __hero_loc_update(self):
        """update hero's location whenever out of screen"""

        if self.hero.rect.centery + self.hero.rect.height // 2 <= 0:
            self.hero.rect.centery = plane_objects.SCREEN_RECT.height + self.hero.rect.height // 2

    def __sprites_loc_update(self):
        """update each sprite's location whenever out of screen
        Due to no specific order in this sprite_group, the way of sprite_list[2:] doesn't work
        """

        for enemy in self.sprite_group.sprites():
            if enemy.rect.centery - enemy.rect.height // 2 >= plane_objects.SCREEN_RECT.height:
                enemy.rect.centery = - enemy.rect.height // 2

    @staticmethod
    def __game_over():

        pygame.quit()
        exit()


if __name__ == '__main__':

    plane_game = PlaneGame()
    plane_game.start_game()
