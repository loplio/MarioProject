from pico2d import *
import Init_value
import Game_FrameWork
import server
RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, JUMP_KEY, JUMP_END_1, JUMP_END_2, FLOATING, DEAD, RESTART = range(10)

PIXEL_PER_METER = (32.0 / 1.0)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYDOWN, SDLK_UP): JUMP_KEY
}

class IdleState:
    def enter(mario, event):
        print("                               #  IdleState ENter")
        if event == RIGHT_DOWN:
            mario.dir = 1
        if event == LEFT_DOWN:
            mario.dir = -1
        mario.velocity = 0
        mario.crash_key = 0

    def exit(mario, event):
        pass

    def do(mario):
        if mario.dir >= 0:
            mario.frame = 5
        else:
            mario.frame = 0

    def draw(mario):
        mario.image.clip_draw(int(mario.frame) * mario.mario_w, 0, mario.mario_w, mario.mario_h, mario.point_view, mario.y)
        draw_rectangle(mario.point_view - mario.mario_w / 2, mario.y - mario.mario_h / 2, mario.point_view + mario.mario_w / 2, mario.y + mario.mario_h / 2)

class RunState:
    def enter(mario, event):
        print("                               #  RunState ENter")
        mario.velocity = RUN_SPEED_PPS
        if event == RIGHT_DOWN:
            mario.dir = 1
            mario.crash_key += 1
            print("Right - crash_key: ", mario.crash_key)

        elif event == LEFT_DOWN:
            mario.dir = -1
            mario.crash_key += 1
            print("Left - crash_key: ", mario.crash_key)

    def exit(mario, event):
        pass

    def do(mario):
        if mario.dir >= 0:  # 프레임
            mario.frame = (mario.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * Game_FrameWork.frame_time) % 4 + 4
        else:
            mario.frame = (mario.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * Game_FrameWork.frame_time) % 4
        mario.x += mario.dir * mario.velocity * Game_FrameWork.frame_time
        if mario.floating():
            mario.add_event(FLOATING)

    def draw(mario):
        if mario.dir >= 0:
            mario.image.clip_draw(int(mario.frame + 1) * mario.mario_w, 0, mario.mario_w, mario.mario_h, mario.point_view, mario.y)
        else:
            mario.image.clip_draw(int(mario.frame) * mario.mario_w, 0, mario.mario_w, mario.mario_h, mario.point_view, mario.y)
        draw_rectangle(mario.point_view - mario.mario_w / 2, mario.y - mario.mario_h / 2, mario.point_view + mario.mario_w / 2, mario.y + mario.mario_h / 2)

class JumpState:
    def enter(mario, event):
        print("                               #  JumpState ENter")
        print(mario.acceleration)
        if mario.acceleration <= 0 and not mario.state_floating:
            mario.acceleration = 5

    def exit(mario, event):
        mario.state_floating = False
        pass

    def do(mario):
        if mario.dir >= 0:
            mario.frame = 9
        else:
            mario.frame = 4
        mario.x += mario.dir * mario.velocity * Game_FrameWork.frame_time
        # print(mario.dir, mario.velocity)
        mario.y += 3 * mario.acceleration
        mario.acceleration = mario.acceleration - 0.98 * 0.34

    def draw(mario):
        mario.image.clip_draw(int(mario.frame) * mario.mario_w, 0, mario.mario_w, mario.mario_h, mario.point_view, mario.y)
        draw_rectangle(mario.point_view - mario.mario_w / 2, mario.y - mario.mario_h / 2, mario.point_view + mario.mario_w / 2, mario.y + mario.mario_h / 2)

class DeadState:
    def enter(mario, event):
        print("                               #  DeadState ENter")
        mario.acceleration = 5
        mario.crash_key = 0
        mario.frame = 10
        mario.state_dead = True

    def exit(mario, event):
        print("DeadState Exit")
        mario.state_dead = False

    def do(mario):
        mario.y += 3 * mario.acceleration
        mario.acceleration = mario.acceleration - 0.98 * 0.34
        if mario.y < 0:
            mario.x, mario.y = Init_value.WINDOW_WIDTH//2, 110
            mario.add_event(RESTART)

    def draw(mario):
        mario.image.clip_draw(int(mario.frame) * mario.mario_w, 0, mario.mario_w, mario.mario_h, mario.point_view, mario.y)
        draw_rectangle(mario.point_view - mario.mario_w / 2, mario.y - mario.mario_h / 2, mario.point_view + mario.mario_w / 2, mario.y + mario.mario_h / 2)


