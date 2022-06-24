
import pygame,sys
from pygame.math import Vector2


pygame.init()
screen=pygame.display.set_mode((1280,700))
black=(0,0,0)
blue=(30,140,255)
clock=pygame.time.Clock()
damp=0.035
left=[]
right=[]
spreads=0.8
clickd=False
cubes=[]


class spring():
    def __init__(self,x,y,speed):
        self.pos=Vector2(x,y)
        self.tile=64
        self.speed=speed
        self.rect=pygame.Rect(self.pos.x,self.pos.y,5,5)
        
class falling_object2():
    def __init__(self,pos,accelartion,speed):
        self.x=pos[0]
        self.y=pos[1]
        self.acc=accelartion
        self.speed=speed
        self.pos=Vector2(self.x,self.y)
        self.inwater=False
    def gravity(self,window):
        self.speed+=self.acc
        self.pos.y+=self.speed
        self.rect=pygame.Rect(self.pos.x,self.pos.y,75,75)
        pygame.draw.rect(window,pygame.Color('red'),self.rect)


springs=[spring(0,700//2,0)] 


for i in range(0,161):
    springs.append(spring(springs[i].pos.x+8,700//2,0))

for i in range(0,161):
    right.append(0)
    left.append(0)
    
def spawn_object(cube_list):
    global clickd
    if pygame.mouse.get_pressed()[0]:
        clickd=True
    else:
        if clickd:
            mouse_pos=pygame.mouse.get_pos()
            cube_list.append(falling_object2(mouse_pos,2,0))
            clickd=False    

def draw_cube(cube_list,water_list):
    for cube in cube_list:
        cube.gravity(screen)
        if cube.pos.y>=710:
            cube_list.pop(cube_list.index(cube))
        for waters in water_list:
            if cube.rect.colliderect(waters.rect):
                cube.inwater=True
                waters.speed+=cube.speed*0.75
                
        if cube.inwater:  
            cube.acc-=cube.acc*2
              
            if cube.speed<0:
                cube.speed=0.01
            
                    
            

    
def oscillation(ob,dampeining):
    k=0.015
    x=ob.pos.y-(700//2)
    acceleration=(-k)*x
    ob.pos.y+=ob.speed
    ob.speed+=acceleration-ob.speed*dampeining
    

def draw_lines(screen,spring_list):
    polygonSurface=pygame.Surface((1280,700))
    polygonSurface.set_colorkey((0,0,0))
    polygon_points=[(1280,700),(0,700)]
    for i in range(0,161):
        if i+1!=len(spring_list):
            pygame.draw.line(screen,pygame.Color('white'),(spring_list[i].pos.x,spring_list[i].pos.y-2.5),(spring_list[i+1].pos.x,spring_list[i+1].pos.y-2.5),5) 
        polygon_points.append((spring_list[i].pos.x,spring_list[i].pos.y))
    pygame.draw.polygon(polygonSurface,blue,polygon_points)
    polygonSurface.set_alpha(120)
    screen.blit(polygonSurface,(0,0))
    wavespread2(springs,spreads)
        
def wavespread2(springs_list,spread):
    for i in range(161):
        oscillation(springs[i],damp)
    for i in range(0,161):
        if i>0:
            left[i]=spread*(springs_list[i].pos.y-springs_list[i-1].pos.y)
            springs_list[i-1].speed+=left[i]
        if i<160:
            right[i]=spread*(springs_list[i].pos.y-springs_list[i+1].pos.y)
            springs_list[i+1].speed+=right[i]
    
def perturbation(lis,index,speed):
    if index>=0 and index<=len(lis):
        lis[index].speed=speed


while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            sys.exit()
    screen.fill(black)
    spawn_object(cubes)
    draw_cube(cubes,springs)
    draw_lines(screen,springs)
    wavespread2(springs,spreads)
    pygame.display.flip()
    clock.tick(60)