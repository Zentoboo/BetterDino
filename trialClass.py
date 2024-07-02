import sys
import pygame
import os
import random
from trialConstant import *

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


class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self,obstacle_speed):
        self.rect.x -= obstacle_speed
        if self.rect.x < -self.rect.width:
            return True  # Signal that this obstacle should be removed
        return False

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
        self.should_remove = False  # New flag to indicate if the tumbleweed should be removed

    def update(self,obstacle_speed):
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

    def is_clicked(self, pos):
        if self.rect.collidepoint(pos):
            self.should_remove = True
            return True
        return False