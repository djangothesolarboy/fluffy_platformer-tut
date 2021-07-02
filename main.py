import pygame
import sys,os

clock=pygame.time.Clock()
from pygame.locals import *

pygame.init() # initiates pygame

pygame.display.set_caption('fluffy tut')
WIN_SIZE=(400,400) # window size
screen=pygame.display.set_mode(WIN_SIZE,0,32)

while True: # game loop
	for event in pygame.event.get():
		if event.type==QUIT:
			pygame.quit()
			sys.exit()

	pygame.display.update()
	clock.tick(60)