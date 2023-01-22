import os
import sys
import csv
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

wasd_cfg = False
defolt_cfg = True

def terminate():
    pygame.quit()
    sys.exit()

def start_screen():
    global WIDTH, HEIGHT
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x1, y1 = event.pos
                print(x1, y1)
                if 129 <= x1 <= 312 and 333 <= y1 <= 409:
                    level_changing()
                elif 571 <= x1 <= 762 and 333 <= y1 <= 409:
                    settings()
        pygame.display.flip()

# 129 333
# 312 409


def settings():
    global wasd_cfg, defolt_cfg, WIDTH, HEIGHT
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    if defolt_cfg:
        fon = pygame.transform.scale(load_image('upravlenie_l.jpg'), (WIDTH, HEIGHT))
    elif wasd_cfg:
        fon = pygame.transform.scale(load_image('upravlenie_p.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x1, y1 = event.pos
                print(x1, y1)
                if 36 <= x1 <= 91 and 8 <= y1 <= 65:
                    start_screen()
                elif 111 <= x1 <= 292 and 337 <= y1 <= 401:
                    fon = pygame.transform.scale(load_image('upravlenie_l.jpg'), (WIDTH, HEIGHT))
                    defolt_cfg = True
                    wasd_cfg = False
                    screen.blit(fon, (0, 0))
                elif 558 <= x1 <= 739 and 337 <= y1 <= 401:
                    fon = pygame.transform.scale(load_image('upravlenie_p.jpg'), (WIDTH, HEIGHT))
                    wasd_cfg = True
                    defolt_cfg = False
                    screen.blit(fon, (0, 0))
        pygame.display.flip()


def level_changing():
    global WIDTH, HEIGHT
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    fon = pygame.transform.scale(load_image('lvlchange.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x1, y1 = event.pos
                print(x1, y1)
                if 48 <= x1 <= 110 and 28 <= y1 <= 91:
                    start_screen()
                if 119 <= x1 <= 256 and 189 <= y1 <= 316:
                    main()
                elif 369 <= x1 <= 509 and 189 <= y1 <= 316:
                    lvl_2()
                elif 608 <= x1 <= 747 and 189 <= y1 <= 316:
                    lvl_3()
        pygame.display.flip()

knight_img = [pygame.image.load('data/3.png'),
              pygame.image.load('data/4.png'), pygame.image.load('data/5.png'), pygame.image.load('data/6.png'),
              pygame.image.load('data/5.png'), pygame.image.load('data/4.png'), pygame.image.load('data/3.png')]
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
check_of_fall3 = True
check_of_fall_32 = True
check_of_fall_33 = True
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
locking = True
gameover = False
youwin = False
knight_jump_count = 0
woodcutter_jump_count = 0
queue_jumping = True
check = True
check2 = True



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
        if img_count == 350:
            img_count = 0
        if not is_jump:
            if vector:
                screen.blit(knight_img[img_count // 50], (self.rect.x, self.rect.y))
            else:
                screen.blit(pygame.transform.flip(knight_img[img_count // 50], True, False), (self.rect.x, self.rect.y))
        img_count += 1

    def jumping(self, vector):
        global jump_count, is_jump, knight_jump_count

        if vector:
            screen.blit(pygame.image.load('data/2.png'), (self.rect.x, self.rect.y))
        else:
            screen.blit(pygame.transform.flip(pygame.image.load('data/2.png'), True, False), (self.rect.x, self.rect.y))
        if jump_count >= -10:
            if knight_jump_count == 10:
                self.rect.y -= jump_count
                jump_count -= 1
                knight_jump_count = 0
                # clock.tick(70)
        else:
            jump_count = 10
            # clock.tick(70)
            is_jump = False
        knight_jump_count += 1



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
        global gameover
        if pygame.sprite.collide_mask(self, knight):
            gameover = True


    def running(self):
        global action
        if self.rect.x >= self.x2:
            self.check = True
            self.vector = False
        if self.rect.x <= self.x1:
            self.check = False
            self.vector = True
        if self.check:
            self.rect.x -=1
        else:
            self.rect.x += 1
        # clock.tick(150)

    def animation(self):
        global skeleton_count, skeleton_img
        if skeleton_count == 400:
            skeleton_count = 0
        if self.vector:
            screen.blit(skeleton_img[skeleton_count // 200], (self.rect.x, self.rect.y))
        else:
            screen.blit(pygame.transform.flip(skeleton_img[skeleton_count // 200], True, False), (self.rect.x, self.rect.y))
        skeleton_count += 1



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
        self.woodcutter_jump_count = 0
        self.checking_jump = True
        self.mask = pygame.mask.from_surface(self.image)
        self.clock = pygame.time.Clock()
        self.vector = False


    def update(self, knight):
        global running, gameover
        if pygame.sprite.collide_mask(self, knight):
            gameover = True


    def running(self):
        global action
        if self.rect.x >= self.x2:
            self.check = True
            self.vector = False
        if self.rect.x <= self.x1:
            self.check = False
            self.vector = True
        if self.check:
            self.rect.x -= 1
        else:
            self.rect.x += 1
        # clock.tick(300)

    def animation(self):
        global woodcutter_count, woodcutter_image
        if woodcutter_count == 300:
            woodcutter_count = 0
        if self.vector:
            screen.blit(woodcutter_image[woodcutter_count // 100], (self.rect.x, self.rect.y))
        else:
            screen.blit(pygame.transform.flip(woodcutter_image[woodcutter_count // 100], True, False), (self.rect.x, self.rect.y))
        woodcutter_count += 1
        # clock.tick(300)


    def jumping(self):
        global jump_count_wc, woodcutter_jump_count, queue_jumping, check
        self.checking_jump = False
        if jump_count_wc >= -10:
            self.rect.y -= jump_count_wc
            jump_count_wc -= 1
            # self.woodcutter_jump_count = 0
        else:
            jump_count_wc = 10
            self.count = 0
            self.checking_jump = True
            if check:
                check = False
            else:
                check = True
        # self.woodcutter_jump_count += 1


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


class GoldenKey(pygame.sprite.Sprite):
    image = load_image("goldenkey.png")
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.radius = 5
        self.image = load_image("goldenkey.png")

        self.rect = pygame.Rect(x, y, 250, 250)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, knight):
        global locking
        if pygame.sprite.collide_mask(self, knight):
            self.kill()
            locking = False


class Lock(pygame.sprite.Sprite):
    image = load_image("lock.png")
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.radius = 5
        self.image = load_image("lock.png")

        self.rect = pygame.Rect(x, y, 250, 250)
        self.mask = pygame.mask.from_surface(self.image)

    def unlocking(self):
        global locking
        if not locking:
            self.kill()



class Sphere(pygame.sprite.Sprite):
    image = load_image("Volume_045.png")

    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.radius = 5
        self.image = load_image("Volume_045.png")

        self.rect = pygame.Rect(x, y, 2 * 5, 2 * 5)
        self.mask = pygame.mask.from_surface(self.image)
        self.x = x


    def actioning(self):
        global action
        self.rect.x += 1
        # clock.tick(300)
        if self.rect.x > 850:
            self.rect.x = self.x


    def update(self, knight):
        global gameover
        if pygame.sprite.collide_mask(self, knight):
            gameover = True


def main():
    global is_jump, action, check_of_fall1, check_of_fall_12, check_of_fall_13, falling, running, score, knight, vector, gameover, youwin, WIDTH, HEIGHT
    pygame.init()
    knight = Knight(800, 50)
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    all_sprites = pygame.sprite.Group()
    skeleton_group = pygame.sprite.Group()
    fon = pygame.transform.scale(load_image('level1_fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    skeleton = Skeleton(5, 680, 5, 185)
    skeleton_group.add(skeleton)
    skeleton2 = Skeleton(200, 840, 840, 300)
    skeleton_group.add(skeleton2)
    score = 0
    counter_of_updating = 0
    gameover = False
    youwin = False
    right_running = False
    left_running = False
    knight_running_count = 0
    knight_falling_count = 0
    with open('points.csv', encoding="utf8") as csvfile:
        reader = list(csv.reader(csvfile, delimiter=';', quotechar='"'))[1:]
        for_level1 = list(map(int, reader[0]))
        pos_x = for_level1[2]
        for i in range(for_level1[5]):
            ball = Ball(3, pos_x, for_level1[3])
            all_sprites.add(ball)
            pos_x -= for_level1[4]
        pos_x = for_level1[7]
        for i in range(for_level1[10]):
            ball = Ball(3, pos_x, for_level1[8])
            all_sprites.add(ball)
            pos_x += for_level1[9]
        pos_x = for_level1[12]
        for i in range(for_level1[15]):
            ball = Ball(3, pos_x, for_level1[13])
            all_sprites.add(ball)
            pos_x -= for_level1[14]
        pos_x = for_level1[17]
        for i in range(for_level1[20]):
            ball = Ball(3, pos_x, for_level1[18])
            all_sprites.add(ball)
            pos_x += for_level1[19]
    while running:
        counter_of_updating += 1
        action = False
        screen.blit(fon, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if counter_of_updating == 9:
            Skeleton.running(skeleton)
            Skeleton.running(skeleton2)
            counter_of_updating = 0
        if ((knight.rect.x < 125 and knight.rect.y != 170) or (knight.rect.x < 255 and knight.rect.y != 170 and 50 < knight.rect.y < 170)) and check_of_fall1 and knight.rect.y >= 50:
            knight_falling_count += 1
            if knight_falling_count == 2:
                knight.rect.y += 2
                knight_falling_count = 0
            falling = True
        if knight.rect.y == 170:
            check_of_fall1 = False
            falling = False
        if ((knight.rect.x > 680 and knight.rect.y > 50 and knight.rect.y != 290) or (knight.rect.x > 600 and knight.rect.y > 50 and knight.rect.y != 290 and 170 < knight.rect.y < 290)) and check_of_fall_12 and knight.rect.y >= 170:
            knight_falling_count += 1
            if knight_falling_count == 2:
                knight.rect.y += 2
                knight_falling_count = 0
            falling = True
        if knight.rect.y == 290:
            check_of_fall_12 = False
            falling = False
            knight.rect.y -= 5
        if ((knight.rect.x < 130 and knight.rect.y != 405 and 285 <= knight.rect.y) or (knight.rect.x < 200 and knight.rect.y != 405 and 285 <= knight.rect.y and 285 < knight.rect.y < 405)) and check_of_fall_13 and knight.rect.y >= 285:
            knight_falling_count += 1
            if knight_falling_count == 2:
                knight.rect.y += 2
                knight_falling_count = 0
            falling = True
        if knight.rect.y == 405:
            check_of_fall_13 = False
            falling = False
            knight.rect.y -= 5
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            action = True
            Knight.animation(knight, vector)
            if knight.rect.x <= 800 and not left_running:
                knight_running_count += 1
                if knight_running_count == 4:
                    right_running = True
                    knight.rect.x += 2
                    vector = True
                    knight_running_count = 0
        else:
            right_running = False
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            Knight.animation(knight, vector)
            action = True
            if knight.rect.x >= 0 and not right_running:
                knight_running_count += 1
                if knight_running_count == 4:
                    left_running = True
                    knight.rect.x -= 2
                    vector = False
                    knight_running_count = 0
        else:
            left_running = False
        if pygame.key.get_pressed()[pygame.K_UP] and not falling:
            if 760 < knight.rect.x < 790 and knight.rect.y == 400:
                youwin = True
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
        all_sprites.draw(screen)
        all_sprites.update(knight)
        if gameover:
            fon = pygame.transform.scale(load_image('game_over.jpg'), (width, height))
            screen.blit(fon, (0, 0))
        if youwin:
            fon = pygame.transform.scale(load_image('win_game.jpg'), (width, height))
            screen.blit(fon, (0, 0))
            intro_text = f'Score: {score}'
            font = pygame.font.Font('data/pixelfont.ttf', 50)
            string_rendered = font.render(intro_text, 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            intro_rect.x = 320
            intro_rect.y = 180
            screen.blit(string_rendered, intro_rect)
        pygame.display.flip()
    pygame.quit()


def lvl_2():
    global running, WIDTH, HEIGHT, vector, is_jump, gameover, youwin, check_of_fall2, check_of_fall_22, check_of_fall_23, falling, check, skeleton_group, score
    pygame.init()
    vector = True
    action = False
    size = width, height = 850, 450
    screen = pygame.display.set_mode(size)
    fon = pygame.transform.scale(load_image('level2_fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    knight = Knight(30, 60)
    skeleton1 = Skeleton(20, 580, 580, 75)
    skeleton_group.add(skeleton1)
    skeleton2 = Skeleton(336, 804, 804, 305)
    skeleton_group.add(skeleton2)
    woodcutter = WoodCutter(100, 696, 100, 195)
    woodcutter2 = WoodCutter(35, 815, 35, 415)
    score = 0
    knight_running_count = 0
    counter_of_updating = 0
    counter_of_jump = 0
    right_running = False
    knight_falling_count = 0
    youwin = False
    gameover = False
    queue_jump = True
    left_running = False
    check = True
    with open('points.csv', encoding="utf8") as csvfile:
        reader = list(csv.reader(csvfile, delimiter=';', quotechar='"'))[1:]
        for_level2 = list(map(int, reader[1]))
        pos_x = for_level2[2]
        for i in range(for_level2[5]):
            ball = Ball(3, pos_x, for_level2[3])
            all_sprites.add(ball)
            pos_x += for_level2[4]
        pos_x = for_level2[7]
        for i in range(for_level2[10]):
            ball = Ball(3, pos_x, for_level2[8])
            all_sprites.add(ball)
            pos_x += for_level2[9]
        pos_x = for_level2[12]
        for i in range(for_level2[15]):
            ball = Ball(3, pos_x, for_level2[13])
            all_sprites.add(ball)
            pos_x += for_level2[14]
        pos_x = for_level2[17]
        for i in range(for_level2[20]):
            ball = Ball(3, pos_x, for_level2[18])
            all_sprites.add(ball)
            pos_x += for_level2[19]
    while running:
        counter_of_jump += 1
        counter_of_updating += 1
        action = False
        screen.blit(fon, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if check:
            if counter_of_jump == 20:
                WoodCutter.jumping(woodcutter)
                counter_of_jump = 0
        else:
            if counter_of_jump == 20:
                WoodCutter.jumping(woodcutter2)
                counter_of_jump = 0
        if counter_of_updating == 9:
            Skeleton.running(skeleton1)
            Skeleton.running(skeleton2)
            WoodCutter.running(woodcutter2)
            WoodCutter.running(woodcutter)
            counter_of_updating = 0
        if ((585 < knight.rect.x and 60 <= knight.rect.y < 180) or (500 < knight.rect.x < 672 and 60 <= knight.rect.y < 180 and falling)) and check_of_fall2:
            knight_falling_count += 1
            if knight_falling_count == 2:
                knight.rect.y += 2
                knight_falling_count = 0
            falling = True
        if knight.rect.y == 180:
            check_of_fall2 = False
            falling = False
        if (((knight.rect.x < 80 and 180 <= knight.rect.y < 290) or (knight.rect.x < 300 and 180 <= knight.rect.y < 290 and falling)) or ((knight.rect.x > 721 and 180 <= knight.rect.y < 290) or (650 < knight.rect.x and 180 <= knight.rect.y < 290 and falling))) and check_of_fall_22:
            knight_falling_count += 1
            if knight_falling_count == 2:
                knight.rect.y += 2
                knight_falling_count = 0
            falling = True
        if knight.rect.y == 290:
            check_of_fall_22 = False
            falling = False
        if ((278 < knight.rect.x < 315 and 290 <= knight.rect.y < 400) or (200 < knight.rect.x < 400 and 290 <= knight.rect.y < 400 and falling)) and check_of_fall_23:
            knight_falling_count += 1
            if knight_falling_count == 2:
                knight.rect.y += 2
                knight_falling_count = 0
            falling = True
        if knight.rect.y == 400:
            check_of_fall_23 = False
            falling = False
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            action = True
            Knight.animation(knight, vector)
            if knight.rect.x <= 800 and not left_running:
                knight_running_count += 1
                if knight_running_count == 4:
                    right_running = True
                    knight.rect.x += 2
                    vector = True
                    knight_running_count = 0
        else:
            right_running = False
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            Knight.animation(knight, vector)
            action = True
            if knight.rect.x >= 0 and not right_running:
                knight_running_count += 1
                if knight_running_count == 4:
                    left_running = True
                    knight.rect.x -= 2
                    vector = False
                    knight_running_count = 0
        else:
            left_running = False
        if pygame.key.get_pressed()[pygame.K_UP] and not falling:
            if 760 < knight.rect.x < 790 and knight.rect.y == 400:
                youwin = True
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
        all_sprites.update(knight)
        all_sprites.draw(screen)
        WoodCutter.animation(woodcutter2)
        # WoodCutter.jumping(woodcutter2)
        WoodCutter.animation(woodcutter)
        # WoodCutter.jumping(woodcutter)
        skeleton_group.update(knight)
        Skeleton.animation(skeleton1)
        Skeleton.animation(skeleton2)
        if gameover:
            fon = pygame.transform.scale(load_image('game_over.jpg'), (width, height))
            screen.blit(fon, (0, 0))
        if youwin:
            fon = pygame.transform.scale(load_image('win_game.jpg'), (width, height))
            screen.blit(fon, (0, 0))
            intro_text = f'Score: {score}'
            font = pygame.font.Font('data/pixelfont.ttf', 50)
            string_rendered = font.render(intro_text, 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            intro_rect.x = 320
            intro_rect.y = 180
            screen.blit(string_rendered, intro_rect)
        pygame.display.flip()


def lvl_3():
    global running, WIDTH, HEIGHT, vector, is_jump, check, score, check_of_fall2, check_of_fall_22, youwin, gameover, check_of_fall_23, falling, skeleton_group, check_of_fall3, check_of_fall_32, check_of_fall_33, locking
    pygame.init()
    vector = True
    action = False
    score = 0
    size = width, height = 850, 450
    screen = pygame.display.set_mode(size)
    fon = pygame.transform.scale(load_image('level3_fon.jpg'), (width, height))
    lock = Lock(788, 393)
    knight = Knight(40, 60)
    sphere = Sphere(35, 191)
    sphere2 = Sphere(35, 300)
    screen.blit(fon, (0, 0))
    woodcutter = WoodCutter(169, 825, 169, 75)
    woodcutter2 = WoodCutter(40, 820, 40, 415)
    skeleton = Skeleton(40, 710, 40, 195)
    skeleton2 = Skeleton(172, 825, 172, 305)
    skeleton_group.add(woodcutter, skeleton, skeleton2, woodcutter2)
    key = GoldenKey(785, 50)
    counter_of_updating = 0
    knight_running_count = 0
    knight_falling_count = 0
    counter_of_jump = 0
    left_running = False
    right_running = False
    all_sprites.add(sphere, sphere2, key, lock)
    with open('points.csv', encoding="utf8") as csvfile:
        reader = list(csv.reader(csvfile, delimiter=';', quotechar='"'))[1:]
        for_level2 = list(map(int, reader[2]))
        pos_x = for_level2[2]
        for i in range(for_level2[5]):
            ball = Ball(3, pos_x, for_level2[3])
            all_sprites.add(ball)
            pos_x += for_level2[4]
        pos_x = for_level2[7]
        for i in range(for_level2[10]):
            ball = Ball(3, pos_x, for_level2[8])
            all_sprites.add(ball)
            pos_x += for_level2[9]
        pos_x = for_level2[12]
        for i in range(for_level2[15]):
            ball = Ball(3, pos_x, for_level2[13])
            all_sprites.add(ball)
            pos_x += for_level2[14]
        pos_x = for_level2[17]
        for i in range(for_level2[20]):
            ball = Ball(3, pos_x, for_level2[18])
            all_sprites.add(ball)
            pos_x += for_level2[19]
    while running:
        counter_of_updating += 1
        counter_of_jump += 1
        action = False
        screen.blit(fon, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(event.pos)
        if check:
            if counter_of_jump == 20:
                WoodCutter.jumping(woodcutter)
                counter_of_jump = 0
        else:
            if counter_of_jump == 20:
                WoodCutter.jumping(woodcutter2)
                counter_of_jump = 0
        if counter_of_updating == 9:
            Skeleton.running(skeleton)
            Skeleton.running(skeleton2)
            WoodCutter.running(woodcutter2)
            WoodCutter.running(woodcutter)
            counter_of_updating = 0
        if ((112 < knight.rect.x < 152 and 60 <= knight.rect.y < 180) or (60 < knight.rect.x < 300 and 60 <= knight.rect.y < 180 and falling)) and check_of_fall3:
            knight_falling_count += 1
            if knight_falling_count == 2:
                knight.rect.y += 2
                knight_falling_count = 0
            falling = True
        if knight.rect.y == 180:
            check_of_fall3 = False
            falling = False
        if ((knight.rect.x > 732 and 180 <= knight.rect.y < 290) or (knight.rect.x > 600 and 180 <= knight.rect.y < 290 and falling)) and check_of_fall_32:
            knight_falling_count += 1
            if knight_falling_count == 2:
                knight.rect.y += 2
                knight_falling_count = 0
            falling = True
        if knight.rect.y == 290:
            check_of_fall_32 = False
            falling = False
        if ((98 < knight.rect.x < 143 and 290 <= knight.rect.y < 400) or (0 < knight.rect.x < 250 and 290 <= knight.rect.y < 400 and falling)) and check_of_fall_33:
            knight_falling_count += 1
            if knight_falling_count == 2:
                knight.rect.y += 2
                knight_falling_count = 0
            falling = True
        if knight.rect.y == 400:
            check_of_fall_33 = False
            falling = False
            knight.rect.y -= 5
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            action = True
            Knight.animation(knight, vector)
            if knight.rect.x <= 800 and not left_running:
                knight_running_count += 1
                if knight_running_count == 4:
                    right_running = True
                    knight.rect.x += 2
                    vector = True
                    knight_running_count = 0
        else:
            right_running = False
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            Knight.animation(knight, vector)
            action = True
            if knight.rect.x >= 0 and not right_running:
                if not ((120 < knight.rect.y <= 180 and knight.rect.x == 34) or (230 < knight.rect.y <= 290 and knight.rect.x == 34)):
                    knight_running_count += 1
                    if knight_running_count == 4:
                        left_running = True
                        knight.rect.x -= 2
                        vector = False
                        knight_running_count = 0
        else:
            left_running = False
        if pygame.key.get_pressed()[pygame.K_UP] and not falling:
            if 760 < knight.rect.x < 790 and knight.rect.y == 395:
                if locking:
                    pass
                else:
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
        Lock.unlocking(lock)
        Sphere.actioning(sphere)
        Sphere.actioning(sphere2)
        Sphere.update(sphere, knight)
        Sphere.update(sphere2, knight)
        WoodCutter.animation(woodcutter)
        WoodCutter.animation(woodcutter2)
        Skeleton.animation(skeleton)
        Skeleton.animation(skeleton2)
        all_sprites.draw(screen)
        all_sprites.update(knight)
        skeleton_group.update(knight)
        if gameover:
            fon = pygame.transform.scale(load_image('game_over.jpg'), (width, height))
            screen.blit(fon, (0, 0))
        if youwin:
            fon = pygame.transform.scale(load_image('win_game.jpg'), (width, height))
            screen.blit(fon, (0, 0))
            intro_text = f'Score: {score}'
            font = pygame.font.Font('data/pixelfont.ttf', 50)
            string_rendered = font.render(intro_text, 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            intro_rect.x = 320
            intro_rect.y = 180
            screen.blit(string_rendered, intro_rect)
        pygame.display.flip()



if __name__ == '__main__':
    start_screen()