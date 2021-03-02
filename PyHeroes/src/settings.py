import os
import json
import arcade
# SETTINGS FOR THE GAME

def load_images(img: str) -> list:
    # load image from file, divide into 32x32 tiles
    # assign to character facing, DOWN, LEFT, RIGHT or UP
    filename = os.path.join(os.path.dirname(__file__), '..', 'assets',
                                             img+".png")
    images = {}
    for h in range(4):
        tmp = []
        for w in range(3):
            x, y = SPRITE_W*w, SPRITE_H*h
            tmp.append(arcade.load_texture(filename,
                                           x, y, 32, 32, False))
        images[["DOWN", "LEFT", "RIGHT", "UP"][h]] = tmp
    return images

# SCREEN SETTINGS AND TITLE
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
SCREEN_TITLE = "pyHeroes"

MOVEMENT_SPEED = 0.6
SPRITE_FPS = 5

SPRITE_W = 32
SPRITE_H = 32
SCALE = 1.1

# UNIT NAME AND PICTURE

# ENEMIES
ENEMIES_LIST = {}
with open(os.path.join(os.path.dirname(__file__), "..","data","enemies.json"),"r") as f:
    ENEMIES_LIST = json.load(f)
ENEMY_SPRITES = {k: load_images(v["img"]) for k, v in ENEMIES_LIST.items()}

# HEROES
HEROES_LIST = {}
with open(os.path.join(os.path.dirname(__file__), "..","data","heroes.json"),"r") as f:
    HEROES_LIST = json.load(f)
HEROES_SPRITES = {k: load_images(v["img"]) for k, v in HEROES_LIST.items()}