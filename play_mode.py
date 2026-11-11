from pico2d import (
    SDL_KEYDOWN, SDL_QUIT, SDLK_ESCAPE,
    clear_canvas, get_events, update_canvas,
)

import game_framework
import game_world
from bird import Bird, FRAME_COUNT
from grass import Grass

BIRD_COUNT = 10
birds = []


def handle_events():
    for event in get_events():
        if (event.type == SDL_QUIT or
                (event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE)):
            game_framework.quit()
            return


def init():
    game_world.clear()
    birds.clear()
    game_world.add_oject(Grass(), 0)

    for index in range(BIRD_COUNT):
        column, row = index % 5, index // 5
        bird = Bird(
            160 + 320 * column, 300 + 180 * row,
            direction=1 if index % 2 == 0 else -1,
            frame=index % FRAME_COUNT,
        )
        birds.append(bird)
        game_world.add_oject(bird, 1)


def pause():
    pass


def resume():
    pass


def finish():
    game_world.clear()
    birds.clear()
    # 캔버스를 닫기 전에 SDL 텍스처의 마지막 참조를 해제한다.
    Bird.image = None


def update():
    game_world.update()


def render():
    clear_canvas()
    game_world.render()
    update_canvas()
