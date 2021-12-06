from pico2d import *
import Game_FrameWork
import Game_World
import server
import Init_value

PIXEL_PER_METER = (32.0 / 1.0)
FIRE_SPEED_KMPH = 40.0
FIRE_SPEED_MPM = (FIRE_SPEED_KMPH * 1000.0 / 60.0)
FIRE_SPEED_MPS = (FIRE_SPEED_MPM / 60.0)
FIRE_SPEED_PPS = (FIRE_SPEED_MPS * PIXEL_PER_METER)

class FireBall:
    image = None
    fireball_w = 15
    fireball_h = 15
    def __init__(self):
        if FireBall.image is None:
            FireBall.image = load_image('fire.png')
        self.point_view = server.mario.point_view
        self.dx = 0
        self.dy = 0
        self.x = server.mario.x
        self.y = server.mario.y
        self.dir = server.mario.dir
        self.velocity = FIRE_SPEED_PPS

    def draw(self):
        print("x", self.x)
        FireBall.image.clip_draw(0, 0, FireBall.fireball_w, FireBall.fireball_h, self.point_view, self.y)

    def update(self):
        self.x += self.dir * self.velocity * Game_FrameWork.frame_time
        self.point_view += (self.dir * self.velocity - server.mario.dir * server.mario.velocity) * Game_FrameWork.frame_time
        if self.point_view < 0 or self.point_view > Init_value.WINDOW_WIDTH:
            Game_World.remove_object(self)