import pygame
import os
from ShakkiKuvanAsetus import Kuvat


class Render:
    def __init__(self, näyttö, ruutuKoko) -> None:
        self.näyttö = näyttö
        self.ruutuKoko = ruutuKoko
        self.laatikot = []
        self.valitunNappulanLaatikko = pygame.Surface(
            self.näyttö.get_size(), pygame.SRCALPHA)
        self.tausta = pygame.image.load(
            os.path.join("ShakkiKuvat", "ShakkiLauta.png")).convert_alpha()
        self.tausta = pygame.transform.scale(self.tausta, self.näytönKoko)

    def update(self, kuva):
        self.kuva = pygame.image.load(
            os.path.join("ShakkiKuvat", kuva)).convert_alpha()
        self.kuva = pygame.transform.scale(
            self.kuva, (self.ruutuKoko, self.ruutuKoko))
        # Laattikko lista tähä eli se jossa on highlited alueet

    def Lisää_kuva(self, x, y, kuva, sprites):
        nappulaKuva = Kuvat((x, y), self.ruutuKoko, kuva, self.näyttö)
        sprites.add(nappulaKuva)

    def renderNappulaOnHiiri(self, klikattu):
        if not klikattu:
            return
        pos = pygame.mouse.get_pos()
        self.näyttö.blit(
            self.kuva, (pos[0]-int(self.ruutuKoko/2), pos[1]-int(self.ruutuKoko/2)))

    def LisääHighlightedRuutu(self, väri):
        surface = pygame.Surface(self.näyttö.get_size(), pygame.SRCALPHA)
        pygame.draw.rect(surface, väri, (0, 0, self.ruutuKoko, self.ruutuKoko))
        self.laatikot.append(surface)

    def HighlightRuudut(self, klikattu,  x, y, mahdollisetPaikat):
        if not klikattu:
            return
        pygame.draw.rect(self.valitunNappulanLaatikko,
                         (255, 255, 153, 128), (0, 0, self.ruutuKoko, self.ruutuKoko))
        self.näyttö.blit(self.valitunNappulanLaatikko,
                         (x*self.ruutuKoko, y*self.ruutuKoko))
        for index, ruutu in enumerate(mahdollisetPaikat):
            self.näyttö.blit(
                self.laatikot[index], (ruutu[0]*self.ruutuKoko,
                                       ruutu[1]*self.ruutuKoko))

    def drawBG(self):
        self.näyttö.blit(self.tausta, (0, 0))
