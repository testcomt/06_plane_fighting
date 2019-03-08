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
ENEMY_OUT_FREQ = 1000
# min and max speed for random enemies
MIN_SPEED = 2
MAX_SPEED = 5


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
        """update location, rewrite this method from parent class"""

        self.rect.y += self.speed

        # judging whether the obj is out of screen
        if self.speed > 0 and self.rect.y >= SCREEN_RECT.height:
                self.rect.y = - self.rect.height
        elif self.speed < 0 and self.rect.y <= - self.rect.height:
                self.rect.y = SCREEN_RECT.height


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

        if self.rect.y >= SCREEN_RECT.height:
            # kill() will remove from all sprite groups
            # and call __delete__() to destroy self
            self.kill()


if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode((400, 700))
    bkg_test = GameObjects("./images/me1.png", 0, 150, 300)

    # print(os.getcwd())

    screen.blit(bkg_test.image, (bkg_test.rect.x, bkg_test.rect.y))
    pygame.display.update()

    while True:
        pass
