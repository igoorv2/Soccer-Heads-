import pygame

class Postac:
    def __init__(self,x,y,obrazek):
        self.rect = pygame.Rect(x,y,70,70)
        self.ustaw_obrazek(obrazek)

    def ustaw_obrazek(self, obrazek):
        self.obrazek = pygame.image.load(obrazek)
        self.obrazek = pygame.transform.scale(self.obrazek, (66,66))

    def rysuj(self, ekran):
        ekran.blit(self.obrazek, self.rect)
