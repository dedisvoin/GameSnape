from library.liball import *


win_size = [8*30,8*20]

win = Window(size=win_size,flag=Flags.win_scales|Flags.win_resize)
global_pos = [0,0]
garss_images = load_block_cheat('data\grass_tiles.png',4,[8,8])
bg_grass_images = load_block_cheat(r'data\bg_grass_tiles.png',4,[8,8])
sound_portal = Sound('data\sounds\Portal.wav')
sound_any_jump = Sound('data\sounds\Jump_any.wav')
sound_jump = Sound('data\sounds\Jump.wav')
sound_open_dor = Sound('data\sounds\Open_dor.wav')
sound_pick_up_key = Sound('data\sounds\Pick_up_key.wav')
sound_player_kill = Sound('data\sounds\PLayer_kill.wav')



class Person:
    def __init__(self, space) -> None:
        self.stay_anim = AnimatedSprite('data\person\person_stay.png',20)
        self.run_anim = AnimatedSprite('data\person\person_run.png',5)
        self.jump_anim = AnimatedSprite('data\person\person_jamp.png',10)
        self.jump_dam = AnimatedSprite('data\person\person_jump_dam.png',6,True)
        self.stay_anim.start()
        self.run_anim.start()
        self.napr = False
        self.move = False
        self.killing = False
        self.killing_timer = 200
        
        self.renderer = True
        
        self.collider = Collider(8,8,6,7)
        space.add(self.collider)
        
        self.level_close_anim = AnimatedSprite('data\level_split_anim.png',3,True)
        
        self.kill_particle  = (
            Particle()
            .set_shape(Shapes.IMAGE)
            .set_sprite(Sprite(load_image('data\person\kill_particle.png')),1.1)
            .set_phisics_trenie(Vector2(0.7,0.7))
            .set_color('blue')
            .set_radius(20)
            .set_size([30,30])
            .set_move_duration(90)
            
            .set_phisics_simulate(True)
            .set_speed(3)
            .set_sprite_mode(SpriteModes.VECTOR)
            .set_size_deller(0.01)
            .set_phisics_gravity(Vector2(0,0.01))
        )
        self.person_particles_space = ParticleSpace([0,0],win_size,win)
        self.kill_particles_spavner = Spavner(spavner_size_=[3,3])
          
    def render(self,win):
        pos = copy([self.collider.center[0],self.collider.center[1]])
        self.stay_anim.center = pos
        self.run_anim.center = pos
        self.jump_anim.center = pos
        self.stay_anim.update()
        self.run_anim.update()
        
        self.jump_dam.update()
        self.jump_dam.render(win)
        if self.renderer:
            if self.collider.collides['down']:
                if self.move:
                    self.run_anim.render(win)
                else:
                    self.stay_anim.render(win)
            else:
                self.jump_anim.render(win)
             
    def set_pos(self,pos):
        self.collider.center = [pos[0],pos[1]]
               
    def out(self):
        return not self.collider.center[0]>win_size[0]
        
    def update(self, rects):
        #self.collider.draw(win())
        
        
        self.run_anim.set_mirror(self.napr)
        self.stay_anim.set_mirror(self.napr)
        self.jump_anim.set_mirror(self.napr)
        
        if self.jump_dam.end_sprite():
            self.jump_dam = AnimatedSprite('data\person\person_jump_dam.png',6,True)
            self.jump_dam.center = [-20,-20]
        self.move = False
        if self.renderer:
            if Keyboard.key_pressed('up') and self.collider.collides['down']:
                self.collider.sy = -2 
                self.jump_dam.start()
                sound_any_jump.play()
                self.jump_dam.center = self.collider.center
            if Keyboard.key_pressed('left'):
                self.collider.sx = -1.5 
                self.napr = True
                self.move = True
            if Keyboard.key_pressed('right'):
                self.collider.sx = 1.5 
                self.napr = False
                self.move = True
            
        
        
        self.person_particles_space.update(rects)
        self.person_particles_space.draw()
        self.person_particles_space.deller()
        
        #if self.collider.y>win_size[1]:
        #    self.collider.y = win_size[1]-10
    
    def KILL(self, game):
        if self.killing:
            self.killing_timer-=1
            if self.killing_timer<=0:
                self.level_close_anim.start()
                if self.level_close_anim.end_sprite():
                    print('rl')
                    game.Reload()
                    
                    
        self.level_close_anim.update()
        for i in range(win_size[0]//16):
            for j in range(win_size[1]//16):
                self.level_close_anim.center = [i*16+8,j*16+8]
                self.level_close_anim.render(win)

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
    
    def render(self, win, person: Person):

        if not self.pressed:
            self.image_no_jump.draw(win)
        else:
            self.image_jump.draw(win)
            
        if person.collider.collide_rect(self.collder) and person.collider.sy>0 and not person.killing:
            person.collider.sy=-3
            sound_jump.play()
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
        self.pos = [0,0]
        self.pressed = False
        self.press_timer = 0
        self.tt = 5
    
    def set_pos(self, pos):
        self.pos = pos
        self.collder = Collider(self.pos[0],self.pos[1]-5+8,8,3)
        self.image_no_jump.center = [self.pos[0]+4,self.pos[1]-7]
        self.image_jump.center = [self.pos[0]+4,self.pos[1]-7]
        self.timer = 0
    
    def render(self, win, person):

        self.press_timer+=0.1
        self.image_no_jump.center[1]+=sin(self.press_timer)/self.tt
        self.image_jump.center[1]+=sin(self.press_timer)/self.tt
        self.image_jump.update()
        self.image_no_jump.update()
        if not self.pressed:
            self.image_no_jump.render(win)
        else:
            self.image_jump.render(win)
            
        #self.collder.draw(win._win)
            
        if person.collider._rect.collide_rect(self.collder) and person.collider.sy>0 and not person.killing:
            person.collider.sy=-3
            sound_jump.play()
            self.timer = 5
            self.tt = 1
            self.press_timer = 0
        
        if self.timer!=0:
            self.pressed = True
            self.timer-=0.1
            self.tt = 1

        if self.timer<0:
            self.pressed = False
            self.timer = 0  
            self.tt = 5  
        
        self.image_no_jump.center[1] -= (self.image_no_jump.center[1]- self.collder.center[1]+10)/10
        self.image_jump.center[1] -= (self.image_jump.center[1]- self.collder.center[1]+10)/10

class Stone:
    def __init__(self) -> None:
        self.animation = AnimatedSprite('data\stone\stone.png',4,True)
    
    def set_pos(self, pos):

        self.colider = Collider(pos[0],pos[1],8,8)
        self.up_collider = Collider(pos[0],pos[1]-2,8,8)
        self.animation.center = self.colider.center

        
        
    def render(self,win, person):

        self.animation.update()
        self.animation.render(win)
        if self.up_collider.collide_rect(person.collider):
            self.animation.start()
        if not self.animation._render:
            self.colider.colliding = False

class Key:
    def __init__(self) -> None:
        self.image = AnimatedSprite('data\key_and_dor\key_anim.png',5)     
        self.image.start()
        self.timer = 0
        self.uped = False
        self.dor_open = False
        self.kill_timer = 50
        self.key_particles = (
            Particle()
            .set_color((255,238,67))
            .set_shape(Shapes.IMAGE)
            .set_size([4,4])
            .set_sprite(Sprite(load_image(f'data\key_and_dor\key_particle.png')))
            .set_size_deller(0.2)
            .set_move_duration(180)
            .set_move_adding(0.8)
        )
        self.key_line_particles = (
            Particle()
            .set_color((255,238,67))
            .set_shape(Shapes.IMAGE)
            .set_size([4,4])
            .set_sprite(Sprite(load_image(f'data\key_and_dor\key_particle.png')),0.5)
            .set_size_deller(0.12)
            .set_speed(0.01)
            .set_move_duration(180)
            .set_move_adding(0.8)
            .set_speed(0.3)
        )
        self.particle_space = ParticleSpace([0,0],win_size,win)
        self.spavner = Spavner(spavner_size_=[1,1])
        self.spavner_line = Spavner(SpavnerTypes.LINE_SPAVNER)
        
        self.circle_render_center = [0,0]
        self.circle_rendering = False
        self.circle_radius = 1
        self.dx = 0
        self.dy = 0
    
    def set_pos(self, pos):
        self.collider = Collider(pos[0],pos[1], 8,8)   
        
    def render(self, win, person: Person, dor):
        self.timer+=1
        self.image.center = self.collider.center
        self.image.center[1]+=sin(self.timer/10)
        self.particle_space.update()
        self.particle_space.draw()
        self.image.update()
        self.image.render(win)
        #self.collider.draw(win._win)
        if person.collider.collide_rect(self.collider) and not self.uped:
            sound_pick_up_key.play()
        if person.collider.collide_rect(self.collider):
            self.uped = True
            
            self.circle_render_center = copy(self.collider.center)
            self.circle_rendering = True
        if not self.dor_open:
            if self.uped:
                if not person.killing:
                    self.dx = self.collider.center[0]-person.collider.center[0]
                    self.dy = self.collider.center[1]-person.collider.center[1]+15
                
                if person.killing:
                    self.dx*=0.9
                    self.dy*=0.9
                else:
                    self.dx*=0.05
                    self.dy*=0.05
                
                self.collider.center = [
                        self.collider.center[0]-self.dx,
                        self.collider.center[1]-self.dy
                ]
                if not person.killing:
                    self.spavner_line.pos_2 = self.collider.center
                    self.spavner_line.pos = person.collider.center
                    
                    self.particle_space.add(self.key_line_particles, self.spavner_line,1,1)
        else:
            dx = self.collider.center[0]-dor.collider.center[0]
            dy = self.collider.center[1]-dor.collider.center[1]
                
            self.collider.center = [
                    self.collider.center[0]-dx*0.1,
                    self.collider.center[1]-dy*0.1
            ]
            self.kill_timer-=1
        
        if self.kill_timer==0:
            self.spavner.pos = self.collider.center
            
            self.image._render = False
            self.particle_space.add(self.key_particles, self.spavner, 5,1)
        
        
        
        
        if self.circle_rendering and self.circle_radius<20:
            Draw.draw_circle(win(), self.circle_render_center, self.circle_radius, (255,238,67), max( int(10-self.circle_radius/2), 1),((110,100,5),1))
            self.circle_radius+=0.5
            
        self.particle_space.deller()
        
class Dor:
    def __init__(self) -> None:
        self.dor_anim = AnimatedSprite('data\key_and_dor\dor_anim.png',5,True) 
        
          
        
    def set_pos(self,pos):
        self.collider = Collider(pos[0],pos[1], 16,16) 
        self.detect_collider = Collider(pos[0]-10,pos[1]-10, 36,36)
        
    def dor_opened(self):
        return self.dor_anim._render
        
    def render(self, win, key, person):
        self.dor_anim.center = self.collider.center
        self.dor_anim.update()
        self.dor_anim.render(win)
        
        if key.uped:
            if person.collider.collide_rect(self.detect_collider):
                self.dor_anim.start()

                key.dor_open = True
                if self.dor_anim.end_sprite():
                    sound_open_dor.play()
                
                
        if not self.dor_anim._render:
            self.collider.colliding = False

class Ship:
    def __init__(self) -> None:
        self.sprite = AnimatedSprite('data\lovishki\ship.png',20)
        self.sprite.start()
        
    def set_pos(self, pos):
        self.collider = Collider(pos[0],pos[1],8,4)
        
    def render(self,win, person: Person):
        person.collider.colliding = True
        self.sprite.update()
        self.sprite.center = self.collider.center
        self.sprite.render(win)
        if self.collider._rect.collide_rect(person.collider._rect):
            
            person.killing = True
            if person.collider.colliding:
                if person.renderer:
                    lenght = max(person.collider._speed.lenght,2)
                    
                    person.kill_particle  = (
                        Particle()
                        .set_shape(Shapes.IMAGE)
                        .set_sprite(Sprite(load_image('data\person\kill_particle.png')),1.1)
                        .set_phisics_trenie(Vector2(0.7,0.7))
                        .set_color('blue')
                        .set_radius(20)
                        .set_size([30,30])
                        .set_move_duration(30)
                        
                        .set_move_angle(person.collider._speed.get_angle()+90)
                        .set_phisics_simulate(True)
                        .set_speed(lenght)
                        .set_sprite_mode(SpriteModes.VECTOR)
                        .set_size_deller(0.01)
                        .set_particle_speed_randoming(3)
                        .set_phisics_gravity(Vector2(0,0.1))
                    )
                    sound_player_kill.play()
                    person.kill_particles_spavner.pos = [person.collider.center[0]-1.5,person.collider.center[1]-1.5]
                    person.person_particles_space.add(person.kill_particle, person.kill_particles_spavner, 30,1)
                person.renderer = False
                
            person.collider.colliding = False
    
class Air_Ship:
    def __init__(self) -> None:
        self.sprite = AnimatedSprite(r'data\lovishki\air_ship.png',6)
        self.sprite.start()
        self.timer=randint(0,100)
        self.start_pos = [0,0]
        self.speed = [0,randint(-100,100)/100]
        
    def set_pos(self, pos):
        self.collider = Collider(pos[0],pos[1],4,4)
        self.sprite.center = self.collider.center
        self.start_pos = copy(self.collider.center)
        
        #self.sprite.center = [0,0]
        
    def render(self,win, person: Person):
        person.collider.colliding = True
        
       
        self.sprite.update()
        self.speed[0] +=  (self.start_pos[0] - self.sprite.center_x)/1000
        self.speed[1] += (self.start_pos[1] - self.sprite.center_y-6)/1000
        
        #self.sprite.center = self.collider.center
        #print(self.speed)
        self.collider.center_x+=self.speed[0]
        self.collider.center_y+=self.speed[1]
        self.timer+=0.1
        self.sprite.center = [self.collider.center[0], self.collider.center[1]-7]
        self.sprite.center_y+=sin(self.timer)
        self.speed[0]*=0.99
        self.speed[1]*=0.99
        
        self.sprite.render(win)
        if self.collider.collide_rect(person.collider) and not person.killing:
            
            
            if person.collider.colliding:
                
                self.speed[0]+=person.collider._speed.x/4
                self.speed[1]+=person.collider._speed.y/4
                if person.renderer:
                    lenght = min(person.collider._speed.lenght,0.5)
                    
                    person.kill_particle  = (
                        Particle()
                        .set_shape(Shapes.IMAGE)
                        .set_sprite(Sprite(load_image('data\person\kill_particle.png')),1.1)
                        .set_phisics_trenie(Vector2(0.7,0.7))
                        .set_color('blue')
                        .set_radius(20)
                        .set_size([30,30])
                        .set_move_duration(30)
                        
                        .set_move_angle(person.collider._speed.get_angle()+90)
                        .set_phisics_simulate(True)
                        .set_speed(lenght)
                        .set_sprite_mode(SpriteModes.VECTOR)
                        .set_size_deller(0.03)
                        .set_particle_speed_randoming(3)
                        .set_phisics_gravity(Vector2(0,0.1))
                    )
                    sound_player_kill.play()
                    person.kill_particles_spavner.pos = [person.collider.center[0]-1.5,person.collider.center[1]-1.5]
                    person.person_particles_space.add(person.kill_particle, person.kill_particles_spavner, 30,1)
                person.renderer = False
            
            person.killing = True
            person.collider.colliding = False
       
        #self.collider.draw(win())
        
class Portal:
    def __init__(self) -> None:
        self.sprite = AnimatedSprite('data\portals\portla.png',8)  
        
        self.sprite_in = Sprite(load_image('data\portals\portal_in.png'))
        self.sprite_out = Sprite(load_image('data\portals\portal_out.png'))
        
        self.sprite.start()
        self.timer=10
        self.partal_particle = (
            Particle()
            .set_shape(Shapes.IMAGE)
            .set_sprite(Sprite(load_image('data\portals\portal_particle.png')),1)
            .set_size([5,5])
            .set_speed(1.5)
            .set_size_deller(0.1)
            .set_move_duration(180)
            .set_speed_rotation(10)
            .set_sprite_mode(SpriteModes.ROTATE)
            .set_move_adding(0.8)
        )
        self.spavner = Spavner(spavner_size_=[1,1])
        self.space = ParticleSpace([0,0],win_size, win)
        self.radius = 0
        self.inner = False
        self.line_size = 0
    
    def set_positions(self, pos1, pos2):
        self.collider_1 = Collider(pos1[0],pos1[1],6,12)
        self.collider_2 = Collider(pos2[0],pos2[1],6,12)
        
    def render(self, win):
        self.timer+=0.1
        self.sprite.update()
        self.line_size-=0.1
        self.line_size = max(0,self.line_size)
        
        Draw.draw_line(win(), self.collider_1.center,self.collider_2.center,'#620cc2',int(self.line_size))
        
        self.space.update()
        
        
        self.spavner.pos = self.collider_1.center
        self.space.add(self.partal_particle, self.spavner, 1,10)
        
        self.space.draw()
        self.sprite.center = self.collider_1.center
        self.sprite.center[1]+=sin(self.timer)
        self.sprite.render(win)
        
        self.spavner.pos = self.collider_2.center
        self.space.add(self.partal_particle, self.spavner, 1,10)
        
        
        
        self.sprite.center = self.collider_2.center
        self.sprite.center[1]+=sin(self.timer)
        self.sprite.render(win)
        
        
        if self.inner:
            self.radius+=1
            Draw.draw_circle(win(), self.collider_1.center, self.radius,(98,12,194),int(10-self.radius/3),((67,13,125),1))
            if self.radius>30-5:
                self.radius = 0
                self.inner = False
        
        self.sprite_in.center = [self.collider_1.center[0],self.collider_1.center[1]-10+sin(self.timer)]
        self.sprite_out.center = [self.collider_2.center[0],self.collider_2.center[1]-10+sin(self.timer)]
        self.sprite_in.draw(win)
        self.sprite_out.draw(win)
        
        
    
    
    def update(self, person):
        if self.collider_1.collide_rect(person.collider) and not person.killing:
            sound_portal.play()
            person.collider.center = self.collider_2.center
            #person.collider.sy = 0
            self.line_size = 4
            self.inner = True
        self.space.deller()

class Font:
    def __init__(self, file_name_: str) -> None:
        self.sprites = AnimatedSprite(file_name_)
        self._syms = 'abcdefghijklmnopqrstuvyxwz .1234567890'
        self._converts_syms = {}
        for sym , sprite in zip(self._syms, self.sprites._sprites):
            self._converts_syms[sym] = sprite
            
            
        self._syms = 'abcdefghijklmnopqrstuvyxwz '.upper()

        for sym , sprite in zip(self._syms, self.sprites._sprites):
            self._converts_syms[sym] = sprite
            
    def render(self,win: Window,text: str, pos: Tuple[int ,int], centering: bool = False):
        x = 0
        for i in range(len(text)):
            sym = text[i]
            self._converts_syms[sym].center = [pos[0]+x,pos[1]]
            
            self._converts_syms[sym].draw(win)
            x+=self._converts_syms[sym].size[0]+1



class Level:
    level_number = 0
    levels = []
    level_close_anim = AnimatedSprite('data\level_split_anim.png',3,True)
    level_open_anim = AnimatedSprite('data\level_split_anim.png',3,True)
    level_open_anim._sprites.reverse()
    
    @classmethod
    def realoadCloseAnim(self):
        self.level_close_anim = AnimatedSprite('data\level_split_anim.png',3,True)
        
    @classmethod
    def realoadOpenAnim(self):
        self.level_open_anim = AnimatedSprite('data\level_split_anim.png',3,True)
        self.level_open_anim._sprites.reverse()
       
    @classmethod
    def new_level_animation(self):
        
        if not self.levels[self.level_number][0].Person.out() :
            self.level_close_anim.start()
            
        #print(self.level_close_anim.index)
        
        if self.level_close_anim.index == len(self.level_close_anim._sprites)-2:
            self.level_number+=1
            print('yes')
            self.realoadCloseAnim()
            self.realoadOpenAnim()
        
        self.level_close_anim.update()
        self.level_open_anim.update()
        
        
        for i in range(win_size[0]//16):
            for j in range(win_size[1]//16):
                self.level_open_anim.center = [i*16+8,j*16+8]
                self.level_open_anim.render(win)
                
        for i in range(win_size[0]//16):
            for j in range(win_size[1]//16):
                self.level_close_anim.center = [i*16+8,j*16+8]
                self.level_close_anim.render(win)
                
    @classmethod
    def restart_level_animation(self):
        if Menu.level_restart_button.pressed :
            self.level_close_anim.start()
            
        if self.level_close_anim.end_sprite():
            self.Reload(self.levels[self.level_number][0])
            self.realoadCloseAnim()
            self.realoadOpenAnim()
        
        #self.level_close_anim.update()
        #self.level_open_anim.update()
        
        
        for i in range(win_size[0]//16):
            for j in range(win_size[1]//16):
                self.level_open_anim.center = [i*16+8,j*16+8]
                self.level_open_anim.render(win)
                
        for i in range(win_size[0]//16):
            for j in range(win_size[1]//16):
                self.level_close_anim.center = [i*16+8,j*16+8]
                self.level_close_anim.render(win)
        
    @classmethod
    def Run(self,win):
        
        self.level_open_anim.start()
        
        
        self.levels[self.level_number][0].Update(win)
        
        self.new_level_animation()
        self.restart_level_animation()
        Menu.level_restart_button.render(win)
        
                    
    def __init__(self, file_name) -> None:
        
        self.file_name = file_name
        file = LoadBinaryFile(file_name)
        self.Map = file[0]
        self.Bg = file[1]
        self.CollidersSpace = ColliderSpace(gravity=Vector2(0,0.2))
        self.Person: Person = Person(self.CollidersSpace)
        self.Dor: Dor
        self.Key: Key
        
        self.Jump_busts: Tuple[Jump_bust | Air_Jump_bust, ...] = []
        self.Rects: Tuple[Collider, ...] = []
        self.Stones: Tuple[Stone, ...] = []
        self.Igles: Tuple[Ship, ...] = []
        self.Portals: Tuple[Portal, ...] = []
        
        
        self.Rectangling(self.Map)
        self.MapSurf = self.MapRender(self.Map,garss_images)
        self.BgSurf = self.MapRender(self.Bg,bg_grass_images)
        self.CreateObjects(self.Map)
        self.realoadOpenAnim()
        self.level_succses = False
        self.levels.append([self,False])
        
        
        
    def Rectangling(self, mapping):
        global rects
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
                        self.Rects.append(Collider(x,y,rect_width,8))
                        rect_start = False
                        rect_width = 0
                except:
                    ...

    def MapRender(self, mapping, garss_images):
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
                
                #? CreateJumpBusts --------------------------------
                if mapping[i][j] == 5 and mapping[i+1][j]==1:
                    jb = Jump_bust()
                    jb.set_pos([j*8,i*8])
                    self.Jump_busts.append(jb)
                if mapping[i][j]==5 and mapping[i+1][j]!=1:
                    jb = Air_Jump_bust()
                    jb.set_pos([j*8,i*8])
                    self.Jump_busts.append(jb)
                #? CreateJumpBusts --------------------------------
                
                #? CreatePerson -----------------------------------
                if mapping[i+1][j]==-1:
                    
                    
                    self.Person.set_pos([j*8+5,i*8+8+4])
                #? CreatePerson -----------------------------------
                
                #? CreateStones -----------------------------------
                if mapping[i][j] == 4:
                    jb = Stone()
                    jb.set_pos([j*8,i*8])
                    self.Rects.append(jb.colider)
                    self.Stones.append(jb)
                #? CreateStones -----------------------------------
                
                #? CreateKey --------------------------------------
                if mapping[i][j] == 3:
                    self.Key = Key()
                    self.Key.set_pos([j*8,i*8])
                #? CreateKey --------------------------------------
                
                #? CreateDor --------------------------------------
                if mapping[i][j] == 6:
                    self.Dor = Dor()
                    self.Dor.set_pos([j*8,i*8])   
                    self.Rects.append(self.Dor.collider)  
                #? CreateDor --------------------------------------
                
                #? CreateIgles ------------------------------------
                if mapping[i][j] == 7 and mapping[i+1][j]==1:
                    d = Ship()
                    d.set_pos([j*8,i*8+4])   
                    self.Igles.append(d)
                if mapping[i][j] == 7 and mapping[i+1][j]!=1:
                    d = Air_Ship()
                    d.set_pos([j*8+2,i*8+2])   
                    self.Igles.append(d)
                #? CreateIgles ------------------------------------
                
                #? CreatePortals ----------------------------------
                if isinstance( mapping[i][j], str):
                    pos1 = [j*8,i*8-6]
                    pos2 = string_to_list(mapping[i][j])
                    pos2[0]*=8
                    pos2[1]*=8
                    pos2[1]-=6
                    portal = Portal()
                    portal.set_positions(pos1, pos2)
                    self.Portals.append(portal)
                #? CreatePortals ----------------------------------




        #self.collder.draw(win._win)
         
    def Reload(self):
        del self.Person
        self.__init__(self.file_name)
          
    def Update(self, win):
        win().blit(self.BgSurf,global_pos)
        win().blit(self.MapSurf,global_pos)
        [s.render(win,self.Person) for s in self.Igles]
        
        [s.render(win,self.Person) for s in self.Stones]
        self.Person.update(self.Rects)
        
        self.Dor.render(win,self.Key, self.Person)
        

        [b.render(win,self.Person) for b in self.Jump_busts]
        [p.render(win) for p in self.Portals]
        [p.update(self.Person) for p in self.Portals]
        self.Key.render(win,self.Person, self.Dor)
        self.Person.render(win)
        self.Person.KILL(self)
        
        self.ui()
        
    def ui(self):
        Menu.level_restart_button.set_pos([win_size[0]-20,7])
        
        
        
        
class Button:
    def __init__(self, press, no_press) -> None:
        self.p = Sprite(load_image(press))   
        self.p.set_size(scale_=1.5)    
        self.np = Sprite(load_image(no_press))  
        self.np.set_size(scale_=1.5)   
        self.pos = [0,0]
        self.pressed = False
        self.rect = Rect(0,0,self.np.render_image.get_width(),self.np.render_image.get_height())
        
    def set_pos(self, pos):
        self.pos = pos
        self.rect.xy = self.pos
        
    def render(self, win, p_c = False):
        self.rect = Rect(0,0,self.np.render_image.get_width(),self.np.render_image.get_height())
        self.rect.xy = self.pos
        if not self.pressed:
            self.np.pos = self.pos
            self.np.draw(win,0)
        else:
            self.p.pos = [self.pos[0],self.pos[1]]
            self.p.draw(win,0)
        f = Mouse.press if p_c else Mouse.click
        if self.rect.collide_point(Mouse.position()) and f():
            self.pressed = True
        else:
            self.pressed = False
        
        #self.rect.draw(win())
         
        
class Menu:
    level_restart_button = Button(r'data\UI\restart_press_button.png',r'data\UI\restart_no_press_button.png')
    exit_button = Button(r'data\UI\exit_press_button.png',r'data\UI\Exit_no_press_button.png')
    levels_button = Button(r'data\UI\levels_press_button.png',r'data\UI\levels_no_press_button.png')
   
class StartMenu:
    def __init__(self) -> None:
        self.uper = 60
        self.start_anim = False
        self.pos1 = [-win_size[0],0]
        self.pos2 = [win_size[0],0]
        self.anim_speed = 5
        self.anim_end = False
        
    def draw(self):
        self.y = 0
        Menu.levels_button.set_pos([5,(self.uper+self.y)])

        
        
        self.y+=15
        Menu.exit_button.set_pos([5,(self.uper+self.y)])
        Menu.exit_button.render(win,1)
        Menu.levels_button.render(win,1)
        
    def levels_animation(self):
        self.anim_end = False
        if Menu.levels_button.pressed:
            self.start_anim = True
            
        if self.start_anim:
            
            self.pos1[0]+=self.anim_speed
            self.pos2[0]-=self.anim_speed
            for i in range(7):
                if i%2==0:
                    Draw.draw_rect(win(), [self.pos1[0],self.pos1[1]+i*20],[win_size[0],20],(40,40,55))
                    
            for i in range(8):
                if i%2!=0:
                    Draw.draw_rect(win(), [self.pos2[0],self.pos2[1]+i*20],[win_size[0],20],(40,40,55))
            
            if self.pos2[0] == 0:
                self.start_anim = False
                self.pos1 = [-win_size[0],0]
                self.pos2 = [win_size[0],0]
                self.anim_end = True
            
class LevelsMap:
    def __init__(self,Levels: Tuple) -> None:
        self.start_anim = False
        self.pos1 = [0,0]
        self.pos2 = [0,0]
        self.anim_speed = 5
        self.anim_end = False
        
        
        
        
        
        
        self.level_sprite = Sprite(load_image(r'data\UI\level_image.png'))   
        self.level_out_sprite = Sprite(load_image(r'data\UI\out_line_image.png'))   
        self.level_succsess = Sprite(load_image(r'data\UI\level_succses.png'))
        self.level_not_succsess = Sprite(load_image(r'data\UI\level_not_succses.png'))
        self.levels_count = len(Levels)
        self.levels = Levels
        
        self.rendering = False
        
        self.levels_map = []
        self.levels_map_poses = [
            100,80,120,40,80
        ]
        
        self.levels_map_form()
        
    def render(self):
 
        if self.rendering:
            lines_poses = []
            
            for index in range(len(self.levels_map)):
                level = self.levels_map[index]
                level[1]+=0.1
                
                lines_poses.append([level[0][0],level[0][1]+sin(level[1])*1.5])
                
            Draw.draw_dashed_lines(win(), lines_poses, (70,50,30),3,10)
            
            for index in range(len(self.levels_map)):
                level = self.levels_map[index]
                self.level_sprite.center=[level[0][0],level[0][1]+sin(level[1])*1.5]
                self.level_out_sprite.center = [level[0][0],level[0][1]+sin(level[1])*1.5]
                rect = Rect([level[0][0],level[0][1]+sin(level[1])*1.5], self.level_sprite.image.get_size())
                rect.center = [level[0][0],level[0][1]+sin(level[1])*1.5]
                if not rect.collide_point(Mouse.position()):
                    self.level_sprite.draw(win)
                else:
                    self.level_out_sprite.draw(win)
                if level[2]:
                    self.level_succsess.center = [level[0][0]+7,level[0][1]+7+sin(level[1])*1.5]
                    self.level_succsess.draw(win)
                else:
                    self.level_not_succsess.center = [level[0][0]+7,level[0][1]+7+sin(level[1])*1.5]
                    self.level_not_succsess.draw(win)
                    
                f.render(win, str(index+1), [level[0][0]-10,level[0][1]+sin(level[1])*1.5-10],True)
            
            
        
        
        
    def levels_map_form(self):
        x = 10
        
        for posy, level in zip(self.levels_map_poses, self.levels):
                
                level_pos = [x+40,posy]
                l = [level_pos, randint(0,100), level[1], level[0]]
                x+=40
                self.levels_map.append(l)
       
    def levels_anim(self, ending):     
        self.anim_end = False
        if ending:
            self.start_anim = True
            self.rendering = True
            
        if self.start_anim:
            
            self.pos1[0]+=self.anim_speed
            self.pos2[0]-=self.anim_speed
            for i in range(7):
                if i%2==0:
                    Draw.draw_rect(win(), [self.pos1[0],self.pos1[1]+i*20],[win_size[0],20],(40,40,55))
                    
            for i in range(8):
                if i%2!=0:
                    Draw.draw_rect(win(), [self.pos2[0],self.pos2[1]+i*20],[win_size[0],20],(40,40,55))
            
            if self.pos2[0] == 0:
                self.start_anim = False
                self.pos1 = [-win_size[0],0]
                self.pos2 = [win_size[0],0]
                self.anim_end = True
        
        
    
        
        

f = Font(r'data\fonts\pixel_font.png')


Level(r'maps\test2.bin')
Level(r'maps\test3.bin')
Level(r'maps\test4.bin')

                




STM = StartMenu()
LVM = LevelsMap(Level.levels)



while win.update(fps=60, fps_view=0, base_color=(170,190,255)):


    Level.Run(win)
    
    #if not LVM.rendering:
    #    STM.draw()
    #    STM.levels_animation()
    #LVM.render()
    #LVM.levels_anim(STM.anim_end)
    
    f.render(win, str(int(win.fps)),[4,4])
    
    
    