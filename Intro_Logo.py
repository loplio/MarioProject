from pico2d import *
import Game_FrameWork
import Game_Lobby
import Init_value
name = "StartState"
image = None
Logo_time = 0

def enter():
    global image
    image = load_image('kpu_credit.png')

def draw():
    image.clip_draw(40, 60, Init_value.WINDOW_WIDTH, Init_value.WINDOW_HEIGHT, Init_value.WINDOW_WIDTH/2, Init_value.WINDOW_HEIGHT/2)
    update_canvas()

def update():
    global Logo_time
    if Logo_time > 1:
        draw()
        # Logo_time = 0
        Game_FrameWork.change_state(Game_Lobby)
    delay(0.04)
    Logo_time += 0.04

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            Game_FrameWork.running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                Game_FrameWork.running = False

def exit():
    global image
    del(image)

def main():
    handle_events()
    draw()
    update()