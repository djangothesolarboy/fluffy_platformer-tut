import pygame,sys,os
import random

CHUNK_SIZE=8
# world->chunks->tiles
def chunk_gen(x,y):
	chunk_data=[]
	for y_pos in range(CHUNK_SIZE):
		for x_pos in range(CHUNK_SIZE):
			target_x=x*CHUNK_SIZE+x_pos
			target_y=y*CHUNK_SIZE+y_pos
			tile_type=0 # nothing
			if target_y>10:
				tile_type=2 # dirt
			elif target_y==10:
				tile_type=1 # grass
			elif target_y==9:
				if random.randint(1,5)==1:
					tile_type=3 # plant
			if tile_type!=0:
				chunk_data.append([[target_x,target_y],tile_type])
	return chunk_data
