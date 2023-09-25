import pygame
import random
import sys
from pygame.locals import *

#Global variables
FPS=32
Screen_WIDTH = 289
Screen_HEIGHT=511
SCREEN=pygame.display.set_mode((Screen_WIDTH,Screen_HEIGHT))
GROUNDY=Screen_HEIGHT*0.8
GAME_SPRITES={}
GAME_SOUNDS={}
PLAYER = '/Images/bird.png'
BACKGROUND='/Images/background.png'
PIPE='/Images/pipe.png'


if __name__=="__main__":
    pygame.init() #Initalize all pygame modules
    FPSCLOCK=pygame.time.Clock()
    pygame.display.set_caption("Flappy Bird")
    GAME_SPRITES['numbers']=(
        pygame.image.load('/Images/0.png').convert_alpha(),
        pygame.image.load('/Images/1.png').convert_alpha(),
        pygame.image.load('/Images/2.png').convert_alpha(),
        pygame.image.load('/Images/3.png').convert_alpha(),
        pygame.image.load('/Images/4.png').convert_alpha(),
        pygame.image.load('/Images/5.png').convert_alpha(),
        pygame.image.load('/Images/6.png').convert_alpha(),
        pygame.image.load('/Images/7.png').convert_alpha(),
        pygame.image.load('/Images/8.png').convert_alpha(),
        pygame.image.load('/Images/9.png').convert_alpha(),
    )