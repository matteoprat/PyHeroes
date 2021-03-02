import arcade
from settings import *
import characters

class EnemyWave():
    def __init__(self, wave_map: list) -> None:
        self.wave = wave_map
        self.enemies_list = self._spawn_enemies()

    @property
    def get_enemies(self) -> list:
        return self.enemies_list
    
    def _spawn_enemies(self) -> list:
        enemies = []
        rows = len(self.wave)
        for i in range(len(self.wave)):
            for j in range(len(self.wave[0])):
                unit = self.wave[i][j]
                if unit != "":
                    enemies.append(self._add_unit(self.wave[i][j], i, j, rows))
        return enemies

    def _add_unit(self, unit: str, posy: int, posx: int, rows: int) -> object:
        this_unit = characters.Enemies(unit)
        this_unit.center_x = (SCREEN_WIDTH-(3*(SPRITE_W*SCALE)))//2+(posx*(SPRITE_W*SCALE))
        this_unit.center_y = (SCREEN_HEIGHT-(SPRITE_H*rows))+posy*(SPRITE_W*SCALE)
        return this_unit