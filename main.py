from Mario import *
from Map import *

open_canvas(Init_value.WINDOW_WIDTH, Init_value.WINDOW_HEIGHT)
mario = Mario()
map = Map()
def Window_Pos():
    map.window_move_len = mario.x - Init_value.WINDOW_WIDTH/2
while Init_value.Game_loop:
    clear_canvas()
    cur_time = get_time() - cur_time
    # print(cur_time)
    Window_Pos()            # 업데이트
    mario.update(cur_time)

    map.draw()              # 그리기
    mario.draw()
    update_canvas()

    delay(0.02)
close_canvas()