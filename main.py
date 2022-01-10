import pygame
from copy import deepcopy
from random import choice, randrange

WIDTH, HEIGHT = 10, 20
T = 45
GAME_RES = WIDTH * T, HEIGHT * T
RES = 750, 940
FPS = 60

pygame.init()
screen = pygame.display.set_mode(RES)
pygame.display.set_caption('TETRiS')
game_sc = pygame.Surface(GAME_RES)
clock = pygame.time.Clock()

fnt1 = pygame.font.Font('files/font/font.ttf', 65)
fnt2 = pygame.font.Font('files/font/font.ttf', 25)

figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)], [(0, -1), (-1, -1), (-1, 0), (0, 0)],
               [(-1, 0), (-1, 1), (0, 0), (0, -1)], [(0, 0), (-1, 0), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, -1)], [(0, 0), (0, -1), (0, 1), (1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, 0)]]
score, lines = 0, 0
scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}
anim_count, anim_speed, anim_limit = 0, 60, 2000

figures = [[pygame.Rect(x + WIDTH // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]
figure_rect = pygame.Rect(0, 0, T - 2, T - 2)
field = [[0 for i in range(WIDTH)] for j in range(HEIGHT)]

bg = pygame.image.load('files/img/bg.jpg').convert()
game_bg = pygame.image.load('files/img/bg.jpg').convert()
tetris_logo = pygame.image.load('files/img/tetris_logo.png').convert()
title_tetris = fnt1.render('TETRIS', True, pygame.Color('darkorange'))
title_score = fnt2.render('набрано очков:', True, pygame.Color('red'))
title_record = fnt2.render('рекорд:', True, pygame.Color('red'))
title_next_figure1 = fnt2.render('следующая', True, pygame.Color('red'))
title_next_figure2 = fnt2.render('фигура:', True, pygame.Color('red'))
title_game_over = fnt2.render('GAME OVER', True, pygame.Color('darkorange'))

new_color = lambda: (randrange(0, 200), randrange(0, 200), randrange(0, 200))
grid = [pygame.Rect(x * T, y * T, T, T) for x in range(WIDTH) for y in range(HEIGHT)]

figure, next_figure = deepcopy(choice(figures)), deepcopy(choice(figures))
color, next_color = new_color(), new_color()


def border_check():
    if figure[i].x < 0 or figure[i].x > WIDTH - 1:
        return False
    elif figure[i].y > HEIGHT - 1 or field[figure[i].y][figure[i].x]:
        return False
    return True


def record_file():
    try:
        with open('files/record') as f:
            return f.readline()
    except FileNotFoundError:
        with open('record', 'w') as f:
            f.write('0')


def set_record(record, score):
    rec = max(int(record), score)
    with open('files/record', 'w') as f:
        f.write(str(rec))


def cheat_record():
    rec = score = 10000
    with open('files/record', 'w') as f:
        f.write(str(rec))


def start_screen():
    intro_text = ['Правила игры в тетрис:',
                  'Случайные фигурки тетрамино падают сверху в прямоугольный стакан шириной 10 и', 'высотой 20 клеток. '
                                                                                                   'В полёте игрок может поворачивать фигурку на 90° и двигать её',
                  ' по горизонтали. '
                  'Также можно «сбрасывать» фигурку, то есть ускорять её падение,',
                  'когда уже решено, куда фигурка должна упасть. '
                  'Фигурка летит до тех пор, пока не', 'наткнётся на другую фигурку либо на дно стакана. ',
                  'Если при этом заполнился горизонтальный ряд из 10 клеток, он пропадает и всё,',
                  'что выше него, опускается на одну клетку. '
                  'Дополнительно показывается фигурка,',
                  'которая будет следовать после текущей — это подсказка, которая позволяет игроку',
                  'планировать действия. '
                  'Игра заканчивается, когда новая фигурка не может', 'поместиться в стакан. '
                                                                      'Игрок получает очки за каждый заполненный ряд, поэтому его',
                  'задача — заполнять ряды, не заполняя сам стакан (по вертикали) как можно дольше,',
                  'чтобы таким образом получить как можно больше очков.',
                  '',
                  '',
                  'Управление:',
                  '<, A - движение фигуры влево',
                  '>, D - движение фигуры вправо',
                  '↓, S - "сброс" фигуры вниз',
                  'SPASE, W - прокрута фигуры',
                  '',
                  '',
                  '',
                  '',
                  '',
                  '',
                  '',
                  '',
                  '',
                  '',
                  'Для начала игры нажмите ПРОБЕЛ.'
                  ]

    fon = pygame.image.load('files/img/start_bg.png').convert()
    screen.blit(fon, (0, 0))
    text_coord = 50
    for line in intro_text:
        string_rendered = fnt2.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
        pygame.display.flip()
        clock.tick(FPS)


def exit_screen():
    screen.fill(pygame.Color('black'))
    text_rect = title_game_over.get_rect(center=(750 / 2, 940 / 2))
    screen.blit(title_game_over, text_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


running = True
start_screen()
while running:
    record = record_file()
    dx, rotate = 0, False
    screen.fill(pygame.Color('black'))
    screen.blit(game_sc, (20, 20))
    game_sc.blit(game_bg, (0, 0))

    # задерка для отрисовки
    for i in range(lines):
        pygame.time.wait(200)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dx = -1
            elif event.key == pygame.K_RIGHT:
                dx = 1
            elif event.key == pygame.K_DOWN:
                anim_limit = 100
            elif event.key == pygame.K_a:
                dx = -1
            elif event.key == pygame.K_d:
                dx = 1
            elif event.key == pygame.K_s:
                anim_limit = 100
            elif event.key == pygame.K_w:
                rotate = True
            elif event.key == pygame.K_SPACE:
                rotate = True
            elif event.key == pygame.K_DELETE:
                cheat_record()

    # движение на x
    figure_old = deepcopy(figure)
    for i in range(4):
        figure[i].x += dx
        if not border_check():
            figure = deepcopy(figure_old)
            break

    # движение по y
    anim_count += anim_speed
    if anim_count > anim_limit:
        anim_count = 0
        figure_old = deepcopy(figure)
        for i in range(4):
            figure[i].y += 1
            if not border_check():
                for i in range(4):
                    field[figure_old[i].y][figure_old[i].x] = color
                figure, color = next_figure, next_color
                next_figure, next_color = deepcopy(choice(figures)), new_color()
                anim_limit = 2000
                break

    # поворот фигуры
    center = figure[0]
    figure_old = deepcopy(figure)
    if rotate:
        for i in range(4):
            x = figure[i].y - center.y
            y = figure[i].x - center.x
            figure[i].x = center.x - x
            figure[i].y = center.y + y
            if not border_check():
                figure = deepcopy(figure_old)
                break

    line, lines = HEIGHT - 1, 0
    for row in range(HEIGHT - 1, -1, -1):
        count = 0
        for i in range(WIDTH):
            if field[row][i]:
                count += 1
            field[line][i] = field[row][i]
        if count < WIDTH:
            line -= 1
        else:
            anim_speed += 3
            lines += 1

    # запоминание очков
    score += scores[lines]
    # отрисовка сетки
    [pygame.draw.rect(game_sc, (40, 40, 40), i_rect, 1) for i_rect in grid]

    # отрисовка фигуры
    for i in range(4):
        figure_rect.x = figure[i].x * T
        figure_rect.y = figure[i].y * T
        pygame.draw.rect(game_sc, color, figure_rect)

    # "застываение" фигуры
    for y, raw in enumerate(field):
        for x, col in enumerate(raw):
            if col:
                figure_rect.x, figure_rect.y = x * T, y * T
                pygame.draw.rect(game_sc, col, figure_rect)

    # отрисовка следующей фигуры
    for i in range(4):
        figure_rect.x = next_figure[i].x * T + 380
        figure_rect.y = next_figure[i].y * T + 550
        pygame.draw.rect(screen, next_color, figure_rect)

    # отрисовка
    screen.blit(title_next_figure1, (500, 450))
    screen.blit(title_next_figure2, (500, 475))
    screen.blit(tetris_logo, (480, 0))
    screen.blit(title_score, (500, 825))
    screen.blit(fnt2.render(str(score), True, pygame.Color('white')), (550, 875))
    screen.blit(title_record, (500, 725))
    screen.blit(fnt2.render(record, True, pygame.Color('gold')), (550, 775))

    # конец игры
    for i in range(WIDTH):
        if field[0][i]:
            set_record(record, score)
            field = [[0 for i in range(WIDTH)] for i in range(HEIGHT)]
            anim_count, anim_speed, anim_limit = 0, 60, 2000
            score = 0
            exit_screen()
    pygame.display.flip()
    clock.tick(FPS)
