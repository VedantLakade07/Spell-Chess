# ui/promotion.py

import pygame

class PromotionUI:
    def __init__(self, win, width, sq, assets):
        self.win = win
        self.width = width
        self.sq = sq
        self.assets = assets

    def draw(self, color):
        overlay = pygame.Surface((self.width, self.width))
        overlay.set_alpha(180)
        overlay.fill((0,0,0))
        self.win.blit(overlay, (0,0))

        pieces = ["q","r","b","n"]
        y = self.width//2 - self.sq//2
        start = self.width//2 - 2*self.sq

        for i,p in enumerate(pieces):
            rect = pygame.Rect(start + i*self.sq, y, self.sq, self.sq)
            pygame.draw.rect(self.win, (200,200,200), rect)
            key = ("w" if color=="white" else "b") + p
            self.win.blit(self.assets.images[key], rect)
