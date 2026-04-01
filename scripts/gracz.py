import pygame
from postac import Postac

class Gracz(Postac):
    def __init__(self, x, y, obrazek, sterowanie):
        super().__init__(x,y,obrazek)
        self.sterowanie = sterowanie

    def ruch(self, keys):
        if keys[self.sterowanie['lewo']] and self.rect.left > 0:
            self.rect.x -= 5
        if keys[self.sterowanie['prawo']] and self.rect.right < 800:
            self.rect.x += 5
        if keys[self.sterowanie['skok']] and self.rect.top > 0:
            self.rect.y -= 5
        if keys[self.sterowanie['dol']] and self.rect.bottom < 600:
            self.rect.y += 5

    def resetuj_pozycje(self,x,y):
        self.rect.topleft = (x,y)
        self.predkosc_y = 0


