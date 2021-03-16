from level_selection_view import LevelSelectionView
from levels_editor_view import LevelEditorWorld
from gui_utils import MenuView
from settings import GUI

class TitleView(MenuView):

    def __init__(self, developer: int=0):
        super().__init__()
        self.developer = developer    
        self.level_selection = LevelSelectionView(self)
        self.options = OptionsView(self)
        self.reset = ResetView(self)
        self.dir = GUI+"/title"
        self.sprt_dir = GUI+"/title"
        self.lvl_editor = LevelEditorWorld(self)
        '''
        self.atk_editor = OptionsView(self, self.ui_manager)
        self.units_editor = ResetView(self, self.ui_manager)
        '''
        self.add_sprite(0, 0, "background", dir_=GUI)
        self.add_sprite(168, 827, "game_title", dir_=self.sprt_dir)
        self.add_sprite(317 ,666, "sprites", dir_=self.sprt_dir)

    def setup(self):
        self.window.ui_manager.purge_ui_elements()
        # Middle screen buttons: Play - Options - Reset
        self.add_view_button(400.0, 583.0, "btn_play", "Play", self.new_view, self.level_selection, y_align="top")
        self.add_view_button(400.0, 503.0, "btn_options", "Options", self.new_view, self.options, y_align="top")
        self.add_view_button(400.0, 423.0, "btn_reset", "Reset", self.reset_save_confirm, self.reset, y_align="top")
        
        if self.developer == 1:
            # Dev buttons bottom left area

            self.add_view_button(50.0, 137.0, "btn_level_editor", "Lvl_Editor", self.new_view, self.lvl_editor, x_align="left", y_align="bottom")
            self.add_view_button(50.0, 98.0, "btn_units_editor", "Units_Editor", self.new_view, self.level_selection, x_align="left", y_align="bottom")
            self.add_view_button(50.0, 59.0, "btn_attacks_editor", "Atk_Editor", self.new_view, self.options, x_align="left", y_align="bottom")

    def reset_save_confirm(self, unused):
        self.add_gui_box(122, 451, "background_reset", "left", "bottom", GUI+"/level_edit/confirmation_window")
        self.add_view_button(252, 477, "btn_no", "No_Btn", self.window_abort, 1, "left", "bottom", dir_ = GUI+"/level_edit/confirmation_window")
        self.add_view_button(551, 477, "btn_yes", "Yes_Btn", self.delete_confirm, 1, "right", "bottom", dir_ = GUI+"/level_edit/confirmation_window")

    def window_abort(self, unused) -> None:
        self.setup()

    def delete_confirm(self, world: int) -> None:
        
        self.setup()

class OptionsView(MenuView):

    def __init__(self, parent: object):
        super().__init__()
        self.title = parent
        self.dir = GUI+"/title"
        self.sprt_dir = GUI+"/title"
        self.add_sprite(0, 0, "background", dir_=GUI)
        self.add_sprite(168, 827, "game_title", dir_=self.sprt_dir)
        self.add_sprite(317 ,666, "sprites", dir_=self.sprt_dir)

    def setup(self):
        self.add_view_button(400.0, 583.0, "btn_play", "Play", self.new_view, self.title, y_align="top")
   
class ResetView(MenuView):

    def __init__(self, parent: object):
        super().__init__()
        self.title = parent
        self.dir = GUI+"/title"
        self.sprt_dir = GUI+"/title"
        self.add_sprite(0, 0, "background", dir_=GUI)
        self.add_sprite(168, 827, "game_title", dir_=self.sprt_dir)
        self.add_sprite(317 ,666, "sprites", dir_=self.sprt_dir)
    
    def setup(self):
        self.add_view_button(400.0, 583.0, "btn_play", "Play", self.new_view, self.title, y_align="top")