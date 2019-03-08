#! /usr/local/bin/python3
# order of importing: official modules; 3rd party modules; program modules
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

        # 5. create a timer
        pygame.time.set_timer(plane_objects.TIMER_EVENT_ID, plane_objects.ENEMY_OUT_FREQ)

    def start_game(self):

        while True:

            self.__set_frame_frequency()
            self.__event_handling()
            self.__check_collisions()
            self.__update_objects()

            pygame.display.update()

    def __create_objects(self):
        """create bkg, hero, sprites using GameObjects class"""

        self.bkg = plane_objects.GameObjects("./images/background.png")
        self.bkg2 = plane_objects.GameObjects("./images/background.png", init_y=-plane_objects.SCREEN_RECT.height)

        self.hero = plane_objects.GameObjects("./images/me1.png", -1, 150, 300)

        self.sprite1 = plane_objects.GameObjects("./images/enemy1.png", 2)
        self.sprite2 = plane_objects.GameObjects("./images/enemy1.png", 3, 250, 60)

        # Attention: The Sprites in the Group are not ordered,
        # so drawing and iterating the Sprites is in no particular order.
        # Doubt: the actual iterating order in this Group depends on the order of def.
        # TODO: UPDATE NAME
        self.objects_group = pygame.sprite.Group(self.bkg, self.bkg2, self.hero, self.sprite1, self.sprite2)

    def __event_handling(self):
        """handling events from users"""

        # monitor events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # use class name to call for static method
                PlaneGame.__game_over()
            elif event.type == plane_objects.TIMER_EVENT_ID:
                self.random_enemy = plane_objects.RandomEnemy()
                self.objects_group.add(self.random_enemy)

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
        # refactor: move these updating actions into class update method
        # self.__sprites_loc_update()
        # self.__hero_loc_update()

        self.objects_group.update()
        self.objects_group.draw(self.screen)

    @staticmethod
    def __game_over():

        pygame.quit()
        exit()


if __name__ == '__main__':

    plane_game = PlaneGame()
    plane_game.start_game()
