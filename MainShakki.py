import pygame
from Shakki_moottori import Lauta

näytönKoko = (600, 600)
pygame.init()
näyttö = pygame.display.set_mode(näytönKoko)
clock = pygame.time.Clock()
lauta = Lauta(näyttö)
päällä = True

# mainloop
while päällä:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            päällä = False
        if event.type == pygame.KEYDOWN:
            # Reset
            if event.key == pygame.K_ESCAPE:
                lauta.lauta = lauta.Luo_lauta()
                lauta.Päivitä_lauta()
                lauta.vuoro = 0
        if event.type == pygame.MOUSEBUTTONDOWN:
            # check for the left mouse button
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if not lauta.klikattu:
                    lauta.Click(pos)
                else:
                    lauta.Syö(pos)

    lauta.Pyöritä_kaikki()
    pygame.display.update()  # update display

    # TO DO

    # -AI botille (Käy läpi jokaisen mahdollisen liikkeen ja vetää niistä randomilla yhe (voi olla että yrittää ottaa parheiden joukosta yhden.))