class Mario:
    def __init__(self):
        self.x, self.y = Init_value.WINDOW_WIDTH//2, 110
        self.frame = 5
        self.image = load_image('Mario.png')
        self.dir = 1
        self.prev_dir = 1
        self.velocity = 0
        self.acceleration = 0
        self.mario_w = 25
        self.mario_h = 25
        self.crash_key = 0
        self.state_dead = False
        self.state_floating = False
        self.point_view = Init_value.WINDOW_WIDTH//2
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def get_bb(self):
        return self.x - 13, self.y - 13, self.x + 13, self.y + 13

    def update(self):
        self.cur_state.do(self)
        # print(self.cur_state)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            # print(self.event_que, "update", event)
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)

    def landing(self):
        print("                               #  endOfJump")
        self.acceleration = 0
        print("landing acceleration=", self.acceleration)
        print(self.velocity)
        if self.velocity > 0:
            self.add_event(JUMP_END_2)
        else:
            self.add_event(JUMP_END_1)

    def floating(self):
        left, right, bottom = int((self.x - self.mario_w/2) // server.map.tile_w), int((self.x + self.mario_w/2) // server.map.tile_w), int((self.y - self.mario_h/2) // server.map.tile_h)
        # print("AAAA====================AAAA", ((server.TILE_W_N - bottom - 1) * server.map.tiles_Row) + left, bottom,
        #       left, ((server.TILE_W_N - bottom - 1) * server.map.tiles_Row) + right, bottom, right)
        # print(server.map.map[((server.TILE_W_N - bottom)*server.map.tiles_Row) + left],server.map.map[((server.TILE_W_N - bottom)*server.map.tiles_Row) + right])
        if server.map.map[((server.TILE_W_N - bottom)*server.map.tiles_Row) + left] == 0\
                and server.map.map[((server.TILE_W_N - bottom)*server.map.tiles_Row) + right] == 0:
            self.state_floating = True
            return True
        return False

    def handle_events(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            if key_event in next_state_table[self.cur_state]:
                if self.crash_key != 2 or (key_event != RIGHT_UP and key_event != LEFT_UP):
                    self.add_event(key_event)
                else:
                    self.crash_key -= 1
                    if (self.dir == 1 and key_event == RIGHT_UP) or (self.dir == -1 and key_event == LEFT_UP):
                        self.dir *= -1
                    print("reason crash crash_key -1 down  , crash_key: ", self.crash_key)
            else:
                if self.cur_state == JumpState and key_event == 0:
                    self.dir = 1
                    self.crash_key += 1
                    self.velocity = RUN_SPEED_PPS
                    # print('first')
                elif self.cur_state == JumpState and key_event == 1:
                    self.dir = -1
                    self.crash_key += 1
                    self.velocity = RUN_SPEED_PPS
                    # print('second')
                elif self.cur_state == JumpState and key_event == 2:
                    self.crash_key -= 1
                    if self.crash_key == 0:
                        self.velocity = 0
                    elif (self.dir == 1 and key_event == RIGHT_UP) or (self.dir == -1 and key_event == LEFT_UP):
                        self.dir *= -1
                    # print('thrid')
                elif self.cur_state == JumpState and key_event == 3:
                    # print('four')
                    self.crash_key -= 1
                    if self.crash_key == 0:
                        self.velocity = 0
                    elif (self.dir == 1 and key_event == RIGHT_UP) or (self.dir == -1 and key_event == LEFT_UP):
                        self.dir *= -1


next_state_table = {
    IdleState: {RIGHT_UP: RunState, LEFT_UP: RunState,
                RIGHT_DOWN: RunState, LEFT_DOWN: RunState,
                JUMP_KEY: JumpState, FLOATING: JumpState,
                JUMP_END_1: IdleState, DEAD: DeadState},
    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState,
               LEFT_DOWN: RunState, RIGHT_DOWN: RunState,
               JUMP_KEY: JumpState, FLOATING: JumpState,
               JUMP_END_2: RunState, DEAD: DeadState},
    JumpState: {JUMP_END_1: IdleState, JUMP_END_2: RunState,
                FLOATING: JumpState, DEAD: DeadState},
    DeadState: {DEAD: DeadState, RESTART: IdleState}
}