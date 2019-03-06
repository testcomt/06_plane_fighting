import pygame


class GameSprites(pygame.sprite.Sprite):
    """create all objects in the screen:
    background, hero, enemies, etc.
    TODO: maybe initial locations can be set as instance properties
    """

    def __init__(self, image_name, speed=1):

        super().__init__()

        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self):
        """update location, rewrite this method from parent class"""

        self.rect.y += self.speed
