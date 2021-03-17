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
        for i in range(len(self.wave)-1,-1, -1):
            for j in range(len(self.wave[0])):
                unit = self.wave[i][j]
                if unit != "":
                    enemies.append(self._add_unit(self.wave[i][j], i, j, rows))
        return enemies

    def _add_unit(self, unit: str, posy: int, posx: int, rows: int) -> object:
        this_unit = characters.Enemies(unit)
        this_unit.left = 63+((this_unit.width+4)*posx)
        this_unit.top = SCREEN_HEIGHT+(this_unit.height*posy)+4
        return this_unit