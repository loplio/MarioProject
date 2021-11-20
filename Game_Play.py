import Game_FrameWork
import MarioProject.Mario
import Game_World
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
    Game_World.add_object(map, 0)
    Game_World.add_object(mario, 1)

def exit():
    Game_World.clear()
    # global mario, map
    # del mario
    # del map

def update():    # 업데이트
    Window_Pos()
    Collide(mario, map)
    for Game_object in Game_World.all_objects():
        Game_object.update()
    # mario.update()

def draw():       # 그리기
    clear_canvas()
    for Game_object in Game_World.all_objects():
        Game_object.draw()
    update_canvas()
    # clear_canvas()
    # map.draw()
    # mario.draw()
    # update_canvas()

def Collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    map_buffer = map.map_return()
    # print(map_buffer)
    return True

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