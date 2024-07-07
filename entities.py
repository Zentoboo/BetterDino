import pygame
import random
import math
from varConstants import *

# Dinosaur class for managing the dino character
class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5

    def __init__(self):
        # Load images for different dino states
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING
        self.dead_img = DINO_DEAD

        # Initialize dino state flags
        self.dinoDuck = False
        self.dinoRun = True
        self.dinoJump = False

        # Additional states for aiming and invincibility
        self.aim = False
        self.prev_a_pressed = False
        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.life_count = 3  # Initial life value is 3
        self.is_invincible = False  # Invincible state
        self.invincible_start_time = 0  # Invincible start time
        self.shake_timer = 0
        self.shake_duration = 15  # Number of frames the jitter lasts
        self.shake_amplitude = 5  # Amplitude of shaking

        # Shrink heart pictures
        self.heart_full = pygame.transform.scale(HEART_FULL, (30, 30))
        self.heart_empty = pygame.transform.scale(HEART_EMPTY, (30, 30))

    # Get the position of the dino
    def getPosition(self):
        return self.dino_rect.center
    
    # Update the state of the dino based on user input
    def update(self, userInput, keyInput):
        if self.dinoDuck:
            self.duck()
        if self.dinoRun:
            self.run()
        if self.dinoJump:
            self.jump(userInput)
        if self.aim:
            self.aimShot()

        if self.step_index >= 10:
            self.step_index = 0

        # Jumping logic
        if (userInput[pygame.K_UP] or userInput[pygame.K_w]) and not self.dinoJump:
            self.dinoDuck = False
            self.dinoRun = False
            self.dinoJump = True
        # Ducking logic
        elif (userInput[pygame.K_DOWN] or userInput[pygame.K_s]) and not self.dinoJump:
            self.dinoDuck = True
            self.dinoRun = False
            self.dinoJump = False
        # Running logic
        elif not (self.dinoJump or userInput[pygame.K_DOWN]):
            self.dinoDuck = False
            self.dinoRun = True
            self.dinoJump = False

        # Toggling aiming mode
        if userInput[pygame.K_a] and not self.prev_a_pressed:
            self.aim = not self.aim
        
        self.prev_a_pressed = userInput[pygame.K_a]

        # Invincibility duration
        if self.is_invincible and (pygame.time.get_ticks() - self.invincible_start_time) > 2000:
            self.is_invincible = False

    # Draw aiming line
    def aimShot(self):
        mouse_pos = pygame.mouse.get_pos()
        offset_dino_pos = (self.dino_rect.center[0]+20, self.dino_rect.center[1]-20)
        pygame.draw.line(SCREEN, (255,0,0), offset_dino_pos, mouse_pos, 2)

    # Ducking state update
    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    # Running state update
    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    # Jumping state update
    def jump(self, userInput):
        self.image = self.jump_img
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

    # Draw the dino
    def draw(self, SCREEN):
        # Display flashing effect only during the first two collisions
        if self.life_count >= 1 and self.is_invincible:
            if (pygame.time.get_ticks() // 250) % 2 == 0:
                SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))
        else:
            SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))
        
    # Handle collision with obstacles
    def handle_collision(self):
        if not self.is_invincible:
            self.shake_timer = self.shake_duration  # Starting to shake.
            if self.life_count > 1:
                pygame.time.delay(300)
            self.life_count -= 1  # Decrease in life value
            self.is_invincible = True  # Enable invincibility
            self.invincible_start_time = pygame.time.get_ticks()  # Record invincibility start time
            if self.life_count == 0:
                return True
        return False

    # Draw hearts representing lives
    def draw_hearts(self, SCREEN):
        for i in range(3):
            x = 30 + i * 40
            y = 30
            if self.shake_timer > 0:
                x += random.randint(-self.shake_amplitude, self.shake_amplitude)
                y += random.randint(-self.shake_amplitude, self.shake_amplitude)
            if i < self.life_count:
                SCREEN.blit(self.heart_full, (x, y))
            else:
                SCREEN.blit(self.heart_empty, (x, y))

    # Start death animation
    def start_death_animation(self):
        self.image = self.dead_img
        self.is_jumping = False
        self.jump_velocity = 15
        self.is_dead_animation = True
        self.y_velocity = 15  # Initialise vertical velocity
        self.death_animation_done = False  # Initialising the death animation completion flag

    # Update death animation
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

