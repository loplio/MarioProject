from Mario import *
from Map import *

open_canvas(Init_value.WINDOW_WIDTH, Init_value.WINDOW_HEIGHT)
mario = Mario()
map = Map()
def Window_Pos():
    if mario.x < Init_value.WINDOW_WIDTH/2:         # 맨 좌측에선 카메라를 움직이지 않느다.
        map.window_move_len = 0
        mario.point_view = mario.x
    else:
        map.window_move_len = Init_value.WINDOW_WIDTH/2 - mario.x
        mario.point_view = Init_value.WINDOW_WIDTH/2
while Init_value.Game_loop:
    cur_time = get_time()
    clear_canvas()
    Window_Pos()            # 업데이트
    mario.update()

    map.draw()              # 그리기
    mario.draw()
    update_canvas()

    frame = cur_time + 1/Init_value.Game_FPS - get_time()
    if frame < 0:
        frame = 0
    delay(frame)
close_canvas()