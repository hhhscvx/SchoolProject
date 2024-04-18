from icecream import ic
from figures import TILE, H, W, figures, figure_rect  # так лучше контролируются значения переменных
import pygame
from copy import deepcopy
from random import choice


ic.disable()


def game(clock: pygame.time.Clock, fps: int) -> int:
    game_size = W * TILE, H * TILE  # убрал дубль
    game_sc = pygame.display.set_mode(game_size)

    grid = [pygame.Rect(x * TILE, y * TILE, TILE, TILE)
            for x in range(10) for y in range(20)]

    figure = deepcopy(choice(figures))
    anim_count, anim_speed, anim_limit = 0, 60, 2000
    field = [[0 for _ in range(W)] for _ in range(H)]  # почему нет ¯\_(ツ)_/¯
    score = 0
    # lines = 0  pycharm говорит, что это не используется
    scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}

    def check_borders():
        if figure[i].x < 0 or figure[i].x > W - 1:
            return False
        elif figure[i].y > H - 1 or field[figure[i].y][figure[i].x]:
            return False
        return True

    while True:  # обращайся за референсами к start_screen
        dx, rotate = 0, False
        game_sc.fill(pygame.Color('black'))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return -1  # еще один бонус работы в функции: можно в любой момент из нее выйти через return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    dx = -1
                elif event.key == pygame.K_RIGHT:
                    dx = 1
                elif event.key == pygame.K_DOWN:
                    anim_limit = 100
                elif event.key == pygame.K_UP:
                    rotate = True

        # move x
        figure_old = deepcopy(figure)

        for i in range(4):
            figure[i].x += dx
            if not check_borders():
                figure = deepcopy(figure_old)
                break

        # move y
        anim_count += anim_speed
        if anim_count > anim_limit:
            anim_count = 0
            for i in range(4):
                figure[i].y += 1
                if not check_borders():
                    for j in range(4):  # тут переменная во внутреннем цикле называлась так же, как и во внешнем
                        field[figure_old[j].y][figure_old[j].x] = pygame.Color('white')
                    figure = deepcopy(choice(figures))
                    anim_limit = 2000
                    break

        # rotate
        center = figure[0]
        figure_old = deepcopy(figure)
        if rotate:
            for i in range(4):
                x = figure[i].y - center.y
                y = figure[i].x - center.x
                figure[i].x = center.x - x
                figure[i].y = center.y + y
                if not check_borders():
                    figure = deepcopy(figure_old)
                    break

        line = H - 1
        lines = 0
        for row in range(H - 1, -1, -1):
            count = 0
            for i in range(W):
                if field[row][i]:
                    count += 1
                field[line][i] = field[row][i]
            if count < W:
                line -= 1
            else:
                lines += 1
        # old_score = int(str(score)[:]) pycharm говорит, что это не используется
        score += scores[lines]
        # if score != old_score: pycharm говорит, что это не используется
        #     # print(f'Score: {score}') pycharm говорит, что это не используется
        #     old_score = int(str(score)[:]) you guess it

        # draw grid
        [pygame.draw.rect(game_sc, (40, 40, 40), i_rect, 1) for i_rect in grid]

        for i in range(4):
            figure_rect.x = figure[i].x * TILE
            figure_rect.y = figure[i].y * TILE
            pygame.draw.rect(game_sc, pygame.Color('white'), figure_rect)

        for y, raw in enumerate(field):
            for x, col in enumerate(raw):
                if col:
                    figure_rect.x, figure_rect.y = x * TILE, y * TILE
                    pygame.draw.rect(game_sc, col, figure_rect)

        # game over
        for i in range(W):
            if field[0][i]:
                field = [[0 for i in range(W)] for i in range(H)]
                # anim_count, anim_speed, anim_limit = 0, 60, 2000 pycharm говорит, что это не используется
                print('------------')
                print(f'Game over!')
                print(f'Total score: {score}')
                print('------------')
                return score

        pygame.display.flip()
        clock.tick(fps)


if __name__ == '__main__':
    pygame.init()
    size = pygame.display.get_desktop_sizes()[0]
    clocc = pygame.time.Clock()

    game(clocc, 60)

    pygame.quit()
