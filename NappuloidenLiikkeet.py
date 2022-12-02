from HighlightedCells import HighlightedCellsRender
class Liikkeet:
    def __init__(self,näyttö,ruutuKoko) -> None:
        self.highlightedCellsRender = HighlightedCellsRender(näyttö,ruutuKoko)
        self.mahdolliset_paikat = []
        self.GREEN = (0, 128, 10, 100)
        self.sotilaan_syönti_pos = [[(-1, 1), (1, 1)],  # Sotilas 1 (Syö alas)
                                    [(-1, -1), (1, -1)]]  # Sotilas 2 (Syö ylös) -1, -1
        
    def Is_within_bounds(self, x, y):
        return x >= 0 and x < 8 and y >= 0 and y < 8

    # Tornin, Kuningattaren ja Lähetin liikkeet
    def TKL_Liikkeet(self,onkoBotti,NappulanNumero,vanhaPos,mahdollinenPos):
        if not NappulanNumero in [3, 4, 5]:
            return
        for suunta in range(1, 9):
            uusiSuunta = (vanhaPos[0]+mahdollinenPos[0]*suunta,vanhaPos[1]+mahdollinenPos[1] *suunta)
            if not self.Is_within_bounds(uusiSuunta[0], uusiSuunta[1]):
                break
            # Onko ruudukko tyhjä vai onko siinä musta tai valkoinen
            ruudunTilanne = self.Check_enmy_or_own(uusiSuunta[0], uusiSuunta[1])
            if ruudunTilanne == 0 or ruudunTilanne == 1:
                self.mahdolliset_paikat.append(uusiSuunta)
                if not onkoBotti:
                    self.highlightedCellsRender.LisääHighlightedRuutu(self.GREEN)
                if ruudunTilanne != 0:
                    break
            break

    #Sotilaan Liikkeet
    def S_Liikkeet(self,onkoBotti,NappulanNumero,vanhaPos,mahdollinenPos):
        if not NappulanNumero in [0, 1]:
            return    
        uusiSuunta = (vanhaPos[0]+mahdollinenPos[0], vanhaPos[1]+mahdollinenPos[1])
        # Normaali liikkumine eteen
        if self.Check_enmy_or_own(uusiSuunta[0],uusiSuunta[1]) == 0:
            self.mahdolliset_paikat.append(uusiSuunta)
            if not onkoBotti:
                self.highlightedCellsRender.LisääHighlightedRuutu(self.GREEN)
        # syönti paikat
        for suunta in self.sotilaan_syönti_pos[self.vuoro]:
            syönti = [vanhaPos[0]-suunta[0], vanhaPos[1]-suunta[1]]
            if not self.Is_within_bounds(syönti[0], syönti[1]):
                continue
            if self.Check_enmy_or_own(syönti[0], syönti[1]) == 1:
                self.mahdolliset_paikat.append((syönti[0], syönti[1]))
                if not onkoBotti:
                    self.highlightedCellsRender.LisääHighlightedRuutu(self.GREEN)

    #Kuninkaan ja Hevosen liikkeet
    def KH_Liikkeet(self,onkoBotti,NappulanNumero,vanhaPos,mahdollinenPos):
        if not NappulanNumero in [2, 6]:
            return
        uusiSuunta = (vanhaPos[0]+mahdollinenPos[0], vanhaPos[1]+mahdollinenPos[1])
        if self.Check_enmy_or_own(uusiSuunta[0],uusiSuunta[1]) in [0, 1]:
            self.mahdolliset_paikat.append(uusiSuunta)
            if not onkoBotti:
                self.highlightedCellsRender.LisääHighlightedRuutu(self.GREEN)
        