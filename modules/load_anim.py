import pygame,sys,os

global anim_frames
anim_frames={}

def load_anim(path,frame_dur):
	global anim_frames
	anim_name=path.split('/')[-1] # will look for end path->assets/anims/player/i͟d͟l͟e͟
	anim_frame_data=[]
	n=0
	for frame in frame_dur:
		anim_frame_id=anim_name+'_'+str(n)
		img_loc=path+'/'+anim_frame_id+'.png'
		anim_img=pygame.image.load(img_loc)
		anim_frames[anim_frame_id]=anim_img.copy()
		for i in range(frame):
			anim_frame_data.append(anim_frame_id)
		n+=1
	return anim_frame_data

def change_action(action_var,frame,new_val):
	if action_var!=new_val:
		action_var=new_val
		frame=0
	return action_var,frame

anim_db={}

anim_db['idle']=load_anim('assets/anims/player/idle',[20,20])
anim_db['run']=load_anim('assets/anims/player/run',[7,7,7,7])

player_action='idle'
player_frame=0
player_flip=False
