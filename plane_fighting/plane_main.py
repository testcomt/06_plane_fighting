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
                if self.__check_hero_collision():
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

        # Attention: The Sprites in the Group are not ordered,
        # so drawing and iterating the Sprites is in no particular order.
        # Doubt: the actual iterating order in this Group depends on the order of def.
        # random_enemy_group: the only purpose of this group is to kill random enemy
        # while they are out of screen (for no clear reason, kill() does not call __del__
        # if used within class def)
        self.objects_group = pygame.sprite.Group(self.bkg, self.bkg2, self.hero)
        self.random_enemy_group = pygame.sprite.Group()
        self.all_enemy_group = pygame.sprite.Group(self.sprite1, self.sprite2)

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

    def __create_random_enemy(self):

        self.random_enemy = plane_objects.RandomEnemy()
        self.random_enemy_group.add(self.random_enemy)
        self.all_enemy_group.add(self.random_enemy)

    def __check_hero_collision(self):

        # This way of checking: collsion with rectangle
        # collide_rect_list = []
        # for enemy in self.all_enemy_group:
        #     collide_rect_list.append(enemy.rect)
        #
        # return self.hero.rect.collidelist(collide_rect_list)

        return len(pygame.sprite.spritecollide(self.hero,
                                               self.all_enemy_group,
                                               True,
                                               pygame.sprite.collide_mask))

    def __handling_hero_collision(self):

        hero_destroy = plane_objects.GameObjects("./images/me_destroy_1.png", 0,
                                                 self.hero.rect.x,
                                                 self.hero.rect.y)

        self.objects_group.add(hero_destroy)

        self.__update_objects()

        pygame.time.set_timer(plane_objects.TIMER_EVENT_ID, 0)
        pygame.time.set_timer(plane_objects.TIMER_EVENT_ID + 1, 0)
        #
        # # in debug mode, random enemies still being created even after collision and timer stoped
        # # so, clear this enemy_list, so that no loop will run in __check_enemies_collision
        # self.enemy_list.clear()
        # TODO: whether the following obj need to be killed explicitly?
        # This may depend on how to deal with restart-game event.
        # self.sprite1.kill()
        # self.sprite2.kill()
        # self.hero.kill()

    def __check_enemies_collision(self):

        # for enemy in self.enemy_list:
        #     for bullet in self.hero.bullet_group:
        #         if enemy.rect.colliderect(bullet.rect):
        #             self.enemy_list.remove(enemy)
        #             self.__handling_enemies_collision(enemy)
        #             break

        pygame.sprite.groupcollide(self.all_enemy_group,
                                   self.hero.bullet_group,
                                   True, True,
                                   pygame.sprite.collide_mask)

    def __set_frame_frequency(self):
        """set fresh frequencies by setting clock ticking frequency"""

        self.clock.tick(plane_objects.FRAME_FREQ)

    def __update_objects(self):
        """redraw objects on the screen"""

        self.objects_group.add(self.hero.bullet_group)
        self.objects_group.add(self.all_enemy_group)

        self.objects_group.update()
        self.objects_group.draw(self.screen)

        # Attention: random_emeny_group update must be done after objects_group update
        # because in objects_group, there is background image.
        # The other way is like above usage: add random_enemy_group into objects_group
        # before update.
        # self.random_enemy_group.update()
        # self.random_enemy_group.draw(self.screen)

        self.__del_enemy_out_of_screen()

        pygame.display.update()

    def __del_enemy_out_of_screen(self):
        """Have to judge out of screen here, because within RandomEnemy class def,
        even use self.kill() in update(), __del__() won't be called.
        """

        for random_enemy in self.random_enemy_group:
            if random_enemy.rect.y > plane_objects.SCREEN_RECT.height:
                # print("out of screen...")
                random_enemy.kill()
                # print("after -- %d" % len(self.random_enemy_group))

    @staticmethod
    def __game_over():

        pygame.quit()
        exit()


if __name__ == '__main__':
    plane_game = PlaneGame()
    plane_game.start_game()
