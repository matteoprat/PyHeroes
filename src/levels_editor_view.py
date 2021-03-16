import arcade
import utils
from gui_utils import MenuView
from settings import GUI, ENEMY_SPRITES

class LevelEditorWorld(MenuView):
    def __init__(self, parent: object):
        super().__init__()
        self.dir = GUI+"/level_edit/common"
        self.world_dir = GUI+"/level_edit/world"
        self.sprt_dir = GUI+"/level_edit/world"
        self.confirmation_dir = GUI+"/level_edit/confirmation_window"
        self.title = parent
        self.page = 0
        self.level_selection = LevelEditorLevels(self)
        self.button_locked = utils.get_file_path(self.sprt_dir,"sprt_disabled_button","png")

    def setup(self):
        self.load_fixed_elements()
        self.window.ui_manager.purge_ui_elements()
        self.add_view_button(335, 42.0, "btn_title", "Title", self.new_view, self.title, x_align="left", y_align="bottom")
        
        # create the world selection
        
        y_margin, y_distance = 732, 152
        x_margin, x_distance = 94, 156

        # draw 4x4 grid with either buttons or sprite
        
        id = 0
        for row in range(4):

            for col in range(4):
                x = x_margin+(x_distance*col)
                y = y_margin-(y_distance*row)
            
                # delete button positions
                dx = x + 105
                dy = y - 10
            
                # edit name button positions
                ex = x +40
                ey = y - 83
            
                if id <= self.window.max_world:
                    self.add_view_button(x, y, "btn_world", "Lvl"+str(id), self.load_world, id, x_align="left", y_align="top", dir_=self.world_dir)
                    self.add_view_button(ex, ey, "btn_rename", "Edit"+str(id), self.edit_world_name, (self.page*16)+id, x_align="left", y_align="top")
            
                    if (self.page*16)+id > 0:
                        self.add_view_button(dx, dy, "btn_delete", "Del"+str(id), self.del_world, (self.page*16)+id, x_align="left", y_align="top")
            
                else:
                    self.add_disabled_world((x,y))
            
                    if (self.page*16)+id-1 == self.window.max_world:
                        self.add_view_button(x+54, y-53, "btn_add", "Add"+str(id), self.add_world, int(self.window.max_world)+1, x_align="left", y_align="top")
                id+=1

    def add_disabled_world(self, pos: tuple) -> None:
        sprt = arcade.Sprite(self.button_locked)
        sprt.left, sprt.top = pos
        self.sprites.append(sprt)

    def load_fixed_elements(self) -> None:
        self.add_sprite(0,0, "background", dir_ = GUI)
        self.add_sprite(245,893, "sprt_game_name", dir_ = self.sprt_dir)
        self.add_sprite(535,893, "sprt_heroes", dir_ = self.sprt_dir)
        self.add_sprite(94,775, "sprt_world_editor", dir_ = self.sprt_dir)

    def load_world(self, world):
        self.level_selection.world = world
        self.new_view(self.level_selection)

    def edit_world_name(self, world: int) -> None:
        self.add_gui_box(122, 451, "background_edit", "left", "bottom", self.confirmation_dir)
        input_box = self.add_input_box(160, 475, 327,47, self.window.levels[world]["Title"], "left", "bottom")
        self.add_view_button(510.9, 475, "btn_confirm", "Confirm_Btn", self.edit_confirm, [self.window.levels, world, input_box], "left", "bottom", dir_=self.confirmation_dir)

    def del_world(self, world: int) -> None:
        self.add_gui_box(122, 451, "background", "left", "bottom", self.confirmation_dir)
        self.add_label(408, 570, f"WORLD {world}")
        self.add_view_button(252, 477, "btn_no", "No_Btn", self.window_abort, world, "left", "bottom", dir_ = self.confirmation_dir)
        self.add_view_button(551, 477, "btn_yes", "Yes_Btn", self.delete_confirm, world, "right", "bottom", dir_ = self.confirmation_dir)

    def add_world(self, world: int) -> None:
        self.window.levels, self.window.max_world = utils.add_world(world, self.window.levels)
        self.edit_world_name(world)

    def window_abort(self, params) -> None:
        self.setup()

    def delete_confirm(self, world: int) -> None:
        self.window.levels, self.window.max_world = utils.del_world(world, self.window.levels)
        self.setup()

    def edit_confirm(self, params) -> None:
        self.window.levels = utils.edit_world_name(params)
        self.setup()

