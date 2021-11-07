# 게임 프레임 워크 # 마리오라는 게임 구성 요소 중 큰 줄기
# 화면 출력
        # -로고
                # -로고 이미지출력
        # -메인 로비
                # -메인 로비 화면 출력, 화면 조작
                        # -설정창
        # -게임 화면
                # -맵
                        # -백그라운드
                # -마리오
import time
frame_time = 0.0
stack = None
running = None
def change_state(state):
    global stack
    if len(stack) > 0:
        stack[-1].exit()
        stack.pop()
    stack.append(state)
    state.enter()
    pass
def push_state(state):
    global stack
    stack.append(state)
    state.enter()
    pass
def pop_state():
    global stack
    stack[-1].exit()
    stack.pop()
    pass
def quit():
    global  running
    running = False
    pass
def run(start_state):
    global stack, running
    running = True
    stack = [start_state]
    start_state.enter()

    global frame_time
    current_time = time.time()

    while running:
        stack[-1].main()
        frame_time = time.time() - current_time
        frame_rate = 1.0 / frame_time
        current_time += frame_time

    while len(stack) > 0:
        stack[-1].exit()
        stack.pop()