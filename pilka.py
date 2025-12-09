import pygame

class Pilka:
    def __init__(self, x, y, predkosc_x, predkosc_y):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.predkosc_x = predkosc_x
        self.predkosc_y = predkosc_y

        self.image = pygame.image.load('pilka.jpg')
        self.image = pygame.transform.scale(self.image, (40, 40))

        self.image.set_colorkey((255, 255, 255))
        self.mask = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.circle(self.mask, (255, 255, 255), (20, 20), 20)

        self.image.blit(self.mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

    def ruch(self):
        self.rect.x += self.predkosc_x
        self.rect.y += self.predkosc_y

    def odbicie(self, gracz1, gracz2, bramka_lewa, bramka_prawa):
        if self.rect.colliderect(gracz1.rect):
            self.predkosc_x = -self.predkosc_x
        if self.rect.colliderect(gracz2.rect):
            self.predkosc_x = -self.predkosc_x

        if self.rect.top <= 0 or self.rect.bottom >= 600:
            self.predkosc_y = -self.predkosc_y

        if self.rect.left <= 0 and not self.rect.colliderect(pygame.Rect(0, 250, 20, 100)):
            self.predkosc_x = -self.predkosc_x

        if self.rect.right >= 800 and not self.rect.colliderect(pygame.Rect(780, 250, 20, 100)):
            self.predkosc_x = -self.predkosc_x

        if self.rect.left <= 0:
            if not self.rect.colliderect(bramka_lewa):
                self.predkosc_x = -self.predkosc_x
            else:
                pass
        elif self.rect.right >= 800:
            if not self.rect.colliderect(bramka_prawa):
                self.predkosc_x = -self.predkosc_x
            else:
                pass

        if self.rect.left < -100 or self.rect.right > 900:
            self.predkosc_x *= -1
            self.rect.center = (400, 300)

    def rysuj(self, ekran):
        ekran.blit(self.image, self.rect)
