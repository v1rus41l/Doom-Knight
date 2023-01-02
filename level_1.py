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
    return image

    # if colorkey is not None:
    #     image = image.convert()
    #     if colorkey == -1:
    #         colorkey = image.get_at((0, 0))
    #     image.set_colorkey(colorkey)
    # else:
    #     image = image.convert_alpha()
    # return image

WIDTH, HEIGHT = 800, 600

FPS = 50

size = width, height = 500, 500
pygame.init()
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

player = None

# группы спрайтов
def main():
    pygame.init()
    size = width, height = 850, 450
    screen = pygame.display.set_mode(size)
    all_sprites = pygame.sprite.Group()
    arrow_image = load_image("1.png")
    arrow_image = pygame.transform.scale(arrow_image, (100, 100))
    cursor = pygame.sprite.Sprite(all_sprites)
    cursor.image = arrow_image
    cursor.rect = cursor.image.get_rect()
    fon = pygame.transform.scale(load_image('level1_fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                cursor.rect.x = cursor.rect.x + 10
            if pygame.key.get_pressed()[pygame.K_LEFT]:
                cursor.rect.x = cursor.rect.x - 10
            if pygame.key.get_pressed()[pygame.K_UP]:
                cursor.rect.y = cursor.rect.y - 10
            if pygame.key.get_pressed()[pygame.K_DOWN]:
                cursor.rect.y = cursor.rect.y + 10

        screen.blit(fon, (0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()
    pygame.quit()

if __name__ == '__main__':
    main()