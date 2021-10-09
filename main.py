from pico2d import *
from Mario import *
Game_loop = True

def handle_events():
    global Game_loop
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            Game_loop = False
        elif event.type == SDL_QUIT and event.key == SDLK_ESCAPE:
            Game_loop = False

open_canvas()
mario = Mario()
while Game_loop:
    start_time = get_time()
    clear_canvas()
    mario.draw()
    mario.update()
close_canvas()