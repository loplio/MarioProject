from pico2d import *
import Init_value
import Game_FrameWork
class Mario:
    def __init__(self):
        self.x, self.y = Init_value.WINDOW_WIDTH//2, 108
        self.frame = 5
        self.image = load_image('Mario.png')
        self.dir = 0
        self.prev_dir = 1
        self.jump = False
        self.acceleration = 0
        self.buffer_y = 0
        self.clash_key = 0
        self.point_view = Init_value.WINDOW_WIDTH//2
    def _frame(self):
        if self.jump:
            if self.dir == 1:
                self.frame = 9
            else:
                self.frame = 4
        elif self.dir == 1:                       # 프레임
            self.frame = self.frame % 4 + 5
        elif self.dir == -1:
            self.frame = (self.frame + 1) % 4
        elif self.dir == 0:
            if self.prev_dir == 1:
                self.frame = 5
            else:
                self.frame = 0
    def move(self):
        self.x += 5 * self.dir  # 이동
        self.y += 3 * self.acceleration
    def update(self):
        self._frame()
        self.move()
        self.handle_events()                    # 이벤트
        self._jump()                            # 점프
    def draw(self):
        self.image.clip_draw(self.frame*25, 0, 25, 25, self.point_view, self.y)
    def _jump(self):
        if self.jump == True:
            self.acceleration = self.acceleration - 0.98 * 0.34
            if(self.buffer_y > self.y):
                self.acceleration = 0
                self.y = self.buffer_y
                self.jump = False
    def handle_events(self):
        events = get_events()
        for event in events:
            if event.type == SDL_QUIT:
                Game_FrameWork.running = False
            elif event.key == SDLK_ESCAPE:
                Game_FrameWork.pop_state()
            if event.type == SDL_KEYDOWN:
                if event.key == SDLK_RIGHT:
                    self.dir = 1
                    self.clash_key += 1
                    self.prev_dir = self.dir
                elif event.key == SDLK_LEFT:
                    self.dir = -1
                    self.clash_key += 1
                    self.prev_dir = self.dir
                elif event.key == SDLK_UP and not self.jump:
                    self.jump = True
                    self.acceleration = 5
                    self.buffer_y = self.y
            elif event.type == SDL_KEYUP:
                if event.key == SDLK_RIGHT or event.key == SDLK_LEFT:
                    self.clash_key -= 1
                    if self.clash_key == 0:
                        self.dir = 0