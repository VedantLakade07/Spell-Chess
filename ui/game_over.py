import pygame

class GameOverUI:
    def __init__(self, win, width, height, font, big_font):
        self.win = win
        self.width = width
        self.height = height
        self.font = font
        self.big = big_font

    def draw(self, text):
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.win.blit(overlay, (0, 0))

        msg = self.big.render(text, True, (255, 255, 255))
        hint = self.font.render(
            "R = Replay    Q / Esc = Quit",
            True,
            (200, 200, 200)
        )

        self.win.blit(
            msg,
            msg.get_rect(center=(self.width // 2, self.height // 2 - 20))
        )
        self.win.blit(
            hint,
            hint.get_rect(center=(self.width // 2, self.height // 2 + 30))
        )
