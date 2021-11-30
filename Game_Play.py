import Game_FrameWork
import MarioProject.Mario
import Game_World
import math
import server
from Mario import *
from Map import *

name = "GameState"
running = True
pIndex = None
Index = None

def enter():
    server.map = Map()
    server.mario = Mario()
    Game_World.add_object(server.map, 0)
    Game_World.add_object(server.mario, 1)

def exit():
    Game_World.clear()
    # global mario, map
    # del mario
    # del map

def update():    # 업데이트
    Window_Pos()
    global pIndex, Index
    for Game_object in Game_World.all_objects():
        Game_object.update()
    server.map.append_collide_map()
    while server.map.collide_map:
        Collide(server.mario, server.map)
    pIndex = Index
    # print(pIndex , "=========================================================")
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
    left_b, bottom_b, right_b, top_b, cIndex = b.get_bb()
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    nIndex = int(server.mario.y // server.map.tile_h), int(server.mario.x // server.map.tile_w)
    CheckCollideBlock = server.map.map[((server.TILE_W_N - cIndex[0] - 1)*server.map.tiles_Row) + cIndex[1]]
    # print('nIndex=', nIndex[0], nIndex[1], server.mario.y, server.mario.y+server.mario.mario_h/2,server.mario.y-server.mario.mario_h/2)
    # print('cIndex=', cIndex[0], cIndex[1], (bottom_b+top_b)/2)
    global pIndex, Index
    if pIndex == None:
        pIndex = nIndex
    # print('pIndex=', pIndex[0])
    # print(nIndex[0], ">", cIndex[0], "or", cIndex[0], ">=", nIndex[0], "and", pIndex[0], ">", nIndex[0])
    if CheckCollideBlock != 0:
        if nIndex[1] < cIndex[1]:
            server.mario.x = cIndex[1] * server.map.tile_w - server.mario.mario_w / 2 - 1
        elif nIndex[1] > cIndex[1]:
            server.mario.x = (cIndex[1] + 1) * server.map.tile_w + server.mario.mario_w / 2 + 1
        if nIndex[0] < cIndex[0]:
            # print("prev=", server.mario.y)
            server.mario.y = cIndex[0] * server.map.tile_h - server.mario.mario_h / 2 - 1
            server.mario.acceleration = 0
            # print("now=", server.mario.y)
            # print("-------------yCollide")
        elif nIndex[0] > cIndex[0] or (cIndex[0] >= nIndex[0] and pIndex[0] > nIndex[0]):
            print("prev=", cIndex)
            if not(nIndex[0] > cIndex[0]):
                cIndex = cIndex[0] + abs(pIndex[0] - cIndex[0]) - 1, cIndex[1]
            print("now=", cIndex)
            server.mario.y = (cIndex[0] + 1) * server.map.tile_h + server.mario.mario_h / 2 + 1
            server.mario.landing()
            print("착지----------------------------------------------(")
    # print('now x=', server.mario.x, 'y=', server.mario.y)
    Index = nIndex
    return True

def Window_Pos():
    if server.mario.x < Init_value.WINDOW_WIDTH/2:         # 맨 좌측에선 카메라를 움직이지 않느다.
        server.map.window_move_len = 0
        server.mario.point_view = server.mario.x
    else:
        server.map.window_move_len = Init_value.WINDOW_WIDTH/2 - server.mario.x
        server.mario.point_view = Init_value.WINDOW_WIDTH/2

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
            server.mario.handle_events(event)

def main():
    cur_time = get_time()
    handle_events()
    draw()
    update()
    frame_check(cur_time)