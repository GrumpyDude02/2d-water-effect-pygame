import pygame,sys
from pygame.math import Vector2


pygame.init()
screen=pygame.display.set_mode((1280,700))
black=(0,0,0)
clock=pygame.time.Clock()


class watercube():
    def __init__(self,x,y,width,height,tile,speed):
        self.width=width
        self.height=height
        self.pos=Vector2(x,y)
        self.tile=64
        self.speed=speed
    
    def drawcube(self,window):
        self.rect=pygame.Rect(self.pos.x,self.pos.y,self.width,self.height)
        pygame.draw.rect(screen,pygame.Color('blue'),self.rect)
        
class falling_object():
    def __init__(self,pos,accelartion,speed):
        self.x=pos[0]
        self.y=pos[1]
        self.acc=accelartion
        self.speed=speed
        self.pos=Vector2(self.x,self.y)
    def gravity(self,window):
        self.speed+=self.acc
        self.pos.y+=self.speed
        self.rect=pygame.Rect(self.pos.x,self.pos.y,50,50)
        pygame.draw.rect(window,pygame.Color('red'),self.rect)
                
#cube=watercube(9,700//2,5,1000,64,0)
damp=0.035
waterlist=[watercube(0,700//2,8,500,64,0.5)]
left=[]
right=[]
cubes=[]
clicked=False
spread=1

for i in range(0,161):
    waterlist.append(watercube(waterlist[i].pos.x+8,(700//2),16,500,64,0))

for i in range(len(waterlist)):
    left.append(0)
    right.append(0)
    
def wavespread(spread):
    for i in range(len(waterlist)):
        if i>0:
            left[i] = spread*(waterlist[i].pos.y-waterlist[i-1].pos.y)
            waterlist[i-1].speed+=left[i]
        if i<len(waterlist)-1:
            right[i]=spread*(waterlist[i].pos.y-waterlist[i+1].pos.y)
            waterlist[i+1].speed+=right[i]

def oscillation(ob,dampeining):
    k=0.025
    x=ob.pos.y-(700//2)
    acceleration=(-k)*x
    ob.speed+=acceleration-ob.speed*dampeining
    ob.pos.y+=ob.speed
    
def wave(ob_list,dampening,):
    for i in range(len(ob_list)):
        oscillation(ob_list[i],damp)
  
def move(ob_list):
    mouse_pos=pygame.mouse.get_pos()   
    for i in range(len(ob_list)):
        if ob_list[i].rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                ob_list[i].pos.y=mouse_pos[1]
                ob_list[i+1].pos.y=mouse_pos[1]
                ob_list[i-1].pos.y=mouse_pos[1]
                
def perturbation(lis,index,speed):
    if index>=0 and index<=len(lis):
        lis[index].speed=speed

def spawn_object(cube_list):
    global clicked
    if pygame.mouse.get_pressed()[0]:
        clicked=True
    else:
        if clicked:
            mouse_pos=pygame.mouse.get_pos()
            cube_list.append(falling_object(mouse_pos,1,0))
            clicked=False   
            
def draw_cubes(cube_list,water_list):
    for cube in cube_list:
        cube.gravity(screen)
        if cube.pos.y>=710:
            cube_list.pop(cube_list.index(cube))
        for waters in water_list:
            if cube.rect.colliderect(waters.rect):
                waters.speed+=cube.speed*0.1
        
perturbation(waterlist,40,50)
       
while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            sys.exit()
    screen.fill(black)
    spawn_object(cubes)
    draw_cubes(cubes,waterlist)
    wave(waterlist,damp)
    for water in waterlist:
        water.drawcube(screen)
    move(waterlist)
    wavespread(spread)
    pygame.display.flip()
    clock.tick(60)