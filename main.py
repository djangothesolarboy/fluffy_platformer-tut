import pygame,sys,os

clock=pygame.time.Clock() # clock setup
from pygame.locals import *

# my module imports
from modules.load_map import load_map
from modules.load_sound import load_sound
from modules.load_anim import *
from modules.col_mov import *

pygame.init() # initiates pygame

pygame.display.set_caption('blue man jumps') # window name
WIN_SIZE=(600,400) # window size
screen=pygame.display.set_mode(WIN_SIZE,0,32) # initiate screen
display=pygame.Surface((300,200))

brick_img=pygame.image.load('assets/backgrounds/brick_tile/brick_one.png')

# tl->top-left;tm->top-mid;tr->top-right;
grass_tl=pygame.image.load('assets/backgrounds/grass_tile/grass_left-end.png')
grass_tm=pygame.image.load('assets/backgrounds/grass_tile/grass_mid.png')
grass_tr=pygame.image.load('assets/backgrounds/grass_tile/grass_right-end.png')
# bl->bot-left;bm->bot-mid;br->bot-right;
grass_bl=pygame.image.load('assets/backgrounds/grass_tile/grass_left-bot-end.png')
grass_bm=pygame.image.load('assets/backgrounds/grass_tile/grass_mid-bot-end.png')
grass_br=pygame.image.load('assets/backgrounds/grass_tile/grass_right-bot-end.png')

TILE_SIZE=brick_img.get_width() # this assumes height and width are the same size(16x16)

game_map=load_map('map')
jump_sound=load_sound('jump.wav')

# 	     scroll multiplier  x   y  w  h
background_objects=[[0.25,[120,10,70,400]],[0.25,[280,30,40,400]],[0.5,[30,40,40,400]],[0.5,[130,90,100,400]],[0.5,[300,80,120,400]]]

moving_right=False
moving_left=False

player_y_momentum=0
air_timer=0

true_scroll=[0,0]

player_rect=pygame.Rect(50,50,16,16)

while True: # game loop
	display.fill((146,244,255)) # background color

	true_scroll[0]+=(player_rect.x-true_scroll[0]-152)/20 # keeps camera on player(x axis)
	true_scroll[1]+=(player_rect.y-true_scroll[1]-106)/20 # keeps camera on player(y axis)
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

	# places sprites/imgs onto surface based on map.txt
	tile_rects=[]
	y=0
	for row in game_map:
		x=0
		for tile in row:
			if tile=='1':
				display.blit(grass_tl,(x*TILE_SIZE-scroll[0],y*TILE_SIZE-scroll[1]))
			if tile=='2':
				display.blit(grass_tm,(x*TILE_SIZE-scroll[0],y*TILE_SIZE-scroll[1]))
			if tile=='3':
				display.blit(grass_tr,(x*TILE_SIZE-scroll[0],y*TILE_SIZE-scroll[1]))
			if tile=='4':
				display.blit(grass_bl,(x*TILE_SIZE-scroll[0],y*TILE_SIZE-scroll[1]))
			if tile=='5':
				display.blit(grass_bm,(x*TILE_SIZE-scroll[0],y*TILE_SIZE-scroll[1]))
			if tile=='6':
				display.blit(grass_br,(x*TILE_SIZE-scroll[0],y*TILE_SIZE-scroll[1]))
			if tile!='0':
				tile_rects.append(pygame.Rect(x*TILE_SIZE,y*TILE_SIZE,TILE_SIZE,TILE_SIZE))
			x+=1
		y+=1

	player_movement=[0,0]
	if moving_right:
		player_movement[0]+=2
	if moving_left:
		player_movement[0]-=2
	player_movement[1]+=player_y_momentum
	player_y_momentum += 0.2

	if player_y_momentum>3:
		player_y_momentum=3

	# activates animations
	if player_movement[0]>0:
		player_action,player_frame=change_action(player_action,player_frame,'run')
		player_flip=False
	if player_movement[0]==0:
		player_action,player_frame=change_action(player_action,player_frame,'idle')
	if player_movement[0]<0:
		player_action,player_frame=change_action(player_action,player_frame,'run')
		player_flip=True

	player_rect,collisions=move(player_rect,player_movement,tile_rects) # collision detection

	# checks if player is on ground before allowing player to jump
	if collisions['bottom']:
		player_y_momentum=0
		air_timer=0
	else:
		air_timer+=1

	player_frame+=1
	if player_frame>=len(anim_db[player_action]):
		player_frame=0
	player_img_id=anim_db[player_action][player_frame]
	player_img=anim_frames[player_img_id]
	display.blit(pygame.transform.flip(player_img,player_flip,False),(player_rect.x-scroll[0],player_rect.y-scroll[1])) # camera follows player

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

	surf=pygame.transform.scale(display,WIN_SIZE)
	screen.blit(surf,(0,0))
	pygame.display.update() # updates display
	clock.tick(60) # maintain 60 fps
