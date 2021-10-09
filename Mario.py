from pico2d import *

class Mario:
    def __init__(self):
        self.x, self.y = 400, 70
        self.frame = 0
        self.image = load_image('Basic.png')
        self.dir = 0
        self.jump = False
        self.acceleration = 0
        self.buffer_y = 0
    def update(self):
        # self.frame = (self.frame + 1) % 8
        self.x += 1.5*self.dir
        self.y += self.acceleration
        self.handle_events()
        self._jump()
    def draw(self):
        self.image.draw_now(self.x, self.y)
        # self.image.clip_draw(self.frame*40, 0, 40, 40, self.x, self.y)
    def _jump(self):
        if self.jump == True:
            print(self.acceleration)
            self.acceleration = self.acceleration - 0.98 * 0.1
            if(self.buffer_y > self.y):
                print(self.buffer_y, self.y)
                self.acceleration = 0
                self.y = self.buffer_y
                self.jump = False
    def handle_events(self):
        events = get_events()
        for event in events:
            if event.type == SDL_KEYDOWN:
                if event.key == SDLK_RIGHT:
                    self.dir = 1
                elif event.key == SDLK_LEFT:
                    self.dir = -1
                elif event.key == SDLK_UP and not self.jump:
                    self.jump = True
                    self.acceleration = 5
                    self.buffer_y = self.y
            elif event.type == SDL_KEYUP:
                if event.key == SDLK_RIGHT or event.key == SDLK_LEFT:
                    self.dir = 0