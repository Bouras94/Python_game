import pygame,math,random



pygame.init()                                                              # Init pygame

font = pygame.font.SysFont("monospace", 41)            # initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
SCALE=2                                                                    # Set Scale 
width,height = 320*SCALE,320*SCALE                         # Set width,height of the win
pygame.display.set_caption("kipoLife")                        # Set game title
display = pygame.display.set_mode((width,height))     # Set  main display
isRunning = True                                                        # Statement for main loop
clock = pygame.time.Clock()                                       # CLOCK
images=[]                                                                   # All images 
gameStatus=True                                                       # Status of the game :FALSE=Game Over
coins_num=0                                                              # count coins
"""==================================
== ~ ~ ~ ~ ~ ~         FUNCTIONS        ~ ~ ~ ~ ~ ~ ==
=================================  """
#Music function
def music():
    pygame.mixer.init()
    pygame.mixer.music.load('music/sound.wav')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.3)

#Find distance between two points
def distance(point1,point2):
    dist = math.sqrt( (point2.x -point1.x)**2 + (point2.y - point1.y)**2 )
    return dist

#Find enemies next node
def find_path(start,end,tiles):
    up=start-10
    down=start+10
    left=start-1
    right=start+1
    d0,d1,d2,d3=1000,1000,1000,1000 
 
    if up>=0:
        if tiles[up].gt=='2':
            d0=distance(tiles[end],tiles[up])
    if down<=len(tiles):
        if tiles[down].gt=='2':
            
            d1=distance(tiles[end],tiles[down]) 
    if left>=0:
        if tiles[left].gt=='2':
            d2=distance(tiles[end],tiles[left])
    if right<=len(tiles):
        if tiles[right].gt=='2':            
            d3=distance(tiles[end],tiles[right])
    mini=min([d0,d1,d2,d3])                         #find min distance

    if mini==d0:
        return  0,32*SCALE,0,-1
    elif mini==d1:        
        return  0,32*SCALE,0,1
    elif mini==d2:
        return  32*SCALE,0,-1,0
    elif mini==d3:
        return  32*SCALE,0,1,0
    else:
        return 0,0,0,0
         
#UPDATE SCREEN
def update(image,x,y):
    display.blit(image,(x,y))

def screen_texts():
    if gameStatus:
        #render text
        label = font.render("COINS:%d"%coins_num,1,(255,255,0))
        display.blit(label,(10,10))
    else:
        gameOver=True
        label = font.render("GAME OVER ! ! ! " ,1,(255,0,0))
        display.blit(label,(200,200))
        pass
            
    
    
 
    
    
# 2dArray for tiles
# Build MAP for the game  
def buildMap(level):
    
    Map = open('levels\map%d.txt'%level)    #open file
    tiles=[]                                                    #Tiles
    i=0
    j=0
    for x in Map:
        
        row = x.split(' ')
        for code in row:
            new_tile = tile(code.replace('\n',''),i,j)
            tiles.append(new_tile)
            i+=32*SCALE
        j+=32*SCALE
        i=0
        
  
    return tiles


# Check if  obj1 collide with obj2
def collide(obj1,obj2):
    if( obj2.y-obj1.image.get_height()<=obj1.y+4*SCALE<=obj2.y+obj2.image.get_height() ) and( obj2.x-obj1.image.get_width()<=obj1.x <=obj2.x+obj2.image.get_width()):
        return True

"""==================================
/////////////////////////////////////////////////////////////
=================================  """

    
"""==================================
== ~ ~ ~ ~ ~ ~         Classes                ~ ~ ~ ~ ~ ~ ==
=================================  """

                
#-----------------------1.Tile class
class tile(object):
    image=None
    def __init__(self,gt,x,y):
        self.gt=gt
        self.x=x
        self.y=y
        self.getImage(gt)
        
    def getImage(self,gt):
        self.image = pygame.image.load('ground/ground1.jpeg')
        if gt == '0' :
            self.image = pygame.image.load('ground/ground1.jpeg')
        elif gt == '1':
            self.image = pygame.image.load('ground/ground0.jpeg')
        elif gt == '2' :
            self.image = pygame.image.load('ground/ground2.jpeg')
        elif gt == '3':
            self.image = pygame.image.load('ground/ground3.jpeg')
        elif gt == '4' :
            self.image = pygame.image.load('ground/start.png')
        elif gt == '5':
            self.image = pygame.image.load('ground/end.png')
        new_image = pygame.transform.scale(self.image,(self.image.get_width()*SCALE,self.image.get_height()*SCALE))
        self.image=new_image
        
    def update(self,x,y):
        update(self.image,x,y)

        
          
#-----------------------2.Coin Class
class coin(object):
    images=[]
    x,y=0,0
    frame=0
    time=0
    def __init__(self,index):
        self.index=index
        for i in range(7):
            img =pygame.image.load('others/coins%d.png'%i)
            image = pygame.transform.scale(img,(img.get_width()*SCALE,img.get_height()*SCALE))
            self.images.append(image)
        self.image=self.images[0]
        self.position(index)
    def position(self,index):
        self.x=index[0]
        self.y=index[1]
    
            
            
        
    def update(self): 
        self.animation(self.images)
        update(self.image,self.x,self.y)
        
            
    def animation(self,images):
        self.image=images[self.frame]
        self.time+=1
        if self.time>5:
            self.frame+=1
            self.time=0
        if self.frame >= len(images):
            self.frame=0
        
        
