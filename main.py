import pygame
import os
import random

pygame.init()

# Constants

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]
JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))
DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]

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

CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))

DESERT_SAND = pygame.image.load(os.path.join("Assets/Other", "Desert.png"))

FONT = pygame.font.Font(None, 36)


class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dinoDuck = False
        self.dinoRun = True
        self.dinoJump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self, userInput):
        if self.dinoDuck:
            self.duck()
        if self.dinoRun:
            self.run()
        if self.dinoJump:
            self.jump(userInput)

        if self.step_index >= 10:
            self.step_index = 0

        if userInput[pygame.K_UP] and not self.dinoJump:
            self.dinoDuck = False
            self.dinoRun = False
            self.dinoJump = True
        elif userInput[pygame.K_DOWN] and not self.dinoJump:
            self.dinoDuck = True
            self.dinoRun = False
            self.dinoJump = False
        elif not (self.dinoJump or userInput[pygame.K_DOWN]):
            self.dinoDuck = False
            self.dinoRun = True
            self.dinoJump = False

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
            if not userInput[pygame.K_UP]:
                if self.jump_vel > 0:
                    self.jump_vel = 0  # Stop upward movement
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8

        if self.dino_rect.y >= self.Y_POS:
            self.dino_rect.y = self.Y_POS
            self.dinoJump = False  # Reset dinoJump when jump is complete
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


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


class Obstacle: # parent class for obstacles
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
    def __init__(self,image):
        self.type = random.randint(0,len(image) - 1)
        super().__init__(image, self.type)
        self.rect.y = 325

        
class LargeCactus(Obstacle):
    def __init__(self,image):
        self.type = random.randint(0,len(image) - 1)
        super().__init__(image, self.type)
        self.rect.y = 300


class Pterodactylus(Obstacle):
    def __init__(self,image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0
    def draw(self,SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1

class Tumbleweed(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, len(image) - 1)
        super().__init__(image, self.type)
        self.rect.y = 325
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 20:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        if self.index % 5 == 0:
            self.rect.y = 310 if self.rect.y == 325 else 325
        self.index += 1

def start_screen():
    SCREEN.fill((255, 255, 255))
    text = FONT.render("Press any key to start", True, (0, 0, 0))
    SCREEN.blit(text, (SCREEN_WIDTH // 2 - text.get_width() //
                2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                waiting = False


def main():
    global bg_game_speed, fg_game_speed, x_pos_bg, y_pos_bg, obstacles
    run = True  # game start
    clock = pygame.time.Clock()
    player = Dinosaur()
    clouds = [Cloud() for _ in range(3)]
    fg_game_speed = 14
    bg_game_speed = 3
    x_pos_bg = 0
    y_pos_bg = 380
    obstacles = []

    start_screen()  # Display start screen

    def background():
        global x_pos_bg, y_pos_bg
        image_width = DESERT_SAND.get_width()
        SCREEN.blit(DESERT_SAND, (x_pos_bg, y_pos_bg))
        SCREEN.blit(DESERT_SAND, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(DESERT_SAND, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= fg_game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()

        player.draw(SCREEN)
        player.update(userInput)

        if len(obstacles) == 0:
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
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect):
                pygame.draw.rect(SCREEN, (255, 0, 0), player.dino_rect, 2)

        background()

        for cloud in clouds:  # Update and draw each cloud
            cloud.draw(SCREEN)
            cloud.update()

        clock.tick(30)
        pygame.display.update()

if __name__ == "__main__":
    main()