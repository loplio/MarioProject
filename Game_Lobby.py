import Game_FrameWork
import Game_Play
from pico2d import *


name = "TitleState"
image = None


def enter():
    pass

def exit():
    pass

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
    pass

def update():
    pass

def pause():
    pass

def resume():
    pass

def main():
    handle_events()
    draw()
    update()