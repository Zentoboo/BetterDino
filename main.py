import sys
import pygame
import random
from varConstants import *
from entities import *

def drawPausedEntity(player, obstacles, clouds, background, projectiles):
    # Draw the game background
    SCREEN.fill((255, 255, 255))
    background(False)  # Do not move the background
    for cloud in clouds:
        cloud.draw(SCREEN)
    for obstacle in obstacles:
        if isinstance(obstacle, Tumbleweed) or isinstance(obstacle, Pterodactylus):
            obstacle.draw(SCREEN, True)
        else:
            obstacle.draw(SCREEN)
    for projectile in projectiles:
        projectile.draw(SCREEN, True)
    player.draw(SCREEN)
    player.draw_hearts(SCREEN)

def countdown(player, obstacles, clouds, background, projectiles):
    large_font = pygame.font.Font(FONT_PATH, 75)
    greyColor = (80, 80, 80)
    count = 3
    while count > 0:
        drawPausedEntity(player, obstacles, clouds, background, projectiles)

        # Draw the countdown
        count_text = large_font.render(str(count), True, greyColor)
        count_rect = count_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
        pygame.draw.rect(SCREEN, (255, 255, 255), count_rect)
        SCREEN.blit(count_text, count_rect)

        if is_music_playing:
            COUNT_SOUND.play()

        pygame.display.update()
        pygame.time.delay(1000)
        count -= 1

    # "GO!" text
    go_text = large_font.render("GO!", True, greyColor)
    if is_music_playing:
        GO_SOUND.play()
    go_rect = go_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
    pygame.draw.rect(SCREEN, (255, 255, 255), go_rect)
    SCREEN.blit(go_text, go_rect)
    pygame.display.update()
    pygame.time.delay(500)
    if is_music_playing:
        pygame.mixer.music.unpause()

def pause_screen(player, obstacles, clouds, background, projectiles):
    global paused, return_to_menu, is_music_playing
    paused = True
    return_to_menu = False

    sound_icon_rect = sound_on.get_rect(center=(1020, 50))

    while paused:
        if is_music_playing:
            pygame.mixer.music.pause()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Resume game if 'R' is pressed
                    paused = False
                elif event.key == pygame.K_q:  # Quit game if 'Q' is pressed
                    if is_music_playing:
                        QUIT_SOUND.play()
                    return_to_menu = True
                    if is_music_playing:
                        pygame.mixer.music.unpause()
                    paused = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if sound_icon_rect.collidepoint(event.pos):
                    is_music_playing = not is_music_playing
                    if is_music_playing:
                        pygame.mixer.music.unpause()
                    else:
                        pygame.mixer.music.pause()

        drawPausedEntity(player, obstacles, clouds, background, projectiles)

        pause_text = FONT.render("PAUSED", True, (0, 0, 0))
        resume_text = FONT.render("Press 'R' to Resume", True, (0, 0, 0))
        quit_text = FONT.render("Press 'Q' to Quit", True, (0, 0, 0))

        SCREEN.blit(pause_text, pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 250)))
        SCREEN.blit(resume_text, resume_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 170)))
        SCREEN.blit(quit_text, quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200)))

        if is_music_playing:
            SCREEN.blit(sound_on, sound_icon_rect)
        else:
            SCREEN.blit(sound_off, sound_icon_rect)

        pygame.display.update()
        clock.tick(30)

    # After unpausing, show countdown if not returning to menu
    if not return_to_menu:
        countdown(player, obstacles, clouds, background, projectiles)

