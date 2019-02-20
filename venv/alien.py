import pygame
import pygame.ftfont
import random
from pygame.sprite import Sprite


class AlienOne(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_settings, screen, spritesheet):
        """Initialize the alien and set its starting position."""
        super(AlienOne, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        self.frame = 0
        self.image_sizes = ((24, 23, 82, 57), (155, 25, 82, 57), (15, 150, 105, 75), (134, 144, 110, 80))
        self.images = spritesheet.images_at(self.image_sizes, colorkey=(255, 255, 255))

        self.rect = self.images[0].get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact posittion.
        self.x = float(self.rect.x)

    def blitme(self):
        """Draw the alien at its current location."""
        self.screen.blit(self.images[self.frame], self.rect)

    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """Move the alien right."""
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def next_frame(self):
        self.frame += 1
        if self.frame == 2:
            self.frame = 0


class AlienTwo(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_settings, screen, spritesheet):
        """Initialize the alien and set its starting position."""
        super(AlienTwo, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        self.frame = 0
        self.image_sizes = ((29, 13, 82, 78), (161, 13, 82, 78), (155, 85, 80, 60), (25, 140, 105, 90),
                            (150, 140, 100, 95), (20, 265, 95, 100))
        self.images = spritesheet.images_at(self.image_sizes, colorkey=(255, 255, 255))

        self.rect = self.images[0].get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact posittion.
        self.x = float(self.rect.x)

    def blitme(self):
        """Draw the alien at its current location."""
        self.screen.blit(self.images[self.frame], self.rect)

    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """Move the alien right."""
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def next_frame(self):
        self.frame += 1
        if self.frame == 2:
            self.frame = 0


class AlienThree(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_settings, screen, spritesheet):
        """Initialize the alien and set its starting position."""
        super(AlienThree, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        self.frame = 0
        self.image_sizes = ((17, 10, 88, 83), (145, 7, 88, 83), (8, 132, 118, 108),
                            (139, 132, 118, 108), (15, 258, 118, 108), (137, 259, 118, 108))
        self.images = spritesheet.images_at(self.image_sizes, colorkey=(255, 255, 255))

        self.rect = self.images[0].get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact posittion.
        self.x = float(self.rect.x)

    def blitme(self):
        """Draw the alien at its current location."""
        self.screen.blit(self.images[self.frame], self.rect)

    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """Move the alien right."""
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def next_frame(self):
        self.frame += 1
        if self.frame == 2:
            self.frame = 0


class AlienFour(Sprite):

    def __init__(self, ai_settings, screen, spritesheet):
        """Initialize the alien and set its starting position."""
        super(AlienFour, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.text = (200, 200, 200)
        self.font = pygame.font.SysFont(None, 24)

        self.frame = 0
        self.image_sizes = ((16, 26, 90, 50), (145, 30, 90, 50), (18, 163, 90, 50), (150, 150, 100, 75))
        self.images = spritesheet.images_at(self.image_sizes, colorkey=(255, 255, 255))

        self.rect = self.images[0].get_rect()
        self.screen_rect = screen.get_rect()
        self.msg_rect = pygame.Rect(0, 0, 0, 0)
        self.rect.right = self.screen_rect.left
        self.rect.y = self.rect.height/4

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.oscillate = -1
        self.active = False
        self.destroyed = False
        self.msgtime = 1
        self.points = 0
        self.direction = False

    def blitme(self):
        """Draw the alien at its current location."""
        self.screen.blit(self.images[self.frame], self.rect)

    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):

        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            self.direction = True
            self.y += 10
            self.rect.y = self.y

        elif self.rect.left <= 0:
            self.direction = False

        if not self.direction:
            self.x += self.ai_settings.alien_speed_factor
            self.rect.x = self.x

        else:
            self.x -= self.ai_settings.alien_speed_factor
            self.rect.x = self.x

    def next_frame(self):
        self.frame += 1
        if self.frame == 2:
            self.frame = 0

    def destroy(self, ai_settings, stats):
        self.points = int(random.randint(8, 10) * ai_settings.score_scale * 10)
        stats.score += self.points
        self.msg_rect.center = self.rect.center
        self.x = self.screen_rect.left
        self.rect.right = self.x
        self.active = False
        self.destroyed = True

    def blitdead(self):
        self.screen.blit(self.font.render(str(self.points), True, self.text), self.msg_rect)
        if pygame.time.get_ticks() % 30 == 0:
            self.msgtime += 1
