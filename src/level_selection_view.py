import arcade
import arcade.gui
from gui_utils import MenuView
import utils
from settings import GUI


class LevelSelectionView(MenuView):
    def __init__(self, parent):
        super().__init__()
        self.window.game.level_view = self
        self.dir = GUI+"/level_selection"
        self.sprt_dir = GUI+"/level_selection"
        self.title = parent
        self.show_world = 0
        self.game = self.window.game
        self.button_locked = utils.get_file_path(GUI+self.sprt_dir,"sprt_lvl_locked","png")
    
    def setup(self):
        self.load_fixed_elements()
        self.add_label(104.9, 872, f"WORLD {self.show_world}: {self.window.levels[self.show_world]['Title']}", x_align="left", y_align="top")

        self.add_view_button(96.0, 110.0, "btn_upgrades", "Upgrades", self.new_view, self.title, x_align="left", y_align="bottom")
        self.add_view_button(573, 110.0, "btn_party", "Party", self.new_view, self.title, x_align="left", y_align="bottom")
        self.add_view_button(96, 44.0, "btn_title", "Title", self.new_view, self.title, x_align="left", y_align="bottom")

        # create the level selection
        # retrieving data of last unlocked world / level
        max_level = self.window.game.last_level.split("-")
        world = int(max_level[0])
        stage = int(max_level[1])
        y_margin, y_distance = 791, 154
        x_margin, x_distance = 94.6, 158
        # draw 4x4 grid with either buttons or sprite
        id = 0
        for row in range(4):
            for col in range(4):
                x = x_margin+(x_distance*col)
                y = y_margin-(y_distance*row)
                
                if world > self.show_world or (world == self.show_world and id <= stage):
                    self.add_view_button(x, y, "btn_lvl", "Lvl"+str(id), self.load_level, str(self.show_world)+"-"+str(id), x_align="left", y_align="top", text=str(self.show_world)+"-"+str(id+1))
                else:
                    self.add_disabled_level((x,y))
                
                id+=1

        # add arrows
        if self.show_world <= 0:
            self.add_sprite(236.0, 109, "sprt_prev_disabled", dir_ = self.sprt_dir)
        else:
            self.add_view_button(236.0, 109, "btn_prev_active", "Prev", self.reload_screen, -1, x_align="left", y_align="bottom")
        
        if self.show_world >= world:
            self.add_sprite(408, 109, "sprt_next_disabled", dir_ = self.sprt_dir)
        else:
            self.add_view_button(408, 109, "btn_next_active", "Next", self.reload_screen, 1, x_align="left", y_align="bottom")

    def add_disabled_level(self, pos: tuple) -> None:
        sprt = arcade.Sprite(self.button_locked)
        sprt.left, sprt.top = pos
        self.sprites.append(sprt)
        
    def load_fixed_elements(self) -> None:
        self.add_sprite(0,0,"background", dir_=GUI)
        self.add_sprite(83.61, 171, "sprt_btn_background", dir_=self.sprt_dir)
        self.add_sprite(266.49, 45,"sprt_game_name",dir_=self.sprt_dir)
        self.add_sprite(83.16, 810, "sprt_title",dir_=self.sprt_dir)

    def load_level(self, stage: str) -> None:
        world, level = stage.split("-")
        self.window.game.world = int(world)
        self.window.game.level = int(level)
        self.ui_manager.purge_ui_elements()
        self.window.game.setup()
        self.window.show_view(self.window.game)

    def reload_screen(self, n: int) -> None:
        self.show_world += n
        self.ui_manager.purge_ui_elements()
        self.setup()