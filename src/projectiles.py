import arcade
from settings import PROJECTILES_LIST, PROJECTILES_IMGS


class Projectile(arcade.Sprite):

    def __init__(self, faction: str, projectile_name: str, dmg: int, x: float, y: float):
        super().__init__()
        self.name = projectile_name
        self.texture = PROJECTILES_IMGS[self.name]
        self.movement = PROJECTILES_LIST[self.name]["movement"]
        self.faction = faction
        self.yspeed, self.xspeed = self._get_speed
        self.damage = dmg
        self.damage_type = dmg
        self.scale = 0.5
        self._set_starting_position(x,y)
        
    @property
    def _get_speed(self) -> tuple:
        if self.faction == "Hero":
            return (PROJECTILES_LIST[self.name]["yspeed"],PROJECTILES_LIST[self.name]["xspeed"])
        else:
            return (-PROJECTILES_LIST[self.name]["yspeed"],PROJECTILES_LIST[self.name]["xspeed"])

    def _set_starting_position(self, x, y) -> None:
        if self.faction == "Hero":
            self.bottom = y + 1
        else:
            self.top = y - 1
        self.center_x = x

    def move(self) -> tuple:
        if self.movement == "parabolic":
            if self.xspeed >= 10 or self.xspeed == 0:
                self.xspeed = 0
                self.yspeed = PROJECTILES_LIST[self.name]["yspeed"]
            else:
                self.xspeed += 1
        self.top += self.yspeed
        self.left += self.xspeed
        return (self.top, self.left)