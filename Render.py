import pygame
import os
from ShakkiKuvanAsetus import Kuvat


class Render:
    def __init__(self, näyttö, ruutuKoko) -> None:
        self.näyttö = näyttö
        self.ruutuKoko = ruutuKoko
        self.tausta = pygame.image.load(os.path.join(
            "ShakkiKuvat", "ShakkiLauta.png")).convert_alpha()
        self.tausta = pygame.transform.scale(
            self.tausta, self.näyttö.get_size())

    def update(self, kuva):
        self.kuva = pygame.image.load(
            os.path.join("ShakkiKuvat", kuva)).convert_alpha()
        self.kuva = pygame.transform.scale(
            self.kuva, (self.ruutuKoko, self.ruutuKoko))

    def Lisää_kuva(self, x, y, kuva, sprites):
        nappulaKuva = Kuvat((x, y), self.ruutuKoko, kuva, self.näyttö)
        sprites.add(nappulaKuva)

    def renderNappulaOnHiiri(self, klikattu):
        if not klikattu:
            return
        pos = pygame.mouse.get_pos()
        self.näyttö.blit(
            self.kuva, (pos[0]-int(self.ruutuKoko/2), pos[1]-int(self.ruutuKoko/2)))

    def drawBG(self):
        self.näyttö.blit(self.tausta, (0, 0))
