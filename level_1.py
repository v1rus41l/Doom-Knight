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

WIDTH, HEIGHT = 850, 450

knight_img = [pygame.image.load('data/3.png'),
              pygame.image.load('data/4.png'), pygame.image.load('data/5.png'), pygame.image.load('data/6.png'),
              pygame.image.load('data/5.png'), pygame.image.load('data/4.png')]
skeleton_img = [pygame.image.load('data/skeleton1.png'), pygame.image.load('data/skeleton2.png')]
woodcutter_image = [pygame.image.load('data/woodcutter1.png'), pygame.image.load('data/woodcutter2.png'),
                    pygame.image.load('data/woodcutter3.png'), pygame.image.load('data/woodcutter2.png'),
                    pygame.image.load('data/woodcutter1.png')]

img_count = 0
jump_count = 10
is_jump = False
check_of_fall1 = True
check_of_fall_12 = True
check_of_fall_13 = True
check_of_fall2 = True
check_of_fall_22 = True
check_of_fall_23 = True
skeleton_count = 10
size = width, height = 500, 500
pygame.init()
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
falling = False
all_sprites = pygame.sprite.Group()
skeleton_group = pygame.sprite.Group()
action = False
player = None
running = True
score = 0
vector = False
jump_count_wc = 10
woodcutter_count = 10



class Knight(pygame.sprite.Sprite):
    image = load_image("1.png")

    def __init__(self, x, y, *group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(*group)
        self.image = Knight.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)

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
        clock.tick(150)

    def jumping(self, vector):
        global jump_count, is_jump
        if vector:
            screen.blit(pygame.image.load('data/2.png'), (self.rect.x, self.rect.y))
        else:
            screen.blit(pygame.transform.flip(pygame.image.load('data/2.png'), True, False), (self.rect.x, self.rect.y))
        if jump_count >= -10:
            self.rect.y -= jump_count
            jump_count -= 1
            clock.tick(70)
        else:
            jump_count = 10
            clock.tick(70)
            is_jump = False




class Ball(pygame.sprite.Sprite):
    def __init__(self, radius, x, y):
        super().__init__(all_sprites)
        self.radius = radius
        self.image = pygame.Surface((2 * radius, 2 * radius),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("white"),
                           (radius, radius), radius)
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, knight):
        global score
        if pygame.sprite.collide_mask(self, knight):
            self.kill()
            score += 10