class LevelEditorLevels(MenuView):
    def __init__(self, parent: object):
        super().__init__()
        self.dir = GUI+"/level_edit/common"
        self.world_dir = GUI+"/level_edit/world"
        self.sprt_dir = GUI+"/level_edit/world"
        self.confirmation_dir = GUI+"/level_edit/confirmation_window"
        self.world_select = parent
        self.stage_wave = WavesEditor(self)
        self.world = 0
        self.button_locked = utils.get_file_path(self.sprt_dir,"sprt_disabled_button","png")
        self.load_fixed_elements()

    def load_fixed_elements(self) -> None:
        self.add_sprite(0,0, "background", dir_ = GUI)
        self.add_sprite(245,893, "sprt_game_name", dir_ = self.sprt_dir)
        self.add_sprite(535,893, "sprt_heroes", dir_ = self.sprt_dir)
        self.add_sprite(94,775, "sprt_level_editor", dir_ = self.sprt_dir)

    def setup(self) -> None:
        max_level = utils.max_level(self.window.levels, self.world)
        self.load_fixed_elements()
        self.window.ui_manager.purge_ui_elements()
        self.add_view_button(335, 42.0, "btn_back", "Title", self.new_view, self.world_select, x_align="left", y_align="bottom")
        
        # create the world selection
        
        y_margin, y_distance = 732, 152
        x_margin, x_distance = 94, 156

        # draw 4x4 grid with either buttons or sprite
        
        id = 0
        for row in range(4):

            for col in range(4):
                x = x_margin+(x_distance*col)
                y = y_margin-(y_distance*row)
            
                # delete button positions
                dx = x + 105
                dy = y - 10
            
                if id <= max_level:
                    self.add_view_button(x, y, "btn_world", "Lvl"+str(id), self.load_level, id, x_align="left", y_align="top", dir_=self.world_dir, text=str(id+1))
                    self.add_view_button(dx, dy, "btn_delete", "Del"+str(id), self.del_level, id, x_align="left", y_align="top")
            
                else:
                    self.add_empty_level((x,y))
                    if id == max_level+1:
                        self.add_view_button(x+54, y-53, "btn_add", "Add"+str(id), self.add_level, id, x_align="left", y_align="top")
                id+=1

    def add_empty_level(self, pos: tuple) -> None:
        sprt = arcade.Sprite(self.button_locked)
        sprt.left, sprt.top = pos
        self.sprites.append(sprt)

    def load_level(self, param):
        self.stage_wave.stage = self.window.levels[self.world]["Levels"][param]
        self.new_view(self.stage_wave)

    def del_level(self, lvl_n: int) -> None:
        self.window.levels[self.world]["Levels"] = utils.delete_stage_from_world(self.window.levels[self.world]["Levels"], lvl_n)
        utils.write_world(self.window.levels)
        self.setup()

    def add_level(self, lvl_n: int) -> None:
        self.window.levels[self.world]["Levels"] = utils.add_stage(self.window.levels[self.world]["Levels"])
        utils.write_world(self.window.levels)
        self.setup()

