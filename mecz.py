import pygame
class Mecz:
    def __init__(self):
        self.wynik_gracza1 = 0
        self.wynik_gracza2 = 0
        self.czas = 300
        self.gol_cooldown = 0

    def licz_czas(self):
        self.czas -= 1 / 60
        if self.czas <= 0:
            self.koniec_gry()

    def koniec_gry(self):
        print("Koniec gry!")

    def aktualizuj_wynik(self, pilka, bramka_lewa, bramka_prawa):
        if self.gol_cooldown > 0:
            self.gol_cooldown -= 1
            return

        if pilka.rect.colliderect(bramka_prawa):
            self.wynik_gracza1 += 1
            pilka.rect.center = (400, 300)
            self.gol_cooldown = 60

        if pilka.rect.colliderect(bramka_lewa):
            self.wynik_gracza2 += 1
            pilka.rect.center = (400, 300)
            self.gol_cooldown = 60