class Skeleton(pygame.sprite.Sprite):
    global action
    image = load_image("skeleton1.png")

    def __init__(self, x1, x2, pos_x, pos_y):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(skeleton_group)
        self.image = Skeleton.image
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.x1 = x1
        self.x2 = x2
        self.check = True
        self.mask = pygame.mask.from_surface(self.image)
        self.clock = pygame.time.Clock()
        self.vector = False


    def update(self, knight):
        global running
        if pygame.sprite.collide_mask(self, knight):
            running = False


    def running(self):
        global action
        if self.rect.x >= self.x2:
            self.check = True
            self.vector = False
        if self.rect.x <= self.x1:
            self.check = False
            self.vector = True
        if self.check:
            if action:
                self.rect.x -= 2
            else:
                self.rect.x -= 1
        else:
            if action:
                self.rect.x += 2
            else:
                self.rect.x += 1
        clock.tick(150)

    def animation(self):
        global skeleton_count, skeleton_img
        if skeleton_count == 30:
            skeleton_count = 0
        if self.vector:
            screen.blit(skeleton_img[skeleton_count // 15], (self.rect.x, self.rect.y))
        else:
            screen.blit(pygame.transform.flip(skeleton_img[skeleton_count // 15], True, False), (self.rect.x, self.rect.y))
        skeleton_count += 1
        clock.tick(150)



class WoodCutter(pygame.sprite.Sprite):
    global action
    image = load_image("woodcutter1.png")

    def __init__(self, x1, x2, pos_x, pos_y):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(skeleton_group)
        self.image = Skeleton.image
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.x1 = x1
        self.x2 = x2
        self.check = True
        self.count = 0
        self.checking_jump = True
        self.mask = pygame.mask.from_surface(self.image)
        self.clock = pygame.time.Clock()
        self.vector = False


    def update(self, knight):
        global running
        if pygame.sprite.collide_mask(self, knight):
            running = False


    def running(self):
        global action
        if self.rect.x >= self.x2:
            self.check = True
            self.vector = False
        if self.rect.x <= self.x1:
            self.check = False
            self.vector = True
        if self.check:
            if action:
                self.rect.x -= 2
            else:
                self.rect.x -= 1
        else:
            if action:
                self.rect.x += 2
            else:
                self.rect.x += 1
        clock.tick(300)

    def animation(self):
        global woodcutter_count, woodcutter_image
        if woodcutter_count == 30:
            woodcutter_count = 0
        if self.vector:
            screen.blit(woodcutter_image[woodcutter_count // 10], (self.rect.x, self.rect.y))
        else:
            screen.blit(pygame.transform.flip(woodcutter_image[woodcutter_count // 15], True, False), (self.rect.x, self.rect.y))
        woodcutter_count += 1
        clock.tick(300)


    def jumping(self):
        global jump_count_wc
        if self.count == 30:
            woodcutter_is_jump = True
            self.checking_jump = False
            if jump_count_wc >= -10:
                self.rect.y -= jump_count_wc
                jump_count_wc -= 1
                clock.tick(300)
            else:
                jump_count_wc = 10
                clock.tick(300)
                self.count = 0
                self.checking_jump = True
                woodcutter_is_jump = False
        if self.checking_jump:
            self.count += 1


def main():
    global is_jump, action, check_of_fall1, check_of_fall_12, check_of_fall_13, falling, running, score, knight, vector
    pygame.init()
    knight = Knight(800, 50)
    size = width, height = 850, 450
    screen = pygame.display.set_mode(size)
    all_sprites = pygame.sprite.Group()
    skeleton_group = pygame.sprite.Group()
    fon = pygame.transform.scale(load_image('level1_fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    pos_x = 750
    skeleton = Skeleton(5, 680, 5, 185)
    skeleton_group.add(skeleton)
    skeleton2 = Skeleton(200, 840, 840, 300)
    skeleton_group.add(skeleton2)
    for i in range(9):
        ball = Ball(3, pos_x, 70)
        all_sprites.add(ball)
        pos_x -= 70
    pos_x = 30
    for i in range(10):
        ball = Ball(3, pos_x, 190)
        all_sprites.add(ball)
        pos_x += 70
    pos_x = 820
    for i in range(10):
        ball = Ball(3, pos_x, 305)
        all_sprites.add(ball)
        pos_x -= 70
    pos_x = 30
    for i in range(11):
        ball = Ball(3, pos_x, 425)
        all_sprites.add(ball)
        pos_x += 70
    while running:
        right_running = False
        left_running = False
        action = False
        screen.blit(fon, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if ((knight.rect.x < 125 and knight.rect.y != 170) or (knight.rect.x < 255 and knight.rect.y != 170 and 50 < knight.rect.y < 170)) and check_of_fall1 and knight.rect.y >= 50:
            knight.rect.y += 10
            clock.tick(70)
            falling = True
        if knight.rect.y == 170:
            check_of_fall1 = False
            falling = False
        if ((knight.rect.x > 680 and knight.rect.y > 50 and knight.rect.y != 290) or (knight.rect.x > 600 and knight.rect.y > 50 and knight.rect.y != 290 and 170 < knight.rect.y < 290)) and check_of_fall_12 and knight.rect.y >= 170:
            knight.rect.y += 10
            clock.tick(70)
            falling = True
        if knight.rect.y == 290:
            check_of_fall_12 = False
            falling = False
            knight.rect.y -= 5
        if ((knight.rect.x < 130 and knight.rect.y != 405 and 285 <= knight.rect.y) or (knight.rect.x < 200 and knight.rect.y != 405 and 285 <= knight.rect.y and 285 < knight.rect.y < 405)) and check_of_fall_13 and knight.rect.y >= 285:
            knight.rect.y += 10
            clock.tick(70)
            falling = True
        if knight.rect.y == 405:
            check_of_fall_13 = False
            falling = False
            knight.rect.y -= 5
        if pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_LEFT]:
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                if knight.rect.x <= 800 and not left_running:
                    right_running = True
                    knight.rect.x += 4
                    vector = True
                    Knight.animation(knight, vector)
                    action = True
            if pygame.key.get_pressed()[pygame.K_LEFT]:
                if knight.rect.x >= 0 and not right_running:
                    left_running = True
                    knight.rect.x -= 4
                    vector = False
                    Knight.animation(knight, vector)
                    action = True
        if pygame.key.get_pressed()[pygame.K_UP] and not falling:
            if 760 < knight.rect.x < 790 and knight.rect.y == 400:
                running = False
            else:
                is_jump = True
        if is_jump:
            Knight.jumping(knight, vector)
        if not action and not is_jump:
            Knight.staying(knight, vector)
        intro_text = f'Очки: {score}'
        font = pygame.font.Font(None, 40)
        string_rendered = font.render(intro_text, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.x = 700
        intro_rect.y = 5
        screen.blit(string_rendered, intro_rect)
        skeleton_group.update(knight)
        Skeleton.animation(skeleton)
        Skeleton.animation(skeleton2)
        Skeleton.running(skeleton2)
        Skeleton.running(skeleton)
        all_sprites.draw(screen)
        all_sprites.update(knight)
        pygame.display.flip()
    pygame.quit()


def lvl_2():
    global running, WIDTH, HEIGHT, vector, is_jump, check_of_fall2, check_of_fall_22, check_of_fall_23, falling, skeleton_group
    pygame.init()
    vector = True
    action = False
    size = width, height = 850, 450
    screen = pygame.display.set_mode(size)
    fon = pygame.transform.scale(load_image('level2_fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    knight = Knight(30, 290)
    skeleton1 = Skeleton(20, 580, 580, 75)
    skeleton_group.add(skeleton1)
    skeleton2 = Skeleton(336, 804, 804, 305)
    skeleton_group.add(skeleton2)
    woodcutter = WoodCutter(100, 696, 100, 195)
    woodcutter2 = WoodCutter(35, 815, 35, 415)
    pos_x = 30
    for i in range(9):
        ball = Ball(3, pos_x, 85)
        all_sprites.add(ball)
        pos_x += 70
    pos_x = 120
    for i in range(10):
        ball = Ball(3, pos_x, 205)
        all_sprites.add(ball)
        pos_x += 65
    pos_x = 800
    # for i in range(7):
    #     ball = Ball(3, pos_x, 320)
    #     all_sprites.add(ball)
    #     pos_x -= 70
    pos_x = 30
    for i in range(14):
        ball = Ball(3, pos_x, 320)
        all_sprites.add(ball)
        pos_x += 70
    pos_x = 30
    for i in range(11):
        ball = Ball(3, pos_x, 430)
        all_sprites.add(ball)
        pos_x += 70
    while running:
        # print(knight.rect.x, knight.rect.y)
        right_running = False
        left_running = False
        action = False
        screen.blit(fon, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if ((585 < knight.rect.x and 60 <= knight.rect.y < 180) or (500 < knight.rect.x < 672 and 60 <= knight.rect.y < 180 and falling)) and check_of_fall2:
            knight.rect.y += 10
            clock.tick(70)
            falling = True
        if knight.rect.y == 180:
            check_of_fall2 = False
            falling = False
        if (((knight.rect.x < 80 and 180 <= knight.rect.y < 290) or (knight.rect.x < 300 and 180 <= knight.rect.y < 290 and falling)) or ((knight.rect.x > 721 and 180 <= knight.rect.y < 290) or (650 < knight.rect.x and 180 <= knight.rect.y < 290 and falling))) and check_of_fall_22:
            knight.rect.y += 10
            clock.tick(70)
            falling = True
        if knight.rect.y == 290:
            check_of_fall_22 = False
            falling = False
        if ((278 < knight.rect.x < 315 and 290 <= knight.rect.y < 400) or (200 < knight.rect.x < 400 and 290 <= knight.rect.y < 400 and falling)) and check_of_fall_23:

            knight.rect.y += 10
            clock.tick(70)
            falling = True
        if knight.rect.y == 400:
            check_of_fall_23 = False
            falling = False
        if pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_LEFT]:
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                if knight.rect.x <= 800 and not left_running:
                    right_running = True
                    knight.rect.x += 5
                    vector = True
                    Knight.animation(knight, vector)
                    action = True
            if pygame.key.get_pressed()[pygame.K_LEFT]:
                if knight.rect.x >= 0 and not right_running:
                    left_running = True
                    knight.rect.x -= 5
                    vector = False
                    Knight.animation(knight, vector)
                    action = True
        if pygame.key.get_pressed()[pygame.K_UP] and not falling:
            if 760 < knight.rect.x < 790 and knight.rect.y == 400:
                running = False
            else:
                is_jump = True
        if is_jump:
            Knight.jumping(knight, vector)
        if not action and not is_jump:
            Knight.staying(knight, vector)
        all_sprites.update(knight)
        all_sprites.draw(screen)
        WoodCutter.running(woodcutter2)
        WoodCutter.animation(woodcutter2)
        WoodCutter.jumping(woodcutter2)
        WoodCutter.running(woodcutter)
        WoodCutter.animation(woodcutter)
        WoodCutter.jumping(woodcutter)
        skeleton_group.update(knight)
        Skeleton.running(skeleton1)
        Skeleton.animation(skeleton1)
        Skeleton.running(skeleton2)
        Skeleton.animation(skeleton2)
        pygame.display.flip()



if __name__ == '__main__':
    lvl_2()