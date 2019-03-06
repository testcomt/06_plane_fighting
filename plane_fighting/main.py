#! /usr/local/bin/python3

import pygame
from plane_fighting import plane_sprites


# When import and use pygame for the 1st time, the following error:
# 2019-03-05 10:57:37.759 Python[38113:44660827] 10:57:37.759 WARNING:  140: This application, or a library it uses, is using the deprecated Carbon Component Manager for hosting Audio Units. Support for this will be removed in a future release. Also, this makes the host incompatible with version 3 audio units. Please transition to the API's in AudioComponent.h.i
#
# For anyone else having problems with graphical glitches on OS X El Capitan and pygame, you can follow these instructions to downgrade to SDL from version 1.2.12 to 1.2.10, which seems to fix the issue (at least in several of the games I've tested so far):
#
# All the following is from the command prompt:
#
# 1. Backup the original ruby Formula (just in case):
#
# mv /usr/local/Library/Formula/sdl_image.rb /usr/local/Library/Formula/sdl_image_backup.rb
#
# 2. This creates a new Formula using the sdl version 1.2.10 instead:
#
# brew create https://www.libsdl.org/projects/SDL_image/release/SDL_image-1.2.10.tar.gz
#
# 3. It should open in a text editor automatically, if not open it with vim/emacs/nano/whatever you prefer and edit it to match most of what the original sdl_image.rb (now sdl_image_backup.rb) says, but skip the "bottle do" part and the "test" part.
#
# 4. Set environment variable (not sure this is required but worked for me):
#
# export SDL_CONFIG=/usr/local/bin/sdl-config
#
# 5. Unlink the old 1.2.12 install:
#
# brew unlink sdl_image
#
# 6. Now reinstall, but brew will use our new Formula for 1.2.10:
#
# brew install sdl_image
#
# In step 3, only copy 3 part from old 1.2.12 sdl_image.rb to new file:
# depends_on part, patch part and def install part
# not necessary to edit any other parts in this file
#
# In step 6, installation succeeds except that of a patch:
# ==> Patching
# ==> Applying IMG_ImageIO.m.patch
# can't find file to patch at input line 3
# Perhaps you used the wrong -p or --strip option?
# The text leading up to this was:
# --------------------------
# |--- IMG_ImageIO.m.orig	2012-01-21 12:51:33.000000000 +1100
# |+++ IMG_ImageIO.m	2016-04-29 22:48:02.000000000 +1000
# --------------------------
# No file to patch.  Skipping patch.
# 1 out of 1 hunk ignored
# Error: Failure while executing; `patch -g 0 -f -p0 -i /private/tmp/sdl_image--patch-20190305-71697-9s9t6n/IMG_ImageIO.m.patch` exited with 1.
#
# So, after all this installation, run program again, the above error still exists.
# Not knowing whether the "graphical glitches" problem disappears or not.
# Deleting patch part in sdl_image.rb file, reinstall, prob still not solved.
# https://bitbucket.org/pygame/pygame/issues/284/max-osx-el-capitan-using-the-deprecated
# Tai Xiaomei: 2019.3.5

# Define size of game screen AND initail loc of hero
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 700
HERO_INIT_X = 250
HERO_INIT_Y = 400
# Define frame frequency AND moving step
FRAME_FREQ = 60

g_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
g_Background = plane_sprites.GameSprites("./images/background.png", 0)
g_Hero = plane_sprites.GameSprites("./images/me1.png")


def game_initial()->None:
    """initialization: prepare screen, images
    R in RIMGEN - Iterations can be multiple ways:
                  step by step of a procedure;
                  from static image, to active action,
                  from one object, to more objects,
                  etc.

    """

    # draw screen update display
    g_screen.blit(g_Background.image, (0, 0))
    g_screen.blit(g_Hero.image, (HERO_INIT_X, HERO_INIT_Y))
    pygame.display.update()

    # set initail location: two ways of coding
    # g_Hero.rect = g_Hero.image.get_rect(center=(HERO_INIT_X, HERO_INIT_Y))
    g_Hero.rect.centerx = HERO_INIT_X
    g_Hero.rect.centery = HERO_INIT_Y

    return


def hero_moving()->None:
    """hero moving from initial location upwards, and back to bottom, recursively"""

    if g_Hero.rect.centery + g_Hero.image.get_height()//2 <= 0:
        g_Hero.rect.centery = SCREEN_HEIGHT + g_Hero.image.get_height()//2

    # TODO-1: what else can be done, if not redrawing a bkg screen?
    # Is current way waste of resources?
    g_screen.blit(g_Background.image, (0, 0))
    g_screen.blit(g_Hero.image, g_Hero.rect)
    pygame.display.update()


def main()->None:
    """main program"""

    # load pygame modules
    pygame.init()

    game_initial()

    clock = pygame.time.Clock()

    while True:
        clock.tick(FRAME_FREQ)

        g_Hero.update()

        hero_moving()

        # monitor events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


if __name__ == "__main__":
    main()
