import sys
import pygame
import os
import random
from trialConstant import *
from trialClass import * 

def countdown(player, obstacles, clouds, background):
    large_font = pygame.font.Font(FONT_PATH, 75)
    greyColor = (80, 80, 80)
    count = 3
    while count > 0:
        # Draw the game background
        SCREEN.fill((255, 255, 255))
        background()
        for cloud in clouds:
            cloud.draw(SCREEN)
        for obstacle in obstacles:
            obstacle.draw(SCREEN)
        player.draw(SCREEN)
        player.draw_hearts(SCREEN)
        
        # Draw the countdown
        count_text = large_font.render(str(count), True, greyColor)  
        count_rect = count_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))  
        pygame.draw.rect(SCREEN, (255, 255, 255), count_rect)  
        SCREEN.blit(count_text, count_rect)
        
        pygame.display.update()
        pygame.time.delay(1000)
        count -= 1
    
    # "GO!" text
    go_text = large_font.render("GO!", True, greyColor)
    go_rect = go_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
    pygame.draw.rect(SCREEN, (255, 255, 255), go_rect)
    SCREEN.blit(go_text, go_rect)
    pygame.display.update()
    pygame.time.delay(500)

def pause_screen(player, obstacles, clouds, background):
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:  # Resume game if 'W' is pressed
                    paused = False
                elif event.key == pygame.K_q:  # Quit game if 'Q' is pressed
                    pygame.quit()
                    sys.exit()

        # Display pause screen
        SCREEN.fill((255, 255, 255))
        background()
        for cloud in clouds:
            cloud.draw(SCREEN)
        for obstacle in obstacles:
            obstacle.draw(SCREEN)
        player.draw(SCREEN)
        player.draw_hearts(SCREEN)

        pause_text = FONT.render("PAUSED", True, (0, 0, 0))
        resume_text = FONT.render("Press 'W' to Resume", True, (0, 0, 0))
        quit_text = FONT.render("Press 'Q' to Quit", True, (0, 0, 0))

        SCREEN.blit(pause_text, pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 250)))
        SCREEN.blit(resume_text, resume_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 170)))
        SCREEN.blit(quit_text, quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200)))

        pygame.display.update()
        clock.tick(30)

    # After unpausing, show countdown
    countdown(player, obstacles, clouds, background)  


def menu():
    global SCREEN, FONT, high_score
    isQuit = False

    while not isQuit:
        # Display starting text
        menu_text = FONT.render("\"Press any key to begin\"", True, (0, 0, 0))
        text_rect = menu_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        SCREEN.fill((255, 255, 255))
        SCREEN.blit(menu_text, text_rect)

        # Display high score
        high_score_text = FONT.render(f"High Score: {high_score}", True, (0, 0, 0))
        high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        SCREEN.blit(high_score_text, high_score_rect)

        pygame.display.flip()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                isQuit = True  # Exit the menu loop to start the game

def main():
    global points, obstacles, x_pos_bg, y_pos_bg, fg_game_speed, bg_game_speed, death_count, high_score
    run = True
    player = Dinosaur()
    obstacles = []
    clouds = [Cloud()]
    is_dead_animation = False
    fg_game_speed = INITIAL_GAME_SPEED  # Reset game speed at the start of each game

    def score():
        global points, fg_game_speed
        if not is_dead_animation:
            points += 1
            # Increase speed every SPEED_INCREMENT_INTERVAL points
            if points % SPEED_INCREMENT_INTERVAL == 0:
                fg_game_speed += SPEED_INCREMENT
        text = FONT.render("Points: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        SCREEN.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        if not is_dead_animation:
            image_width = DESERT_SAND.get_width()
            SCREEN.blit(DESERT_SAND, (x_pos_bg, y_pos_bg))
            SCREEN.blit(DESERT_SAND, (image_width + x_pos_bg, y_pos_bg))
            if x_pos_bg <= -image_width:
                SCREEN.blit(DESERT_SAND, (image_width + x_pos_bg, y_pos_bg))
                x_pos_bg = 0
            x_pos_bg -= fg_game_speed
        else:
            SCREEN.blit(DESERT_SAND, (x_pos_bg, y_pos_bg))
            SCREEN.blit(DESERT_SAND, (DESERT_SAND.get_width() + x_pos_bg, y_pos_bg))


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

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause_screen(player, obstacles, clouds, background)
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for obstacle in obstacles:
                    if isinstance(obstacle, Tumbleweed) and obstacle.is_clicked(pos):
                        break  # No need to remove here, we'll remove it in the main loop

        SCREEN.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()
        keyInput = pygame.mouse.get_pressed()

        if not is_dead_animation:
            player.update(userInput, keyInput)
        else:
            player.update_death_animation()

        player.draw(SCREEN)
        player.draw_hearts(SCREEN)  # Display hearts pictures

        if len(obstacles) == 0 and not is_dead_animation:
            obstacles.append(create_obstacle())

        obstacles_to_remove = []
        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            if not is_dead_animation:
                if obstacle.update() or (isinstance(obstacle, Tumbleweed) and obstacle.should_remove):
                    obstacles_to_remove.append(obstacle)
            if player.dino_rect.colliderect(obstacle.rect):
                if player.handle_collision():
                    is_dead_animation = True
                    player.start_death_animation()

        # Remove obstacles that are off-screen or clicked (for Tumbleweed)
        for obstacle in obstacles_to_remove:
            obstacles.remove(obstacle)

        # Add new obstacle if all are removed and not in death animation
        if len(obstacles) == 0 and not is_dead_animation:
            obstacles.append(create_obstacle())

        background()

        for cloud in clouds:
            cloud.draw(SCREEN)
            if not is_dead_animation:  # Pause cloud updates
                cloud.update()

        score()

        # Detecting the completion of the death animation
        if is_dead_animation and player.death_animation_done:
            pygame.time.delay(1000)
            death_count += 1

            # Update high score if points exceed current high score
            if points > high_score:
                high_score = points

            # Reset points for new game
            points = 0
            run = False

        clock.tick(30)
        pygame.display.update()
    
    fg_game_speed = INITIAL_GAME_SPEED

if __name__ == "__main__":
    pygame.init()
    while True:
        menu()
        main()