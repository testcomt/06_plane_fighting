#! /usr/local/bin/python3

import pygame
from plane_fighting import plane_sprites

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 700


class PlaneGame(object):
    """main program module impl in OOP method"""

    def __init__(self):

        # 1. load pygame modules
        pygame.init()

        # 2. create clock object
        self.clock = pygame.time.Clock()

        # 3. create screen object
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        # 4. create game objects: bkg, hero, sprites
        self.__create_objects__()

    def start_game(self):

        print("game start")

    def __create_objects__(self):
        """create bkg, hero, sprites using GameObjects class"""

        self.bkg = plane_sprites.GameSprites()


if __name__ == '__main__':

    plane_game = PlaneGame()
    plane_game.start_game()
