import json
import arcade
import utils

# SETTINGS FOR THE GAME
# SCREEN SETTINGS AND TITLE

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 1000
SCREEN_TITLE = "pyHeroes"

# Gui directory
GUI = "assets/gui"

MOVEMENT_SPEED = 4
SPRITE_FPS = 5

SPRITE_W = 32
SPRITE_H = 32
SCALE = 1.5

LAST_LEVEL = "3-0"
WORLDS = ["ONCE UPON A TIME...", "...A HERO HAS RISED", "GATHERING FRIENDS", "HARD BATTLES"]

# UNITS NAMES AND PICTURES
# ENEMIES
ENEMIES_LIST = {}

with open(utils.get_file_path("data", "enemies","json"), "r") as f:
    ENEMIES_LIST = json.load(f)
ENEMY_SPRITES = {k: utils.load_images(v["img"], SPRITE_W, SPRITE_H) for k, v in ENEMIES_LIST.items()}

# HEROES
HEROES_LIST = {}
with open(utils.get_file_path("data", "heroes","json"), "r") as f:
    HEROES_LIST = json.load(f)
HEROES_SPRITES = {k: utils.load_images(v["img"], SPRITE_W, SPRITE_H) for k, v in HEROES_LIST.items()}

# PROJECTILES NAMES AND PICTURES
PROJECTILES_LIST = {}
with open(utils.get_file_path("data", "attacks","json"), "r") as f:
    PROJECTILES_LIST = json.load(f)
PROJECTILES_IMGS = {k:arcade.load_texture(utils.get_file_path("assets",PROJECTILES_LIST[k]["media"],"png")) for k in PROJECTILES_LIST}