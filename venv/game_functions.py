import sys

import random
import pygame

from pygame.sprite import Group
from time import sleep
from bullet import Bullet
from alien import AlienOne
from alien import AlienTwo
from alien import AlienThree
from bullet import AlienBullet


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        # Move the ship to the right
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, sb, play_button, high_score_button, ship, alien1, alien2, alien3,
                 bullets, alienbullets, spritesheet1, spritesheet2, spritesheet3):
    """Respond to keypresses and mouse events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, alien1, alien2, alien3, bullets,
                              alienbullets, mouse_x, mouse_y, spritesheet1, spritesheet2, spritesheet3)
            check_high_score_button(stats, sb, high_score_button, mouse_x, mouse_y)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def check_high_score_button(stats, sb, high_score_button, mouse_x, mouse_y):
    button_clicked = high_score_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not sb.highscores_active and not stats.game_active:
        sb.highscores_active = True
    elif button_clicked and sb.highscores_active:
        sb.highscores_active = False


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, alien1, alien2, alien3, bullets,
                      alienbullets, mouse_x, mouse_y, spritesheet1, spritesheet2, spritesheet3):

    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:

        ai_settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active = True

        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        alien1.empty()
        alien2.empty()
        alien3.empty()
        alienbullets.empty()
        bullets.empty()

        create_fleet(ai_settings, screen, ship, alien1, alien2, alien3, spritesheet1, spritesheet2, spritesheet3)
        ship.center_ship()


def update_screen(ai_settings, screen, stats, sb, ship, aliens1, aliens2, aliens3, alien4, bullets, alienbullets,
                  play_button, high_score_button, back_button, title1, title2, title3, alienpoints):

    screen.fill(ai_settings.bg_color)
    sb.show_score()
    if not ship.hit:
        ship.blitme()
    else:
        ship.blithit()

    if pygame.time.get_ticks() % 30 == 0:
        for alien1 in aliens1.sprites():
            alien1.next_frame()
        for alien2 in aliens2.sprites():
            alien2.next_frame()
        for alien3 in aliens3.sprites():
            alien3.next_frame()
        if alien4.active:
            alien4.next_frame()
        if alien4.destroyed:
            if alien4.msgtime % 5 == 0:
                alien4.destroyed = False
                alien4.msgtime += 1
    if alien4.destroyed:
        if alien4.msgtime % 5 != 0:
            alien4.blitdead()
    for alien1 in aliens1.sprites():
        alien1.blitme()
    for alien2 in aliens2.sprites():
        alien2.blitme()
    for alien3 in aliens3.sprites():
        alien3.blitme()
    if alien4.active:
        alien4.blitme()
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    for alienbullet in alienbullets.sprites():
        alienbullet.draw_bullet()

    if sb.highscores_active:
        screen.fill(ai_settings.start_color)
        if back_button.rect.collidepoint(pygame.mouse.get_pos()):
            back_button.button_color = ai_settings.button_hover_color
            back_button.text_color = ai_settings.text_hover_color
        else:
            back_button.button_color = ai_settings.button_color
            back_button.text_color = ai_settings.text_color
        for x in range(0, len(stats.high_score_list)):
            sb.show_high_score_list(stats.high_score_list, x)
        title3.draw()
        back_button.draw_button()

    elif not stats.game_active:
        if play_button.rect.collidepoint(pygame.mouse.get_pos()):
            play_button.button_color = ai_settings.button_hover_color
            play_button.text_color = ai_settings.text_hover_color
        elif high_score_button.rect.collidepoint(pygame.mouse.get_pos()):
            high_score_button.button_color = ai_settings.button_hover_color
            high_score_button.text_color = ai_settings.text_hover_color
        else:
            play_button.button_color = ai_settings.button_color
            play_button.text_color = ai_settings.text_color
            high_score_button.button_color = ai_settings.button_color
            high_score_button.text_color = ai_settings.text_color
        screen.fill(ai_settings.start_color)
        title1.draw()
        title2.draw()
        alienpoints.draw()
        play_button.draw_button()
        high_score_button.draw_button()

    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens1, aliens2, aliens3, alien4, bullets, alienbullets,
                       spritesheet1, spritesheet2, spritesheet3):
    """Update position of bullets and get rid of old bullets"""
    if pygame.time.get_ticks() % 30:
        for alien1 in aliens1:
            if random.randint(1, 1000) == 10:
                alien_bullet(ai_settings, screen, alien1, alienbullets)
        for alien2 in aliens2:
            if random.randint(1, 1000) == 10:
                alien_bullet(ai_settings, screen, alien2, alienbullets)
        for alien3 in aliens3:
            if random.randint(1, 1000) == 10:
                alien_bullet(ai_settings, screen, alien3, alienbullets)
        if alien4.active:
            if random.randint(1, 200) == 10:
                alien_bullet(ai_settings, screen, alien4, alienbullets)

    bullets.update()
    alienbullets.update()

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    for alienbullet in alienbullets.copy():
        if alienbullet.rect.bottom >= ai_settings.screen_height:
            alienbullets.remove(alienbullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens1, aliens2, aliens3, alien4, bullets,
                                  alienbullets, spritesheet1, spritesheet2, spritesheet3)
    check_bullet_ship_collisions(ai_settings, screen, stats, sb, ship, aliens1, aliens2, aliens3, alien4, bullets,
                                  alienbullets, spritesheet1, spritesheet2, spritesheet3)


def check_bullet_ship_collisions(ai_settings, screen, stats, sb, ship, aliens1, aliens2, aliens3, alien4, bullets,
                                 alienbullets, spritesheet1, spritesheet2, spritesheet3):
    ships = Group()
    ships.add(ship)
    collisions = pygame.sprite.groupcollide(ships, alienbullets, False, False)
    if collisions:
        ship_hit(ai_settings, screen, stats, sb, ship, aliens1, aliens2, aliens3, alien4, bullets, alienbullets,
                 spritesheet1, spritesheet2, spritesheet3)


def alien_bullet(ai_settings, screen, alien, alienbullets):
    new_bullet = AlienBullet(ai_settings, screen, alien)
    alienbullets.add(new_bullet)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens1, aliens2, aliens3, alien4,
                                  bullets, alienbullets, spritesheet1, spritesheet2, spritesheet3):
    aliens4 = Group()
    aliens4.add(alien4)
    collisions1 = pygame.sprite.groupcollide(bullets, aliens1, True, True)
    collisions2 = pygame.sprite.groupcollide(bullets, aliens2, True, True)
    collisions3 = pygame.sprite.groupcollide(bullets, aliens3, True, True)
    collisions4 = pygame.sprite.groupcollide(bullets, aliens4, True, True)
    if collisions1:
        for aliens1 in collisions1.values():
            stats.score += ai_settings.alien1_points * len(aliens1)

    elif collisions2:
        for aliens2 in collisions2.values():
            stats.score += ai_settings.alien2_points * len(aliens2)

    elif collisions3:
        for aliens3 in collisions3.values():
            stats.score += ai_settings.alien3_points * len(aliens3)

    elif collisions4:
        alien4.destroy(ai_settings, stats)

    sb.prep_score()
    check_high_score(stats, sb)

    if len(aliens1) == 0 and len(aliens2) == 0 and len(aliens3) == 0:
        bullets.empty()
        alienbullets.empty()
        alien4.destroy(ai_settings, stats)
        stats.score -= alien4.points
        alien4.destroyed = False
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, ship, aliens1, aliens2, aliens3, spritesheet1, spritesheet2, spritesheet3)
        ship.center_ship()

        stats.level += 1
        sb.prep_level()
        sleep(2)


def fire_bullet(ai_settings, screen, ship, bullets):
    # Create a new bullet and add it to the bullets group.
    if len(bullets) < ai_settings.bullets_allowed:

        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
    bullets.update()


def get_number_aliens_x(ai_settings, alien_width):
    """Determine the number of aliens that fit in a row."""
    available_space_x = ai_settings.screen_width - 3 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width) + 4)
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit to the screen."""
    available_space_y = (ai_settings.screen_height - (2 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien1(ai_settings, screen, aliens1, alien_number, row_number, spritesheet):
    alien1 = AlienOne(ai_settings, screen, spritesheet)
    alien1_width = alien1.rect.width
    alien1.x = alien1_width + 1.25 * alien1_width * alien_number
    alien1.rect.x = alien1.x
    alien1.rect.y = alien1.rect.height + 1.25 * alien1.rect.height * row_number
    aliens1.add(alien1)


def create_alien2(ai_settings, screen, aliens2, alien_number, row_number, spritesheet):
    alien2 = AlienTwo(ai_settings, screen, spritesheet)
    alien2_width = alien2.rect.width
    alien2.x = alien2_width + 1.25 * alien2_width * alien_number
    alien2.rect.x = alien2.x
    alien2.rect.y = alien2.rect.height + 1.25 * alien2.rect.height * row_number
    aliens2.add(alien2)


def create_alien3(ai_settings, screen, aliens3, alien_number, row_number, spritesheet):
    alien3 = AlienThree(ai_settings, screen, spritesheet)
    alien3_width = alien3.rect.width
    alien3.x = alien3_width + 1.25 * alien3_width * alien_number
    alien3.rect.x = alien3.x
    alien3.rect.y = alien3.rect.height + 1.25 * alien3.rect.height * row_number
    aliens3.add(alien3)


def create_fleet(ai_settings, screen, ship, aliens1, aliens2, aliens3, spritesheet1, spritesheet2, spritesheet3):
    alien = AlienOne(ai_settings, screen, spritesheet1)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    for row_number in range(int(number_rows/3)):
        for alien_number in range(number_aliens_x):
            create_alien3(ai_settings, screen, aliens3, alien_number, row_number, spritesheet3)
    for row_number in range(int(number_rows/3), int(number_rows*2/3)):
        for alien_number in range(number_aliens_x):
            create_alien2(ai_settings, screen, aliens2, alien_number, row_number, spritesheet2)
    for row_number in range(int(number_rows*2/3) + 1, int(number_rows) + 1):
        for alien_number in range(number_aliens_x):
            create_alien1(ai_settings, screen, aliens1, alien_number, row_number, spritesheet1)


def check_fleet_edges(ai_settings, aliens1, aliens2, aliens3):
    """Respond appropriately if any aliens have reached an edge"""
    check = 0
    for alien1 in aliens1.sprites():
        if alien1.check_edges():
            check = 1
            break
    if check != 1:
        for alien2 in aliens2.sprites():
            if alien2.check_edges():
                check = 1
                break
    if check != 1:
        for alien3 in aliens3.sprites():
            if alien3.check_edges():
                check = 1
                break
    if check == 1:
        change_fleet_direction(ai_settings, aliens1, aliens2, aliens3)


def change_fleet_direction(ai_settings, aliens1, aliens2, aliens3):
    """Drop the entire fleet and change the fleet's direction"""
    for alien1 in aliens1.sprites():
        alien1.rect.y += ai_settings.fleet_drop_speed
    for alien2 in aliens2.sprites():
        alien2.rect.y += ai_settings.fleet_drop_speed
    for alien3 in aliens3.sprites():
        alien3.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, screen, stats, sb, ship, alien1, alien2, alien3, alien4, bullets, alien_bullets,
                 spritesheet1, spritesheet2, spritesheet3):
    ship.hit = True

    for x in range(1, 11):
        update_screen(ai_settings, screen, stats, sb, ship, alien1, alien2, alien3, alien4, bullets, alien_bullets,
                      x, x, x, x, x, x, x)
        sleep(.4)

    if stats.ships_left > 0:
        stats.ships_left -= 1

        sb.prep_ships()
        alien_bullets.empty()
        bullets.empty()
        ship.center_ship()
        sleep(1)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
        for x in range(0, len(stats.high_score_list)):
            if stats.score > stats.high_score_list[x]:
                stats.high_score_list.insert(x, stats.score)
                stats.high_score_list.pop()
                break
        high_score_file = open("High_Scores.txt", "w")
        for x in range(0, len(stats.high_score_list) - 1):
            high_score_file.write(str(stats.high_score_list[x]) + "\n")
        high_score_file.write(str(stats.high_score_list[8]))
        high_score_file.close()
        print(list(map(str, stats.high_score_list)))


def update_aliens(ai_settings, screen, stats, sb, ship, alien1, alien2, alien3, alien4, bullets,
                  alien_bullets, spritesheet1, spritesheet2, spritesheet3):
    check_fleet_edges(ai_settings, alien1, alien2, alien3)
    alien1.update()
    alien2.update()
    alien3.update()
    if alien4.active:
        alien4.update()
        if alien4.rect.left == alien4.screen_rect.right:
            alien4.destroy(ai_settings, stats)
            stats.score -= alien4.points
            alien4.destroyed = False

    if pygame.sprite.spritecollideany(ship, alien1) or pygame.sprite.spritecollideany(ship, alien2) or \
            pygame.sprite.spritecollideany(ship, alien3):
        ship_hit(ai_settings, screen, stats, sb, ship, alien1, alien2, alien3, alien4, bullets, alien_bullets,
                 spritesheet1, spritesheet2, spritesheet3)

    check_aliens_bottom(ai_settings, screen, stats, sb, ship, alien1, alien2, alien3, alien4, bullets, alien_bullets,
                        spritesheet1, spritesheet2, spritesheet3)


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, alien1, alien2, alien3, alien4, bullets, alien_bullets,
                        spritesheet1, spritesheet2, spritesheet3):
    screen_rect = screen.get_rect()

    for alien1 in alien1.sprites():
        if alien1.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, screen, stats, sb, ship, alien1, alien2, alien3, alien4, bullets, alien_bullets,
                     spritesheet1, spritesheet2, spritesheet3)
            break
    for alien2 in alien2.sprites():
        if alien2.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, screen, stats, sb, ship, alien1, alien2, alien3, alien4, bullets, alien_bullets,
                     spritesheet1, spritesheet2, spritesheet3)
            break
    for alien3 in alien3.sprites():
        if alien3.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, screen, stats, sb, ship, alien1, alien2, alien3, alien4, bullets, alien_bullets,
                     spritesheet1, spritesheet2, spritesheet3)
            break


def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
