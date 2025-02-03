import pygame
import sys
from random import randint, choice
import math


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('Imagens/Player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('Imagens/Player/player_walk_2.png').convert_alpha()
        player_walk_3 = pygame.image.load('Imagens/Player/player_walk_3.png').convert_alpha()
        player_walk_4 = pygame.image.load('Imagens/Player/player_walk_4.png').convert_alpha()
        player_walk_5 = pygame.image.load('Imagens/Player/player_walk_5.png').convert_alpha()
        player_walk_6 = pygame.image.load('Imagens/Player/player_walk_6.png').convert_alpha()
        player_walk_7 = pygame.image.load('Imagens/Player/player_walk_7.png').convert_alpha()
        player_walk_8 = pygame.image.load('Imagens/Player/player_walk_8.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2, player_walk_3, player_walk_4, player_walk_5, player_walk_6, player_walk_7,  player_walk_8]
        self.player_index = 0

        self.player_jump = pygame.image.load('Imagens/Player/player_jump_4.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('Audio/jump.mp3')
        self.jump_sound.set_volume(0.1)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -17
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'Vulture':
            fly_1 = pygame.image.load('Imagens/Vulture/volture_walk_1.png').convert_alpha()
            fly_2 = pygame.image.load('Imagens/Vulture/vulture_walk_2.png').convert_alpha()
            fly_3 = pygame.image.load('Imagens/Vulture/vulture_walk_3.png').convert_alpha()
            fly_4 = pygame.image.load('Imagens/Vulture/vulture_walk_4.png').convert_alpha()
            self.frames = [fly_1, fly_2, fly_3, fly_4]
            y_pos = 210
        else:
            scorpio1 = pygame.image.load('Imagens/Scorpio/scorpio_walk_1.png').convert_alpha()
            scorpio2 = pygame.image.load('Imagens/Scorpio/scorpio_walk_2.png').convert_alpha()
            scorpio3 = pygame.image.load('Imagens/Scorpio/scorpio_walk_3.png').convert_alpha()
            scorpio4 = pygame.image.load('Imagens/Scorpio/scorpio_walk_4.png').convert_alpha()

            self.frames = [scorpio1, scorpio2, scorpio3, scorpio4]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]

        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0

        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 10
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


def display_score():
    current_time = int(pygame.time.get_ticks() / 100) - start_time
    score_surf = test_font.render(f'{current_time}', False, (255, 255, 255))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False, pygame.sprite.collide_mask):
        obstacle_group.empty()
        music.stop()
        return False
    else:
        return True


pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Infinity Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('Font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0
music = pygame.mixer.Sound('Audio/music.wav')
music.set_volume(0.05)

# Groups

player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

sky_surface = pygame.image.load('Imagens/forest.png').convert()
sky_surface = pygame.transform.scale(sky_surface, (800, 300))
sky_width = sky_surface.get_width()
scroll_sky = 0
tiles_sky = math.ceil(800/sky_width) + 1

ground_surface = pygame.image.load('Imagens/GroundRunner.png').convert()
ground_width = ground_surface.get_width()
scroll_ground = 0
tiles_ground = math.ceil(800/ground_width) + 1

# Intro screen
player_idle_1 = pygame.image.load('Imagens/Player/player_idle_1.png').convert_alpha()
player_idle_2 = pygame.image.load('Imagens/Player/player_idle_2.png').convert_alpha()
player_idle_3 = pygame.image.load('Imagens/Player/player_idle_3.png').convert_alpha()
player_idle_4 = pygame.image.load('Imagens/Player/player_idle_4.png').convert_alpha()
player_idle_5 = pygame.image.load('Imagens/Player/player_idle_5.png').convert_alpha()

player_index = 0

player_idle = [player_idle_1, player_idle_2, player_idle_3, player_idle_4, player_idle_5]
player_image = player_idle[player_index]

player_stand = pygame.transform.rotozoom(player_image, 0, 2)

player_stand_rect = player_stand.get_rect(center=(400, 150))

game_name = test_font.render('Infinity Runner', False, (0, 200, 0))
game_name_rect = game_name.get_rect(center=(400, 80))

game_message = test_font.render('Press space to start', False, (0, 200, 0))
game_message_rect = game_message.get_rect(center=(400, 330))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

while True:
    for i in range(0, tiles_ground):
        screen.blit(ground_surface, (i * ground_width + scroll_ground, 300))
    scroll_ground -= 5
    if abs(scroll_ground) > ground_width:
        scroll_ground = 0

    for j in range(0, tiles_sky):
        screen.blit(sky_surface, (j * sky_width + scroll_sky, 0))
    scroll_sky -= 5
    if abs(scroll_sky) > sky_width:
        scroll_sky = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['Vulture', 'Scorpio', 'Scorpio', 'Scorpio'])))

        else:
            game_active = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:

                game_active = True
                start_time = int(pygame.time.get_ticks() / 100)
                music.play()

    if game_active:
        score = display_score()

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active = collision_sprite()

    else:
        screen.fill((50, 125, 150))
        screen.blit(player_stand, player_stand_rect)

        score_message = test_font.render(f'Your score: {score}', False, (0, 200, 0))
        score_message_rect = score_message.get_rect(center=(400, 330))
        screen.blit(game_name, game_name_rect)

        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)

    sys.setrecursionlimit(1500)
