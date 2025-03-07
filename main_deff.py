import pygame
from random import randint

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PIPE_GAP = 150
FPS = 15
FONT_SIZE = 30
BACKGROUND_SCROLL_SPEED = 2
HERO_JUMP_HEIGHT = 60


# Настройка экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fly Bird Game")

# Шрифт
game_font = pygame.font.Font(None, FONT_SIZE)

# Загрузка изображений


def load_image(path, size=None):
    image = pygame.image.load(path)
    if size:
        image = pygame.transform.scale(image, size)
    return image


background_image = load_image(
    'images/background/background (2).jpg', (SCREEN_WIDTH, SCREEN_HEIGHT))
background_image_2 = load_image(
    'images/background/background (2).jpg', (SCREEN_WIDTH, SCREEN_HEIGHT))
hero_images = [load_image(
    f'images/bird_right/bird_right ({i}).png') for i in range(1, 7)]
enemy_images = [load_image(
    f'images/bird_left/bird_leff ({i}).png') for i in range(1, 7)]
rocket_image = load_image('images/Shoot/rocket.png', (70, 30))
pipe_image = load_image(
    'images/dangerous/pipe.png', (100, 180 + PIPE_GAP))
rotated_pipe_image = pygame.transform.rotate(pipe_image, 180)

# Звуки
background_sound = pygame.mixer.Sound('sounds/back_sound.mp3')
error_sound = pygame.mixer.Sound('sounds/bump.mp3')
bird_bump_sound = pygame.mixer.Sound('sounds/bird_bump.mp3')

# Инициализация переменных
pipe_speed = 20
rocket_speed = pipe_speed
background_x = 0
hero_x = SCREEN_WIDTH / 2 - 3 * (hero_images[0].get_width() / 2)
hero_y = SCREEN_HEIGHT / 2 - hero_images[0].get_height() / 2
hero_animation_index = 0
enemy_animation_index = 0
pipe_x = SCREEN_WIDTH
pipe_y = SCREEN_HEIGHT - pipe_image.get_height()
pipe_rotate_x = SCREEN_WIDTH
pipe_rotate_y = 0
enemy_x = pipe_x
enemy_y = (pipe_y+pipe_rotate_y)/2 + enemy_images[0].get_height()/2
pipe_random_y = randint(-PIPE_GAP, PIPE_GAP)
rocket_x, rocket_y = 0, 0
fire_flag = False
game_over_flag = False
enemy_spawn_interval = 5
game_score = 0
delta_score = 6
max_score = int(open("max_score.txt", "r").read())
pipe_transform_y = pipe_y + PIPE_GAP - pipe_random_y
pipe_rotate_transform_y = pipe_rotate_y - PIPE_GAP - pipe_random_y


# Функции
def draw_background():
    screen.blit(background_image, (background_x, 0))
    screen.blit(background_image, (background_x + SCREEN_WIDTH, 0))


def update_background():
    global background_x
    background_x -= BACKGROUND_SCROLL_SPEED
    if background_x <= -SCREEN_WIDTH:
        background_x = 0


def draw_hero():
    screen.blit(hero_images[hero_animation_index], (hero_x, hero_y))


def update_hero():
    global hero_y, hero_animation_index
    if hero_y < SCREEN_HEIGHT - hero_images[0].get_height():
        hero_y += 10
    hero_animation_index = (hero_animation_index + 1) % len(hero_images)


def update_enemy():
    global enemy_x, enemy_y, enemy_animation_index
    enemy_animation_index = (enemy_animation_index + 1) % len(enemy_images)
    enemy_x -= pipe_speed
    if enemy_x < -130:
        enemy_x = SCREEN_WIDTH


def draw_pipes_and_enemy():
    global pipe_transform_y, pipe_rotate_transform_y
    screen.blit(pipe_image, (pipe_x, pipe_transform_y))
    screen.blit(rotated_pipe_image, (pipe_rotate_x,
                pipe_rotate_transform_y))
    if game_score % enemy_spawn_interval == 0 and game_score != 0:
        screen.blit(enemy_images[enemy_animation_index],
                    (enemy_x, ((pipe_transform_y)+(pipe_rotate_transform_y))/2+enemy_images[0].get_height()))


def update_pipes_and_enemy():
    global enemy_x, pipe_x, pipe_rotate_x, pipe_random_y, game_score
    pipe_x -= pipe_speed
    pipe_rotate_x -= pipe_speed
    if pipe_x < -130:
        pipe_random_y = randint(-PIPE_GAP, PIPE_GAP)
        pipe_x = SCREEN_WIDTH
        pipe_rotate_x = SCREEN_WIDTH
        enemy_x = SCREEN_WIDTH+10
        game_score += 1


