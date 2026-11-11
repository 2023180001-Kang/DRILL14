from pico2d import get_canvas_width, load_image

import game_framework


SHEET_WIDTH = 918
SHEET_HEIGHT = 506
SHEET_COLUMNS = 5
FRAME_WIDTH = 182
FRAME_HEIGHT = 170
FRAME_COUNT = 14
ANIMATION_FPS = 10.0
FLIGHT_SPEED_PPS = 180.0
DRAW_WIDTH = 100
DRAW_HEIGHT = DRAW_WIDTH * FRAME_HEIGHT / FRAME_WIDTH

# 오른쪽 8픽셀과 마지막 빈 칸은 제외한다. 마지막 행은 실제 높이가 166이다.
FRAME_RECTS = tuple(
    (
        (index % SHEET_COLUMNS) * FRAME_WIDTH,
        max(0, SHEET_HEIGHT - (index // SHEET_COLUMNS + 1) * FRAME_HEIGHT),
        FRAME_WIDTH,
        min(FRAME_HEIGHT, SHEET_HEIGHT - (index // SHEET_COLUMNS) * FRAME_HEIGHT),
    )
    for index in range(FRAME_COUNT)
)


class Bird:
    image = None

    def __init__(self, x, y, direction=1, frame=0, speed=FLIGHT_SPEED_PPS):
        if Bird.image is None:
            Bird.image = load_image('bird_animation.png')
        self.x, self.y = x, y
        self.frame = float(frame) % FRAME_COUNT
        self.draw_width = DRAW_WIDTH
        self.draw_height = DRAW_HEIGHT
        self.left = self.draw_width / 2
        self.right = get_canvas_width() - self.draw_width / 2
        self.span = self.right - self.left
        if self.span <= 0:
            raise ValueError('캔버스 너비는 새의 표시 너비보다 커야 합니다.')
        self.x = max(self.left, min(self.right, self.x))
        self.speed = speed
        offset = self.x - self.left
        self.phase = (offset if direction >= 0 else 2 * self.span - offset) % (
            2 * self.span
        )
        self.direction = 1 if self.phase < self.span else -1

    def update(self):
        dt = game_framework.frame_time
        self.frame = (self.frame + ANIMATION_FPS * dt) % FRAME_COUNT
        # 삼각파로 이동 거리를 접어 큰 dt에서도 여러 번의 반사를 보존한다.
        self.phase = (self.phase + self.speed * dt) % (2 * self.span)
        self.x = self.left + self.span - abs(self.phase - self.span)
        self.direction = 1 if self.phase < self.span else -1

    def draw(self):
        left, bottom, width, height = FRAME_RECTS[int(self.frame)]
        scale = self.draw_width / FRAME_WIDTH
        # 마지막 행 아래의 누락된 투명 여백을 보정해 셀의 위쪽 기준점을 유지한다.
        height_on_canvas = height * scale
        y = self.y + (self.draw_height - height_on_canvas) / 2
        self.image.clip_composite_draw(
            left, bottom, width, height,
            0, '' if self.direction == 1 else 'h',
            self.x, y, self.draw_width, height_on_canvas,
        )
