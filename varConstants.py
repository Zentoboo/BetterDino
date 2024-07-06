import pygame
import os

pygame.init()
pygame.mixer.init()

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

MENU_DINO = [
    pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
    pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))
]

SOUND_ON = pygame.image.load(os.path.join("Assets/Sound", "SoundOn.png"))
SOUND_OFF = pygame.image.load(os.path.join("Assets/Sound", "SoundOff.png"))
sound_on = pygame.transform.scale(SOUND_ON, (30, 30))
sound_off = pygame.transform.scale(SOUND_OFF, (30, 30))

COLLISION_SOUND = pygame.mixer.Sound('Assets/Sound/Collision.MP3')
DIE_SOUND = pygame.mixer.Sound('Assets/Sound/Die.wav')
JUMP_SOUND = pygame.mixer.Sound('Assets/Sound/Jump.MP3')
MENU_BG = 'Assets/Sound/Menuscreen BG.mp3'
PLAY_BG = 'Assets/Sound/Play BG.mp3'
SHOOT_SOUND = pygame.mixer.Sound('Assets/Sound/Shoot.mp3')
TUMBLEWEED_SOUND = pygame.mixer.Sound('Assets/Sound/Tumbleweed Scoring.mp3')
COUNT_SOUND = pygame.mixer.Sound('Assets/Sound/Count.wav')
GO_SOUND = pygame.mixer.Sound('Assets/Sound/Go.mp3')
PAUSE_SOUND = pygame.mixer.Sound('Assets/Sound/Pause.wav')
QUIT_SOUND = pygame.mixer.Sound('Assets/Sound/Pause.wav')

COLLISION_SOUND.set_volume(0.3)
DIE_SOUND.set_volume(0.5)
JUMP_SOUND.set_volume(0.3)
SHOOT_SOUND.set_volume(0.3)
TUMBLEWEED_SOUND.set_volume(0.2)
COUNT_SOUND.set_volume(1.5)

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
paused = False

INITIAL_GAME_SPEED = 14
SPEED_INCREMENT = 1
SPEED_INCREMENT_INTERVAL = 100  # Increase speed every 100 points

is_music_playing = True