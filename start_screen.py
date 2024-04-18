import pygame
import math
from icecream import ic


class Effect:
    def __init__(self, w: int, h: int, tg_time: int):
        self.w, self.h = w, h
        self.is_going = True
        self.secs = 0
        self.tg_time = tg_time

    def update(self, dtime: int):
        self.secs += dtime
        if self.secs >= self.tg_time:
            self.is_going = False

    def __bool__(self):
        return self.is_going


class StartAnim(Effect):
    def __init__(self, w, h):
        super().__init__(w, h, 5000)

        self.bg = pygame.Surface((w, h))
        self.title_text = Text((w // 2, -500), ['The Tetris'], text_size=w // 20)
        self.press_text = Text((w // 2, h // 5 * 4), ['Press any key', ' to continue'], color='#BBBBBB',
                               text_size=w // 50)
        self.press_text.set_alpha(0)

    def play(self, surface: pygame.Surface, dtime: int):
        if self.secs <= 1000:
            surface.blit(self.bg, (0, 0))
        elif self.secs <= 1500:
            surface.blit(self.bg, (0, 0))
            self.title_text.set_pos(self.w / 2, self.h // 2 * (self.secs - 1000) // 500)
            self.title_text.render(surface)
        elif self.secs <= 4000:
            self.title_text.render(surface)
            self.title_text.set_pos(self.w / 2, self.h // 2)
        else:
            self.title_text.render(surface)
            self.press_text.set_alpha(round((self.secs - 4000) * 0.255))
            self.press_text.render(surface)

        super().update(dtime)


class EndAnim(Effect):
    def __init__(self, w, h):
        super().__init__(w, h, 2000)
        self.effect = pygame.Surface((w, h))
        self.effect.fill('#000000')
        self.alpha = 0

    def play(self, surface: pygame.Surface, dtime: int):
        self.alpha += 0.1275 * dtime
        self.effect.set_alpha(self.alpha)
        surface.blit(self.effect, (0, 0))

        super().update(dtime)


class Text:  # TODO: change font
    def __init__(self, pos: tuple[float, float], text: list[str], color: str = '#FFFFFF',
                 text_size: int = 50, speed: int = 0):
        self.x, self.y = pos
        self.text = text
        self.color = color
        self.text_size = text_size
        self.speed = speed
        self.font = pygame.font.Font('SAIBA-45.otf', self.text_size)
        self.ccnt = 0
        self.alpha = -1

    def render(self, surface: pygame.Surface, dtime: int = 0):
        self.ccnt += self.speed * dtime / 1000
        for i in range(len(self.text)):
            line = self.font.render(self.text[i], 1, self.color)
            line.set_alpha(round(64 * math.cos(self.ccnt) + 191) if self.alpha == -1 else self.alpha)
            surface.blit(line, line.get_rect(center=(self.x, self.y + i * self.text_size + 10)))

    def set_alpha(self, alpha: int):
        self.alpha = alpha

    def set_pos(self, x: float, y: float):
        self.x, self.y = x, y


def start_screen(surface: pygame.Surface, clock: pygame.time.Clock, fps: int) -> bool:
    """
    Just a beautiful start screen
    :param surface: where to render
    :param clock:
    :param fps:
    :returns: True if start_screen was escaped correctly (space_bar key pressed) False otherwise
    """

    w, h = ic(surface.get_rect()[2:])
    texts = [Text((w // 2, h // 5 * 4), ['Press any key', ' to continue'], color='#BBBBBB', text_size=w // 50, speed=5),
             Text(ic(w // 2, h // 2), ['The Tetris'], text_size=w // 20)]

    bg = pygame.Surface((w, h))
    bg.fill('#010101')
    pygame.draw.circle(bg, '#757575', (0, h // 6), w // 2)
    pygame.draw.lines(bg, '#757575', False, ((w // 5 * 3, h + 6), (w // 5 * 4, h // 5 * 4), (w + 6, h // 6),
                                             (w + 6, h // 2), (w // 5 * 4, h // 5 * 4), (w + 6, h // 9 * 8),
                                             (w + 6, h + 6), (w // 17 * 15, h + 6), (w // 5 * 4, h // 5 * 4)), 5)

    vfx = [StartAnim(w, h)]
    end_anim_flag = True
    text_flag = False
    dtime = 1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYUP and end_anim_flag and text_flag:
                vfx.append(EndAnim(w, h))
                end_anim_flag = False
        surface.blit(bg, (0, 0))

        [text.render(surface, dtime) for text in texts] if text_flag else None

        for effect in vfx[:]:
            if not effect:
                if isinstance(effect, EndAnim):
                    return True
                if isinstance(effect, StartAnim):
                    text_flag = True
                vfx.remove(effect)
            effect.play(surface, dtime)

        pygame.display.flip()
        dtime = clock.tick(fps)


if __name__ == '__main__':
    pygame.init()
    size = pygame.display.get_desktop_sizes()[0]
    size = (size[0] // 2, size[1] // 2)
    surfaced = pygame.display.set_mode(size)
    clocc = pygame.time.Clock()

    start_screen(surfaced, clocc, fps=60)

    pygame.quit()
