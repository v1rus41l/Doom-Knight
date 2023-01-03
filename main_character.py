import os
import random
import sys

import pygame
from level_1 import  img_count


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Knight(pygame.sprite.Sprite):
    image = load_image("1.png")

    def __init__(self, *group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(*group)
        self.image = Knight.image
        self.rect = self.image.get_rect()

    def animation(self):
        global img_count
        if img_count == 6:
            img_count = 0
        screen