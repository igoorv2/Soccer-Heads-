import pygame
import json
from gracz import Gracz
from pilka import Pilka
from mecz import Mecz


class Gra:
    def zapisz_wynik(self):
        wynik = {
            "gracz1_nazwa": self.gracz1_nazwa,
            "gracz2_nazwa": self.gracz2_nazwa,
            "wynik_gracza1": self.mecz.wynik_gracza1,
            "wynik_gracza2": self.mecz.wynik_gracza2,
            "czas_gry": (pygame.time.get_ticks() - self.start_time) // 1000
        }
        try:
            with open('wyniki.json', 'r') as f:
                wszystkie_wyniki = json.load(f)
                if not isinstance(wszystkie_wyniki, list):
                    wszystkie_wyniki = []
        except FileNotFoundError:
            wszystkie_wyniki = []
        wszystkie_wyniki.append(wynik)

        if len(wszystkie_wyniki) > 5:
            wszystkie_wyniki = wszystkie_wyniki[-5:]
        with open('wyniki.json', 'w') as f:
            json.dump(wszystkie_wyniki, f, indent=4)

    def wczytaj_wyniki(self):
        try:
            with open('wyniki.json', 'r') as f:
                wyniki = json.load(f)
            return wyniki
        except FileNotFoundError:
            return []

    def __init__(self):

        pygame.init()
        pygame.font.init()
        pygame.mixer.init()
        self.wyniki = self.wczytaj_wyniki()

        if self.wyniki:
            print(f"Ostatni wynik: {self.wyniki[-1]}")

        self.kolory = {
            'biały': (255, 255, 255),
            'czarny': (0, 0, 0),
            'aktywny': (0, 0, 255),
            'nieaktywny': (255, 255, 255),
            'szary': (150, 150, 150)
        }

        self.menu_tlo = self.zaladuj_obrazek('menu.jpg', (800, 600))
        self.tlo = self.zaladuj_obrazek('stadion_real.jpg', (1024, 1024))
        self.champ_tlo = self.zaladuj_obrazek('champ.jpg', (800, 600))
        self.game_started = False

        obrazek1 = self.wybierz_postac(1)
        obrazek2 = self.wybierz_postac(2)
        self.gracz1_nazwa = ""
        self.gracz2_nazwa = ""

        self.gracz1 = Gracz(100, 500, obrazek1,
                            {'lewo': pygame.K_a, 'prawo': pygame.K_d, 'skok': pygame.K_w, 'dol': pygame.K_s})
        self.gracz2 = Gracz(650, 500, obrazek2,
                            {'lewo': pygame.K_LEFT, 'prawo': pygame.K_RIGHT, 'skok': pygame.K_UP, 'dol': pygame.K_DOWN})

        """

        self.gracz1 = Gracz(100, 500, 'lewy.jpg',
                            {'lewo': pygame.K_a, 'prawo': pygame.K_d, 'skok': pygame.K_w, 'dol': pygame.K_s})
        self.gracz2 = Gracz(650, 500, 'mbappe.jpg',
                            {'lewo': pygame.K_LEFT, 'prawo': pygame.K_RIGHT, 'skok': pygame.K_UP, 'dol': pygame.K_DOWN})

        """
        self.bramka_lewa_img = pygame.image.load("bramka_lewa.png")
        self.bramka_prawa_img = pygame.image.load("bramka_prawa.png")

        self.bramka_lewa_img = pygame.transform.scale(self.bramka_lewa_img, (50, 200))
        self.bramka_prawa_img = pygame.transform.scale(self.bramka_prawa_img, (50, 200))

        self.bramka_lewa_rect = pygame.Rect(0, 250, 50, 200)
        self.bramka_prawa_rect = pygame.Rect(780, 250, 50, 200)

        self.pilka = Pilka(400, 300, 5, 5)
        self.mecz = Mecz()
        self.start_time = None
        self.font = pygame.font.SysFont('Arial', 30, bold=True)
        self.player_font = pygame.font.SysFont('Arial', 30, bold=True)
        self.title_font = pygame.font.SysFont('Arial', 50, bold=True)

        pygame.mixer.music.load('kibice.mp3')
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(loops=-1, start=0.0)

    def zaladuj_obrazek(self, sciezka, rozmiar):
        obraz = pygame.image.load(sciezka)
        return pygame.transform.scale(obraz, rozmiar)

    def wyswietl_tekst(self, ekran, tekst, x, y, font, color):
        tekst_render = font.render(tekst, True, color)
        ekran.blit(tekst_render, (x, y))

    def wczytaj_nazwy(self):
        ekran = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Fußball Heads")
        font = pygame.font.SysFont('Arial', 30)
        input_box1 = pygame.Rect(100, 200, 200, 40)
        input_box2 = pygame.Rect(100, 300, 200, 40)
        start_button = pygame.Rect(100, 400, 150, 50)
        results_button = pygame.Rect(300, 400, 150, 50)

        color_inactive = pygame.Color(255, 255, 255)
        color_active = pygame.Color(0, 0, 255)
        active1 = False
        active2 = False
        text1 = ''
        text2 = ''
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box1.collidepoint(event.pos):
                        active1 = True
                        active2 = False
                    elif input_box2.collidepoint(event.pos):
                        active2 = True
                        active1 = False
                    else:
                        active1 = active2 = False

                    if start_button.collidepoint(event.pos):
                        if text1.strip() != '' and text2.strip() != '':
                            self.gracz1_nazwa = text1
                            self.gracz2_nazwa = text2
                            self.start_time = pygame.time.get_ticks()
                            self.game_started = True
                            running = False

                    if results_button.collidepoint(event.pos):
                        self.wyswietl_wyniki()

                if event.type == pygame.KEYDOWN:
                    if active1:
                        if event.key == pygame.K_BACKSPACE:
                            text1 = text1[:-1]
                        elif event.key == pygame.K_RETURN:
                            active1 = False
                            active2 = True
                        else:
                            text1 += event.unicode
                    elif active2:
                        if event.key == pygame.K_BACKSPACE:
                            text2 = text2[:-1]
                        elif event.key == pygame.K_RETURN:
                            if text1.strip() != '' and text2.strip() != '':
                                self.gracz1_nazwa = text1
                                self.gracz2_nazwa = text2
                                self.start_time = pygame.time.get_ticks()
                                self.game_started = True
                                running = False
                        else:
                            text2 += event.unicode

            ekran.blit(self.menu_tlo, (0, 0))

            self.wyswietl_tekst(ekran, "Witaj w grze", 250, 50, self.title_font, (255, 255, 255))
            self.wyswietl_tekst(ekran, "Wprowadź nazwę Gracza 1:", 100, 150, self.player_font, (255, 255, 255))
            self.wyswietl_tekst(ekran, "Wprowadź nazwę Gracza 2:", 100, 250, self.player_font, (255, 255, 255))
            pygame.draw.rect(ekran, color_active if active1 else color_inactive, input_box1, 2)
            pygame.draw.rect(ekran, color_active if active2 else color_inactive, input_box2, 2)

            ekran.blit(font.render(text1, True, (255, 255, 255)), (input_box1.x + 5, input_box1.y + 5))
            ekran.blit(font.render(text2, True, (255, 255, 255)), (input_box2.x + 5, input_box2.y + 5))

            pygame.draw.rect(ekran, (0, 200, 0), start_button)
            self.wyswietl_tekst(ekran, "Start", start_button.x + 40, start_button.y + 10, self.font, (255, 255, 255))

            pygame.draw.rect(ekran, (0, 0, 200), results_button)
            self.wyswietl_tekst(ekran, "Wyniki", results_button.x + 30, results_button.y + 10, self.font,
                                (255, 255, 255))

            pygame.display.update()
            clock.tick(30)

    def uruchom_gry(self, auto_start=False):
        if not auto_start:
            ekran = pygame.display.set_mode((800, 600))
            pygame.display.set_caption("Fußball Heads - Menu")
            font = pygame.font.SysFont('Arial', 50, bold=True)
            small_font = pygame.font.SysFont('Arial', 30)

            start_btn = pygame.Rect(300, 300, 200, 60)
            running = True
            while running:
                ekran.fill((0, 100, 200))
                ekran.blit(self.menu_tlo, (0, 0))
                self.wyswietl_tekst(ekran, "Fußball Heads", 250, 100, font, self.kolory['biały'])

                pygame.draw.rect(ekran, (0, 200, 0), start_btn)
                self.wyswietl_tekst(ekran, "Start", start_btn.x + 60, start_btn.y + 15, small_font,
                                    self.kolory["biały"])

                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if start_btn.collidepoint(event.pos):
                            running = False
                            break

            self.wczytaj_nazwy()

        print(f"Gracz 1: {self.gracz1_nazwa}, Gracz 2: {self.gracz2_nazwa}")

        self.bramka_lewa_rect = self.bramka_lewa_img.get_rect(topleft=(0, 250))
        self.bramka_prawa_rect = self.bramka_prawa_img.get_rect(topleft=(750, 250))
        ekran = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Fußball Heads")
        clock = pygame.time.Clock()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False

            keys = pygame.key.get_pressed()
            self.gracz1.ruch(keys)
            self.gracz2.ruch(keys)
            self.pilka.ruch()

            self.mecz.licz_czas()
            self.mecz.aktualizuj_wynik(self.pilka, self.bramka_lewa_rect, self.bramka_prawa_rect)

            if self.mecz.wynik_gracza1 >= 5 or self.mecz.wynik_gracza2 >= 5:
                self.koniec_gry()

            ekran.blit(self.tlo, (0, 0))
            self.gracz1.rysuj(ekran)
            self.gracz2.rysuj(ekran)
            self.pilka.rysuj(ekran)
            ekran.blit(self.bramka_lewa_img, self.bramka_lewa_rect.topleft)
            ekran.blit(self.bramka_prawa_img, self.bramka_prawa_rect.topleft)
            self.pilka.odbicie(self.gracz1, self.gracz2, self.bramka_lewa_rect, self.bramka_prawa_rect)
            self.mecz.aktualizuj_wynik(self.pilka, self.bramka_lewa_rect, self.bramka_prawa_rect)

            wynik_text = self.player_font.render(
                f"{self.gracz1_nazwa}: {self.mecz.wynik_gracza1} | {self.gracz2_nazwa}: {self.mecz.wynik_gracza2}",
                True, self.kolory['biały'])
            ekran.blit(wynik_text, (300, 10))

            elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
            timer_text = self.font.render(f"Time: {elapsed_time}s", True, self.kolory['biały'])
            pygame.draw.rect(ekran, self.kolory['biały'], (10, 10, 150, 40), 5)
            pygame.draw.rect(ekran, self.kolory['czarny'], (10, 10, 150, 40), 2)
            ekran.blit(timer_text, (20, 15))

            pygame.display.update()
            clock.tick(60)

        pygame.quit()

    def koniec_gry(self):
        winner = self.gracz1_nazwa if self.mecz.wynik_gracza1 >= 5 else self.gracz2_nazwa
        self.zapisz_wynik()
        self.ekran_koncowy(winner)

    def display_gratulacje(self, winner):
        ekran = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Gratulacje")
        font = pygame.font.SysFont('Arial', 50, bold=True)
        text = f"Gratulacje! Wygrał gracz {winner}"

        ekran.blit(self.champ_tlo, (0, 0))
        text_render = font.render(text, True, self.kolory['biały'])
        ekran.blit(text_render, (100, 250))

        pygame.mixer.music.load('champ_m.mp3')
        pygame.mixer.music.play()
        pygame.display.update()

    def ekran_koncowy(self, winner):
        ekran = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Koniec Gry")

        font = pygame.font.SysFont('Arial', 40, bold=True)
        small_font = pygame.font.SysFont('Arial', 30)

        rewanż_btn = pygame.Rect(250, 400, 130, 50)
        menu_btn = pygame.Rect(420, 400, 200, 50)

        pygame.mixer_music.load("champ_m.mp3")
        pygame.mixer_music.play()

        running = True
        while running:
            ekran.blit(self.champ_tlo, (0, 0))

            self.wyswietl_tekst(ekran, f"Gratulacje! Wygrał: {winner}", 150, 200, font, self.kolory["biały"])

            pygame.draw.rect(ekran, (0, 200, 0), rewanż_btn)
            pygame.draw.rect(ekran, (200, 0, 0), menu_btn)

            self.wyswietl_tekst(ekran, "Rewanż", rewanż_btn.x + 20, rewanż_btn.y + 10, small_font, self.kolory["biały"])
            self.wyswietl_tekst(ekran, "Powrót do menu", menu_btn.x + 10, menu_btn.y + 10, small_font,
                                self.kolory["biały"])

            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if rewanż_btn.collidepoint(event.pos):
                        self.zresetuj_gre()
                        self.uruchom_gry(auto_start=True)
                        return
                    elif menu_btn.collidepoint(event.pos):
                        self.uruchom_gry()
                        return

    def zresetuj_gre(self):
        self.pilka = Pilka(400, 300, 5, 5)
        self.mecz = Mecz()
        self.start_time = pygame.time.get_ticks()
        self.game_started = True
        self.gracz1.resetuj_pozycje(100, 500)
        self.gracz2.resetuj_pozycje(650, 500)

    def wyswietl_wyniki(self):
        ekran = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Tabela wyników")

        wyniki = self.wczytaj_wyniki()
        title_font = pygame.font.SysFont('Arial', 40, bold=True)
        text_font = pygame.font.SysFont('Arial', 25)

        running = True
        while running:
            ekran.fill((30, 30, 30))

            self.wyswietl_tekst(ekran, "Ostatnie wyniki", 250, 30, title_font, (255, 255, 255))

            for i, wynik in enumerate(wyniki):
                tekst = f"{i + 1}. {wynik['gracz1_nazwa']} [{wynik['wynik_gracza1']}] vs {wynik['gracz2_nazwa']} [{wynik['wynik_gracza2']}] - {wynik['czas_gry']}s"
                self.wyswietl_tekst(ekran, tekst, 50, 100 + i * 40, text_font, (255, 255, 255))

            self.wyswietl_tekst(ekran, "Wciśnij ESC  aby wrócić.", 250, 500, text_font, (200, 200, 200))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

    def wybierz_postac(self, gracz_nr):
        ekran = pygame.display.set_mode((800, 600))
        pygame.display.set_caption(f"Wybierz postać dla Gracza {gracz_nr}")
        font = pygame.font.SysFont('Arial', 30, bold=True)

        postacie = [
            {"plik": "lewy.jpg", "nazwa": "Lewandowski"},
            {"plik": "ronaldo.jpg", "nazwa": "Ronaldo"},
            {"plik": "mbappe.jpg", "nazwa": "Mbappe"},
            {"plik": "messi.jpg", "nazwa": "Messi"},
            {"plik": "vini.jpg", "nazwa": "Vinicius"},
            {"plik": "yamal.jpg", "nazwa": "Yamal"},
        ]

        clock = pygame.time.Clock()
        selected_index = 0
        running = True
        while running:
            ekran.fill((50, 50, 50))
            ekran.blit(self.menu_tlo, (0, 0))
            self.wyswietl_tekst(ekran, f"Gracz {gracz_nr}  wybiera postać:", 200, 50, font, (255, 255, 255))

            for i, postac in enumerate(postacie):
                x = 100 + (i % 3) * 220
                y = 200 + (i // 3) * 180
                kolor = (0, 255, 0) if i == selected_index else (255, 255, 255)
                obraz = pygame.image.load(postac['plik'])
                obraz = pygame.transform.scale(obraz, (100, 100))
                ekran.blit(obraz, (x, y))
                self.wyswietl_tekst(ekran, postac['nazwa'], x, y + 110, font, kolor)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.type == pygame.K_LEFT:
                        selected_index = (selected_index - 1) % len(postacie)
                    elif event.key == pygame.K_RIGHT:
                        selected_index = (selected_index + 1) % len(postacie)
                    elif event.key == pygame.K_RETURN:
                        return postacie[selected_index]['plik']

            clock.tick(30)
