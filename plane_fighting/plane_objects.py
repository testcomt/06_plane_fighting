import random
import pygame

# TODO: why need to define these constants in this file instead of main file?
# don't define multiple single constants, but define one compound constant
# constants can also be defined by using methods
# SCREEN_WIDTH = 480
# SCREEN_HEIGHT = 700
SCREEN_RECT = pygame.Rect(0, 0, 480, 700)
FRAME_FREQ = 60
# create random_enemy event, using pygame's user event constant
TIMER_EVENT_ID = pygame.USEREVENT
# how frequent will an random enemy be out
# TODO enemy out from slow to fast, from less to more to less...
ENEMY_OUT_FREQ = 300
BULLET_OUT_FREQ = 100
# min and max speed for random enemies
MIN_SPEED = 3
MAX_SPEED = 6
# set bullet speed
BULLET_SPEED = -3


class GameObjects(pygame.sprite.Sprite):
    """create all objects in the screen:
    background, hero, enemies, etc.
    """

    def __init__(self, image_name, speed=1, init_x=0, init_y=0):

        super().__init__()

        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.rect.x = init_x
        self.rect.y = init_y
        self.speed = speed

    def update(self):
        """
        1. update location based on speed, rewrite this method from parent class
        2. out of screen judgement: update y
        """

        self.rect.y += self.speed

        # judging whether the obj is out of screen
        if self.speed > 0 and self.rect.y >= SCREEN_RECT.height:
                self.rect.y = - self.rect.height
        elif self.speed < 0 and self.rect.y <= - self.rect.height:
                self.rect.y = SCREEN_RECT.height

    # def __del__(self):
    #
    #     print("sprites died...")


class RandomEnemy(GameObjects):
    """A random enemy will appear every a period of time"""

    def __init__(self):
        super().__init__("./images/enemy1.png")
        # let bottom be 0, so that enemy will appear right from up line
        self.rect.bottom = 0

        self.speed = random.randint(MIN_SPEED, MAX_SPEED)
        self.rect.x = random.randint(0, SCREEN_RECT.width - self.rect.width)

    def update(self):

        self.rect.y += self.speed

        # if self.rect.y > SCREEN_RECT.bottom:
        #     # kill() will remove from all sprite groups
        #     # and call __delete__() to destroy self
        #     print("out of screen now ...")
        #     self.kill()

    # def __del__(self):
    #     """TODO: WHY? This method is not called when enemy.kill() is executed.
    #        possible reason: if kill() is called from an instance, it may call __del__()
    #        if called from within the class def, it won't call __del__()
    #        but,
    #        for Bullet class, self.kill() will call self.__del__() automatically
    #        for RandomEnemy, self.kill() won't call its self.__del()
    #      """
    #
    #     print("Random enemy died...")


class Hero(GameObjects):

    def __init__(self):

        super().__init__("./images/me1.png", 0)
        self.rect.centerx = SCREEN_RECT.width // 2
        self.rect.bottom = SCREEN_RECT.height - 120
        self.bullet_group = pygame.sprite.Group()

    def update(self):
        """hero can move left or right based on keys"""

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.__left_right(-1)
        elif keys[pygame.K_RIGHT]:
            self.__left_right(1)

    def __left_right(self, direction=1):
        """
        1. moving leftward or rightward direction: if left key, -1; else 1
        2. update loc while judging whether hero is out of screen
        """
        # TODO when use ctrl key, the result is: only command + ctrl take effect
        if pygame.key.get_mods() & pygame.KMOD_SHIFT:
            self.rect.x += 4 * direction
        else:
            self.rect.x += 2 * direction

        if self.rect.left <= 0:
            self.rect.left = 0

        if self.rect.right >= SCREEN_RECT.width:
            self.rect.right = SCREEN_RECT.width

    def fire(self):
        """create bullet obj and add into bullet_group"""

        for i in (0, 1, 2):
            bullet1 = Bullet()
            bullet1.rect.bottom = self.rect.top - i * 20
            bullet1.rect.centerx = self.rect.centerx

            self.bullet_group.add(bullet1)

    # def __del__(self):
    #
    #     print("hero is dead.")


class Bullet(GameObjects):
    """create bullets"""

    def __init__(self):

        super().__init__("./images/bullet1.png", BULLET_SPEED)

    def update(self):
        """
        1. update y based on speed;
        2. destroy bullets when out of screen
        Remark: only for Bullet, self.kill() takes effect:
                actually call __del__ to destroy itself.
        :return:
        """

        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

    # def __del__(self):
    #     """to observe whether bullet obj has been deleted"""
    #     print("bullet is gone...")


if __name__ == '__main__':

    enemy = RandomEnemy()

    while True:
        screen = pygame.display.set_mode(SCREEN_RECT.size)
        screen.blit(enemy.image, (enemy.rect.x, enemy.rect.y))
        pygame.display.update()

        enemy.update()
        if enemy.rect.y > SCREEN_RECT.bottom:

            print("enemy is dead: ", enemy)
            del enemy
            enemy = RandomEnemy()
