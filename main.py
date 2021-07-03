import pygame
import sys,os

clock=pygame.time.Clock() # clock setup
from pygame.locals import *

pygame.init() # initiates pygame

pygame.display.set_caption('fluffy tut') # window name
WIN_SIZE=(400,400) # window size
screen=pygame.display.set_mode(WIN_SIZE,0,32) # initiate screen

player_img=pygame.image.load('./assets/sprites/survivor-blue_idle-strip.png')

move_right=False
move_left=False

player_loc=[50,50]
player_y_momentum=0

player_rect=pygame.Rect(player_loc[0],player_loc[1],player_img.get_width(),player_img.get_height())
test_rect=pygame.Rect(100,100,100,50)

while True: # game loop
	screen.fill((146,244,255)) # background color
	screen.blit(player_img,player_loc)

	if player_loc[1] > WIN_SIZE[1]-player_img.get_height():
	    player_y_momentum = -player_y_momentum
	else:
		player_y_momentum += 0.2
	player_loc[1] += player_y_momentum

	if move_right==True:
		player_loc[0]+=4 # adds 4 to x(player_loc[x,y])
	if move_left==True:
		player_loc[0]-=4 # minus 4 to x(player_loc[x,y])

	player_rect.x=player_loc[0]
	player_rect.y=player_loc[1]

	if player_rect.colliderect(test_rect):
		pygame.draw.rect(screen,(255,0,0),test_rect)
	else:
		pygame.draw.rect(screen,(0,0,0),test_rect)


	for event in pygame.event.get(): # event loop
		if event.type==QUIT: # check for window quit
			pygame.quit() # stop pygame
			sys.exit() # stop script
		if event.type==KEYDOWN: # while key is pressed
			if event.key==K_ESCAPE:
				pygame.quit()
				sys.exit()
			if event.key==K_RIGHT or event.key==K_d:
				move_right=True
			if event.key==K_LEFT or event.key==K_a:
				move_left=True
		if event.type==KEYUP: # once key is let go
			if event.key==K_RIGHT or event.key==K_d:
				move_right=False
			if event.key==K_LEFT or event.key==K_a:
				move_left=False



	pygame.display.update() # updates display
	clock.tick(60) # maintain 60 fps