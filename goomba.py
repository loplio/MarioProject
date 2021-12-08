import Game_FrameWork
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode
from pico2d import *
import Game_World
import server
import Init_value

# zombie Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# zombie Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 2


# animation_names = ['Walk', 'Dead', 'Jump']


class Goomba:
    image = None
    goomba_w = 25
    goomba_h = 25
    goombas_pos = [(1795, 110),  (2555, 110), (2650, 110), (3180, 205), (3780, 110),
    (4170, 110), (2465, 365), (2700, 365), (2875, 270), (650, 110)]
    def load_images(self):
        if Goomba.image == None:
            Goomba.image = load_image('Mario.png')

    def __init__(self, x, y):
        self.x, self.y = x, y
        self.load_images()
        self.dir = -1
        self.speed = 0
        self.frame = 0
        self.dead_num = 0
        self.state_dead = False
        self.state_floating = False
        self.acceleration = 0
        self.build_behavior_tree()

    def move(self):
        self.speed = RUN_SPEED_PPS
        return BehaviorTree.SUCCESS
        # fill here

    def build_behavior_tree(self):
        move_node = LeafNode('Move', self.move)

        MoveAndJump_node = SequenceNode('move')
        MoveAndJump_node.add_children(move_node)

        self.bt = BehaviorTree(MoveAndJump_node)
        # fill here
        pass

    def floating(self):
        left, right, bottom = int((self.x - Goomba.goomba_w/2) // server.map.tile_w), int((self.x + Goomba.goomba_w/2) // server.map.tile_w), int((self.y - Goomba.goomba_h/2) // server.map.tile_h)
        if server.map.map[((server.TILE_W_N - bottom)*server.map.tiles_Row) + left] == 0\
                and server.map.map[((server.TILE_W_N - bottom)*server.map.tiles_Row) + right] == 0:
            self.state_floating = True
            return True
        return False

    def dead(self, num):
        self.state_dead = True
        self.dead_num = num
        if num == 1:
            self.acceleration = 2
        else:
            self.acceleration = 0

    def collide(self):
        nIndex = int(self.x // server.map.tile_w), int(self.y // server.map.tile_h)
        dx, dy = self.dir * self.speed * Game_FrameWork.frame_time, 3 * self.acceleration
        mx, my = self.x, self.y
        LB, RB, LT, RT = server.map.get_collide_map(self, Goomba.goomba_w, Goomba.goomba_h)
        if nIndex[1] + 1 < server.TILE_W_N and nIndex[1] >= 0:
            if not self.state_dead:
                if dx > 0:
                    for nIndex_y in range(RB[1], RT[1]):
                        cIndex = nIndex[0] + 1, nIndex_y
                        CheckCollideBlock = server.map.map[
                            ((server.TILE_W_N - nIndex_y - 1) * server.map.tiles_Row) + cIndex[0]]
                        if type(CheckCollideBlock) is list:
                            CheckCollideBlock = CheckCollideBlock[0]
                        if 0 < CheckCollideBlock < 20 and cIndex[0] * server.map.tile_w < (
                                mx + dx + self.goomba_w / 2):
                            self.x = int(cIndex[0] * server.map.tile_w - self.goomba_w / 2 - dx)
                            self.dir *= -1

                elif dx < 0:
                    for nIndex_y in range(LB[1], LT[1]):
                        cIndex = nIndex[0] - 1, nIndex_y
                        CheckCollideBlock = server.map.map[
                            ((server.TILE_W_N - nIndex_y - 1) * server.map.tiles_Row) + cIndex[0]]
                        if type(CheckCollideBlock) is list:
                            CheckCollideBlock = CheckCollideBlock[0]
                        if 0 < CheckCollideBlock < 20 and (cIndex[0] + 1) * server.map.tile_w > (
                                mx + dx - self.goomba_w / 2):
                            self.x = (cIndex[0] + 1) * server.map.tile_w + self.goomba_w / 2 - dx
                            self.dir *= -1

                if dy > 0:
                    for nIndex_x in range(LT[0], RT[0]):
                        cIndex = nIndex_x, nIndex[1] + 1
                        CheckCollideBlock = server.map.map[
                            ((server.TILE_W_N - cIndex[1] - 1) * server.map.tiles_Row) + nIndex_x]
                        if type(CheckCollideBlock) is list:
                            CheckCollideBlock = CheckCollideBlock[0]
                        if 0 < CheckCollideBlock < 20 and cIndex[1] * server.map.tile_h < (
                                my + dy + self.goomba_h / 2):
                            self.y = cIndex[1] * server.map.tile_h - self.goomba_h / 2 - 1
                            self.speed = 0

                elif dy < 0:
                    for nIndex_x in range(LB[0], RB[0]):
                        cIndex = nIndex_x, nIndex[1] - 1
                        print("cIndex=",cIndex[1] , nIndex[1])
                        if cIndex[1] < 0:
                            Game_World.remove_object(self)
                            server.goomba.remove(self)
                            break
                        CheckCollideBlock = server.map.map[
                            ((server.TILE_W_N - cIndex[1] - 1) * server.map.tiles_Row) + nIndex_x]
                        if type(CheckCollideBlock) is list:
                            CheckCollideBlock = CheckCollideBlock[0]
                        if 0 < CheckCollideBlock < 20 and (cIndex[1] + 1) * server.map.tile_h > (
                                my + dy - self.goomba_h / 2):
                            self.y = (cIndex[1] + 1) * server.map.tile_h + self.goomba_h / 2 + 1
                            self.acceleration = 0
                            self.state_floating = False
            elif dy < 0:
                for nIndex_x in range(LB[0], RB[0]):
                    cIndex = nIndex_x, nIndex[1] - 1
                    print("cIndex=",cIndex[1] , nIndex[1])
                    if cIndex[1] < 0:
                        Game_World.remove_object(self)
                        server.goomba.remove(self)
                        break


    def get_bb(self):
        return self.x - 12, self.y - 12, self.x + 12, self.y + 12

    def update(self):
        # fill here
        self.bt.run()
        window_left = server.mario.x - Init_value.WINDOW_WIDTH/2
        if window_left + Init_value.WINDOW_WIDTH > self.x > window_left > 0:
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * Game_FrameWork.frame_time) % FRAMES_PER_ACTION
            self.x += self.dir * self.speed * Game_FrameWork.frame_time
            self.y += 3 * self.acceleration
            self.collide()
            if self.state_floating is False and self.state_dead is False:
                if self.floating():
                    print("floating")
            else:
                self.acceleration = self.acceleration - 0.98 * 0.34

    def draw(self):
        window_left = server.mario.x - Init_value.WINDOW_WIDTH/2
        if self.state_dead and self.dead_num == 1:
            Goomba.image.clip_draw(11 * Goomba.goomba_w, 0, Goomba.goomba_w, Goomba.goomba_h, self.x - window_left, self.y)
        elif self.state_dead and self.dead_num == 2:
            Goomba.image.clip_composite_draw(12 * Goomba.goomba_w, 0, Goomba.goomba_w, Goomba.goomba_h, 3.141592, 'h', self.x - window_left, self.y, Goomba.goomba_w, Goomba.goomba_h)
        else:
            if window_left + Init_value.WINDOW_WIDTH > self.x > window_left > 0:
                Goomba.image.clip_draw((int(self.frame)+12) * Goomba.goomba_w, 0, Goomba.goomba_w, Goomba.goomba_h, self.x - window_left, self.y)
            elif window_left <= 0:
                Goomba.image.clip_draw((int(self.frame)+12) * Goomba.goomba_w, 0, Goomba.goomba_w, Goomba.goomba_h, self.x, self.y)

    def handle_event(self, event):
        pass

