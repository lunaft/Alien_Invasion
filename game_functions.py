import sys
from time import sleep

import pygame

from bullet import Bullet
from alien import Alien


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """Responder a los movimientos de teclas"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    """Responder a los movimientos de las teclas"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    """Responder a los movimientos de las teclas y del ratón"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(
                ai_settings,
                screen,
                stats,
                sb,
                play_button,
                ship,
                aliens,
                bullets,
                mouse_x,
                mouse_y,
            )


def check_play_button(
    ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y
):
    """Iniciar una nueva partida cuando el jugador haga clic en Play"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reinicia la configuración del juego
        ai_settings.initialize_dynamic_settings()

        #  Ocultar el cursor del ratón
        pygame.mouse.set_visible(False)

        # Restablecer las estadísticas del juego
        stats.reset_stats()
        stats.game_active = True

        # Restablecer las imágenes del marcador
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        #  Vacía la lista de aliens y balas
        aliens.empty()
        bullets.empty()

        # Crea una nueva flota y centra la nave
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def fire_bullet(ai_settings, screen, ship, bullets):
    """Dispara una bala, si aún no se ha alcanzado el límite"""
    # Crear una nueva bala, añadir al grupo de balas
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    """Actualizar imágenes en la pantalla, y pasar a la nueva pantalla"""
    # Redibuja la pantalla, en cada pasada por el bucle
    screen.fill(ai_settings.bg_color)

    # Redibuja todas las balas, detrás de la nave y los aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

     # Dibuja la puntuación
    sb.show_score()

    # Dibuja el botón de jugar si el juego está inactivo
    if not stats.game_active:
        play_button.draw_button()

    # Hacer visible la pantalla dibujada más recientemente
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Actualiza la posición de las balas, y deshazte de las balas viejas."""
    #  Actualizar las posiciones de las balas
    bullets.update()

    #  Deshazte de las balas que han desaparecido
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_high_score(stats, sb):
    """Comprueba si hay una nueva puntuación más alta"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def check_bullet_alien_collisions(
    ai_settings, screen, stats, sb, ship, aliens, bullets
):
    """Responde al choque de bala y alien"""
    # Elimina las balas y alienígenas que hayan colisionado
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # Si toda la flota es destruida, comienza un nuevo nivel
        bullets.empty()
        ai_settings.increase_speed()

        # Aumenta el nivel
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)


def check_fleet_edges(ai_settings, aliens):
    """Responde apropiadamente si algún alienígena ha alcanzado un borde"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet, and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Suelta toda la flota, y cambia la dirección de la flota"""
    if stats.ships_left > 0:
        # Disminuir naves de la izquierda
        stats.ships_left -= 1

        # Actualizar el marcador
        sb.prep_ships()

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

    # Vacía la lista de alienígenas y balas
    aliens.empty()
    bullets.empty()

    # Crea una nueva flota, y centra la nave
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()

    # Pausa
    sleep(0.5)


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Comprueba si algún alienígena ha llegado al fondo de la pantalla"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Trata esto igual que si la nave fuera golpeada
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """
     Comprueba si la flota está en un borde,
      entonces actualiza las posiciones de todos los alienígenas de la flota.
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    #   # Busca colisiones entre naves alienígenas.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)

    # Busca a los alienígenas en la parte inferior de la pantalla.
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)


def get_number_aliens_x(ai_settings, alien_width):
    """Determina el número de alienígenas que caben en una fila"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """Determina el número de filas de alienígenas que caben en la pantalla"""
    available_space_y = ai_settings.screen_height - (3 * alien_height) - ship_height
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Crea un alienígena y colócalo en la fila"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """Crea una flota completa de alienígenas"""
    # Crea un alien, y encuentra el número de aliens en una fila.
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # Crea la flota de alienígenas
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

