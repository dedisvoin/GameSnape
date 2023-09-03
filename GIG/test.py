#имопрт модулей
import pygame as pg
import pymunk.pygame_util
pymunk.pygame_util.positive_y_is_up = False

#Настройки PyGame
RES = WIDTH, HEIGHT = 900, 720
FPS = 60

pg.init()
surface = pg.display.set_mode(RES)
clock = pg.time.Clock()
draw_options = pymunk.pygame_util.DrawOptions(surface)


space = pymunk.Space()
space.iterations = 5
space.gravity = 0, 8000



def create_square(space, pos):
    m = 1; size = (20,20)
    square_Moment = pymunk.moment_for_box(m, size)
    body = pymunk.Body(m, square_Moment)
    body.position = pos
    shape = pymunk.Poly.create_box(body, size)
    shape.elasticity = 0
    shape.friction = 2
    space.add(body, shape)


segment_shape = pymunk.Segment(space.static_body, (1,HEIGHT), (WIDTH,HEIGHT),26)
space.add(segment_shape)
segment_shape.elasticity = 0.4
segment_shape.friction = 1

#Отрисовка PyGame
while True:
    surface.fill(pg.Color('black'))

    for i in pg.event.get():
        if i.type == pg.QUIT:
            exit()
        if i.type == pg.MOUSEMOTION:
                create_square(space, i.pos)
            
    space.step(1/FPS)
    space.debug_draw(draw_options)
            
    pg.display.flip()
    clock.tick(FPS)