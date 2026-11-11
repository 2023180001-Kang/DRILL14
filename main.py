from pico2d import close_canvas, open_canvas

import game_framework
import play_mode


def main():
    open_canvas(1600, 600)
    try:
        game_framework.run(play_mode)
    finally:
        close_canvas()


if __name__ == '__main__':
    main()
