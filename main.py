import Game_FrameWork
import Game_Play
import Game_Lobby
import Intro_Logo
import Init_value
from pico2d import *
if __name__ == '__main__':
    open_canvas(Init_value.WINDOW_WIDTH, Init_value.WINDOW_HEIGHT)
    Game_FrameWork.run(Intro_Logo)
    clear_canvas()