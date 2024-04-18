import pygame
import os
from start_screen import start_screen
from result_screen import result_screen
from game import game
from icecream import ic

FPS = 60


def create_scorefile(file_name: str):
    open(fr'{os.path.curdir}\{file_name}', 'wt', encoding='utf-8').write('0')
    return open_scorefile(file_name)


def open_scorefile(file_name: str):
    return open(fr'{os.path.curdir}\{file_name}', 'rt', encoding='utf-8')\
        if os.path.exists(fr'{os.path.curdir}\{file_name}') else create_scorefile(file_name)


def write_scorefile(file_name: str, result: int) -> None:
    if not os.path.exists(fr'{os.path.curdir}\{file_name}'):
        create_scorefile(file_name)
    open(fr'{os.path.curdir}\{file_name}', 'wt', encoding='utf-8').write(str(result))


def main() -> None:
    """
    Main body of the whole game. This like a container form where we can start the game or change settings
    """
    pygame.init()
    pygame.display.set_caption('Tetris')
    width, height = pygame.display.get_desktop_sizes()[0]
    surface = pygame.display.set_mode((width // 2, height // 2))
    clock = pygame.time.Clock()

    prev_result = int(open_scorefile('scores').read().strip())
    running = start_screen(surface, clock, FPS)
    while running:
        result = game(clock, FPS)
        if result == -1:
            break
        running = result_screen(surface, clock, FPS, result, prev_result)
        if result > prev_result:
            prev_result = ic(result)
            write_scorefile('scores', result)

    pygame.quit()


if __name__ == '__main__':
    main()
