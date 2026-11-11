from pico2d import close_canvas, hide_lattice, open_canvas

import game_framework
import play_mode


def main():
    open_canvas(1600, 600, sync=True)
    try:
        hide_lattice()
        game_framework.run(play_mode)
    finally:
        close_canvas()


if __name__ == '__main__':
    main()
