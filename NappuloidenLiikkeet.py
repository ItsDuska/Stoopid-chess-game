from HighlightedCells import HighlightedCellsRender


class Liikkeet:
    def __init__(self, näyttö, ruutuKoko) -> None:
        self.highlightedCellsRender = HighlightedCellsRender(näyttö, ruutuKoko)
        self.mahdolliset_paikat = []
        self.GREEN = (0, 128, 10, 100)
        self.sotilaan_syönti_pos = [[(-1, 1), (1, 1)],  # Sotilas 1 (Syö alas)
                                    [(-1, -1), (1, -1)]]  # Sotilas 2 (Syö ylös) -1, -1
        self.vihollinen = ["S", "K", "Q", "L", "T", "H"]
        self.oma = ["s", "k", "q", "l", "t", "h"]

    def Is_within_bounds(self, x, y):
        return x >= 0 and x < 8 and y >= 0 and y < 8

    def Check_enmy_or_own(self, nappula):
        if nappula in self.vihollinen[0]:
            return 1
        elif nappula in self.oma:
            return 2
        return 0

    # Tornin, Kuningattaren ja Lähetin liikkeet
    def TKL_Liikkeet(self, onkoBotti, nappulat, nappula, vanhaPos, mahdollinenPos, lauta, vuoro):
        print(nappulat[vuoro], nappula)
        print(mahdollinenPos)
        if not nappulat[vuoro][nappula] in [3, 4, 5]:
            return
        for suunta in range(1, 9):
            uusiSuunta = (vanhaPos[0]+mahdollinenPos[0] *
                          suunta, vanhaPos[1]+mahdollinenPos[1] * suunta)
            if not self.Is_within_bounds(uusiSuunta[0], uusiSuunta[1]):
                break
            # Onko ruudukko tyhjä vai onko siinä musta tai valkoinen
            ruudunTilanne = self.Check_enmy_or_own(
                lauta[uusiSuunta[0]][uusiSuunta[1]])
            if ruudunTilanne == 0 or ruudunTilanne == 1:
                self.mahdolliset_paikat.append(uusiSuunta)
                if not onkoBotti:
                    self.highlightedCellsRender.LisääHighlightedRuutu(
                        self.GREEN)
                if ruudunTilanne != 0:
                    break
            break

    # Sotilaan Liikkeet
    def S_Liikkeet(self, onkoBotti, nappulat, nappula, vanhaPos, mahdollinenPos, lauta, vuoro):
        if not nappulat[vuoro][nappula] in [0, 1]:
            return
        uusiSuunta = (vanhaPos[0]+mahdollinenPos[0],
                      vanhaPos[1]+mahdollinenPos[1])
        # Normaali liikkumine eteen
        if self.Check_enmy_or_own(lauta[uusiSuunta[0]][uusiSuunta[1]]) == 0:
            self.mahdolliset_paikat.append(uusiSuunta)
            if not onkoBotti:
                self.highlightedCellsRender.LisääHighlightedRuutu(self.GREEN)
        # syönti paikat
        for suunta in self.sotilaan_syönti_pos[vuoro]:
            syönti = [vanhaPos[0]-suunta[0], vanhaPos[1]-suunta[1]]
            if not self.Is_within_bounds(syönti[0], syönti[1]):
                continue
            if self.Check_enmy_or_own(lauta[syönti[0]][syönti[1]]) == 1:
                self.mahdolliset_paikat.append((syönti[0], syönti[1]))
                if not onkoBotti:
                    self.highlightedCellsRender.LisääHighlightedRuutu(
                        self.GREEN)

    # Kuninkaan ja Hevosen liikkeet
    def KH_Liikkeet(self, onkoBotti, nappulat, nappula, vanhaPos, mahdollinenPos, lauta, vuoro):
        if not nappulat[vuoro][nappula] in [2, 6]:
            return
        uusiSuunta = (vanhaPos[0]+mahdollinenPos[0],
                      vanhaPos[1]+mahdollinenPos[1])
        if self.Check_enmy_or_own(lauta[uusiSuunta[0]][uusiSuunta[1]]) in [0, 1]:
            self.mahdolliset_paikat.append(uusiSuunta)
            if not onkoBotti:
                self.highlightedCellsRender.LisääHighlightedRuutu(self.GREEN)

    def Check_liikkuminen(self, nappula, nappulat, x, y, xx, yy, onkoBotti, lauta, vuoro):
        self.TKL_Liikkeet(
            onkoBotti, nappulat, nappula, [x, y], [xx, yy], lauta, vuoro)
        self.S_Liikkeet(
            onkoBotti, nappulat, nappula, [x, y], [xx, yy], lauta, vuoro)
        self.KH_Liikkeet(
            onkoBotti, nappulat, nappula, [x, y], [xx, yy], lauta, vuoro)

    # nappula = nappulat[vuoro]
    def katsoJokaisenNappulanPaikat(self, lauta, nappulat, nappula, liikkeidenPos, vuoro):
        kaikkiPaikat = []

        for y in range(len(lauta)):
            for x in range(len(lauta)):
                if not lauta[y][x] in nappulat[vuoro]:
                    continue
                liikkeet = liikkeidenPos[nappulat[vuoro][lauta[y][x]]]
                for pos in liikkeet:
                    if not self.Is_within_bounds(x+pos[0], y+pos[1]):
                        continue
                    self.Check_liikkuminen(
                        lauta[y][x], nappula, x, y, pos[0], pos[1], True, lauta, vuoro)
                    if len(self.mahdolliset_paikat) != 0:
                        kaikkiPaikat.append([(x, y)])
                        kaikkiPaikat.append(
                            self.mahdolliset_paikat)
                    self.mahdolliset_paikat = []
                    # Eka siirto on index 1 ja seuraava 3 eli kerrot kahdella. index 0 ja 2... on alkuperänen nappula cords
        return kaikkiPaikat
