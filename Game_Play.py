import Game_FrameWork
from Mario import *
from Map import *

name = "GameState"
mario = None
map = None
running = True

def enter():
    global mario, map
    mario = Mario()
    map = Map()

def exit():
    global mario, map
    del(mario)
    del(map)

def update():    # 업데이트
    clear_canvas()
    Window_Pos()
    mario.update()

def draw():       # 그리기
    map.draw()
    mario.draw()
    update_canvas()

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

def main():
    cur_time = get_time()
    draw()
    update()
    frame_check(cur_time)