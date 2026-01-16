import pygame
import os
import sys


def ask_game_mode(self):
    clock = pygame.time.Clock()

    btn_pvp = pygame.Rect(self.WIDTH//2 - 120, 180, 240, 50)
    btn_pvc = pygame.Rect(self.WIDTH//2 - 120, 260, 240, 50)

    while True:
        self.WIN.fill((20, 20, 20))

        title = self.BIG.render("Select Game Mode", True, (255,255,255))
        self.WIN.blit(title, title.get_rect(center=(self.WIDTH//2, 100)))

        pygame.draw.rect(self.WIN, (70,70,70), btn_pvp, border_radius=6)
        pygame.draw.rect(self.WIN, (70,70,70), btn_pvc, border_radius=6)

        self.WIN.blit(self.FONT.render("Player vs Player", True, (255,255,255)),
                      self.FONT.render("Player vs Player", True, (255,255,255)).get_rect(center=btn_pvp.center))

        self.WIN.blit(self.FONT.render("Player vs Computer", True, (255,255,255)),
                      self.FONT.render("Player vs Computer", True, (255,255,255)).get_rect(center=btn_pvc.center))

        pygame.display.update()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_pvp.collidepoint(event.pos):
                    return "pvp"
                if btn_pvc.collidepoint(event.pos):
                    return "pvc"



def ask_time_screen(self):
    clock = pygame.time.Clock()

    mode = "sudden"
    minutes = ""
    increment = ""

    # Clickable mode buttons
    btn_none = pygame.Rect(self.WIDTH//2 - 120, 130, 240, 40)
    btn_sudden = pygame.Rect(self.WIDTH//2 - 120, 180, 240, 40)
    btn_inc = pygame.Rect(self.WIDTH//2 - 120, 230, 240, 40)

    input_minutes = pygame.Rect(self.WIDTH//2 - 100, 300, 200, 40)
    input_increment = pygame.Rect(self.WIDTH//2 - 100, 350, 200, 40)

    active_field = "minutes"

    while True:
        self.WIN.fill((20, 20, 20))

        title = self.BIG.render("Choose Clock Mode", True, (255, 255, 255))
        self.WIN.blit(title, title.get_rect(center=(self.WIDTH//2, 70)))

        # -------- DRAW MODE BUTTONS --------
        for rect, text, m in [
            (btn_none, "No Clock", "none"),
            (btn_sudden, "Sudden Death", "sudden"),
            (btn_inc, "Increment", "increment")
        ]:
            color = (90, 140, 200) if mode == m else (70, 70, 70)
            pygame.draw.rect(self.WIN, color, rect, border_radius=6)
            label = self.FONT.render(text, True, (255, 255, 255))
            self.WIN.blit(label, label.get_rect(center=rect.center))

        # -------- INPUT FIELDS --------
        if mode != "none":
            pygame.draw.rect(self.WIN, (255,255,255), input_minutes, 2)
            txt = minutes if minutes else "Minutes"
            self.WIN.blit(
                self.FONT.render(txt, True, (255,255,255)),
                (input_minutes.x + 10, input_minutes.y + 8)
            )

        if mode == "increment":
            pygame.draw.rect(self.WIN, (255,255,255), input_increment, 2)
            txt = increment if increment else "Increment (sec)"
            self.WIN.blit(
                self.FONT.render(txt, True, (255,255,255)),
                (input_increment.x + 10, input_increment.y + 8)
            )

        hint = self.FONT.render("Click mode • Type time • ENTER to start", True, (180,180,180))
        self.WIN.blit(hint, hint.get_rect(center=(self.WIDTH//2, 420)))

        pygame.display.update()
        clock.tick(30)

        # -------- EVENTS --------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_none.collidepoint(event.pos):
                    mode = "none"
                elif btn_sudden.collidepoint(event.pos):
                    mode = "sudden"
                elif btn_inc.collidepoint(event.pos):
                    mode = "increment"

                elif input_minutes.collidepoint(event.pos):
                    active_field = "minutes"
                elif input_increment.collidepoint(event.pos):
                    active_field = "increment"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if mode == "none":
                        return ("none", 0, 0)
                    if minutes.isdigit() and int(minutes) > 0:
                        inc = int(increment) if increment.isdigit() else 0
                        return (mode, int(minutes)*60, inc)

                elif event.key == pygame.K_BACKSPACE:
                    if active_field == "minutes":
                        minutes = minutes[:-1]
                    elif active_field == "increment":
                        increment = increment[:-1]

                elif event.unicode.isdigit():
                    if active_field == "minutes":
                        minutes += event.unicode
                    elif active_field == "increment":
                        increment += event.unicode
