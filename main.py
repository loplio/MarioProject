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
    clear_canvas()
    # cur_time = get_time() - cur_time
    # print(cur_time)
    Window_Pos()            # 업데이트
    mario.update(cur_time)
    map.draw()              # 그리기
    mario.draw()
    update_canvas()

    delay(0.015)
close_canvas()