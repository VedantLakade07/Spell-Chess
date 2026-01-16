# ui/assets.py

import pygame
import os
import sys

class Assets:
    def __init__(self, sq):
        self.sq = sq
        self.images = self.load_pieces()

    def resource_path(self, relative):
        try:
            base = sys._MEIPASS
        except Exception:
            base = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base, "..", relative)

    def load_pieces(self):
        images = {}
        for color in ["w", "b"]:
            for p in ["p", "r", "n", "b", "q", "k"]:
                path = self.resource_path(f"assets/pieces/{color}{p}.png")
                img = pygame.image.load(path)
                images[color + p] = pygame.transform.scale(img, (self.sq, self.sq))
        return images
