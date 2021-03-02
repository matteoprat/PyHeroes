import arcade
import os
from settings import *

class Projectile(arcade.Sprite):

    def __init__(self, faction: str, projectile_name: str, x:float, y:float):
        super().__init__()
        
        self.texture = arcade.load_texture(PROJECTILES_IMGS[projectile_name])
        self.faction = faction
        self.speed = -PROJECTILES_LIST[projectile_name]["speed"] if self.faction == "Enemy" else PROJECTILES_LIST[projectile_name]["speed"]

        
