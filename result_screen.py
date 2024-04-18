import pygame
from start_screen import Text, EndAnim
from icecream import ic


def result_screen(surface: pygame.Surface, clock: pygame.time.Clock, fps: int, score: int, prev_score: int) -> bool:
    w, h = surface.get_rect()[2:]
    dtime = 0
    you_loose_text = Text((w // 2, h // 3), [f'Your score: {score}', f'Best score: {prev_score}'], '#9F9F9F',
                          w // 20)
    restart_text = Text((w // 2, h // 3 * 2), ['Press r', 'To restart'], '#9F9F9F', w // 20, 5)

    vfx = []
    end_anim_flag = True
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYUP and event.key == 27:
                return False
            if event.type == pygame.KEYUP and event.key == 114 and end_anim_flag:
                vfx.append(EndAnim(w, h))
                end_anim_flag = False
        surface.fill('#000000')

        you_loose_text.render(surface)
        restart_text.render(surface, dtime)

        for effect in vfx[:]:
            if not effect:
                if isinstance(effect, EndAnim):
                    return True
                vfx.remove(effect)
            else:
                effect.play(surface, dtime)

        pygame.display.flip()
        dtime = clock.tick(fps)


if __name__ == '__main__':
    pygame.init()
    size = pygame.display.get_desktop_sizes()[0]
    size = (size[0] // 2, size[1] // 2)
    surfaced = pygame.display.set_mode(size)
    clocc = pygame.time.Clock()

    result_screen(surfaced, clocc, 60, 0, 0)

    pygame.quit()
