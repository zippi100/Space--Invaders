import pygame
import game_functions as gf
import random

from pygame.sprite import Group
from settings import Settings
from game_stats import GameStats
from ship import Ship
from alien import AlienFour

from button import Button
from scoreboard import Scoreboard
from start_screen import Titles
from start_screen import AlienPoints
from spritesheet import SpriteSheet


def run_game():

    # Initialize game
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Space Invaders The Game")
    spritesheet1 = SpriteSheet('SpriteSheets/alien1.png', screen)
    spritesheet2 = SpriteSheet('SpriteSheets/alien2.png', screen)
    spritesheet3 = SpriteSheet('SpriteSheets/alien3.png', screen)
    spritesheet4 = SpriteSheet('SpriteSheets/alien4.png', screen)
    spritesheet5 = SpriteSheet('SpriteSheets/player.png', screen)
    title1 = Titles(screen, "SPACE INVADERS", 0, (255, 0, 0))
    title2 = Titles(screen, "The Game", 50, (255, 255, 0))
    title3 = Titles(screen, "HIGH SCORES", 0, (200, 200, 200))

    alienpoints = AlienPoints(screen, spritesheet1, spritesheet2, spritesheet3, spritesheet4, ai_settings)

    play_button = Button(ai_settings, screen, "Play", ai_settings.screen_height * 0.75)
    high_score_button = Button(ai_settings, screen, "High Scores", ai_settings.screen_height * 0.85)
    back_button = Button(ai_settings, screen, "Back", ai_settings.screen_height * 0.85)

    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats, spritesheet5)

    # Make a ship.
    ship = Ship(ai_settings, screen, spritesheet5)
   
    bullets = Group()
    alien_bullets = Group()
    alien1 = Group()
    alien2 = Group()
    alien3 = Group()
    alien4 = AlienFour(ai_settings, screen, spritesheet4)

    # Creating the fleet of aliens
    gf.create_fleet(ai_settings, screen, ship, alien1, alien2, alien3, spritesheet1, spritesheet2, spritesheet3)

    while True:
        timer = pygame.time.Clock()
        timer.tick(60)
        gf.check_events(ai_settings, screen, stats, sb, play_button, high_score_button, ship, alien1, alien2, alien3,
                        bullets, alien_bullets, spritesheet1, spritesheet2, spritesheet3)

        if stats.game_active:
            if not alien4.active:
                if pygame.time.get_ticks() % 10 == 0:
                    if random.randint(1, 150) == 100:
                        alien4.active = True
                        alien4.blitme()
            ship.update()

            gf.update_bullets(ai_settings, screen, stats, sb, ship, alien1, alien2, alien3, alien4, bullets,
                              alien_bullets, spritesheet1, spritesheet2, spritesheet3)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, alien1, alien2, alien3, alien4, bullets,
                             alien_bullets, spritesheet1, spritesheet2, spritesheet3)
        gf.update_screen(ai_settings, screen, stats, sb, ship, alien1, alien2, alien3, alien4, bullets, alien_bullets,
                         play_button, high_score_button, back_button, title1, title2, title3, alienpoints)

run_game()

