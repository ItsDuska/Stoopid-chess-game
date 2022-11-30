import pygame
import os
from ShakkiKuvanAsetus import Kuvat
from MinMax import MinMaxNuts
pygame.font.init()


class Lauta():
    def __init__(self, näyttö):
        self.liikkeet_pos = [
            [(0, 1)],  # sotilas 1 (Liikkuu alas)
            [(0, -1)],  # sotilas 2 (Liikkuu ylös)
            [(0, -1), (-1, -1), (-1, 0), (-1, 1),
             (0, 1), (1, 1), (1, 0), (1, -1)],  # kunkku
            [(0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1),
             (1, 1), (1, 0), (1, -1)],  # kuningatar
            [(-1, -1), (-1, 1), (1, 1), (1, -1)],  # lähetti
            [(0, -1), (-1, 0), (0, 1), (1, 0)],  # torni
            [(-1, 2), (1, 2), (1, -2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]]  # hevonen

        self.vuoro = 0  # 0 = alaspäin    1 = ylöspäin
        self.vihollinen = ["S", "K", "Q", "L", "T", "H"]
        self.oma = ["s", "k", "q", "l", "t", "h"]
        self.nappulat = [{"s": 1, "k": 2, "q": 3, "l": 4, "t": 5, "h": 6}, {
            "S": 0, "K": 2, "Q": 3, "L": 4, "T": 5, "H": 6}]
        self.sotilaan_syönti_pos = [[(-1, 1), (1, 1)],  # Sotilas 1 (Syö alas)
                                    [(-1, -1), (1, -1)]]  # Sotilas 2 (Syö ylös) -1, -1
        self.kuvat = {"q": "ValkoinenKuningatar.png", "Q": "MustaKuningatar.png", "s": "ValkoinenSotilas.png", "S": "MustaSotilas.png",
                      "k": "ValkoinenKunkku.png", "K": "MustaKunkku.png", "l": "ValkoinenLahetti.png", "L": "MustaLahetti.png", "t": "ValkoinenTorni.png",
                      "T": "MustaTorni.png", "h": "ValkoinenHevonen.png", "H": "MustaHevonen.png"}
        self.näytönKoko = näyttö.get_size()
        self.GREEN = (0, 128, 10, 100)
        self.klikattu = False
        self.varmistus = False
        self.näyttö = näyttö
        self.ruutuKoko = int(self.näytönKoko[0]/8)
        self.lauta = self.Luo_lauta()
        self.laatikot = []
        self.Päivitä_lauta()
        self.fontti = pygame.font.SysFont('Arial', 100)
        self.tausta = pygame.image.load(
            os.path.join("ShakkiKuvat", "ShakkiLauta.png")).convert_alpha()
        self.tausta = pygame.transform.scale(self.tausta,self.näytönKoko)
        #
        #
        self.onBotti = False
        #
        #
        self.minMax = MinMaxNuts(self.lauta)

    def Luo_lauta(self):
        # Isolla on musta
        # Pienellä valkoinen
        lauta = [
            ["T", "H", "L", "Q", "K", "L", "H", "T"],
            ["S", "S", "S", "S", "S", "S", "S", "S"],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            ["s", "s", "s", "s", "s", "s", "s", "s"],
            ["t", "h", "l", "q", "k", "l", "h", "t"]
        ]
        return lauta

    def Päivitä_lauta(self):
        self.nappulaSprites = pygame.sprite.Group()
        for row_index, row in enumerate(self.lauta):
            for col_index, cell in enumerate(row):
                if cell != " ":
                    x = col_index * self.ruutuKoko
                    y = row_index * self.ruutuKoko
                    if cell in self.kuvat:
                        self.Lisää_kuva(x, y, self.kuvat[cell], self.näyttö)

    def Lisää_kuva(self, x, y, kuva, näyttö):
        self.nappulaKuva = Kuvat((x, y), self.ruutuKoko, kuva, näyttö)
        self.nappulaSprites.add(self.nappulaKuva)

    def renderNappulaOnHiiri(self):
        if not self.klikattu:
            return
        pos = pygame.mouse.get_pos()
        self.näyttö.blit(self.HiiriKuva, (pos[0]-int(self.ruutuKoko/2), pos[1]-int(self.ruutuKoko/2)))

    def Lisää_surface(self, väri):
        surface = pygame.Surface(self.näytönKoko, pygame.SRCALPHA)
        pygame.draw.rect(surface, väri, (0, 0, self.ruutuKoko, self.ruutuKoko))
        self.laatikot.append(surface)

    def HighlightRuudut(self):
        if not self.klikattu:
            return
        self.näyttö.blit(self.omaLaatikko, (self.xx*self.ruutuKoko, self.yy*self.ruutuKoko))
        for ruutu in range(len(self.mahdolliset_paikat)):
            self.näyttö.blit(
                self.laatikot[ruutu], (self.mahdolliset_paikat[ruutu][0]*self.ruutuKoko, 
                self.mahdolliset_paikat[ruutu][1]*self.ruutuKoko))

    def Pyöritä_kaikki(self):
        self.näyttö.blit(self.tausta, (0, 0))
        self.nappulaSprites.draw(self.näyttö)
        self.HighlightRuudut()
        self.Check_winning()
        self.BottiKämä()
        self.renderNappulaOnHiiri()

    def Is_within_bounds(self, x, y):
        return x >= 0 and x < 8 and y >= 0 and y < 8

    def Click(self, x, y):
        self.mahdolliset_paikat = []
        self.xx, self.yy = x // self.ruutuKoko, y // self.ruutuKoko
        self.nappula = self.GetNappula(self.xx, self.yy)
        if not self.nappula in self.nappulat[self.vuoro]:
            return
        # tämä on esim self.liikket_pos[3] tai mikä muu listan osa
        liikkeet = self.liikkeet_pos[self.nappulat[self.vuoro][self.nappula]]
        # onko laudalla ja lisää ne listaan jotka on
        for pos in liikkeet:
            if not self.Is_within_bounds(self.xx+pos[0], self.yy+pos[1]):
                continue
            self.omaLaatikko = pygame.Surface(self.näytönKoko, pygame.SRCALPHA)
            pygame.draw.rect(self.omaLaatikko,
                             (255, 255, 153, 128), (0, 0, self.ruutuKoko, self.ruutuKoko))
            self.Check_liikkuminen(
                self.nappula, self.nappulat[self.vuoro], self.xx, self.yy, pos[0], pos[1], False)
        self.klikattu = True
        self.lauta[self.yy][self.xx] = " "
        self.Päivitä_lauta()
        self.HiiriKuva = pygame.image.load(
            os.path.join("ShakkiKuvat", self.kuvat[self.nappula])).convert_alpha()
        self.HiiriKuva = pygame.transform.scale(self.HiiriKuva,(self.ruutuKoko,self.ruutuKoko))
        print(self.vihollinen)

    def Check_winning(self):
        if self.klikattu:
            return
        kunkku = "k" if self.vuoro == 0 else "K"
        for nappula in self.lauta:
            if kunkku in nappula:
                return
        teksti = "Pelaaja 1 voitti!" if kunkku == "k" else "Pelaaja 2 Voitti!"
        self.tekstijuttu = self.fontti.render(teksti, 1, (20, 150, 20))
        self.näyttö.blit(self.tekstijuttu, (50, 340))

    def Check_enmy_or_own(self, x, y):
        if self.lauta[y][x] in self.vihollinen:
            return 1
        elif self.lauta[y][x] in self.oma:
            return 2
        return 0

    # xx ja yy on klikatun nappulan cordinaatti
    def Check_liikkuminen(self, nappula, nappulat, x, y, xx, yy, onkoBotti):
        # Torni, kuningatar, lähetti
        if nappulat[nappula] in [3, 4, 5]:
            for suunta in range(1, 9):
                newX, newY = x+xx*suunta, y+yy*suunta
                if not self.Is_within_bounds(newX, newY):
                    break
                # Onko ruudukko tyhjä vai onko siinä musta tai valkoinen
                ruudunTilanne = self.Check_enmy_or_own(newX, newY)
                if ruudunTilanne == 0 or ruudunTilanne == 1:
                    self.mahdolliset_paikat.append((newX, newY))
                    if not onkoBotti:
                        self.Lisää_surface(self.GREEN)
                    if ruudunTilanne == 1:
                        break
                else:
                    break
        # sotilas
        elif nappulat[nappula] in [0, 1]:
            if self.Check_enmy_or_own(x+xx, y+yy) == 0:
                self.mahdolliset_paikat.append((x+xx, y+yy))
                if not onkoBotti:
                    self.Lisää_surface(self.GREEN)
            # syönti paikat
            for suunta in self.sotilaan_syönti_pos[self.vuoro]:
                print(suunta)
                syönti = [x-suunta[0], y-suunta[1]]
                print(syönti)
                if not self.Is_within_bounds(syönti[0], syönti[1]):
                    continue
                if self.Check_enmy_or_own(syönti[0], syönti[1]) == 1:
                    self.mahdolliset_paikat.append((syönti[0], syönti[1]))
                    if not onkoBotti:
                        self.Lisää_surface(self.GREEN)
        # kunkku + hevonen
        elif nappulat[nappula] in [2, 6]:
            if self.Check_enmy_or_own(x+xx, y+yy) in [0, 1]:
                self.mahdolliset_paikat.append((x+xx, y+yy))
                if not onkoBotti:
                    self.Lisää_surface(self.GREEN)

    def GetNappula(self, x, y):
        return self.lauta[y][x]

    def Syö(self, x, y):
        xx, yy = x // self.ruutuKoko, y // self.ruutuKoko
        self.klikattu = False
        if (xx, yy) in self.mahdolliset_paikat:
            self.laitaNappula(xx, yy)
        else:
            self.lauta[self.yy][self.xx] = self.nappula
            self.Päivitä_lauta()

    def laitaNappula(self, x, y):
        self.laatikot = []
        self.lauta[y][x] = self.nappula
        self.lauta[self.yy][self.xx] = " "
        self.mahdolliset_paikat.clear()
        self.Päivitä_lauta()
        self.vuoro = 0 if self.vuoro == 1 else 1
        print(self.vuoro)
        self.vihollinen = ["s", "k", "q", "l", "t", "h"] if self.vuoro == 1 else [
            ["S", "K", "Q", "L", "T", "H"]]
        self.oma = ["S", "K", "Q", "L", "T", "H"] if self.vuoro == 1 else [
            "s", "k", "q", "l", "t", "h"]

    def katsoJokaisenNappulanPaikat(self):
        kaikkiPaikat = []
        for y in range(len(self.lauta)):
            for x in range(len(self.lauta)):
                if not self.lauta[y][x] in self.nappulat[self.vuoro]:
                    continue
                liikkeet = self.liikkeet_pos[self.nappulat[self.vuoro]
                                             [self.lauta[y][x]]]
                for pos in liikkeet:
                    if not self.Is_within_bounds(x+pos[0], y+pos[1]):
                        continue
                    self.Check_liikkuminen(
                        self.lauta[y][x], self.nappulat[self.vuoro], x, y, pos[0], pos[1], True)
                    if len(self.mahdolliset_paikat) != 0:
                        kaikkiPaikat.extend(self.mahdolliset_paikat)
                    self.mahdolliset_paikat = []
                    # extend
        print(kaikkiPaikat)
        return kaikkiPaikat

    def BottiKämä(self):
        if not (self.vuoro == 1 and self.onBotti):
            return
        kaikkiPaikat = self.katsoJokaisenNappulanPaikat()

        self.minMax.update(self.lauta, kaikkiPaikat)
        point = self.minMax.minimax(
            0, 0, True, self.minMax.getValueList(), self.minMax.MIN, self.minMax.MAX)

        print(point, self.minMax.index)

        self.nappula = self.GetNappula(
            kaikkiPaikat[self.minMax.index][1], kaikkiPaikat[self.minMax.index][0])
        self.laitaNappula(
            kaikkiPaikat[self.minMax.index][0], kaikkiPaikat[self.minMax.index][1])