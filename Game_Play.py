import Game_FrameWork
import MarioProject.Mario
from Mario import *
from Map import *

name = "GameState"
mario = None
map = None
running = True

def enter():
    global mario, map
    map = Map()
    mario = Mario()

def exit():
    global mario, map
    del mario
    del map

def update():    # 업데이트
    Window_Pos()
    Collision()
    mario.update()

def draw():       # 그리기
    clear_canvas()
    map.draw()
    mario.draw()
    update_canvas()

def Collision():
    map_buffer = map.map_return()
    # print(map_buffer)

def Window_Pos():
    if mario.x < Init_value.WINDOW_WIDTH/2:         # 맨 좌측에선 카메라를 움직이지 않느다.
        map.window_move_len = 0
        mario.point_view = mario.x
    else:
        map.window_move_len = Init_value.WINDOW_WIDTH/2 - mario.x
        mario.point_view = Init_value.WINDOW_WIDTH/2

def frame_check(cur_time):
    frame = cur_time + 1 / Init_value.Game_FPS - get_time()
    if frame < 0:
        frame = 0
    delay(frame)

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            Game_FrameWork.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            Game_FrameWork.quit()
        else:
            mario.handle_events(event)

def main():
    cur_time = get_time()
    handle_events()
    draw()
    update()
    frame_check(cur_time)