class WavesEditor(MenuView):
    def __init__(self, parent: object):
        super().__init__()
        self.dir = GUI+"/level_edit/common"
        self.world_dir = GUI+"/level_edit/world"
        self.sprt_dir = GUI+"/level_edit/world"
        self.confirmation_dir = GUI+"/level_edit/confirmation_window"
        self.stage_select = parent
        self.selected_unit = ""
        self.stage = ""
        self.button_locked = utils.get_file_path(self.sprt_dir,"sprt_wave_disabled_button","png")
        self.edit = 0
        self.current_wave = 0
        self.units_ = [[k,v["DOWN"][1]] for k, v in ENEMY_SPRITES.items()]
        self.load_fixed_elements()

    def load_fixed_elements(self) -> None:
        self.add_sprite(0,0, "background", dir_ = GUI)
        self.add_sprite(245,893, "sprt_game_name", dir_ = self.sprt_dir)
        self.add_sprite(535,893, "sprt_heroes", dir_ = self.sprt_dir)
        self.add_sprite(94,775, "sprt_wave_editor", dir_ = self.sprt_dir)

    def setup(self) -> None:
        self.window.ui_manager.purge_ui_elements()
        self.load_fixed_elements()

        if self.edit == 0:
            self.load_screen_0()

        else:
            self.load_screen_1()

    def load_screen_0(self) -> None:
        self.waves = utils.load_waves(self.stage)
        max_wave = utils.max_wave(self.waves)
        self.add_view_button(335, 42.0, "btn_back", "Title", self.new_view, self.stage_select, x_align="left", y_align="bottom")
            
        # create the world selection
            
        y_margin, y_distance = 743, 102
        x_margin, x_distance = 94, 103

        # draw 4x4 grid with either buttons or sprite
            
        id = 0
        for row in range(6):

            for col in range(6):
                x = x_margin+(x_distance*col)
                y = y_margin-(y_distance*row)
                
                # delete button positions
                dx = x + 61
                dy = y - 8
                
                if id <= max_wave:
                    self.add_view_button(x, y, "btn_wave", "Lvl"+str(id), self.load_wave, id, x_align="left", y_align="top", dir_=self.world_dir, text=str(id+1))
                    self.add_view_button(dx, dy, "btn_delete_small", "Del"+str(id), self.del_wave, id, x_align="left", y_align="top")
                
                else:
                    self.add_empty_wave_icon((x,y))
                    if id == max_wave+1:
                        self.add_view_button(x+28, y-28, "btn_add", "Add"+str(id), self.add_wave, id, x_align="left", y_align="top")
                id+=1
    
    def load_screen_1(self):
        
        if self.selected_unit == "":
            self.selected_unit = self.units_[0][0]
        self.wave = utils.load_waves(self.stage)[self.current_wave]
        this_dir = GUI+"/level_edit/wave"
        
        # GUI fixed elements / Sprites
        self.add_sprite(36, 149, "sprt_background", dir_ = this_dir)
        self.add_sprite(50.4, 368, "sprt_grid", dir_ = this_dir)
        self.add_sprite(50.4, 165, "sprt_units_grid", dir_ = this_dir)

        # GUI Buttons - SAVE / CANCEL
        self.add_view_button(608, 231, "btn_save", "save_btn", self.save_wave, self.current_wave, x_align="left", y_align="bottom", dir_=this_dir)
        self.add_view_button(608, 170, "btn_cancel", "cancel_btn", self.load_default, 1, x_align="left", y_align="bottom", dir_=this_dir)

        # GUI Buttons - Units
        x_margin, x_distance = 181, 53
        y_margin, y_distance = 280, 59

        unit_id = 0
        for i in range(2):
            for j in range(7):
                this_sprite = self.units_[unit_id]
                x = x_margin + (j*x_distance)
                y = y_margin - (i*y_distance)
                self.add_unit_button(x,y, this_sprite[1], unit_id, self.select_sprite, this_sprite[0], x_align="left", y_align="top")
                unit_id += 1
        self.add_unit_selected(111, 231, ENEMY_SPRITES[self.selected_unit]["DOWN"][1])


    def select_sprite(self, name: str):
        self.selected_unit = name
        self.setup()

    def add_empty_wave_icon(self, pos: tuple) -> None:
        sprt = arcade.Sprite(self.button_locked)
        sprt.left, sprt.top = pos
        self.sprites.append(sprt)

    def load_wave(self, id: int):
        self.current_wave = id
        self.edit = 1
        self.setup()

    def del_wave(self, wave_n: int) -> None:
        self.waves = utils.del_wave(self.waves, wave_n)
        utils.write_wave(self.stage, self.waves)
        self.setup()

    def save_wave(self, param):
        pass

    def load_default(self, param):
        self.edit = 0
        self.setup()

    def add_wave(self, lvl_n: int) -> None:
        #self.window.levels[self.world]["Levels"] = utils.add_stage(self.window.levels[self.world]["Levels"])
        #utils.write_world(self.window.levels)
        #self.setup()
        pass


    
