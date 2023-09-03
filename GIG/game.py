from library.liball import *



WIN_SIZE = [1920//6,1080//6]
win = Window(size=WIN_SIZE, flag=Flags.win_scales | Flags.win_resize)
GRASS_IMAGES = load_block_cheat('data\grass_tiles.png',4,[8,8])
BG_GRASS_IMAGES = load_block_cheat(r'data\bg_grass_tiles.png',4,[8,8])

class Person:
    def __init__(self, space) -> None:
        self.stay_anim = AnimatedSprite('data\person\person_stay.png',20)
        self.run_anim = AnimatedSprite('data\person\person_run.png',5)
        self.jump_anim = AnimatedSprite('data\person\person_jamp.png',10)
        
        self.stay_anim.start()
        self.run_anim.start()
        self.napr = False
        self.move = False
        self.killing = False
        self.killing_timer = 200
        self.rendering_pos = [0,0]
        
        
        
        self.renderer = True
        
        self.collider = Collider(8,8,6,7, True, id='person', mass=10)
        
        
        
        space.add(self.collider)
        

          
    def render(self,win,global_pos):
        pos = copy([self.collider.center[0],self.collider.center[1]])
        pos = [
            pos[0]+global_pos[0],
            pos[1]+global_pos[1]
        ]
        self.rendering_pos = copy(pos)
        self.stay_anim.center = pos
        self.run_anim.center = pos
        self.jump_anim.center = pos
        self.stay_anim.update()
        self.run_anim.update()
        

        if self.renderer:
            if self.collider._collides['down']:
                if self.move:
                    self.run_anim.render(win)
                else:
                    self.stay_anim.render(win)
            else:
                self.jump_anim.render(win)
             
    def set_pos(self,pos):
        self.collider.center = [pos[0],pos[1]]
   
    def update(self):
        #self.collider.draw(win())
        
        
        self.run_anim.set_mirror(self.napr)
        self.stay_anim.set_mirror(self.napr)
        self.jump_anim.set_mirror(self.napr)
        
        
        self.move = False
        if self.renderer:
            if Keyboard.key_pressed('up') and self.collider._collides['down']:
                self.collider.sy = -2 
                

            if Keyboard.key_pressed('left'):
                self.collider.sx = -1.5 
                self.napr = True
                self.move = True
            if Keyboard.key_pressed('right'):
                self.collider.sx = 1.5 
                self.napr = False
                self.move = True
            
        

        
        #if self.collider.y>win_size[1]:
        #    self.collider.y = win_size[1]-10

class Camera:
    def __init__(self) -> None:
        self.sx = 0
        self.sy = 0
        
    def camera_speed(self, item, target_item,speed=0.5):
        self.sx = (item[0]-target_item[0])*speed
        self.sy = (item[1]-target_item[1])*speed

class Jump_bust:
    def __init__(self) -> None:
        self.image_no_jump = Sprite(load_image( r'data\jump_ponj\nopr_jump.png' ))
        self.image_jump = Sprite( load_image( r'data\jump_ponj\press_jump.png'))
        self.pos = [0,0]
        self.pressed = False
    
    def set_pos(self, pos):
        self.pos = pos
        self.collder = Collider(self.pos[0],self.pos[1]-5+8,8,3)
        self.image_no_jump.center = [self.pos[0]+4,self.pos[1]+4]
        self.image_jump.center = [self.pos[0]+4,self.pos[1]+4]
        self.timer = 0
    
    def render(self, win, person: Person, global_pos):
        pos = [
            self.collder.center[0]+global_pos[0],
            self.collder.center[1]+global_pos[1]
        ]
        self.image_no_jump.center = pos
        self.image_jump.center = pos

        if not self.pressed:
            self.image_no_jump.draw(win)
        else:
            self.image_jump.draw(win)
            
        if person.collider._rect.collide_rect(self.collder._rect) and person.collider.sy>0:
            person.collider.sy=-3
            self.timer = 5
        
        if self.timer!=0:
            self.pressed = True
            self.timer-=0.1

        if self.timer<0:
            self.pressed = False
            self.timer = 0

class Air_Jump_bust:
    def __init__(self) -> None:
        self.image_no_jump = AnimatedSprite( r'data\jump_ponj\air_not_jump.png' )
        self.image_jump = AnimatedSprite( r'data\jump_ponj\air_jump.png')
        self.image_jump.start()
        self.image_no_jump.start()

        self.pressed = False
        self.press_timer = 0
        self.speed = 0
    
    def set_pos(self, pos):
        
        self.collder = Collider(pos[0],pos[1]-5+8,8,3)
        self.pos = copy(self.collder._rect.y)
        self.image_no_jump.center = [pos[0]+4,pos[1]-7]
        self.image_jump.center = [pos[0]+4,pos[1]-7]
        self.timer = 0
        
    
    def render(self, win, person,global_pos):
        

        self.press_timer+=0.1
        
        
        self.speed *=0.5
        self.speed+=(self.collder._rect.y-self.pos)/50
        
        self.collder._rect.y-=self.speed
        
        
        
        
        
        
        
        
        
        pos = [
            self.collder.center[0]+global_pos[0],
            self.collder.center[1]+global_pos[1]-4
        ]
        self.image_no_jump.center = pos
        self.image_jump.center = pos

        self.image_jump.update()
        self.image_no_jump.update()
        if not self.pressed:
            self.image_no_jump.render(win)
        else:
            self.image_jump.render(win)
            
        #self.collder.draw(win._win)
            
        if person.collider._rect.collide_rect(self.collder._rect) and person.collider.sy>0:
            person.collider.sy=-2.5
            self.speed = -10
            

            self.timer = 5
            self.press_timer = 0
        
        if self.timer!=0:
            self.pressed = True
            self.timer-=0.1

        if self.timer<0:
            self.pressed = False
            self.timer = 0  

class Small_Box:
    def __init__(self) -> None:
        self.sprite = Sprite(load_image(r'data\boxes\small_box.png'))  
        
    def set_pos(self,pos, colliders):
        self.collider = Collider(pos[0],pos[1], 8,8, True, resistance=Vector2(1,1), mass=1,)
        colliders.add(self.collider)
        
    def render(self ,win, global_pos):
        
        pos = [
            self.collider.center[0]+global_pos[0],
            self.collider.center[1]+global_pos[1]
        ]

        
        self.sprite.center = pos
        self.sprite.draw(win)
        


class Level:
    def __init__(self, level_file_: Any) -> None:
        self._level_file = LoadBinaryFile(level_file_)
        
        self.map_surf = self.CreateTilesMap(self._level_file[0], GRASS_IMAGES)
        self.bg_map_surf = self.CreateTilesMap(self._level_file[1], BG_GRASS_IMAGES)
        
        self.rects_space = ColliderSpace(gravity=Vector2(0,0.1),air_resistance=Vector2(0.8,1))
        self.CreateColliders(self._level_file[0])
        
        self.Camera = Camera()
        self.Person: Person = Person(self.rects_space)
        self.jump_busts: Tuple[Jump_bust, ...] = []
        self.boxes: Tuple[Small_Box, ...] = []
        
        self.CreateObjects(self._level_file[0])
        
        self.global_pos = [0,0]
        
        
    def CreateColliders(self, mapping):
        x = 0
        y = 0
        for i in range(len(mapping)):
            
            rect_start = False
            rect_width = 0
            y = i*8
            
            for j in range(len(mapping[i])):
                #if mapping[i][j] == 4:
                #    rects.append(Collider(j*8,i*8,8,8))
                
                if mapping[i][j]==1 and rect_start == False:
                    rect_start = True
                    x = j*8
                
                if rect_start and mapping[i][j]==1:
                    rect_width +=8
                    
                try:
                    if rect_start and mapping[i][j+1]!=1:
                        self.rects_space.add(Collider(x,y,rect_width,8,resistance=Vector2(0.99,0.5)))
                        rect_start = False
                        rect_width = 0
                except:
                    ...
        
    def CreateTilesMap(self, mapping, garss_images):
       
        surf = pygame.Surface([len(mapping[0])*8,len(mapping)*8]).convert_alpha()
        surf.set_colorkey((0,0,0))
        
        for i in range(len(mapping)):
            for j in range(len(mapping[i])):
                
                if j+1==len(mapping[0]):j-=1
                if i+1==len(mapping):i-=1
                if mapping[i][j] == 1 and mapping[i-1][j] != 1:
                    
                    if mapping[i][j-1] == 1 and mapping[i][j+1] ==1:
                        garss_images['top_middle'].center = [j*8+4,i*8+4]
                        garss_images['top_middle'].draw_surf(surf)
                    if mapping[i][j-1] != 1 and mapping[i][j+1] ==1:
                        garss_images['top_left'].center = [j*8+4,i*8+4]
                        garss_images['top_left'].draw_surf(surf)
                    if mapping[i][j-1] == 1 and mapping[i][j+1] !=1:
                        garss_images['top_right'].center = [j*8+4,i*8+4]
                        garss_images['top_right'].draw_surf(surf)
                    
                    if mapping[i][j-1] != 1 and mapping[i][j+1] !=1:
                        garss_images['top_vertical'].center = [j*8+4,i*8+4]
                        garss_images['top_vertical'].draw_surf(surf)
                        
                    if mapping[i][j-1] == 1 and mapping[i][j+1] ==1 and mapping[i+1][j] !=1:
                        garss_images['center_horizontal'].center = [j*8+4,i*8+4]
                        garss_images['center_horizontal'].draw_surf(surf)
                        
                    if mapping[i][j-1] == 1 and mapping[i][j+1] !=1 and mapping[i+1][j] !=1:
                        garss_images['right_horizontal'].center = [j*8+4,i*8+4]
                        garss_images['right_horizontal'].draw_surf(surf)
                        
                    if mapping[i][j-1] != 1 and mapping[i][j+1] == 1 and mapping[i+1][j] !=1:
                        garss_images['left_horizontal'].center = [j*8+4,i*8+4]
                        garss_images['left_horizontal'].draw_surf(surf)
                    
                        
                elif mapping[i][j]==1 and mapping[i-1][j] == 1 and mapping[i+1][j]!=1:
                    if mapping[i][j-1] == 1 and mapping[i][j+1] == 1:
                        garss_images['down_middle'].center = [j*8+4,i*8+4]
                        garss_images['down_middle'].draw_surf(surf)
                    if mapping[i][j-1] != 1 and mapping[i][j+1] ==1:
                        garss_images['down_left'].center = [j*8+4,i*8+4]
                        garss_images['down_left'].draw_surf(surf)
                    if mapping[i][j-1] == 1 and mapping[i][j+1] !=1:
                        garss_images['down_right'].center = [j*8+4,i*8+4]
                        garss_images['down_right'].draw_surf(surf)
                        
                    if mapping[i][j-1] != 1 and mapping[i][j+1] !=1:
                        garss_images['down_vertical'].center = [j*8+4,i*8+4]
                        garss_images['down_vertical'].draw_surf(surf)
                        
                elif mapping[i][j]==1 and mapping[i-1][j] == 1 and mapping[i+1][j]==1 and mapping[i][j-1] != 1 and mapping[i][j+1]!=1 :
                    garss_images['center_vertical'].center = [j*8+4,i*8+4]
                    garss_images['center_vertical'].draw_surf(surf)
                    
                if mapping[i][j]==1 and mapping[i+1][j]==1 and mapping[i-1][j]==1 and mapping[i][j+1]==1 and mapping[i][j-1]==1:
                    garss_images['center_middle'].center = [j*8+4,i*8+4]
                    garss_images['center_middle'].draw_surf(surf)
                    if mapping[i-1][j-1]!=1:
                        garss_images['left_up'].center = [j*8+4,i*8+4]
                        garss_images['left_up'].draw_surf(surf)
                    elif mapping[i-1][j+1]!=1:
                        garss_images['right_up'].center = [j*8+4,i*8+4]
                        garss_images['right_up'].draw_surf(surf)
                        
                    if mapping[i+1][j-1]!=1:
                        garss_images['left_down'].center = [j*8+4,i*8+4]
                        garss_images['left_down'].draw_surf(surf)
                    elif mapping[i+1][j+1]!=1:
                        garss_images['right_down'].center = [j*8+4,i*8+4]
                        garss_images['right_down'].draw_surf(surf)
                
                if mapping[i][j]==1 and mapping[i+1][j]==1 and mapping[i-1][j]==1 and mapping[i][j+1]!=1 and mapping[i][j-1]==1:
                    garss_images['center_right'].center = [j*8+4,i*8+4]
                    garss_images['center_right'].draw_surf(surf)
                if mapping[i][j]==1 and mapping[i+1][j]==1 and mapping[i-1][j]==1 and mapping[i][j+1]==1 and mapping[i][j-1]!=1:
                    garss_images['center_left'].center = [j*8+4,i*8+4]
                    garss_images['center_left'].draw_surf(surf)
                
                if mapping[i][j]==1 and mapping[i+1][j]!=1 and mapping[i-1][j]!=1 and mapping[i][j+1]!=1 and mapping[i][j-1]!=1:
                    garss_images['one'].center = [j*8+4,i*8+4]
                    garss_images['one'].draw_surf(surf)
                    
        return surf
    
    def CreateObjects(self, mapping):
        for i in range(len(mapping)):
            for j in range(len(mapping[i])):
                
                if j+1==len(mapping[0]):j-=1
                if i+1==len(mapping):i-=1
                
                #? CreatePerson -----------------------------------
                if mapping[i+1][j]==-1:
                    self.Person.set_pos([j*8+5,i*8+8+4])
                #? CreatePerson -----------------------------------
                
                #? CreateJumpBusts --------------------------------
                if mapping[i][j] == 5 and mapping[i+1][j]==1:
                    jb = Jump_bust()
                    jb.set_pos([j*8,i*8])
                    self.jump_busts.append(jb)
                if mapping[i][j]==5 and mapping[i+1][j]!=1:
                    jb = Air_Jump_bust()
                    jb.set_pos([j*8,i*8])
                    self.jump_busts.append(jb)
                #? CreateJumpBusts --------------------------------
                
                if mapping[i][j]==99:
                    b = Small_Box()
                    b.set_pos([j*8,i*8],self.rects_space)
                    self.boxes.append(b)
                    
                
                
    
    def update(self):
        
        
        self.Camera.camera_speed(self.Person.rendering_pos, [WIN_SIZE[0]/2, WIN_SIZE[1]/2],0.1)
        self.global_pos[0]-=round( self.Camera.sx,0 )
        self.global_pos[1]-=round( self.Camera.sy,0 )
        
        win().blit(self.bg_map_surf,self.global_pos)
        win().blit(self.map_surf,self.global_pos)
        
        self.rects_space.simulate()
        
        [b.render(win, self.Person, self.global_pos) for b in self.jump_busts]
        
        self.Person.render(win, self.global_pos)
        self.Person.update()
        
        [b.render(win, self.global_pos) for b in self.boxes]
        
        
        #self.Person.collider.draw(win())
        #self.rects_space.render(win())















l = Level(r'maps\test5.bin')



while win.update(fps_view=0,base_color='gray'):
    l.update()

