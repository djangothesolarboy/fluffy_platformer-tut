import pygame,sys,os

def load_map(path):
	f=open(path+'.txt','r')
	data=f.read()
	f.close()
	data=data.split('\n')
	game_map=[]
	for row in data:
		game_map.append(list(row))
	return game_map
