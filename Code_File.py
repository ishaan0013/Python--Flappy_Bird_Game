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
    messagex = int(Screen_WIDTH-GAME_SPRITES['message'].get_height())/2
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
        {'x': Screen_WIDTH+200+(Screen_WIDTH/2), 'y': newPipe2[0]['y']},
    ]
    lowerPipes = [
        {'x': Screen_WIDTH+200, 'y': newPipe1[1]['y']},
        {'x': Screen_WIDTH+200+(Screen_WIDTH/2), 'y': newPipe2[1]['y']},
    ]

    pipeVelocityx = -4

    playerVelocityY = -9
    playerMaxVelocityY = 10
    playerMinVelocityY = -8
    playerAccVelocityY = 1

    playerFlapAccv = -8  # *velocity while flapping
    playerFlapped = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_ESCAPE or event.key == K_UP):
                if playery > 0:
                    playerVelocityY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()
        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes)
        if crashTest:
            return

        # *Check Score
        playerMidPos = playerx+GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x']+GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos <= playerMidPos < pipeMidPos+4:
                score += 1
                print(f"Your score is{score}")
                GAME_SOUNDS['point'].play()
        if playerAccVelocityY < playerMaxVelocityY and not playerFlapped:
            playerVelocityY += playerAccVelocityY
        if playerFlapped:
            playerFlapped = False
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery+min(playerVelocityY, GROUNDY-playery-playerHeight)

        # *Move Pipes to left of screen
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelocityx
            lowerPipe['x'] += pipeVelocityx

        # *ADD a new pipe
        if 0 < upperPipes[0]['x'] < 5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        # *If the pipe is out of screen, remove it:
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0],
                        (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1],
                        (lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))

        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        xOffset = (Screen_WIDTH-width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit],
                        (xOffset, Screen_HEIGHT*0.12))
            xOffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery > GROUNDY - 25 or playery < 0:
        GAME_SOUNDS['hit'].play()
        return True

    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if (playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

    return False


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
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    while True:
        welcomeScreen()
        mainGame()
