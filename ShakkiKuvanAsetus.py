import pygame
import os


class Kuvat(pygame.sprite.Sprite):
    def __init__(self, pos, size, kuva, näyttö):
        super().__init__()
        self.image = pygame.image.load(
            os.path.join("ShakkiKuvat", kuva)).convert_alpha()
        näyttö.blit(self.image, (size, size))
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect(topleft=pos)
