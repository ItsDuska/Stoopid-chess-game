#Tänne se uus class
import pygame

class HighlightedCellsRender:
    def __init__(self,näyttö,ruutuKoko) -> None:
        self.laatikot = []
        self.näyttö = näyttö
        self.ruutuKoko = ruutuKoko
        self.valitunNappulanLaatikko = pygame.Surface(
            self.näyttö.get_size(), pygame.SRCALPHA)

    def LisääHighlightedRuutu(self, väri):
        surface = pygame.Surface(self.näyttö.get_size(), pygame.SRCALPHA)
        pygame.draw.rect(surface, väri, (0, 0, self.ruutuKoko, self.ruutuKoko))
        self.laatikot.append(surface)

    def HighlightRuudut(self, klikattu,pos, mahdollisetPaikat):
        if not klikattu:
            return
        pygame.draw.rect(self.valitunNappulanLaatikko, (255, 255,
                         153, 128), (0, 0, self.ruutuKoko, self.ruutuKoko))
        self.näyttö.blit(self.valitunNappulanLaatikko,
                         (pos[0]*self.ruutuKoko, pos[1]*self.ruutuKoko))
        for index, ruutu in enumerate(mahdollisetPaikat):
            self.näyttö.blit(
                self.laatikot[index], (ruutu[0]*self.ruutuKoko, ruutu[1]*self.ruutuKoko))