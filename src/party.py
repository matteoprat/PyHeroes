from settings import *

class Party():
    def __init__(self) -> None:
        self.positions =[["" for i in range(3)] for j in range(3)]
        self.formation = None
        self.left = 0
        self.right = 0
        self.top = 0
        self.bottom = 0
        self.size = 0

    def add_unit(self, unit: object, posy: int, posx: int) -> None:
        self.positions[posy][posx] = unit
        unit.center_x = (SCREEN_WIDTH-(3*(SPRITE_W*SCALE)))//2+(posx*(SPRITE_W*SCALE))
        unit.center_y = 200-posy*(SPRITE_W*SCALE)
        self.size += 1

    def del_unit(self, unit: object) -> None:
        for i in range(3):
            for j in range(3):
                if self.positions[i][j] == unit:
                    self.position[i][j] = ""

    @property
    def list_units(self) -> list:
        units = []
        for i in range(3):
            for j in range(3):
                unit = self.positions[i][j]
                if unit != "":
                    units.append(unit)
        return units

    def get_party_boundaries(self, units: list) -> None:
        tmp_left, tmp_right, tmp_top, tmp_bottom = SCREEN_WIDTH, 0, 0, SCREEN_HEIGHT
        for unit in units:
            tmp_left = min(unit.left, tmp_left)
            tmp_right = max(unit.right, tmp_right)
            tmp_top = max(unit.top, tmp_top)
            tmp_bottom = min(unit.bottom, tmp_bottom)
        self.left = tmp_left
        self.right = tmp_right
        self.top = tmp_top
        self.bottom = tmp_bottom
        