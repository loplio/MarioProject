from pico2d import *
import Init_value
import Game_FrameWork

RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, JUMP_KEY, JUMP_END_1, JUMP_END_2 = range(7)

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
        print("IdleState ENter")
        if event == RIGHT_DOWN:
            mario.dir = 1
        if event == LEFT_DOWN:
            mario.dir = -1
        mario.velocity = 0

    def exit(mario, event):
        pass

    def do(mario):
        if mario.dir >= 0:
            mario.frame = 5
        else:
            mario.frame = 0

    def draw(mario):
        mario.image.clip_draw(int(mario.frame) * 25, 0, 25, 25, mario.point_view, mario.y)
        draw_rectangle(mario.point_view - 25 / 2, mario.y - 25 / 2, mario.point_view + 25 / 2, mario.y + 25 / 2)

class RunState:
    def enter(mario, event):
        print("RunState ENter")
        mario.velocity = RUN_SPEED_PPS
        if event == RIGHT_DOWN:
            mario.dir = 1
        if event == LEFT_DOWN:
            mario.dir = -1
        # if event == RIGHT_DOWN:
        #     mario.clash_key += 1
        #     mario.prev_dir = mario.dir
        #     mario.velocity += 5
        # elif event == LEFT_DOWN:
        #     mario.clash_key += 1
        #     mario.prev_dir = mario.dir
        #     mario.velocity -= 5
        # elif event == RIGHT_UP or event == LEFT_UP:
        #     mario.clash_key -= 1
        #     if mario.clash_key == 0:
        #         mario.dir = 0
        #     elif mario.clash_key == 1:
        #         if (mario.dir > 0 and event.key == SDLK_RIGHT) or (mario.dir < 0 and event.key == SDLK_LEFT):
        #             mario.dir *= -1
        #             mario.prev_dir *= -1
        #     if event == RIGHT_UP:
        #         mario.velocity -= 5
        #     else:
        #         mario.velocity += 5


    def exit(mario, event):
        pass

    def do(mario):
        if mario.dir >= 0:  # 프레임
            mario.frame = (mario.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * Game_FrameWork.frame_time) % 4 + 4
        else:
            mario.frame = (mario.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * Game_FrameWork.frame_time) % 4
        mario.x += mario.dir * mario.velocity * Game_FrameWork.frame_time
        print(mario.dir)
    def draw(mario):
        if mario.dir >= 0:
            mario.image.clip_draw(int(mario.frame + 1) * 25, 0, 25, 25, mario.point_view, mario.y)
        else:
            mario.image.clip_draw(int(mario.frame) * 25, 0, 25, 25, mario.point_view, mario.y)
        draw_rectangle(mario.point_view - 25 / 2, mario.y - 25 / 2, mario.point_view + 25 / 2, mario.y + 25 / 2)

class JumpState:
    def enter(mario, event):
        print("JumpState ENter")
        if mario.acceleration == 0:
            mario.acceleration = 5
            mario.buffer_y = mario.y

    def exit(mario, event):
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
        if(mario.buffer_y > mario.y):
            mario.acceleration = 0
            mario.y = mario.buffer_y
            if mario.velocity > 0:
                mario.add_event(JUMP_END_2)
            else:
                mario.add_event(JUMP_END_1)

    def draw(mario):
        mario.image.clip_draw(int(mario.frame) * 25, 0, 25, 25, mario.point_view, mario.y)
        draw_rectangle(mario.point_view - 25 / 2, mario.y - 25 / 2, mario.point_view + 25 / 2, mario.y + 25 / 2)

class Mario:
    state_crash = None

    def __init__(self):
        self.x, self.y = Init_value.WINDOW_WIDTH//2, 108
        self.frame = 5
        self.image = load_image('Mario.png')
        self.dir = 1
        self.velocity = 0
        self.prev_dir = 1
        self.acceleration = 0
        self.buffer_y = 0
        self.clash_key = 0
        self.point_view = Init_value.WINDOW_WIDTH//2
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)

        if Mario.state_crash == None:
            Mario.state_crash = False

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            print(self.event_que, "update", event)
            self.cur_state.exit(self, event)
            print("1")
            self.cur_state = next_state_table[self.cur_state][event]
            print("2")
            self.cur_state.enter(self, event)
            print("3")

    def draw(self):
        self.cur_state.draw(self)

    def handle_events(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            if key_event in next_state_table[self.cur_state]:
                self.add_event(key_event)
            else:
                if self.cur_state == JumpState and key_event == 0:
                    self.dir = 1
                    self.velocity = RUN_SPEED_PPS
                    print('first')
                elif self.cur_state == JumpState and key_event == 1:
                    self.dir = -1
                    self.velocity = RUN_SPEED_PPS
                    print('second')
                elif self.cur_state == JumpState and key_event == 2:
                    self.velocity = 0
                    print('thrid')
                elif self.cur_state == JumpState and key_event == 3:
                    print('four')
                    self.velocity = 0

            # if 'JUMP_END_1' in key_event_table['JumpState'] == True\
            #         and 'JUMP_END_2' in key_event_table['JumpState'] == True:
            #     print("AAA")
            #     key_event = key_event_table[(event.type, event.key)]
            #     self.add_event(key_event)

next_state_table = {
    IdleState: {RIGHT_UP: RunState, LEFT_UP: RunState,
                RIGHT_DOWN: RunState, LEFT_DOWN: RunState,
                JUMP_KEY: JumpState},
    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState,
               LEFT_DOWN: RunState, RIGHT_DOWN: RunState,
               JUMP_KEY: JumpState},
    JumpState: {JUMP_END_1: IdleState, JUMP_END_2: RunState}
}