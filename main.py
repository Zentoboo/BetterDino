import sys
import pygame
import os
import random

pygame.init()

death_count = 0
high_score = 0

# Constants
LVL_LENGHT = 50
SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1nw.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoRun2nw.png"))]
JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJumpnw.png"))
DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1nw.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2nw.png"))]
DINO_DEAD = pygame.image.load(os.path.join("Assets/Dino", "DinoDead.png"))

SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

PTERODACTYLUS = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
                 pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

TUMBLEWEED = [pygame.image.load(os.path.join("Assets/Tumbleweed", "Tumbleweed1.png")),
              pygame.image.load(os.path.join("Assets/Tumbleweed", "Tumbleweed2.png")),
              pygame.image.load(os.path.join("Assets/Tumbleweed", "Tumbleweed3.png")),
              pygame.image.load(os.path.join("Assets/Tumbleweed", "Tumbleweed4.png"))]

PROJECTILE = [pygame.image.load(os.path.join("Assets/Projectile", "Projectile1.png")),
              pygame.image.load(os.path.join("Assets/Projectile", "Projectile2.png")),
              pygame.image.load(os.path.join("Assets/Projectile", "Projectile3.png")),
              pygame.image.load(os.path.join("Assets/Projectile", "Projectile4.png"))]

CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))

DESERT_SAND = pygame.image.load(os.path.join("Assets/Other", "Desert.png"))

FONT_SIZE = 25
FONT_PATH = "Assets/Font/PixelifySans-Regular.ttf"
FONT = pygame.font.Font(FONT_PATH, FONT_SIZE)

HEART_FULL = pygame.image.load(os.path.join("Assets/Heart", "Heart1.png"))
HEART_EMPTY = pygame.image.load(os.path.join("Assets/Heart", "Heart2.png"))

class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING
        self.dead_img = DINO_DEAD

        self.dinoDuck = False
        self.dinoRun = True
        self.dinoJump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.life_count = 3  # Initial life value is 3
        self.is_invincible = False  # Invincible state
        self.invincible_start_time = 0  # Invincible start time

        # Shrink heart pictures
        self.heart_full = pygame.transform.scale(HEART_FULL, (30, 30))
        self.heart_empty = pygame.transform.scale(HEART_EMPTY, (30, 30))

    def update(self, userInput, keyInput):
        global obstacles
        if self.dinoDuck:
            self.duck()
        if self.dinoRun:
            self.run()
        if self.dinoJump:
            self.jump(userInput)

        if self.step_index >= 10:
            self.step_index = 0

        if (userInput[pygame.K_UP] or userInput[pygame.K_w]) and not self.dinoJump:
            self.dinoDuck = False
            self.dinoRun = False
            self.dinoJump = True
        elif (userInput[pygame.K_DOWN] or userInput[pygame.K_s]) and not self.dinoJump:
            self.dinoDuck = True
            self.dinoRun = False
            self.dinoJump = False
        elif not (self.dinoJump or userInput[pygame.K_DOWN]):
            self.dinoDuck = False
            self.dinoRun = True
            self.dinoJump = False

        if keyInput[0]:
            pos = pygame.mouse.get_pos()
            for obstacle in obstacles:
                if isinstance(obstacle, Tumbleweed) and obstacle.is_clicked(pos):
                    obstacles.remove(obstacle)
                    break

        # Set the invincibility time to 2 seconds
        if self.is_invincible and (pygame.time.get_ticks() - self.invincible_start_time) > 2000:
            self.is_invincible = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self, userInput):
        self.image = self.jump_img  # Set image to jump_img when jumping
        if self.dinoJump:
            if not userInput[pygame.K_UP] and not userInput[pygame.K_w]:
                if self.jump_vel > 0:
                    self.jump_vel = 0  # Stop upward movement
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8

        if self.dino_rect.y >= self.Y_POS:
            self.dino_rect.y = self.Y_POS
            self.dinoJump = False  # Reset dinoJump when jump is complete
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        # Display flashing effect only during the first two collisions
        if self.life_count >= 1 and self.is_invincible:
            if (pygame.time.get_ticks() // 250) % 2 == 0:
                SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))
        else:
            SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

    def handle_collision(self):
        if not self.is_invincible:
            if self.life_count > 1:
                pygame.time.delay(300)
            self.life_count -= 1  # Decrease in life value
            self.is_invincible = True  # Enable invincibility
            self.invincible_start_time = pygame.time.get_ticks()  # Record invincibility start time
            if self.life_count == 0:
                return True
        return False

    def draw_hearts(self, SCREEN):
        # Display hearts pictures
        for i in range(3):
            if i < self.life_count:
                SCREEN.blit(self.heart_full, (30 + i * 40, 30))
            else:
                SCREEN.blit(self.heart_empty, (30 + i * 40, 30))

    def start_death_animation(self):
        self.image = self.dead_img
        self.is_jumping = False
        self.jump_velocity = 15
        self.is_dead_animation = True
        self.y_velocity = 15  # Initialise vertical velocity
        self.death_animation_done = False  # Initialising the death animation completion flag

    def update_death_animation(self):
        if self.is_dead_animation:
            self.dino_rect.y -= self.jump_velocity
            self.jump_velocity -= 1  # Simulation of gravitational acceleration

            if self.dino_rect.y >= 325:
                self.dino_rect.y = 325
                self.is_dead_animation = False
                self.y_velocity = 15  # Reset vertical speed for drop animation

        elif self.dino_rect.y < SCREEN_HEIGHT:
            self.dino_rect.y += self.y_velocity
            self.y_velocity += 1  # Accelerated descent

            if self.dino_rect.y >= SCREEN_HEIGHT:
                self.death_animation_done = True  # Animation complete.

