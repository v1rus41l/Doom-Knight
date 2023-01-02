import pygame
import sys
from qwe import WIDTH, HEIGHT
import os

FPS = 50
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

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
    intro_text = "Нажмите,чтобы начать"

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 40)
    string_rendered = font.render(intro_text, 1, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    intro_rect.x = 270
    intro_rect.y = 390
    screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                main()
        pygame.display.flip()
        clock.tick(FPS)

def main():
    pygame.init()
    size = width, height = 850, 450
    screen = pygame.display.set_mode(size)
    all_sprites = pygame.sprite.Group()
    arrow_image = load_image("2.png")
    cursor = pygame.sprite.Sprite(all_sprites)
    cursor.image = arrow_image
    cursor.rect = cursor.image.get_rect()
    cursor.rect.x = -60
    cursor.rect.y = 20
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

        screen.fill('white')
        all_sprites.draw(screen)
        pygame.display.flip()
    pygame.quit()

if __name__ == '__main__':
    start_screen()