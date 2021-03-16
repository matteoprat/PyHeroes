import arcade
import arcade.gui
import utils
import os
dummy_texture = arcade.load_texture(utils.get_file_path("assets/gui/title","btn_play_normal","png"))

class SwitchViewButton(arcade.gui.UIImageButton):
    
    def __init__(self, dir_:str, texture:str, id: str, command, params):
        super().__init__(dummy_texture)
        self.id = id
        self.normal_texture = arcade.load_texture(utils.get_file_path(dir_,texture+"_normal","png"))
        self.hover_texture = arcade.load_texture(utils.get_file_path(dir_,texture+"_hover","png"))
        self.press_texture = arcade.load_texture(utils.get_file_path(dir_,texture+"_pressed","png"))
        self.action = command
        self.params = params
    
    def on_click(self):
        self.action(self.params)

class UnitButton(arcade.gui.UIImageButton):
    
    def __init__(self, texture:object, id: str, command, params):
        super().__init__(dummy_texture)
        self.id = id
        self.normal_texture = texture
        self.hover_texture = self.normal_texture
        self.press_texture = self.normal_texture
        self.scale = 1.2
        self.action = command
        self.params = params
    
    def on_click(self):
        self.action(self.params)

class GuiBox(arcade.gui.UIImageButton):
    def __init__(self, dir_: str, texture: str):
        super().__init__(dummy_texture)
        self.texture = arcade.load_texture(utils.get_file_path(dir_, texture,"png"))
        self.normal_texture = self.texture
        self.hover_texture = self.texture
        self.pressed_texture = self.texture

class UnitSelected(arcade.Sprite):
    def __init__(self, dummy, texture):
        super().__init__(dummy)
        self.texture = texture
        self.scale = 1.8

class MenuView(arcade.View):
    
    def __init__(self):
        super().__init__()
        self.sprites = arcade.SpriteList()
        self.dir = ""
        self.ui_manager = self.window.ui_manager

    def align_ui_item(self, item: object, x: float, y:float, x_align: str="center_x", y_align: str="center_y"):
        if x_align == "left":
            item.left = x
        elif x_align == "right":
            item.right = x
        else:
            item.center_x = x

        if y_align == "top":
            item.top = y
        elif y_align == "bottom":
            item.bottom = y
        else:
            item.center_y = y

    def on_show_view(self):
        self.setup()

    def setup(self):
        ''' placeholder, overrided by top object '''
        pass

    def on_draw(self):
        arcade.start_render()
        self.sprites.draw()

    def new_view(self, params: object) -> None:
        next_view = params
        self.ui_manager.purge_ui_elements()
        self.window.show_view(next_view)
    
    def add_view_button(self, x:float, y:float, name:str, id:str, command, params, x_align: str="center_x", y_align: str="center_y", text="", dir_:str = "") -> None:
        if dir_ == "":
            dir_ = self.dir
        button = SwitchViewButton(dir_, name, id, command, params)
        self.align_ui_item(button, x, y, x_align, y_align)
        if text != "":
            button.text=text
        self.ui_manager.add_ui_element(button)

    def add_unit_button(self, x:float, y:float, texture:object, id:str, command, params, x_align: str="center_x", y_align: str="center_y") -> None:
        unit = UnitButton(texture, id, command, params)
        self.align_ui_item(unit, x, y, x_align, y_align)
        self.ui_manager.add_ui_element(unit)

    def add_gui_box(self, x:float, y:float, texture: str, x_align: str="center_x", y_align:str="center_y", dir_: str="") -> None:
        box = GuiBox(dir_, texture)
        self.align_ui_item(box, x, y, x_align, y_align)
        box.id = "ConfirmationBox"
        self.ui_manager.add_ui_element(box)

    def add_sprite(self, x: float, y: float, name: str, x_align: str="left", y_align: str="bottom", dir_: str="") -> None:
        ''' sprite by default is positioned bottom left '''
        element = arcade.Sprite(utils.get_file_path(dir_, name,"png"))
        self.align_ui_item(element, x, y, x_align, y_align)
        self.sprites.append(element)

    def add_label(self, x: float, y: float, text: str, x_align: str="center_x", y_align: str="center_y") -> None:
        ''' the label by default is positioned on its center '''
        label = arcade.gui.UILabel(text)
        self.align_ui_item(label, x, y, x_align, y_align)
        self.ui_manager.add_ui_element(label)

    def add_input_box(self, x: float, y: float, width: float, height: float, text: str, x_align: str="center_x", y_align: str="center_y") -> object:
        ''' input box by default is positioned on its center '''
        input_box = arcade.gui.UIInputBox(x, y, width, height, text=text, id="InputBox")
        self.align_ui_item(input_box, x, y, x_align, y_align)
        input_box.text=text
        self.ui_manager.add_ui_element(input_box)
        return input_box

    def add_unit_selected(self, x: float, y: float, texture: object, x_align: str="center_x", y_align: str="center_y"):
        element = UnitSelected(utils.get_file_path("assets/gui/title","btn_play_normal","png"), texture)
        self.align_ui_item(element, x, y, x_align, y_align)
        self.sprites.append(element)