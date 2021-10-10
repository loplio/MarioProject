from pico2d import *
import Init_value
class Mario:
    def __init__(self):
        self.x, self.y = 400, 108
        self.frame = 0
        self.image = load_image('Mario.png')
        self.dir = 0
        self.jump = False
        self.acceleration = 0
        self.buffer_y = 0
        self.clash_key = 0
    def update(self, cur_time):
        # print('updating.....')
        if self.dir == 1:                       # 프레임
            self.frame = self.frame % 4 + 5
        elif self.dir == -1:
            self.frame = (self.frame + 1) % 4
        self.x += 5*self.dir                    # 이동
        self.y += 3*self.acceleration
        self.handle_events()                    # 이벤트
        self._jump()                            # 점프
    def draw(self):
        self.image.clip_draw(self.frame*25, 0, 25, 25, self.x, self.y)
    def _jump(self):
        if self.jump == True:
            self.acceleration = self.acceleration - 0.98 * 0.34
            if(self.buffer_y > self.y):
                self.acceleration = 0
                self.y = self.buffer_y
                self.jump = False
    def handle_events(self):
        events = get_events()
        # print(events)
        for event in events:
            # print(event.type)
            if event.type == SDL_QUIT:
                Init_value.Game_loop = False
            elif event.key == SDLK_ESCAPE:
                Init_value.Game_loop = False
            if event.type == SDL_KEYDOWN:
                if event.key == SDLK_RIGHT:
                    self.dir = 1
                    self.clash_key += 1
                elif event.key == SDLK_LEFT:
                    self.dir = -1
                    self.clash_key += 1
                elif event.key == SDLK_UP and not self.jump:
                    self.jump = True
                    self.acceleration = 5
                    self.buffer_y = self.y
            elif event.type == SDL_KEYUP:
                if event.key == SDLK_RIGHT or event.key == SDLK_LEFT:
                    self.clash_key -= 1
                    if self.clash_key == 0:
                        self.dir = 0