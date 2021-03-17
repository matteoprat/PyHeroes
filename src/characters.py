'''
Created on 24 feb 2021

@author: Matteo Pratellesi
'''
import arcade
import projectiles
from settings import *
from typing import Union

class Character(arcade.Sprite):
    def __init__(self, unit_name: str, unit_type: str, direction: str):
        super().__init__()
                   
        # Default character facing
        self.character_face_direction = direction
        
        self.cur_texture = 0
        self.scale = SCALE
        self.name = unit_name
        self.type = unit_type
        
        # Load textures for walking
        if unit_type == "Hero":
            self.walk_textures = HEROES_SPRITES[unit_name]
        elif unit_type == "Enemy":
            self.walk_textures = ENEMY_SPRITES[unit_name]
        self.texture = self.walk_textures[self.character_face_direction][self.cur_texture]

    def update_animation(self, delta_time: float = 1/60) -> None:

        # Figure out if we need to flip face up or down
        self.hp_bar()

        if self.change_y < 0 and self.character_face_direction != "DOWN" and self.type=="Enemy":
            self.character_face_direction = "DOWN"
        elif self.change_y > 0 and self.character_face_direction != "UP":
            self.character_face_direction = "UP"
        
        # Idle animation
        if self.change_x == 0 and self.change_y == 0:
            self.character_face_direction = "UP" if self.type == "Hero" else "DOWN"
            self.texture = self.walk_textures[self.character_face_direction][1]
            return

        # Walking animation
        self.cur_texture += 1
        if self.cur_texture == 3:
            self.cur_texture = 0
        self.frame = self.cur_texture
        
        self.texture = self.walk_textures[self.character_face_direction][self.frame]

    def hp_bar(self) -> None:
        up = self.bottom+(self.height*(self.current_hp/self.hp))
        arcade.draw_line(self.left-3, self.bottom, self.left-3, self.bottom+self.height, arcade.color.RED, 4)
        arcade.draw_line(self.left-3, self.bottom, self.left-3, up, arcade.color.GREEN, 4)

    def fire(self) -> Union[None, object]:
        self.active_atk_cooldown -= 1
        if self.active_atk_cooldown == 0:
            self.active_atk_cooldown = self.atk_cooldown
            if self.active == True:
                if self.type == "Hero":
                    projectile = projectiles.Projectile(self.type, self.atk_type, self.atk_dmg, self.center_x, self.top)
                else:
                    projectile = projectiles.Projectile(self.type, self.atk_type, self.atk_dmg, self.center_x, self.bottom)
                return projectile
            else:
                return None

    def take_damage(self, projectile) -> None:
        if self.active == True:
            new_hp = self.current_hp - projectile.damage
            self.current_hp = new_hp if new_hp > 0 else 0

    def killed(self):
        self.active = False

class Heroes(Character):
    def __init__(self, unit_name: str, unit_type: str="Hero", direction:str ="UP"):
        super().__init__(unit_name, unit_type, direction)
        self.hp = HEROES_LIST[unit_name]["hp"]
        self.current_hp = HEROES_LIST[unit_name]["hp"]

        self.active = True
        self.atk_type = HEROES_LIST[unit_name]["atk_type"]
        self.atk_dmg = HEROES_LIST[unit_name]["dmg"]
        self.atk_cooldown = HEROES_LIST[unit_name]["cooldown"]
        self.active_atk_cooldown = HEROES_LIST[unit_name]["cooldown"]

class Enemies(Character):
    def __init__(self,unit_name: str, unit_type="Enemy", direction="DOWN"):
        super().__init__(unit_name, unit_type, direction)
        self.speed = -ENEMIES_LIST[unit_name]["speed"]
        self.movement_counter = 0

        self.hp = ENEMIES_LIST[unit_name]["hp"]
        self.current_hp =  ENEMIES_LIST[unit_name]["hp"]
        self.active = False

        self.atk_type = ENEMIES_LIST[unit_name]["atk_type"]
        self.atk_dmg = ENEMIES_LIST[unit_name]["dmg"]
        self.atk_cooldown = ENEMIES_LIST[unit_name]["cooldown"]
        self.active_atk_cooldown = ENEMIES_LIST[unit_name]["cooldown"]

        self.gold = ENEMIES_LIST[unit_name]["gold"]
        self.xp = ENEMIES_LIST[unit_name]["xp"]
    
    def update_position(self) -> None:
        self.movement_counter += 1
        if self.movement_counter == 5:
            self.change_y += self.speed
            self.update_animation()
            self.movement_counter = 0
            if self.active == False:
                if self.bottom <= SCREEN_HEIGHT:
                    self.active = True