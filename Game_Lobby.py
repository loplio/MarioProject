import Game_FrameWork
import Game_Play
import Init_value
from pico2d import *


name = "TitleState"
image1 = None
image2 = None
frame = 0


def enter():
    global image1, image2
    image1 = load_image('lobby.png')
    image2 = load_image('press.png')

def exit():
    global image1, image2
    del(image1)
    del(image2)

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            Game_FrameWork.running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                Game_FrameWork.running = False
            elif event.key == SDLK_KP_ENTER:
                print('a')
                Game_FrameWork.push_state(Game_Play)


def draw():
    global image1, image2, frame
    image1.clip_draw(0, 0, Init_value.WINDOW_WIDTH, Init_value.WINDOW_HEIGHT, Init_value.WINDOW_WIDTH/2, Init_value.WINDOW_HEIGHT/2)
    if frame == 0:
        image2.clip_draw(0, 0, 500, 30, Init_value.WINDOW_WIDTH/2, 120)
    update_canvas()

def update():
    global frame
    frame = (frame + 1) % 2
    delay(0.5)

def pause():
    pass

def resume():
    pass

def main():
    handle_events()
    draw()
    update()