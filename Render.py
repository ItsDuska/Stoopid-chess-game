import pygame
from ShakkiKuvanAsetus import Kuvat

class Render:
    def __init__(self,näyttö,ruutuKoko) -> None:
        self.näyttö = näyttö
        self.ruutuKoko = ruutuKoko
        self.laatikot = []
        #Laattikko lista tähä eli se jossa on highlited alueet
        
    def Lisää_kuva(self,x, y, kuva,sprites):
        nappulaKuva = Kuvat((x, y), self.ruutuKoko, kuva, self.näyttö)
        sprites.add(nappulaKuva)

    def renderNappulaOnHiiri(self,klikattu,kuva):
        if not klikattu or kuva == None:
            return
        pos = pygame.mouse.get_pos()
        self.näyttö.blit(
            kuva,(pos[0]-int(self.ruutuKoko/2), pos[1]-int(self.ruutuKoko/2)))
       
    def LisääHighlightedRuutu(self,väri):
        surface = pygame.Surface(self.näyttö.get_size(), pygame.SRCALPHA)
        pygame.draw.rect(surface, väri, (0, 0, self.ruutuKoko, self.ruutuKoko))
        self.laatikot.append(surface)
    
    def HighlightRuudut(self,klikattu,valitunNappulanLaatikko,x,y,mahdollisetPaikat,):
        if not klikattu:
            return
        self.näyttö.blit(valitunNappulanLaatikko,
                         (x*self.ruutuKoko, y*self.ruutuKoko))
        for index,ruutu in enumerate(mahdollisetPaikat):
            self.näyttö.blit(
                self.laatikot[index], (ruutu[0]*self.ruutuKoko,
                                       ruutu[1]*self.ruutuKoko))
