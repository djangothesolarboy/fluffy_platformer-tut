import pygame,sys,os
import random
from pygame.locals import *
# my module imports
import data.engine as e
from modules.chunk_gen import *
from modules.load_sound import load_sound

WIN_SIZE=(600,400) # window size

clock=pygame.time.Clock() # clock setup
pygame.init() # initiates pygame

pygame.display.set_caption('blue man jumps') # window name
screen=pygame.display.set_mode(WIN_SIZE,0,32) # initiate screen
display=pygame.Surface((300,200))

brick_img=pygame.image.load('data/imgs/backgrounds/brick_tile/brick_one.png')

# tl->top-left;tm->top-mid;tr->top-right;
grass_tl=pygame.image.load('data/imgs/backgrounds/grass_tile/grass_left-end.png')
grass_tm=pygame.image.load('data/imgs/backgrounds/grass_tile/grass_mid.png')
grass_tr=pygame.image.load('data/imgs/backgrounds/grass_tile/grass_right-end.png')
# bl->bot-left;bm->bot-mid;br->bot-right;
grass_bl=pygame.image.load('data/imgs/backgrounds/grass_tile/grass_left-bot-end.png')
grass_bm=pygame.image.load('data/imgs/backgrounds/grass_tile/grass_mid-bot-end.png')
grass_br=pygame.image.load('data/imgs/backgrounds/grass_tile/grass_right-bot-end.png')

tile_index={1:grass_tl,2:grass_tm,3:grass_tr,4:grass_bl,5:grass_bm,6:grass_br}
TILE_SIZE=brick_img.get_width() # this assumes height and width are the same size(16x16)

e.load_anims('data/imgs/entities/')

game_map={}
jump_sound=load_sound('jump.wav')

moving_right=False
moving_left=False
player_y_momentum=0
air_timer=0

true_scroll=[0,0]

player=e.entity(50,50,16,16,'player')

# 	     scroll multiplier  x   y  w  h
background_objects=[[0.25,[120,10,70,400]],[0.25,[280,30,40,400]],[0.5,[30,40,40,400]],[0.5,[130,90,100,400]],[0.5,[300,80,120,400]]]

while True: # game loop
	display.fill((146,244,255)) # background color

	true_scroll[0]+=(player.x-true_scroll[0]-152)/20 # keeps camera on player(x axis)
	true_scroll[1]+=(player.y-true_scroll[1]-106)/20 # keeps camera on player(y axis)
	scroll=true_scroll.copy()
	scroll[0]=int(scroll[0])
	scroll[1]=int(scroll[1])

	pygame.draw.rect(display,(7,80,75),pygame.Rect(0,120,300,80))
	for background_object in background_objects:
		obj_rect=pygame.Rect(background_object[1][0]-scroll[0]*background_object[0],background_object[1][1]-scroll[1]*background_object[0],background_object[1][2],background_object[1][3])
		if background_object[0]==0.5:
			pygame.draw.rect(display,(14,222,150),obj_rect)
		else:
			pygame.draw.rect(display,(9,91,85),obj_rect)

	tile_rects=[]
	for y in range(3): # calculates chunk ids that are visible on screen
		for x in range(4):
			target_x=x-1+int(round(scroll[0]/(CHUNK_SIZE*16)))
			target_y=y-1+int(round(scroll[1]/(CHUNK_SIZE*16)))
			target_chunk=str(target_x)+';'+str(target_y)
			if target_chunk not in game_map: # generates chunks if they don't exist
				game_map[target_chunk]=chunk_gen(target_x,target_y)
			for tile in game_map[target_chunk]:
				display.blit(tile_index[tile[1]],(tile[0][0]*16-scroll[0],tile[0][1]*16-scroll[1]))
				if tile[1] in [1,2]:
					tile_rects.append(pygame.Rect(tile[0][0]*16,tile[0][1]*16,16,16))

	# moves player
	player_movement=[0,0]
	if moving_right:
		player_movement[0]+=2
	if moving_left:
		player_movement[0]-=2
	player_movement[1]+=player_y_momentum
	player_y_momentum += 0.2
	# keeps momentum low
	if player_y_momentum>3:
		player_y_momentum=3

	# activates animations
	if player_movement[0]==0:
		player.set_action('idle')
	if player_movement[0]>0:
		player.set_flip(False)
		player.set_action('run')
	if player_movement[0]<0:
		player.set_flip(True)
		player.set_action('run')

	collisions_types=player.move(player_movement,tile_rects) # collision detection

	# checks if player is on ground before allowing player to jump
	if collisions_types['bottom']==True:
		player_y_momentum=0
		air_timer=0
	else:
		air_timer+=1

	player.change_frame(1)
	player.display(display,scroll)

	for event in pygame.event.get(): # event loop
		if event.type==QUIT: # check for window quit
			pygame.quit() # stop pygame
			sys.exit() # stop script
		if event.type==KEYDOWN: # while key is pressed
			if event.key==K_ESCAPE:
				pygame.quit()
				sys.exit()
			if event.key==K_RIGHT or event.key==K_d:
				moving_right=True
			if event.key==K_LEFT or event.key==K_a:
				moving_left=True
			# if event.key==K_r:
			if event.key==K_UP or event.key==K_SPACE or event.key==K_w:
				if air_timer<6:
					jump_sound.play()
					player_y_momentum=-5
		if event.type==KEYUP: # once key is let go
			if event.key==K_RIGHT or event.key==K_d:
				moving_right=False
			if event.key==K_LEFT or event.key==K_a:
				moving_left=False

	screen.blit(pygame.transform.scale(display,WIN_SIZE),(0,0))
	pygame.display.update() # updates display
	clock.tick(60) # maintain 60 fps
