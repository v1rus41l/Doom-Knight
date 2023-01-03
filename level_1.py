import os
import sys

import pygame


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image

WIDTH, HEIGHT = 800, 600

knight_img = [pygame.image.load('data/3.png'),
              pygame.image.load('data/4.png'), pygame.image.load('data/5.png'), pygame.image.load('data/6.png'),
              pygame.image.load('data/5.png'), pygame.image.load('data/4.png')]
img_count = 0

FPS = 50

size = width, height = 500, 500
pygame.init()
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

player = None

class Knight(pygame.sprite.Sprite):
    image = load_image("1.png")

    def __init__(self, *group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(*group)
        self.image = Knight.image
        self.rect = self.image.get_rect()
        self.rect.x = 800
        self.rect.y = 50

    def staying(self, vector):
        if vector:
            screen.blit(pygame.image.load('data/1.png'), (self.rect.x, self.rect.y))
        else:
            screen.blit(pygame.transform.flip(pygame.image.load('data/1.png'), True, False), (self.rect.x, self.rect.y))

    def animation(self, vector):
        global img_count
        if img_count == 30:
            img_count = 0
        if vector:
            screen.blit(knight_img[img_count // 5], (self.rect.x, self.rect.y))
        else:
            screen.blit(pygame.transform.flip(knight_img[img_count // 5], True, False), (self.rect.x, self.rect.y))
        img_count += 1
        clock.tick(80)

    def jumping(self):
        self.rect.y -= 5 * clock.tick(60)
        self.rect.y += 15 * clock.tick(60)




# группы спрайтов
def main():
    pygame.init()
    size = width, height = 850, 450
    screen = pygame.display.set_mode(size)
    all_sprites = pygame.sprite.Group()
    knight = Knight()
    arrow_image = load_image("1.png")
    arrow_image = pygame.transform.scale(arrow_image, (100, 100))
    cursor = pygame.sprite.Sprite(all_sprites)
    cursor.image = arrow_image
    cursor.rect = cursor.image.get_rect()
    fon = pygame.transform.scale(load_image('level1_fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    running = True
    vector = False
    while running:
        action = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.blit(fon, (0, 0))
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            knight.rect.x += 2
            vector = True
            Knight.animation(knight, vector)
            action = True
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            knight.rect.x -= 2
            vector = False
            Knight.animation(knight, vector)
            action = True
        if pygame.key.get_pressed()[pygame.K_UP]:
            Knight.jumping(knight)
        if not action:
            Knight.staying(knight, vector)
        # screen.blit(pygame.image.load('data/1.png'), (0, 0))
        # all_sprites.draw(screen)
        pygame.display.flip()
    pygame.quit()

if __name__ == '__main__':
    main()