def menu():
    global SCREEN, FONT, high_score, current_score, death_count, is_music_playing
    isQuit = False
    dino_index = 0
    dino_rect = MENU_DINO[0].get_rect()
    dino_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150)
    clock = pygame.time.Clock()

    # Load menu background music
    if is_music_playing:
        pygame.mixer.music.load(MENU_BG)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)  # Loop indefinitely

    while not isQuit:
        # White canvas
        SCREEN.fill((255, 255, 255))

        # Animate the dino
        SCREEN.blit(MENU_DINO[dino_index], dino_rect)
        dino_index = (dino_index + 1) % 2  # Alternate between 0 and 1

        # Display starting text
        menu_text = FONT.render("\"Press any key to begin\"", True, (0, 0, 0))
        text_rect = menu_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        SCREEN.blit(menu_text, text_rect)
        
        # Display high score
        high_score_text = FONT.render(f"High Score: {high_score}", True, (0, 0, 0))
        high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 0))
        SCREEN.blit(high_score_text, high_score_rect)

        # Display score
        current_score_text = FONT.render(f"Current Score: {current_score}", True, (0, 0, 0))
        current_score_rect = current_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        SCREEN.blit(current_score_text, current_score_rect)
        
        # Display death count
        death_count_text = FONT.render(f"Death Count: {death_count}", True, (0, 0, 0))
        death_count_rect = death_count_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
        SCREEN.blit(death_count_text, death_count_rect)

        # Draw sound icon based on current state
        sound_icon_rect = sound_on.get_rect(center=(1020, 50))
        if is_music_playing:
            SCREEN.blit(sound_on, sound_icon_rect)
        else:
            SCREEN.blit(sound_off, sound_icon_rect)

        pygame.display.flip()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                isQuit = True  # Exit the menu loop to start the game
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if sound_icon_rect.collidepoint(pos):
                    if is_music_playing:
                        SCREEN.blit(sound_on, sound_icon_rect)
                        pygame.mixer.music.stop()
                    else:
                        SCREEN.blit(sound_off, sound_icon_rect)
                        pygame.mixer.music.load(MENU_BG)
                        pygame.mixer.music.set_volume(0.5)
                        pygame.mixer.music.play(-1)
                    is_music_playing = not is_music_playing
        
        clock.tick(10)  # Control the animation speed
        pygame.display.update()

