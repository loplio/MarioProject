import Game_FrameWork
import MarioProject.Mario
import Game_World
import math
import server
from Mario import *
from Map import *
from Goomba import *

name = "GameState"
running = True
pIndex = None
Index = None
test_font = None
def enter():
    server.map = Map()
    server.mario = Mario()
    server.goomba = [Goomba(x, y) for x, y in Goomba.goombas_pos]
    font = os.getenv('PICO2D_DATA_PATH') + '/ConsolaMalgun.TTF'
    global test_font
    if test_font is None:
        test_font = load_font(font, 10)
    Game_World.add_object(server.map, 0)
    Game_World.add_object(server.mario, 1)
    for g in server.goomba:
        Game_World.add_object(g, 1)

def exit():
    Game_World.clear()

def update():    # 업데이트
    Window_Pos()
    # print(len(server.goomba))
    for g in server.goomba:
        window_left = server.mario.x - Init_value.WINDOW_WIDTH / 2
        if window_left < g.x < window_left + Init_value.WINDOW_WIDTH:
            if collide(server.mario, g):
                if g.x - Goomba.goomba_w < server.mario.x < g.x + Goomba.goomba_w and server.mario.y >= g.y + Goomba.goomba_h/2\
                        and not server.mario.state_hit:
                    # Game_World.remove_object(g)
                    # server.goomba.remove(g)
                    g.dead()
                    server.mario.acceleration = 3
                elif not server.mario.state_hit:
                    server.mario.hit()
    predictCollide()
    for Game_object in Game_World.all_objects():
        Game_object.update()

def draw():       # 그리기
    clear_canvas()
    for Game_object in Game_World.all_objects():
        Game_object.draw()
    update_canvas()

def predictCollide():
    nIndex = int(server.mario.x // server.map.tile_w), int(server.mario.y // server.map.tile_h)
    dx, dy = server.mario.dir * server.mario.velocity * Game_FrameWork.frame_time, 3 * server.mario.acceleration
    mx, my = server.mario.x, server.mario.y
    LB, RB, LT, RT = server.map.get_collide_map(server.mario, server.mario.mario_w, server.mario.mario_h)
    if nIndex[1] + 1 < server.TILE_W_N and nIndex[1] >= 0 and not server.mario.state_dead:
        if dx > 0:
            for nIndex_y in range(RB[1], RT[1]):
                cIndex = nIndex[0] + 1, nIndex_y
                if cIndex[1] < 0:
                    server.mario.add_event(DEAD)
                    break
                CheckCollideBlock = server.map.map[((server.TILE_W_N - nIndex_y - 1) * server.map.tiles_Row) + cIndex[0]]
                if type(CheckCollideBlock) is list:
                    CheckCollideBlock = CheckCollideBlock[0]
                if 0 < CheckCollideBlock < 20 and cIndex[0] * server.map.tile_w < (mx + dx + server.mario.mario_w / 2):
                        server.mario.x = int(cIndex[0]*server.map.tile_w - server.mario.mario_w/2 - dx)
                elif CheckCollideBlock == 50:
                    server.map.map[((server.TILE_W_N - nIndex_y - 1) * server.map.tiles_Row) + cIndex[0]] = 0
                    server.mario.superMario()
                elif CheckCollideBlock == 51:
                    server.map.map[((server.TILE_W_N - nIndex_y - 1) * server.map.tiles_Row) + cIndex[0]] = 0
                    server.mario.fireMario()

        elif dx < 0:
            for nIndex_y in range(LB[1], LT[1]):
                cIndex = nIndex[0] - 1, nIndex_y
                if cIndex[1] < 0:
                    server.mario.add_event(DEAD)
                    break
                CheckCollideBlock = server.map.map[((server.TILE_W_N - nIndex_y - 1) * server.map.tiles_Row) + cIndex[0]]
                if type(CheckCollideBlock) is list:
                    CheckCollideBlock = CheckCollideBlock[0]
                if 0 < CheckCollideBlock < 20 and (cIndex[0]+1) * server.map.tile_w > (mx + dx - server.mario.mario_w / 2):
                        server.mario.x = (cIndex[0]+1)*server.map.tile_w + server.mario.mario_w/2 - dx
                elif CheckCollideBlock == 50:
                    server.map.map[((server.TILE_W_N - nIndex_y - 1) * server.map.tiles_Row) + cIndex[0]] = 0
                    server.mario.superMario()
                elif CheckCollideBlock == 51:
                    server.map.map[((server.TILE_W_N - nIndex_y - 1) * server.map.tiles_Row) + cIndex[0]] = 0
                    server.mario.fireMario()

        if dy > 0:
            for nIndex_x in range(LT[0], RT[0]):
                cIndex = nIndex_x, nIndex[1] + 1
                CheckCollideBlock = server.map.map[((server.TILE_W_N - cIndex[1] - 1) * server.map.tiles_Row) + nIndex_x]
                if type(CheckCollideBlock) is list:
                    CheckCollideBlock = CheckCollideBlock[0]
                if 0 < CheckCollideBlock < 20 and cIndex[1] * server.map.tile_h < (my + dy + server.mario.mario_h / 2):
                    server.mario.y = cIndex[1] * server.map.tile_h - server.mario.mario_h / 2 - 1
                    server.mario.acceleration = 0
                    if CheckCollideBlock == 1:
                        server.map.BrickBlock.append(cIndex)
                        server.map.frame = 0
                    if CheckCollideBlock == 10:
                        server.map.QuestionBlock.append(cIndex)
                        server.map.frame = 0
                elif CheckCollideBlock == 50:
                    server.map.map[((server.TILE_W_N - cIndex[1] - 1) * server.map.tiles_Row) + nIndex_x] = 0
                    server.mario.superMario()
                elif CheckCollideBlock == 51:
                    server.map.map[((server.TILE_W_N - cIndex[1] - 1) * server.map.tiles_Row) + nIndex_x] = 0
                    server.mario.fireMario()

        elif dy < 0:
            for nIndex_x in range(LB[0], RB[0]):
                cIndex = nIndex_x, nIndex[1] - 1
                if cIndex[1] < 0:
                    server.mario.add_event(DEAD)
                    break
                CheckCollideBlock = server.map.map[((server.TILE_W_N - cIndex[1] - 1) * server.map.tiles_Row) + nIndex_x]
                if type(CheckCollideBlock) is list:
                    CheckCollideBlock = CheckCollideBlock[0]
                if 0 < CheckCollideBlock < 20 and (cIndex[1]+1) * server.map.tile_h > (my + dy - server.mario.mario_h / 2):
                    server.mario.y = (cIndex[1]+1) * server.map.tile_h + server.mario.mario_h / 2 + 1
                    server.mario.landing()
                elif CheckCollideBlock == 50:
                    server.map.map[((server.TILE_W_N - cIndex[1] - 1) * server.map.tiles_Row) + nIndex_x] = 0
                    server.mario.superMario()
                elif CheckCollideBlock == 51:
                    server.map.map[((server.TILE_W_N - cIndex[1] - 1) * server.map.tiles_Row) + nIndex_x] = 0
                    server.mario.fireMario()

def collide(a, b):
    # fill here
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

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