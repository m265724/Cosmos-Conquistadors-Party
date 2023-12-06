import pygame
import sys
from CC_Player import Player
from CC_Second_Player import Second_Player
from CC_Alien import Alien
from random import choice
from CC_Laser import Laser
from CC_Alien_Laser import Alien_Laser


class Game:
    def __init__(self):
        player_sprite = Player((screen_width, screen_height), screen_width, 5)
        second_player_sprite = Second_Player((screen_width / 4, screen_height), screen_width, 5)
        self.player = pygame.sprite.GroupSingle(player_sprite)
        self.second_player = pygame.sprite.GroupSingle(second_player_sprite)

        # Health & score
        self.lives = 3
        self.second_player_lives = 3
        self.live_surf = pygame.image.load('Items/heart.jpg')
        self.live_x_start_pos = screen_width - (self.live_surf.get_size()[0] * 2 + 20)
        self.live_2_x_start_pos = screen_width - (self.live_surf.get_size()[0] * 2 + 20)
        self.score = 0
        self.second_score = 0
        self.font = pygame.font.Font('Items/Black_Crayon.ttf', 40)

        # Create aliens
        self.aliens = pygame.sprite.Group()
        self.alien_lasers = pygame.sprite.Group()
        self.alien_setup(rows=5, cols=5)
        self.alien_direction = 1

        # Audio
        music = pygame.mixer.Sound('Items/game_music.mp3')
        music.set_volume(1)
        music.play(loops=1)
        self.ship_destruction = pygame.mixer.Sound('Items/explosion.mp3')
        self.ship_destruction.set_volume(0.3)
        self.alien_destruction = pygame.mixer.Sound('Items/missile_hit.mp3')
        self.alien_destruction.set_volume(0.3)
        self.alien_laser_sound = pygame.mixer.Sound('Items/missile_launch.mp3')
        self.alien_laser_sound.set_volume(0.5)

    def make_background(self):
        # Load images
        space = pygame.image.load("Items/space.jpg").convert()

        # Cover screen with space images
        for x in range(0, screen_width, space.get_width()):
            for y in range(0, screen_height, space.get_height()):
                screen.blit(space, (x, y))

    def alien_setup(self, rows, cols, x_distance=90, y_distance=50, x_offset=0, y_offset=100):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset
                alien_sprite = Alien(x, y)
                self.aliens.add(alien_sprite)

    def alien_positions_checker(self):
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.right >= screen_width + 75:
                self.alien_direction = -1
                self.alien_move_down(2)
            if alien.rect.left <= -75:
                self.alien_direction = 1
                self.alien_move_down(2)

    def alien_move_down(self, distance):
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y += distance

    def alien_shoot(self):
        if self.aliens.sprites():
            random_alien = choice(self.aliens.sprites())
            laser_sprite = Alien_Laser(random_alien.rect.center, 6, screen_height)
            self.alien_lasers.add(laser_sprite)
            self.alien_laser_sound.play()

    def collision_checks(self):

        # Player lasers
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                aliens_hit = pygame.sprite.spritecollide(laser, self.aliens, True)
                if aliens_hit:
                    self.alien_destruction.play()
                    laser.kill()
                    for alien in aliens_hit:
                        self.score += alien.value

        # Second Player lasers
        if self.second_player.sprite.lasers:
            for laser in self.second_player.sprite.lasers:
                aliens_hit = pygame.sprite.spritecollide(laser, self.aliens, True)
                if aliens_hit:
                    self.alien_destruction.play()
                    laser.kill()
                    for alien in aliens_hit:
                        self.second_score += alien.value

        # Alien lasers
        if self.alien_lasers:
            for laser in self.alien_lasers:
                if pygame.sprite.spritecollide(laser, self.player, False):
                    self.ship_destruction.play()
                    laser.kill()
                    self.lives -= 1
                    if self.lives <= 0:
                        pygame.quit()
                        sys.exit()
                if pygame.sprite.spritecollide(laser, self.second_player, False):
                    self.ship_destruction.play()
                    laser.kill()
                    self.second_player_lives -= 1
                    if self.second_player_lives <= 0:
                        pygame.quit()
                        sys.exit()

        # Aliens
        if self.aliens:
            for alien in self.aliens:
                if pygame.sprite.spritecollide(alien, self.player, False):
                    pygame.quit()
                    sys.exit()
                if pygame.sprite.spritecollide(alien, self.second_player, False):
                    pygame.quit()
                    sys.exit()

    def display_lives(self):
        for live in range(self.lives - 1):
            x = self.live_x_start_pos + (live * self.live_surf.get_size()[0] + 10)
            screen.blit(self.live_surf, (x, 8))
        for live in range(self.second_player_lives - 1):
            x = self.live_2_x_start_pos + (live * self.live_surf.get_size()[0] + 10)
            screen.blit(self.live_surf, (x, 30))

    def display_score(self):
        score_surf = self.font.render(f'Score: {self.score}', False, 'white')
        second_score_surf = self.font.render(f'Player 2 Score: {self.second_score}', False, 'white')
        score_rect = score_surf.get_rect(topleft=(0, 0))
        second_score_rect = second_score_surf.get_rect(topleft=(0, 30))
        screen.blit(score_surf, score_rect)
        screen.blit(second_score_surf, second_score_rect)

    def victory(self):
        if not self.aliens.sprites():
            player_1_victory_surf = self.font.render('Player 1 Won', False, 'white')
            player_2_victory_surf = self.font.render('Player 2 Won', False, 'white')
            player_1_victory_rect = player_1_victory_surf.get_rect(center=(screen_width / 2, screen_height / 2))
            player_2_victory_rect = player_2_victory_surf.get_rect(center=(screen_width / 2, screen_height / 2))
            if self.score > self.second_score:
                screen.blit(player_1_victory_surf, player_1_victory_rect)
            if self.second_score > self.score:
                screen.blit(player_2_victory_surf, player_2_victory_rect)

    def run(self):
        self.make_background()
        self.player.update()
        self.second_player.update()
        self.aliens.update(self.alien_direction)
        self.alien_positions_checker()
        self.alien_lasers.update()
        self.collision_checks()
        self.player.sprite.lasers.draw(screen)
        self.second_player.sprite.lasers.draw(screen)
        self.player.draw(screen)
        self.second_player.draw(screen)
        self.aliens.draw(screen)
        self.alien_lasers.draw(screen)
        self.display_lives()
        self.display_score()
        self.victory()


if __name__ == '__main__':
    pygame.init()
    screen_width = 800
    screen_height = 800
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    game = Game()

    ALIENLASER = pygame.USEREVENT + 1
    pygame.time.set_timer(ALIENLASER, 800)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == ALIENLASER:
                game.alien_shoot()

        screen.fill((30, 30, 30))
        game.run()

        pygame.display.flip()
        clock.tick(60)
