import pygame
import os
from MinMax import MinMaxNuts
from Render import Render
from NappuloidenLiikkeet import Liikkeet
pygame.font.init()


class Lauta():
    def __init__(self, näyttö):
        self.mahdolliset_paikat = []
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
        self.vuoro = 0  # 0 = valkone    1 = musta
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
        self.vanhaX, self.vanhaY = 0, 0
        self.onBotti = True
        self.klikattu = False
        self.näyttö = näyttö
        self.ruutuKoko = int(self.näytönKoko[0]/8)
        self.lauta = self.Luo_lauta()
        self.liikkeet = Liikkeet(self.näyttö,self.ruutuKoko)
        self.nappulaSprites = pygame.sprite.Group()

        self.render = Render(self.näyttö, self.ruutuKoko)
        self.minMax = MinMaxNuts()

        self.HiiriKuva = None
        self.Päivitä_lauta()
        self.fontti = pygame.font.SysFont('Arial', 100)

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
        self.nappulaSprites.empty()
        for row_index, row in enumerate(self.lauta):
            for col_index, cell in enumerate(row):
                if cell != " ":
                    x = col_index * self.ruutuKoko
                    y = row_index * self.ruutuKoko
                    if cell in self.kuvat:
                        self.render.Lisää_kuva(
                            x, y, self.kuvat[cell], self.nappulaSprites)

    def Pyöritä_kaikki(self):
        self.Check_winning()
        self.BottiKämä()
        self.render.drawBG()
        self.render.h.HighlightRuudut(
            self.klikattu, self.vanhaX, self.vanhaY, self.mahdolliset_paikat)
        self.render.renderNappulaOnHiiri(self.klikattu)
        self.nappulaSprites.draw(self.näyttö)

    def Click(self, x, y):
        self.mahdolliset_paikat = []
        self.vanhaX, self.vanhaY = x // self.ruutuKoko, y // self.ruutuKoko
        self.nappula = self.GetNappula(self.vanhaX, self.vanhaY)
        if not self.nappula in self.nappulat[self.vuoro]:
            return
        self.render.update(self.kuvat[self.nappula])
        # tämä on esim self.liikket_pos[3] tai mikä muu listan osa
        liikkeet = self.liikkeet_pos[self.nappulat[self.vuoro][self.nappula]]
        # onko laudalla ja lisää ne listaan jotka on
        for pos in liikkeet:
            if not self.Is_within_bounds(self.vanhaX+pos[0], self.vanhaY+pos[1]):
                continue
            self.Check_liikkuminen(
                self.nappula, self.nappulat[self.vuoro], self.vanhaX, self.vanhaY, pos[0], pos[1], False)
        self.klikattu = True
        self.lauta[self.vanhaY][self.vanhaX] = " "
        self.Päivitä_lauta()

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
        if self.lauta[y][x] in self.vihollinen[0]:
            return 1
        if self.lauta[y][x] in self.oma:
            return 2
        return 0

    def GetNappula(self, x, y):
        return self.lauta[y][x]

    def Syö(self, x, y):
        xx, yy = x // self.ruutuKoko, y // self.ruutuKoko
        self.klikattu = False
        if (xx, yy) in self.mahdolliset_paikat:
            self.laitaNappula(xx, yy, self.vanhaX, self.vanhaY)
        else:
            self.lauta[self.vanhaY][self.vanhaX] = self.nappula
            self.Päivitä_lauta()

    def laitaNappula(self, uusiX, uusiY, vanhaX, VanhaY):
        self.liikkeet.highlightCells.laatikot = []
        self.lauta[uusiY][uusiX] = self.nappula
        self.lauta[VanhaY][vanhaX] = " "
        self.mahdolliset_paikat.clear()
        self.Päivitä_lauta()
        self.vuoro = 0 if self.vuoro == 1 else 1
        # print(self.vuoro)
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
                        kaikkiPaikat.append([(x, y)])
                        kaikkiPaikat.append(
                            self.mahdolliset_paikat)
                    self.mahdolliset_paikat = []
        return kaikkiPaikat  # Eka siirto on index 1 ja seuraava 3 eli kerrot kahdella. index 0 ja 2... on alkuperänen nappula cords

    def BottiKämä(self):
        if not (self.vuoro == 1 and self.onBotti):
            # if not (self.onBotti):
            return
        kaikkiPaikat = self.katsoJokaisenNappulanPaikat()
        point = self.minMax.minimax(
            2, 0, True, self.minMax.getValueList(self.lauta, kaikkiPaikat), self.minMax.MIN, self.minMax.MAX)
        #print(point)
        self.nappula = self.GetNappula(
            kaikkiPaikat[self.minMax.index-1][0][0], kaikkiPaikat[self.minMax.index-1][0][1])
        print(self.minMax.index)
        self.laitaNappula(
            kaikkiPaikat[self.minMax.index][0][0], kaikkiPaikat[self.minMax.index][0][1], kaikkiPaikat[self.minMax.index-1][0][0], kaikkiPaikat[self.minMax.index-1][0][1])
