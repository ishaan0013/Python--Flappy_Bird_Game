import pygame
import random
import sys
from pygame.locals import *


# ?Global variables

FPS = 32
Screen_WIDTH = 289
Screen_HEIGHT = 511
SCREEN = pygame.display.set_mode((Screen_WIDTH, Screen_HEIGHT))
GROUNDY = Screen_HEIGHT*0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'Images/bird.png'
BACKGROUND = 'Images/background.png'
PIPE = 'Images/pipe.png'


def welcomeScreen():
    """
    Shows welcome image on the Screen.
    """
    playerx = int(Screen_WIDTH/5)
    playery = int(Screen_HEIGHT-GAME_SPRITES['player'].get_height())/2
    messagex = int(Screen_WIDTH-GAME_SPRITES['message'].get_height())/3
    messagey = int(Screen_HEIGHT*0.13)
    basex = 0
    while True:
        for event in pygame.event.get():
            # *Closing the game
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            # *Starting the Game
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))
                SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
                SCREEN.blit(GAME_SPRITES['message'], (messagex, messagey))
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)


def mainGame():
    score = 0
    playerx = int(Screen_WIDTH/5)
    playery = int(Screen_WIDTH/2)
    basex = 0
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()
    upperPipes = [
        {'x': Screen_WIDTH+200, 'y': newPipe1[0]['y']},
        {'x': Screen_WIDTH+200+(Screen_WIDTH/2), 'y': newPipe2[1]['y']}
    ]
    lowerPipes = [
        {'x': Screen_WIDTH+200, 'y': newPipe1[0]['y']},
        {'x': Screen_WIDTH+200+(Screen_WIDTH/2), 'y': newPipe2[1]['y']}
    ]

    pipeVelocityx = -4

    playerVelocityY = -9
    playerMaxVelocityY = 10
    playerMinVelocityY = -8
    playerAccVelocityY = 1

    playerFlapAccv = -8  # velocity while flapping
    playerFlapped = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.kry == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_ESCAPE or event.key == K_UP):
                if playery > 0:
                    playerVelocityY = playerAccVelocityY
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()
        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes)
        if crashTest:
            return
        playerMidPos = playerx+GAME_SPRITES['player'].get


def getRandomPipe():
    """Generate positions of 2 pipes for blitting on screen."""
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = Screen_HEIGHT/3
    y2 = offset+random.randrange(0, int(Screen_HEIGHT -
                                 GAME_SPRITES['base'].get_height()-1.2*offset))
    pipeX = Screen_WIDTH+10
    y1 = pipeHeight-y2+offset
    pipe = [
        {'x': pipeX, 'y': -y1},
        {'x': pipeX, 'y': y2}

    ]
    return pipe


# ? Main
if __name__ == "__main__":
    pygame.init()       # *Initalize all pygame modules
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption("Flappy Bird")
    GAME_SPRITES['numbers'] = (
        pygame.image.load('Images/1.png').convert_alpha(),
        pygame.image.load('Images/0.png').convert_alpha(),
        pygame.image.load('Images/2.png').convert_alpha(),
        pygame.image.load('Images/3.png').convert_alpha(),
        pygame.image.load('Images/4.png').convert_alpha(),
        pygame.image.load('Images/5.png').convert_alpha(),
        pygame.image.load('Images/6.png').convert_alpha(),
        pygame.image.load('Images/7.png').convert_alpha(),
        pygame.image.load('Images/8.png').convert_alpha(),
        pygame.image.load('Images/9.png').convert_alpha(),
    )
    GAME_SPRITES['message'] = pygame.image.load(
        'Images/message.jpg').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load('Images/base.png').convert_alpha()
    GAME_SPRITES['pipe'] = (
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
        pygame.image.load(PIPE).convert_alpha()
    )

    GAME_SOUNDS['die'] = pygame.mixer.Sound('Audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('Audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('Audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('Audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('Audio/wing.wav')

    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert()

    while True:
        welcomeScreen()
        mainGame()
