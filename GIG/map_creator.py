from library.liball import *


win_size = [8*30+50,8*20]
win = Window(size=win_size,flag=Flags.win_scales)
garss_images = load_block_cheat('data\grass_tiles.png',4,[8,8])

bg_grass_images = load_block_cheat(r'data\bg_grass_tiles.png',4,[8,8])
person_image = AnimatedSprite('data\person\person_stay.png',50)
jump_image = Sprite(load_image(r'data\jump_ponj\nopr_jump.png'))
key_image = AnimatedSprite('data\key_and_dor\key_anim.png')
ship_image = AnimatedSprite('data\lovishki\ship.png')
dor_image = AnimatedSprite('data\key_and_dor\dor_anim.png')
stone = AnimatedSprite('data\stone\stone.png')
portal_image = AnimatedSprite('data\portals\portla.png')

person_image.start()


portal_setup = False
vabor = 1
sloy = 1
portal_pos = [0,0]
def vaboring():
    global vabor,sloy
    if Keyboard.key_pressed('p'):
        vabor = -1
    if Keyboard.key_pressed('d'):
        vabor = 1
    if Keyboard.key_pressed('j'):
        vabor = 5
        
    if Keyboard.key_pressed('r'):
        vabor = 4
        
    if Keyboard.key_pressed('k'):
        vabor = 3
        
    if Keyboard.key_pressed('l'):
        vabor = 6
    
    if Keyboard.key_pressed('i'):
        vabor = 7
    
    if Keyboard.key_pressed('g'):
        vabor = 'portal'
        
    if Keyboard.key_pressed('1'):
        sloy = 1
        
    if Keyboard.key_pressed('0'):
        sloy = 0
        
    if Keyboard.key_pressed('a'):
        vabor = 99
        

def save(name: str):
    if Keyboard.key_pressed('s'):
        data = [map, bg]
        WirteBinaryFile(f'maps/{name}.bin',data)


def map_create(mapping, garss_images):
    
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
                    
                if mapping[i+1][j-1]!=1 and mapping[i+1][j+1]!=1:
                    garss_images['left_right_down'].center = [j*8+4,i*8+4]
                    garss_images['left_right_down'].draw_surf(surf)
                    
                if mapping[i-1][j-1]!=1 and mapping[i-1][j+1]!=1:
                    garss_images['left_right_up'].center = [j*8+4,i*8+4]
                    garss_images['left_right_up'].draw_surf(surf)
            
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


map = []
for i in range(20+1):
    m = []
    for j in range(30+1):
        m.append(0)
    map.append(m)
    
bg = []
for i in range(20+1):
    m = []
    for j in range(30+1):
        m.append(0)
    bg.append(m)

def viev_map():
    person_image.update()
    
    
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == -1:
                
                person_image.center = [j*8+4,i*8+4]
                person_image.render(win)
            if map[i][j] == 5:
                
                jump_image.center = [j*8+4,i*8+4]
                jump_image.draw(win)
            if map[i][j] == 3:
                
                key_image._sprites[0].center = [j*8+4,i*8+4]
                key_image._sprites[0].draw(win)
                
            if map[i][j] == 7:
                
                ship_image._sprites[0].center = [j*8+4,i*8+4+2]
                ship_image._sprites[0].draw(win)
            if map[i][j] == 6:
                
                dor_image._sprites[0].center = [j*8+8,i*8+8]
                dor_image._sprites[0].draw(win)
            
            if map[i][j] == 4:
                
                stone._sprites[0].center = [j*8+4,i*8+4]
                stone._sprites[0].draw(win)
            
            if  isinstance( map[i][j] ,str) :
                
                portal_image._sprites[0].center = [j*8+4,i*8+4]
                portal_image._sprites[0].draw(win)
                
                pos = string_to_list(map[i][j])
                portal_image._sprites[0].center = [pos[0]*8+4,pos[1]*8+4]
                portal_image._sprites[0].draw(win)
                
                
def map_setter():
    global map,portal_pos, portal_setup
    mouse_coord = Mouse.position()
    mouse_coord[0]-=mouse_coord[0]%8
    mouse_coord[1]-=mouse_coord[1]%8
    dx = mouse_coord[0]//8
    dy = mouse_coord[1]//8
    try:
        if Mouse.press(Mouse.right):
                map[dy][dx] = 0
        if vabor != 'portal':
            if Mouse.press():
                if sloy == 1:
                    map[dy][dx] = vabor
                elif sloy == 0:
                    print('yes')
                    bg[dy][dx] = vabor
            
        else:
            if portal_setup and Mouse.click():
                if sloy == 1:
                    map[dy][dx] = str(portal_pos)
                portal_pos = [0,0]
                portal_setup = False

            if Mouse.click():
                portal_pos = [dx,dy]
                portal_setup = True
            
                
        
    except:...

def render_grid():
    [Draw.draw_dashed_vline(win(), [i*8,0],[i*8,20*8], (200,200,200),1,4) for i in range(30+1)]
    [Draw.draw_dashed_hline(win(), [0,i*8],[30*8,i*8], (200,200,200),1,4) for i in range(20+1)]


while win.update(fps_view=0,fps='max'):
    
    render_grid()
    vaboring()
    map_setter()

    surf = map_create(map,garss_images)
    surf2 = map_create(bg,bg_grass_images)
    win._win.blit(surf2,[0,0])
    viev_map()
    win._win.blit(surf,[0,0])
    save('test5')