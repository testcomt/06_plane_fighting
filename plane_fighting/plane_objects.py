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
        self.pos = [init_x, init_y]
        self.rect.centerx = init_x + self.rect.width // 2
        self.rect.centery = init_y + self.rect.height // 2
        # print("rect is ", self.rect)
        self.speed = speed

    def update(self):
        """update location, rewrite this method from parent class
        TODO: heritate this method for hero: moving upwards; rewrite for other obj
        """

        self.rect.y += self.speed


if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode((400, 700))
    bkg_test = GameObjects("./images/me1.png", 0, 150, 300)

    # print(os.getcwd())

    screen.blit(bkg_test.image, bkg_test.pos)
    pygame.display.update()

    while True:
        pass
