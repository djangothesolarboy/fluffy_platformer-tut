import pygame,math,os
from pygame.locals import *

global e_colorkey
e_colorkey=(255,255,255)

def set_global_colorkey(colorkey):
    global e_colorkey
    e_colorkey=colorkey

# physics core
# 2d collisions test
def collision_test(object_1,object_list):
    collision_list=[]
    for obj in object_list:
        if obj.colliderect(object_1):
            collision_list.append(obj)
    return collision_list

# 2d physics object
class physics_obj(object):
    def __init__(self,x,y,x_size,y_size):
        self.width=x_size
        self.height=y_size
        self.rect=pygame.Rect(x,y,self.width,self.height)
        self.x=x
        self.y=y

    def move(self,movement,platforms,ramps=[]):
        self.x+=movement[0]
        self.rect.x=int(self.x)
        block_hit_list=collision_test(self.rect,platforms)
        collision_types={'top':False,'bottom':False,'right':False,'left':False,'slant_bottom':False,'data':[]}
        # added collision data to "collision_types". ignore the poorly chosen variable name
        for block in block_hit_list:
            markers=[False,False,False,False]
            if movement[0]>0:
                self.rect.right=block.left
                collision_types['right']=True
                markers[0]=True
            elif movement[0] < 0:
                self.rect.left=block.right
                collision_types['left']=True
                markers[1]=True
            collision_types['data'].append([block,markers])
            self.x=self.rect.x
        self.y+=movement[1]
        self.rect.y=int(self.y)
        block_hit_list=collision_test(self.rect,platforms)
        for block in block_hit_list:
            markers=[False,False,False,False]
            if movement[1]>0:
                self.rect.bottom=block.top
                collision_types['bottom']=True
                markers[2]=True
            elif movement[1] < 0:
                self.rect.top=block.bottom
                collision_types['top']=True
                markers[3]=True
            collision_types['data'].append([block,markers])
            self.change_y=0
            self.y=self.rect.y
        return collision_types

# 3d collision detection
class cuboid(object):
    def __init__(self,x,y,z,x_size,y_size,z_size):
        self.x=x
        self.y=y
        self.z=z
        self.x_size=x_size
        self.y_size=y_size
        self.z_size=z_size

    def set_pos(self,x,y,z):
        self.x=x
        self.y=y
        self.z=z

    def collidecuboid(self,cuboid_2):
        cuboid_1_xy=pygame.Rect(self.x,self.y,self.x_size,self.y_size)
        cuboid_1_yz=pygame.Rect(self.y,self.z,self.y_size,self.z_size)
        cuboid_2_xy=pygame.Rect(cuboid_2.x,cuboid_2.y,cuboid_2.x_size,cuboid_2.y_size)
        cuboid_2_yz=pygame.Rect(cuboid_2.y,cuboid_2.z,cuboid_2.y_size,cuboid_2.z_size)
        if (cuboid_1_xy.colliderect(cuboid_2_xy)) and (cuboid_1_yz.colliderect(cuboid_2_yz)):
            return True
        else:
            return False

# entity stuff
def simple_entity(x,y,e_type):
    return entity(x,y,1,1,e_type)

def flip(img,boolean=True):
    return pygame.transform.flip(img,boolean,False)

def blit_center(surf,surf2,pos):
    x=int(surf2.get_width()/2)
    y=int(surf2.get_height()/2)
    surf.blit(surf2,(pos[0]-x,pos[1]-y))