def main():
    global points, obstacles, x_pos_bg, y_pos_bg, fg_game_speed, bg_game_speed, death_count, high_score, current_score, return_to_menu, is_music_playing
    return_to_menu = False
    run = True
    player = Dinosaur()
    obstacles = []
    projectiles = []
    clouds = [Cloud()]
    is_dead_animation = False
    fg_game_speed = INITIAL_GAME_SPEED  # Reset game speed at the start of each game
    collision_detected = False

    # Stop menu background music if playing
    pygame.mixer.music.stop()

    if is_music_playing:
        pygame.mixer.music.load(PLAY_BG)
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)  # Loop indefinitely

    def score():
        global points, fg_game_speed
        if not is_dead_animation:
            points += 1
            # Increase speed every SPEED_INCREMENT_INTERVAL points
            if points % SPEED_INCREMENT_INTERVAL == 0:
                fg_game_speed += SPEED_INCREMENT
        # Display score
        score_text = FONT.render("Points: " + str(points), True, (0, 0, 0))
        score_text_rect = score_text.get_rect()
        score_text_rect.center = (1000, 40)
        SCREEN.blit(score_text, score_text_rect)
        
        # Display game speed
        game_speed_text = FONT.render("Game Speed: " + str(fg_game_speed-INITIAL_GAME_SPEED+1), True, (0, 0, 0))
        game_speed_text_rect = game_speed_text.get_rect()
        game_speed_text_rect.center = (300, 40)
        SCREEN.blit(game_speed_text, game_speed_text_rect)

    def background(move=True):
        global x_pos_bg, y_pos_bg
        image_width = DESERT_SAND.get_width()
        SCREEN.blit(DESERT_SAND, (x_pos_bg, y_pos_bg))
        SCREEN.blit(DESERT_SAND, (image_width + x_pos_bg, y_pos_bg))
        if is_dead_animation:
            move=False
        if move:
            if x_pos_bg <= -image_width:
                SCREEN.blit(DESERT_SAND, (image_width + x_pos_bg, y_pos_bg))
                x_pos_bg = 0
            x_pos_bg -= fg_game_speed

    def create_obstacle():
        obstacle_type = random.randint(0, 3)
        if obstacle_type == 0:
            return SmallCactus(SMALL_CACTUS)
        elif obstacle_type == 1:
            return LargeCactus(LARGE_CACTUS)
        elif obstacle_type == 2:
            return Pterodactylus(PTERODACTYLUS)
        elif obstacle_type == 3:
            return Tumbleweed(TUMBLEWEED)
    
    def create_projectile():
        pos = pygame.mouse.get_pos()
        dino_pos = player.getPosition()
        offset_dino_pos = (dino_pos[0] + 20, dino_pos[1] - 20)  # offset dino position
        if is_music_playing:
            SHOOT_SOUND.play()
        return Projectile(offset_dino_pos, pos, fg_game_speed, PROJECTILE)

    sound_icon_rect = sound_on.get_rect(center=(880, 40))
    
    def draw_and_update_animating_obstacles(obstacle, SCREEN, paused, fg_game_speed, obstacles_to_remove, is_dead_animation):
        obstacle.draw(SCREEN, paused)
        if not is_dead_animation and not paused:
            if obstacle.update(fg_game_speed, paused):
                obstacles_to_remove.append(obstacle)
        return is_dead_animation

    def draw_and_update_regular_obstacles(obstacle, SCREEN, fg_game_speed, obstacles_to_remove, is_dead_animation):
        obstacle.draw(SCREEN)
        if not is_dead_animation and not paused:
            if obstacle.update(fg_game_speed):
                obstacles_to_remove.append(obstacle)
        return is_dead_animation

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if is_music_playing:
                        PAUSE_SOUND.play()
                    pause_screen(player, obstacles, clouds, background, projectiles)
                    if return_to_menu:
                        run = False
                        break
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    if not is_dead_animation and not player.dinoJump and is_music_playing:
                        JUMP_SOUND.play()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if sound_icon_rect.collidepoint(event.pos):
                    is_music_playing = not is_music_playing
                    if is_music_playing:
                        pygame.mixer.music.load(PLAY_BG)
                        pygame.mixer.music.set_volume(0.3)
                        pygame.mixer.music.play(-1)  # Loop indefinitely
                    else:
                        pygame.mixer.music.pause()
                else:
                    projectiles.append(create_projectile())

        if not run:
            break

        SCREEN.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()
        keyInput = pygame.mouse.get_pressed()

        if not is_dead_animation and not paused:
            player.update(userInput, keyInput)
        else:
            player.update_death_animation()

        player.draw(SCREEN)
        player.draw_hearts(SCREEN)  # Display hearts pictures

        if player.shake_timer > 0:
            player.shake_timer -= 1

        if len(obstacles) == 0 and not is_dead_animation:
            obstacles.append(create_obstacle())

        projectiles_to_remove = []
        for projectile in projectiles:
            if not paused:
                projectile.update(paused)
            projectile.draw(SCREEN,paused)
            # Check if projectile collide with obstacle
            for obstacle in obstacles:
                if isinstance(obstacle, Tumbleweed) and projectile.rect.colliderect(obstacle.rect):
                    obstacle.should_remove = True
                    projectiles_to_remove.append(projectile)
                    if is_music_playing:
                        TUMBLEWEED_SOUND.play()
            # Check if projectile is offscreen
            if projectile.rect.right < 0 or projectile.rect.left > SCREEN_WIDTH or \
            projectile.rect.bottom < 0 or projectile.rect.top > SCREEN_HEIGHT:
                projectiles_to_remove.append(projectile)

        # Remove projectiles that hit a tumbleweed
        for projectile in projectiles_to_remove:
            projectiles.remove(projectile)

        obstacles_to_remove = []
        for obstacle in obstacles:
            if isinstance(obstacle, Tumbleweed) or isinstance(obstacle, Pterodactylus):
                is_dead_animation = draw_and_update_animating_obstacles(obstacle, SCREEN, paused, fg_game_speed, obstacles_to_remove, is_dead_animation)
            else:
                is_dead_animation = draw_and_update_regular_obstacles(obstacle, SCREEN, fg_game_speed, obstacles_to_remove, is_dead_animation)
            
            if player.dino_rect.colliderect(obstacle.rect):
                # Checks if the collision has been detected and if the remaining life value is greater than 1
                if not collision_detected and player.life_count > 1:
                    if is_music_playing:
                        COLLISION_SOUND.play()
                    collision_detected = True  # Set the flag to indicate that a collision has been detected
                if player.handle_collision():
                    pygame.mixer.music.stop()  # Stop game music on death
                    if is_music_playing:
                        DIE_SOUND.play()
                    is_dead_animation = True
                    player.start_death_animation()
            else:
                collision_detected = False  # Reset flag for no collision

        # Remove obstacles that are off-screen
        for obstacle in obstacles_to_remove:
            obstacles.remove(obstacle)

        # Add new obstacle if all are removed and not in death animation
        if len(obstacles) == 0 and not is_dead_animation:
            obstacles.append(create_obstacle())

        background()

        for cloud in clouds:
            cloud.draw(SCREEN)
            if not is_dead_animation and not paused:  # Pause cloud updates
                cloud.update()

        score()

        if is_music_playing:
            SCREEN.blit(sound_on, sound_icon_rect)
        else:
            SCREEN.blit(sound_off, sound_icon_rect)

        # Detecting the completion of the death animation
        if is_dead_animation and player.death_animation_done:
            pygame.time.delay(1000)
            death_count += 1

            # Update high score if points exceed current high score
            if points > high_score:
                high_score = points
            current_score = points

            # Reset points for new game
            points = 0
            run = False

        clock.tick(30)
        pygame.display.update()

    fg_game_speed = INITIAL_GAME_SPEED
    if return_to_menu:
        points = 0  # Reset points when returning to the menu

if __name__ == "__main__":
    pygame.init()
    while True:
        menu()
        main()