import pygame
# import os

# TODO: why need to define these constants in this file instead of main file?
# don't define multiple single constants, but define one compound constant
# constants can also be defined by using methods
# SCREEN_WIDTH = 480
# SCREEN_HEIGHT = 700
SCREEN_RECT = pygame.Rect(0, 0, 480, 700)
FRAME_FREQ = 60


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


if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode((400, 700))
    bkg_test = GameObjects("./images/me1.png", 0, 150, 300)

    # print(os.getcwd())

    screen.blit(bkg_test.image, (bkg_test.rect.x, bkg_test.rect.y))
    pygame.display.update()

    while True:
        pass