class entity(object):
    global anim_db, anim_higher_db

    def __init__(self,x,y,size_x,size_y,e_type): # x, y, size_x, size_y, type
        self.x=x
        self.y=y
        self.size_x=size_x
        self.size_y=size_y
        self.obj=physics_obj(x,y,size_x,size_y)
        self.anim=None
        self.img=None
        self.anim_frame=0
        self.anim_tags=[]
        self.flip=False
        self.offset=[0,0]
        self.rotation=0
        self.type=e_type # used to determine anim set among other things
        self.action_timer=0
        self.action=''
        self.set_action('idle') # overall action for the entity
        self.entity_data={}
        self.alpha=None

    def set_pos(self,x,y):
        self.x=x
        self.y=y
        self.obj.x=x
        self.obj.y=y
        self.obj.rect.x=x
        self.obj.rect.y=y

    def move(self,momentum,platforms,ramps=[]):
        collisions=self.obj.move(momentum,platforms,ramps)
        self.x=self.obj.x
        self.y=self.obj.y
        return collisions

    def rect(self):
        return pygame.Rect(self.x,self.y,self.size_x,self.size_y)

    def set_flip(self,boolean):
        self.flip=boolean

    def set_anim_tags(self,tags):
        self.anim_tags=tags

    def set_anim(self,seq):
        self.anim=seq
        self.anim_frame=0

    def set_action(self,action_id,force=False):
        if (self.action==action_id) and (force==False):
            pass
        else:
            self.action=action_id
            anim=anim_higher_db[self.type][action_id]
            self.anim=anim[0]
            self.set_anim_tags(anim[1])
            self.anim_frame=0

    def get_entity_angle(entity_2):
        x1=self.x+int(self.size_x/2)
        y1=self.y+int(self.size_y/2)
        x2=entity_2.x+int(entity_2.size_x/2)
        y2=entity_2.y+int(entity_2.size_y/2)
        angle=math.atan((y2-y1)/(x2-x1))
        if x2 < x1:
            angle+=math.pi
        return angle

    def get_center(self):
        x=self.x+int(self.size_x/2)
        y=self.y+int(self.size_y/2)
        return [x,y]

    def clear_anim(self):
        self.anim=None

    def set_img(self,img):
        self.img=img

    def set_offset(self,offset):
        self.offset=offset

    def set_frame(self,amount):
        self.anim_frame=amount

    def handle(self):
        self.action_timer+=1
        self.change_frame(1)

    def change_frame(self,amount):
        self.anim_frame+=amount
        if self.anim!=None:
            while self.anim_frame < 0:
                if 'loop' in self.anim_tags:
                    self.anim_frame+=len(self.anim)
                else:
                    self.anim=0
            while self.anim_frame >= len(self.anim):
                if 'loop' in self.anim_tags:
                    self.anim_frame -= len(self.anim)
                else:
                    self.anim_frame=len(self.anim)-1

    def get_cur_img(self):
        if self.anim==None:
            if self.img!=None:
                return flip(self.img,self.flip)
            else:
                return None
        else:
            return flip(anim_db[self.anim[self.anim_frame]],self.flip)

    def get_drawn_img(self):
        img_to_render=None
        if self.anim==None:
            if self.img!=None:
                img_to_render=flip(self.img,self.flip).copy()
        else:
            img_to_render=flip(anim_db[self.anim[self.anim_frame]],self.flip).copy()
        if img_to_render!=None:
            center_x=img_to_render.get_width()/2
            center_y=img_to_render.get_height()/2
            img_to_render=pygame.transform.rotate(img_to_render,self.rotation)
            if self.alpha!=None:
                img_to_render.set_alpha(self.alpha)
            return img_to_render, center_x, center_y

    def display(self,surface,scroll):
        img_to_render=None
        if self.anim==None:
            if self.img!=None:
                img_to_render=flip(self.img,self.flip).copy()
        else:
            img_to_render=flip(anim_db[self.anim[self.anim_frame]],self.flip).copy()
        if img_to_render!=None:
            center_x=img_to_render.get_width()/2
            center_y=img_to_render.get_height()/2
            img_to_render=pygame.transform.rotate(img_to_render,self.rotation)
            if self.alpha!=None:
                img_to_render.set_alpha(self.alpha)
            blit_center(surface,img_to_render,(int(self.x)-scroll[0]+self.offset[0]+center_x,int(self.y)-scroll[1]+self.offset[1]+center_y))

# anim stuff
global anim_db
anim_db={}

global anim_higher_db
anim_higher_db={}

# a seq looks like [[0,1],[1,1],[2,1],[3,1],[4,2]]
# the first numbers are the image name(as integer), while the second number shows the duration of it in the seq
def anim_seq(seq,base_path,colorkey=(255,255,255),transparency=255):
    global anim_db
    result=[]
    for frame in seq:
        image_id=base_path+base_path.split('/')[-2]+'_'+str(frame[0])
        image=pygame.image.load(image_id+'.png').convert()
        image.set_colorkey(colorkey)
        image.set_alpha(transparency)
        anim_db[image_id]=image.copy()
        for i in range(frame[1]):
            result.append(image_id)
    return result

def get_frame(ID):
    global anim_db
    return anim_db[ID]

def load_anims(path):
    global anim_higher_db, e_colorkey
    f=open(path+'entity_anims.txt','r')
    data=f.read()
    f.close()
    for anim in data.split('\n'):
        sections=anim.split(' ')
        anim_path=sections[0]
        entity_info=anim_path.split('/')
        entity_type=entity_info[0]
        anim_id=entity_info[1]
        timings=sections[1].split(';')
        tags=sections[2].split(';')
        seq=[]
        n=0
        for timing in timings:
            seq.append([n,int(timing)])
            n+=1
        anim=anim_seq(seq,path+anim_path,e_colorkey)
        if entity_type not in anim_higher_db:
            anim_higher_db[entity_type]={}
        anim_higher_db[entity_type][anim_id]=[anim.copy(),tags]

# other useful functions
def swap_color(img,old_c,new_c):
    global e_colorkey
    img.set_colorkey(old_c)
    surf=img.copy()
    surf.fill(new_c)
    surf.blit(img,(0,0))
    surf.set_colorkey(e_colorkey)
    return surf
