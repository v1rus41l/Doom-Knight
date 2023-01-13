import pygame
from level_1 import Knight, Skeleton, clock, screen, knight_group, load_image, Ball

def main():
    global is_jump, action, check_of_fall, check_of_fall_2, check_of_fall_3, falling, running, score
    pygame.init()
    size = width, height = 850, 450
    screen = pygame.display.set_mode(size)
    all_sprites = pygame.sprite.Group()
    skeleton_group = pygame.sprite.Group()
    knight = Knight()
    knight_group.add(knight)
    fon = pygame.transform.scale(load_image('level1_fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    vector = False
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
        action = False
        screen.blit(fon, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if ((knight.rect.x < 125 and knight.rect.y != 170) or (knight.rect.x < 255 and knight.rect.y != 170 and 50 < knight.rect.y < 170)) and check_of_fall and knight.rect.y >= 50:
            knight.rect.y += 10
            clock.tick(70)
            falling = True
        if knight.rect.y == 170:
            check_of_fall = False
            falling = False
        if ((knight.rect.x > 680 and knight.rect.y > 50 and knight.rect.y != 290) or (knight.rect.x > 600 and knight.rect.y > 50 and knight.rect.y != 290 and 170 < knight.rect.y < 290)) and check_of_fall_2 and knight.rect.y >= 170:
            knight.rect.y += 10
            clock.tick(70)
            falling = True
        if knight.rect.y == 290:
            check_of_fall_2 = False
            falling = False
            knight.rect.y -= 5
        if ((knight.rect.x < 130 and knight.rect.y != 405 and 285 <= knight.rect.y) or (knight.rect.x < 200 and knight.rect.y != 405 and 285 <= knight.rect.y and 285 < knight.rect.y < 405)) and check_of_fall_3 and knight.rect.y >= 285:
            knight.rect.y += 10
            clock.tick(70)
            falling = True
        if knight.rect.y == 405:
            check_of_fall_3 = False
            falling = False
            knight.rect.y -= 5
        if pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_LEFT]:
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                if knight.rect.x <= 800:
                    knight.rect.x += 4
                    vector = True
                    Knight.animation(knight, vector)
                    action = True
            if pygame.key.get_pressed()[pygame.K_LEFT]:
                if knight.rect.x >= 0:
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

if __name__ == '__main__':
    main()