#-----------------------3.Player class
class player(object):
    time=0
    frame=0
    images=[]
    def __init__(self,x,y,image):
        self.x=x
        self.y=y
        self.vx,self.vy=0,0
        for i in range(9):
            img = pygame.image.load('blue_monster/blue_monster%d.png'%i)
            self.image =pygame.transform.scale(img,(image.get_width()*SCALE,image.get_height()*SCALE))
            self.images.append(self.image)
            
    def update(self):
        self.animation(self.images)
        update(self.image,self.x,self.y)
        
    def animation(self,images):
        self.image=images[self.frame]
        self.time+=1
        if self.time>2:
            self.frame+=1
            self.time=0
        if self.frame >= len(images):
            self.frame=0

#-----------------------4. Enemy class
class enemy(object):
    rangex=0
    rangey=0
    last_w=''
    
    def __init__(self,x,y,image):
        self.x=x
        self.vx,self.vy=0,0
        self.y=y
        self.cx=0
        self.cy=0
        self.image = pygame.transform.scale(image,(image.get_width()*SCALE,image.get_height()*SCALE))
    def update(self): 
        update(self.image,self.x,self.y)
        
    def Range(self,x,y):
        if self.rangex==0 and self.rangey==0:
            self.rangex=x
            self.rangey=y
        else:
            if self.rangex>0:
                self.rangex-=1
            if self.rangey>0:
                self.rangey-=1
        
         
    
    def move(self):
        print "move"
"""==================================
/////////////////////////////////////////////////////////////
=================================  """


"""===========================================
~~|||||||||||||||||||||||||||||||||||   INIT SOME VARIABLES ||||||||||||||||||||||||||||||||||||||||||||||
~~===========================================
"""
p_image = pygame.image.load('blue_monster/blue_monster0.png')
e_image = pygame.image.load('green_monster/green_monster0.png')
enemies=[]
for i in range(2):
    i = enemy(0,0,e_image)
    enemies.append(i)
                                                                     


nextLevel=True
kipo = player(0,0,p_image)
tiles=buildMap(1)
#SET PLAYER POSITION 
for tile in tiles:
        if tile.gt=='4':
            kipo.x=tile.x+16*SCALE/2
            kipo.y=tile.y+16*SCALE/2
        if tile.gt=='5':
            for i in enemies:
                i.x=tile.x+16*SCALE/2
                i.y=tile.y+16*SCALE/2

def find(obj,tiles):
    index =0
    i=0
    for tile in tiles:
        if collide(obj,tile):
            index=i
            return index
        
        i+=1
    
music()
woods=[]
for tile in tiles:
    if tile.gt=='2':
        woods.append((tile.x,tile.y))
 
coins=[]
for i in range(10):
    rand=random.randint(0,len(woods)-1)
    c = coin(woods[rand])
    coins.append(c)




"""====================================== ==
====                        MAIN LOOP                                           "==
========================================"""
    
while isRunning: 
    pygame.display.update()         #Main display update method
    col=False                                # Collide
    col2=False                              # Collide
    distance(kipo,enemies[0])        #find distance
    start = find(enemies[0],tiles)    #find where is  enemy
    end = find(kipo,tiles)               #find where is kipo

    #====================================
    # bot settings
    #====================================
    if  enemies[0].rangex==0 and enemies[0].rangey==0:
        m1,m2,v1,v2=find_path(start,end,tiles)
        enemies[0].vx=v1
        enemies[0].vy=v2
    enemies[0].Range(m1,m2)
    #====================================
    # check if enemy col =True , if player col=True ,gameover
    #====================================    
    for tile in tiles:
        tile.update(tile.x,tile.y)
        if tile.gt=='5':#the end
            if collide(kipo,tile):
                print "Game OVer"
        if tile.gt=='0' or tile.gt=='1' or tile.gt=='3':
            if collide(kipo,tile):
                col=True
            if collide(enemies[0],tile):
                col2=True
        
            
    #====================================
    # * * * * * * Keyboard Input
    #====================================
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning=False
        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:                
                    kipo.vx=-3
            if event.key==pygame.K_RIGHT:
                    kipo.vx=3
            if event.key==pygame.K_UP:
                    kipo.vy=-3
            if event.key==pygame.K_DOWN:
                    kipo.vy=3
        if event.type == pygame.KEYUP:
            kipo.vx=0
            kipo.vy=0

    #====================================
    # check if player col =True
    #====================================
    if col:
        print("Col Kipo{%d,%d]"%(kipo.x,kipo.y))
        if kipo.vx==-3:
            kipo.vx=0
            kipo.x+=4
        elif kipo.vx==3:
            kipo.vx=0
            kipo.x-=4
        if kipo.vy==-3:
            kipo.vy=0
            kipo.y+=4
        elif kipo.vy==3:
            kipo.vy=0
            kipo.y-=4

    #====================================
    # check if enemy col =True
    #====================================
    if col2:
        print("Col Enemy{%d,%d]"%(enemies[0].x,enemies[0].y))
        if enemies[0].vx==-1:
            enemies[0].vx=0
            enemies[0].x+=4
        elif enemies[0].vx==1:
            enemies[0].vx=0
            enemies[0].x+=-4
        if enemies[0].vy==-1:
            enemies[0].vy=0
            enemies[0].y+=4
        elif enemies[0].vy==1:
            enemies[0].vy=0
            enemies[0].y+=-4

            
    if collide(kipo,enemies[0]):
        gameStatus=False
    screen_texts()
     
    kipo.y+=kipo.vy
    kipo.x+=kipo.vx
    for coin in coins:
        if collide(kipo,coin):
            coins_num+=10
            coin.x=-100
            coin.y=-100
            pickup= pygame.mixer.Sound("music/pickup_coin.wav")
            pickup.set_volume(0.2)
            pickup.play()
        coin.update()
    
    enemies[0].x+=enemies[0].vx
    enemies[0].y+=enemies[0].vy
    
    enemies[0].update()
    kipo.update()
    
    clock.tick(70)
    if len(images)>0:
        update()
    
pygame.quit()
        
    
     
