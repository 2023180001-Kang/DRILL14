from pico2d import load_image


SHEET_WIDTH = 918
SHEET_HEIGHT = 506
SHEET_COLUMNS = 5
FRAME_WIDTH = 182
FRAME_HEIGHT = 170
FRAME_COUNT = 14
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

    def __init__(self, x, y):
        if Bird.image is None:
            Bird.image = load_image('bird_animation.png')
        self.x, self.y = x, y
        self.frame = 0.0
        self.draw_width = DRAW_WIDTH
        self.draw_height = DRAW_HEIGHT

    def update(self):
        pass

    def draw(self):
        left, bottom, width, height = FRAME_RECTS[int(self.frame)]
        scale = self.draw_width / FRAME_WIDTH
        # 마지막 행 아래의 누락된 투명 여백을 보정해 셀의 위쪽 기준점을 유지한다.
        height_on_canvas = height * scale
        y = self.y + (self.draw_height - height_on_canvas) / 2
        self.image.clip_draw(
            left, bottom, width, height,
            self.x, y, self.draw_width, height_on_canvas,
        )
