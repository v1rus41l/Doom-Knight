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
jump_count = 10
is_jump = False
check_of_fall = True
check_of_fall_2 = True
check_of_fall_3 = True


# FPS = 50

size = width, height = 500, 500
pygame.init()
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
falling = False
all_sprites = pygame.sprite.Group()

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
        global img_count, is_jump
        if img_count == 30:
            img_count = 0
        if not is_jump:
            if vector:
                screen.blit(knight_img[img_count // 5], (self.rect.x, self.rect.y))
            else:
                screen.blit(pygame.transform.flip(knight_img[img_count // 5], True, False), (self.rect.x, self.rect.y))
        img_count += 1
        clock.tick(60)

    def jumping(self, vector):
        global jump_count, is_jump
        if vector:
            screen.blit(pygame.image.load('data/2.png'), (self.rect.x, self.rect.y))
        else:
            screen.blit(pygame.transform.flip(pygame.image.load('data/2.png'), True, False), (self.rect.x, self.rect.y))
        if jump_count >= -10:
            self.rect.y -= jump_count
            jump_count -= 1
            clock.tick(60)
        else:
            jump_count = 10
            clock.tick(60)
            is_jump = False


        # print(jump_count)
        # if not is_jump:
        #     jump_count -= 1
        #     self.rect.y += 10
        #     clock.tick(30)
        #     print(11)
        #     if jump_count == 0:
        #         is_jump = True
        # if is_jump:
        #     jump_count += 1
        #     self.rect.y -= 10
        #     clock.tick(30)
        #     if jump_count == 2:
        #         print(1)
        #         is_jump = False



action = False

class Ball(pygame.sprite.Sprite):
    def __init__(self, radius, x, y):
        super().__init__(all_sprites)
        self.radius = radius
        self.image = pygame.Surface((2 * radius, 2 * radius),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("red"),
                           (radius, radius), radius)
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)


# группы спрайтов
def main():
    global is_jump, action, check_of_fall, check_of_fall_2, check_of_fall_3, falling
    pygame.init()
    size = width, height = 850, 450
    screen = pygame.display.set_mode(size)
    all_sprites = pygame.sprite.Group()
    knight = Knight()
    fon = pygame.transform.scale(load_image('level1_fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    running = True
    vector = False
    Ball(10, 50, 50)
    while running:
        action = False
        screen.blit(fon, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if ((knight.rect.x < 125 and knight.rect.y != 170) or (knight.rect.x < 255 and knight.rect.y != 170 and 50 < knight.rect.y < 170)) and check_of_fall and knight.rect.y >= 50:
            knight.rect.y += 10
            clock.tick(60)
            falling = True
        if knight.rect.y == 170:
            check_of_fall = False
            falling = False
        if ((knight.rect.x > 690 and knight.rect.y > 50 and knight.rect.y != 290) or (knight.rect.x > 600 and knight.rect.y > 50 and knight.rect.y != 290 and 170 < knight.rect.y < 290)) and check_of_fall_2 and knight.rect.y >= 170:
            knight.rect.y += 10
            clock.tick(60)
            falling = True
        if knight.rect.y == 290:
            check_of_fall_2 = False
            falling = False
            knight.rect.y -= 5
        if ((knight.rect.x < 130 and knight.rect.y != 405 and 285 <= knight.rect.y) or (knight.rect.x < 200 and knight.rect.y != 405 and 285 <= knight.rect.y and 285 < knight.rect.y < 405)) and check_of_fall_3 and knight.rect.y >= 285:
            knight.rect.y += 10
            clock.tick(60)
            falling = True
        if knight.rect.y == 405:
            check_of_fall_3 = False
            falling = False
            knight.rect.y -= 5
        if pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_LEFT]:
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                if knight.rect.x <= 800:
                    knight.rect.x += 3
                    vector = True
                    Knight.animation(knight, vector)
                    action = True
            if pygame.key.get_pressed()[pygame.K_LEFT]:
                if knight.rect.x >= 0:
                    knight.rect.x -= 3
                    vector = False
                    Knight.animation(knight, vector)
                    action = True
        if pygame.key.get_pressed()[pygame.K_UP] and not falling:
            is_jump = True
        if is_jump:
            Knight.jumping(knight, vector)
        if not action and not is_jump:
            Knight.staying(knight, vector)
        all_sprites.draw(screen)
        pygame.display.flip()
    pygame.quit()

if __name__ == '__main__':
    main()