import pygame
import sys
from qwe import WIDTH, HEIGHT
import os

FPS = 50
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
wasd_cfg = False
defolt_cfg = True

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image

def terminate():
    pygame.quit()
    sys.exit()

def start_screen():
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
        clock.tick(FPS)

# 129 333
# 312 409


def settings():
    global wasd_cfg, defolt_cfg
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
        clock.tick(FPS)


def level_changing():
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
                    print(1)
                elif 369 <= x1 <= 509 and 189 <= y1 <= 316:
                    print(2)
                elif 608 <= x1 <= 747 and 189 <= y1 <= 316:
                    print(3)
        pygame.display.flip()
        clock.tick(FPS)


def game_over_screen():
    fon = pygame.transform.scale(load_image('game_over.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x1, y1 = event.pos
                print(x1, y1)
                if 78 <= x1 <= 158 and 336 <= y1 <= 415:
                    level_changing()
                if 707 <= x1 <= 783 and 336 <= y1 <= 415:
                    print(2)
        pygame.display.flip()


if __name__ == '__main__':
    game_over_screen()