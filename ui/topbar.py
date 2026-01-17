# ui/topbar.py
import pygame
from ui.constants import TOP_BG, TOP_TEXT, BTN_BG, BTN_TEXT, BTN_HOVER


class TopBar:
    def __init__(self, win, width, height, font):
        self.win = win
        self.width = width
        self.height = height
        self.font = font

        self.resign_rect = pygame.Rect(width // 2 - 60, 20, 120, 40)

    def draw(self, clock, turn):
        # -------- BACKGROUND --------
        pygame.draw.rect(
            self.win,
            TOP_BG,
            (0, 0, self.width, self.height)
        )

        # -------- CLOCK --------
        if clock.mode != "none":
            w_col = (255, 255, 255) if turn == "white" else (150, 150, 150)
            b_col = (255, 255, 255) if turn == "black" else (150, 150, 150)

            w = f"{int(clock.white_time)//60:02}:{int(clock.white_time)%60:02}"
            b = f"{int(clock.black_time)//60:02}:{int(clock.black_time)%60:02}"

            self.win.blit(
                self.font.render(f"White {w}", True, w_col),
                (20, 30)
            )
            self.win.blit(
                self.font.render(f"Black {b}", True, b_col),
                (self.width - 170, 30)
            )

        # -------- RESIGN BUTTON --------
        mouse_pos = pygame.mouse.get_pos()
        btn_color = BTN_HOVER if self.resign_rect.collidepoint(mouse_pos) else BTN_BG

        pygame.draw.rect(
            self.win,
            btn_color,
            self.resign_rect,
            border_radius=6
        )

        txt = self.font.render("Resign", True, BTN_TEXT)
        self.win.blit(
            txt,
            txt.get_rect(center=self.resign_rect.center)
        )