def draw_rocket():
    global rocket_x, rocket_y, fire_flag
    if rocket_x+rocket_image.get_width() > SCREEN_WIDTH:
        fire_flag = False
    if fire_flag:
        screen.blit(rocket_image, (rocket_x, rocket_y))

    else:
        rocket_x = 0
        rocket_y = 0


def update_rocket():
    global rocket_x, fire_flag
    if fire_flag:
        rocket_x += rocket_speed
        if rocket_x >= SCREEN_WIDTH:
            fire_flag = False


def check_collisions():
    global delta_score, game_over_flag, enemy_spawn_interval, game_score, fire_flag, pipe_transform_y, pipe_rotate_transform_y, enemy_x
    hero_rect = pygame.Rect(
        hero_x, hero_y, hero_images[0].get_width(), hero_images[0].get_height())
    top_pipe_rect = pygame.Rect(pipe_rotate_x, pipe_rotate_transform_y,
                                rotated_pipe_image.get_width(), rotated_pipe_image.get_height())
    bottom_pipe_rect = pygame.Rect(
        pipe_x, pipe_transform_y, pipe_image.get_width(), pipe_image.get_height())

    rocket_rect = pygame.Rect(
        rocket_x, rocket_y, rocket_image.get_width(), rocket_image.get_height())
    if game_score % enemy_spawn_interval == 0 and game_score != 0:
        enemy_rect = pygame.Rect(
            enemy_x, ((pipe_transform_y)+(pipe_rotate_transform_y))/2+enemy_images[0].get_height(), enemy_images[0].get_width(), enemy_images[0].get_height())
        if enemy_rect.colliderect(rocket_rect):
            fire_flag = False
            bird_bump_sound.play()
            game_score += delta_score
        if hero_rect.colliderect(enemy_rect):
            game_over_flag = True
            error_sound.play()

    if hero_rect.colliderect(top_pipe_rect) or hero_rect.colliderect(bottom_pipe_rect):
        error_sound.play()
        game_over_flag = True

    if rocket_rect.colliderect(top_pipe_rect) or rocket_rect.colliderect(bottom_pipe_rect):
        if rocket_x != 0 and rocket_y != 0:
            error_sound.play()
            fire_flag = False


def more_diff():
    global pipe_speed, delta_score
    if game_score >= 52 and game_score < 102:
        pipe_speed = 25
    if game_score >= 102 and game_score < 152:
        pipe_speed = 30
    if game_score >= 152 and game_score < 202:
        delta_score = 7
        pipe_speed = 29
    if game_score >= 202 and game_score < 500:
        delta_score = 8
        pipe_speed = 28
    if game_score >= 500:
        delta_score = 9
        pipe_speed = 27


def reset_game():
    global enemy_x, hero_y, pipe_x, pipe_rotate_x, game_score, game_over_flag
    hero_y = SCREEN_HEIGHT / 2 - hero_images[0].get_height() / 2
    pipe_x = SCREEN_WIDTH
    pipe_rotate_x = SCREEN_WIDTH
    enemy_x = SCREEN_WIDTH
    game_score = 0
    game_over_flag = False


# Настройки шрифта
font = pygame.font.Font(None, 36)


# Основной игровой цикл
background_sound.play(-1)
clock = pygame.time.Clock()
running = True
game_start = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and hero_y > 10:
                hero_y -= HERO_JUMP_HEIGHT
            if event.key == pygame.K_f:
                fire_flag = True
                rocket_x = hero_x + hero_images[0].get_width() + 20
                rocket_y = hero_y + hero_images[0].get_height() / 2

    if game_start:
        draw_background()
        update_background()
        draw_hero()
        update_hero()
        draw_pipes_and_enemy()
        update_pipes_and_enemy()
        update_enemy()
        draw_rocket()
        update_rocket()
        check_collisions()
        more_diff()

        if game_over_flag:
            reset_game()

        #  Отображение счета и условий игры

        fire_button = game_font.render(f"Use button F for fire", True, 'white')
        score_text = game_font.render(f"Your score: {game_score}", True, 'red')
        max_score_text = game_font.render(
            f"Max score: {max_score}", True, 'red')
        game_speed_text = game_font.render(
            f"Game speed: {pipe_speed}", True, 'red')
        delta_text = game_font.render(
            f"Enemy spawn: {delta_score}", True, 'red')
        screen.blit(score_text, (20, 20))
        screen.blit(max_score_text, (20, 50))
        screen.blit(game_speed_text, (320, 20))
        screen.blit(delta_text, (320, 50))
        screen.blit(fire_button, (20, SCREEN_HEIGHT-20))
        if game_score > max_score:
            max_score = game_score
            with open("max_score.txt", "w") as file:
                file.write(str(max_score))
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
