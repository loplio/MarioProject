from pico2d import *
import Game_FrameWork
import Game_World
import Game_Play
import server
import Init_value

PIXEL_PER_METER = (32.0 / 1.0)
FIRE_SPEED_KMPH = 50.0
FIRE_SPEED_MPM = (FIRE_SPEED_KMPH * 1000.0 / 60.0)
FIRE_SPEED_MPS = (FIRE_SPEED_MPM / 60.0)
FIRE_SPEED_PPS = (FIRE_SPEED_MPS * PIXEL_PER_METER)
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4
EFFECT_ACTION_PER_TIME = 3
EFFECT_FRAMES_PER_ACTION = 3
class FireBall:
    image = None
    effect = None
    fireball_w = 15
    fireball_h = 15
    effect_wh = 20
    def __init__(self):
        if FireBall.image is None:
            FireBall.image = load_image('fire.png')
        if FireBall.effect is None:
            FireBall.effect = load_image('fireEffect.png')
        self.point_view = server.mario.point_view
        self.dx = 0
        self.dy = 0
        self.frame = 0
        self.x = server.mario.x
        self.y = server.mario.y
        self.state_explosion = False
        self.count = 3.5
        self.acceleration = 1.5
        self.dir = server.mario.dir
        self.velocity = FIRE_SPEED_PPS

    def draw(self):
        if not self.state_explosion:
            FireBall.image.clip_draw(int(self.frame)*FireBall.fireball_w, 0, FireBall.fireball_w, FireBall.fireball_h, self.point_view, self.y)
        else:
            FireBall.effect.clip_draw(int(self.frame)*FireBall.effect_wh, 0, FireBall.effect_wh, FireBall.effect_wh, self.point_view, self.y)

    def update(self):
        if not self.state_explosion:
            self.collide()
            self.predictCollide()
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * Game_FrameWork.frame_time) % 4
            self.x += self.dir * self.velocity * Game_FrameWork.frame_time
            self.y += 3 * self.acceleration
            self.acceleration = self.acceleration - 0.98 * 0.34
            self.point_view += (self.dir * self.velocity - server.mario.dir * server.mario.velocity) * Game_FrameWork.frame_time
            if self.point_view < 0 or self.point_view > Init_value.WINDOW_WIDTH:
                Game_World.remove_object(self)
        else:
            self.frame = (self.frame + EFFECT_ACTION_PER_TIME * EFFECT_ACTION_PER_TIME * Game_FrameWork.frame_time) % 4
            if self.frame > 3:
                Game_World.remove_object(self)

    def explosion(self):
        self.state_explosion = True
        self.frame = 0

    def collide(self):
        for g in server.goomba:
            window_left = server.mario.x - Init_value.WINDOW_WIDTH / 2
            if window_left < g.x < window_left + Init_value.WINDOW_WIDTH:
                if Game_Play.collide(self, g):
                    g.dead(2)
                    self.explosion()

    def predictCollide(self):
        nIndex = int(self.x // server.map.tile_w), int(self.y // server.map.tile_h)
        dx, dy = self.dir * self.velocity * Game_FrameWork.frame_time, 3 * self.acceleration
        mx, my = self.x, self.y
        LB, RB, LT, RT = server.map.get_collide_map(self, FireBall.fireball_w, FireBall.fireball_h)
        if nIndex[1] + 1 < server.TILE_W_N and nIndex[1] >= 0:
            if dx > 0:
                for nIndex_y in range(RB[1], RT[1]):
                    cIndex = nIndex[0] + 1, nIndex_y
                    CheckCollideBlock = server.map.map[
                        ((server.TILE_W_N - nIndex_y - 1) * server.map.tiles_Row) + cIndex[0]]
                    if type(CheckCollideBlock) is list:
                        CheckCollideBlock = CheckCollideBlock[0]
                    if 0 < CheckCollideBlock < 20:
                        self.x = cIndex[0] * server.map.tile_w - FireBall.fireball_w
                        self.dir *= -1

            elif dx < 0:
                for nIndex_y in range(LB[1], LT[1]):
                    cIndex = nIndex[0] - 1, nIndex_y
                    CheckCollideBlock = server.map.map[
                        ((server.TILE_W_N - nIndex_y - 1) * server.map.tiles_Row) + cIndex[0]]
                    if type(CheckCollideBlock) is list:
                        CheckCollideBlock = CheckCollideBlock[0]
                    # print(cIndex, CheckCollideBlock)
                    if 0 < CheckCollideBlock < 20:
                        print("change")
                        self.x = (cIndex[0] + 1) * server.map.tile_w + FireBall.fireball_w
                        self.dir *= -1

            if dy > 0:
                for nIndex_x in range(LT[0], RT[0]):
                    cIndex = nIndex_x, nIndex[1] + 1
                    CheckCollideBlock = server.map.map[
                        ((server.TILE_W_N - cIndex[1] - 1) * server.map.tiles_Row) + nIndex_x]
                    if type(CheckCollideBlock) is list:
                        CheckCollideBlock = CheckCollideBlock[0]
                    if 0 < CheckCollideBlock < 20 and cIndex[1] * server.map.tile_h < (
                            my + dy + FireBall.fireball_h / 2):
                        self.y = cIndex[1] * server.map.tile_h - FireBall.fireball_h / 2 - 1
                        self.acceleration = 0

            elif dy < 0:
                for nIndex_x in range(LB[0], RB[0]):
                    cIndex = nIndex_x, nIndex[1] - 1
                    # print("cIndex=", cIndex[1], nIndex[1])
                    if cIndex[1] < 0:
                        Game_World.remove_object(self)
                        break
                    CheckCollideBlock = server.map.map[
                        ((server.TILE_W_N - cIndex[1] - 1) * server.map.tiles_Row) + nIndex_x]
                    if type(CheckCollideBlock) is list:
                        CheckCollideBlock = CheckCollideBlock[0]
                    # print((cIndex[1] + 1) * server.map.tile_h, "<", my + dy - FireBall.fireball_h / 2)
                    if 0 < CheckCollideBlock < 20:
                        print("FIreBall Collide")
                        if self.count > 0.8:
                            self.y = (cIndex[1]+1) * server.map.tile_h + FireBall.fireball_h / 2 + 1
                            self.count *= 0.8
                            self.acceleration = self.count
                        else:
                            self.explosion()

        elif dy < 0:
            for nIndex_x in range(LB[0], RB[0]):
                cIndex = nIndex_x, nIndex[1] - 1
                print("cIndex=", cIndex[1], nIndex[1])
                if cIndex[1] < 0:
                    Game_World.remove_object(self)
                    break

    def get_bb(self):
        return self.x - FireBall.fireball_w/2, self.y - FireBall.fireball_h/2, self.x + FireBall.fireball_w/2, self.y + FireBall.fireball_h/2