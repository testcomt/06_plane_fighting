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

        # 5. create timers: random enemy out timer; bullet out timer
        pygame.time.set_timer(plane_objects.TIMER_EVENT_ID, plane_objects.ENEMY_OUT_FREQ)
        pygame.time.set_timer(plane_objects.TIMER_EVENT_ID + 1, plane_objects.BULLET_OUT_FREQ)

        # 6. collide sign
        self.b_collide = False

    def start_game(self):

        while True:

            self.__set_frame_frequency()
            self.__event_handling()

            if not self.b_collide:
                if self.__check_hero_collision() != -1:
                    self.__handling_hero_collision()
                    self.b_collide = True
                else:
                    self.__check_enemies_collision()
                    self.__update_objects()

    def __create_objects(self):
        """create bkg, hero, sprites using GameObjects class"""

        self.bkg = plane_objects.GameObjects("./images/background.png")
        self.bkg2 = plane_objects.GameObjects("./images/background.png", init_y=-plane_objects.SCREEN_RECT.height)

        self.hero = plane_objects.Hero()

        # create 2 non-random out sprites
        self.sprite1 = plane_objects.GameObjects("./images/enemy1.png", 2)
        self.sprite2 = plane_objects.GameObjects("./images/enemy1.png", 3, 250, 60)

        # enemy_group includes all enemies, used for judging collisions
        self.enemy_group = [self.sprite1, self.sprite2]
        # Attention: The Sprites in the Group are not ordered,
        # so drawing and iterating the Sprites is in no particular order.
        # Doubt: the actual iterating order in this Group depends on the order of def.
        # objects.group: all objects in the game, which are updated together
        self.objects_group = pygame.sprite.Group(self.bkg, self.bkg2, self.hero, self.sprite1, self.sprite2)

    def __event_handling(self):
        """handling events from users"""

        # monitor events
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                # use class name to call for static method
                PlaneGame.__game_over()
            elif event.type == plane_objects.TIMER_EVENT_ID:
                self.__create_random_enemy()
            # This branch judgement originally is: elif event.type in (pygame.K_LEFT, pygame.K_RIGHT)...
            # But, actually this branch is never reached. TODO : a bug e.g of non-reachable codes
            # elif event.type == pygame.KEYDOWN and event.key in (pygame.K_LEFT, pygame.K_RIGHT):
            #     print("left or right...")
            #     self.hero.update()

            # TODO: what the usage of KEYDOWN; now, when space is down all the time,
            # There are two types of judging keys:
            # 1) one time event model (do next until KEYUP and keydwon again):
            #    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE
            # 2) continuous operating model:
            #    if pygame.key.get_pressed()[pygame.K_SPACE]
            # it can only shoot one bullet
            # TODO why is model 1 when collision happens, model 2 in playing mode?
            elif (pygame.key.get_pressed()[pygame.K_SPACE] and not self.b_collide) or \
                 (event.type == plane_objects.TIMER_EVENT_ID + 1):
                self.hero.fire()
                # self.objects_group.add(self.hero.bullet_group)

    def __create_random_enemy(self):

        self.random_enemy = plane_objects.RandomEnemy()
        self.objects_group.add(self.random_enemy)
        self.enemy_group.append(self.random_enemy)

    def __check_hero_collision(self):

        collide_rect_list = []
        for enemy in self.enemy_group:
            collide_rect_list.append(enemy.rect)

        return self.hero.rect.collidelist(collide_rect_list)

    def __handling_hero_collision(self):

        hero_destroy = plane_objects.GameObjects("./images/me_destroy_1.png", 0,
                                                 self.hero.rect.x,
                                                 self.hero.rect.y)
        # after empty group, all obj will be freezed on the screen
        # otherwise, objs will move on until disappear from the screen
        self.objects_group.empty()

        self.objects_group.add(hero_destroy)

        self.__update_objects()

        pygame.time.set_timer(plane_objects.TIMER_EVENT_ID, 0)
        pygame.time.set_timer(plane_objects.TIMER_EVENT_ID + 1, 0)
        #
        # # in debug mode, random enemies still being created even after collision and timer stoped
        # # so, clear this enemy_group, so that no loop will run in __check_enemies_collision
        # self.enemy_group.clear()
        #
        # self.sprite1.kill()
        # self.sprite2.kill()
        # self.hero.kill()

    def __check_enemies_collision(self):

        for enemy in self.enemy_group:
            for bullet in self.hero.bullet_group:
                if enemy.rect.colliderect(bullet.rect):
                    self.__handling_enemies_collision(enemy)

    @staticmethod
    def __handling_enemies_collision(enemy):

        enemy.kill()

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
        # before update, add bullet_group into objects_group
        self.objects_group.add(self.hero.bullet_group)

        self.objects_group.update()
        self.objects_group.draw(self.screen)
        pygame.display.update()

    @staticmethod
    def __game_over():

        pygame.quit()
        exit()


if __name__ == '__main__':
    plane_game = PlaneGame()
    plane_game.start_game()