class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(500, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= bg_game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


class Obstacle:  # parent class for obstacles
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= fg_game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, len(image) - 1)
        super().__init__(image, self.type)
        self.rect.y = 325


class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, len(image) - 1)
        super().__init__(image, self.type)
        self.rect.y = 300


class Pterodactylus(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 270
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        self.index += 1


class Tumbleweed(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, len(image) - 1)
        super().__init__(image, self.type)
        self.rect.y = random.randint(0, 325)
        self.index = 0
        self.y_velocity = -8  # Initial vertical velocity
        self.gravity = 0.5  # Gravity effect

    def draw(self, SCREEN):
        if self.index >= 20:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        self.index += 1

    def update(self):
        self.rect.x -= fg_game_speed

        # Bounce effect
        self.rect.y += self.y_velocity
        self.y_velocity += self.gravity

        # Check if the tumbleweed hits the ground and make it bounce
        if self.rect.y >= 320:
            self.rect.y = 320
            self.y_velocity = -abs(self.y_velocity) * 0.8  # Reduce velocity for bouncing effect

        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


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
    clock = pygame.time.Clock()
    player = Dinosaur()
    obstacles = []
    bg_game_speed = 5
    fg_game_speed = 14
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    clouds = [Cloud()]
    is_dead_animation = False  # Add a global variable for the death animation state

    def score():
        global points, fg_game_speed
        if not is_dead_animation:  # Pause score updates
            points += 1
            if points % LVL_LENGHT == 0:
                fg_game_speed += 1
        text = FONT.render("Points: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        SCREEN.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        if not is_dead_animation:  # Pause background movement
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

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for obstacle in obstacles:
                    if isinstance(obstacle, Tumbleweed) and obstacle.is_clicked(pos):
                        obstacles.remove(obstacle)
                        break

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
            obstacle_type = random.randint(0, 3)
            if obstacle_type == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif obstacle_type == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif obstacle_type == 2:
                obstacles.append(Pterodactylus(PTERODACTYLUS))
            elif obstacle_type == 3:
                obstacles.append(Tumbleweed(TUMBLEWEED))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            if not is_dead_animation:  # Pause obstacle updates
                obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect):
                if player.handle_collision():
                    is_dead_animation = True
                    player.start_death_animation()

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

if __name__ == "__main__":
    pygame.init()
    while True:
        menu()
        main()


