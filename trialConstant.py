import sys
import pygame
import os
import random

pygame.init()

# Constants
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

# Global variables
clock = pygame.time.Clock()
death_count = 0
high_score = 0
current_score = 0
points = 0
obstacles = []
x_pos_bg = 0
y_pos_bg = 380
fg_game_speed = 14
bg_game_speed = 5

INITIAL_GAME_SPEED = 14
SPEED_INCREMENT = 1
SPEED_INCREMENT_INTERVAL = 100  # Increase speed every 100 points