# Cloud class for managing the cloud obstacles
class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(500, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    # Update cloud position
    def update(self):
        self.x -= bg_game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(500, 3000)
            self.y = random.randint(50, 100)

    # Draw the cloud
    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))

# Base obstacle class
class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    # Update obstacle position
    def update(self, obstacle_speed):
        self.rect.x -= obstacle_speed
        if self.rect.x < -self.rect.width:
            return True  # Signal that this obstacle should be removed
        return False

    # Draw the obstacle
    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)

# Small cactus obstacle class
class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, len(image) - 1)
        super().__init__(image, self.type)
        self.rect.y = 325

# Large cactus obstacle class
class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, len(image) - 1)
        super().__init__(image, self.type)
        self.rect.y = 300

# Pterodactylus obstacle class
class Pterodactylus(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 270
        self.index = 0

    # Update Pterodactylus position and animation
    def update(self, obstacle_speed, paused):
        if paused:
            return False
        self.rect.x -= obstacle_speed
        if self.rect.x < -self.rect.width:
            return True  # Signal that this obstacle should be removed
        return False

    # Draw Pterodactylus with animation
    def draw(self, SCREEN, paused):
        if paused:
            SCREEN.blit(self.image[self.index // 5], self.rect)
            return
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        self.index += 1

# Tumbleweed obstacle class
class Tumbleweed(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, len(image) - 1)
        super().__init__(image, self.type)
        self.rect.y = random.randint(0, 325)
        self.index = 0
        self.y_velocity = -8  # Initial vertical velocity
        self.gravity = 0.5  # Gravity effect
        self.should_remove = False  # New flag to indicate if the tumbleweed should be removed

    # Update Tumbleweed position and bouncing effect
    def update(self, obstacle_speed, paused):
        if not paused:
            self.rect.x -= obstacle_speed

            # Bounce effect
            self.rect.y += self.y_velocity
            self.y_velocity += self.gravity

            # Check if the tumbleweed hits the ground and make it bounce
            if self.rect.y >= 320:
                self.rect.y = 320
                self.y_velocity = -abs(self.y_velocity) * 0.8  # Reduce velocity for bouncing effect

            if self.rect.x < -self.rect.width:
                self.should_remove = True  # Set flag to True instead of modifying the obstacles list

            return self.should_remove  # Return the flag

    # Draw Tumbleweed with animation
    def draw(self, SCREEN, paused):
        if paused:  # Skip updating animation if paused
            SCREEN.blit(self.image[self.index // 5], self.rect)
            return
        if self.index >= 19:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        self.index += 1

# Helper function to find the angle between sprite and mouse positions
def findAngle(sprite_pos, mouse_pos):
    dx = mouse_pos[0] - sprite_pos[0]
    dy = mouse_pos[1] - sprite_pos[1]
    try:
        angle = math.atan2(dy, dx)
    except ZeroDivisionError:
        angle = math.pi / 2  # Default to pi/2 (90 degrees) if dx is zero

    return angle

# Projectile class for managing projectiles fired by the dino
class Projectile(object):
    def __init__(self, sprite_pos, mouse_pos, projectile_speed, image):
        self.index = 0
        self.angle = findAngle(sprite_pos, mouse_pos)
        self.projectile_speed = projectile_speed
        self.image = image
        self.rect = self.image[0].get_rect()
        self.rect.x = sprite_pos[0]
        self.rect.y = sprite_pos[1]
        self.x_velocity = math.cos(self.angle) * self.projectile_speed
        self.y_velocity = math.sin(self.angle) * self.projectile_speed

    # Update projectile position
    def update(self, paused):
        if not paused:
            self.rect.x += self.x_velocity
            self.rect.y += self.y_velocity

    # Draw projectile with animation
    def draw(self, SCREEN, paused):
        if paused:  # Skip updating animation if paused
            SCREEN.blit(self.image[self.index // 5], self.rect)
            return
        if self.index >= 19:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        self.index += 1
