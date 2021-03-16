'''
Created on 24 feb 2021

@author: Matteo Pratellesi
'''

# map tileset Stealthix
# char sprites Pipoya

import arcade
import titles_views
import game_view
from utils import load_levels, load_savegame
from arcade.gui import UIManager
from settings import SCREEN_HEIGHT, SCREEN_WIDTH

def main() -> None:
    """ Main method """
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "PyHeroes")
    window.center_window()
    window.total_score = 0
    window.ui_manager = UIManager()
    window.game = game_view.MyGame()
    window.levels, window.max_world = load_levels()
    window.savegame = load_savegame()
    title_window = titles_views.TitleView(1) # 1 = dev tools / 0 or empty normal view

    # Show title window
    window.show_view(title_window)
    arcade.run()

if __name__ == "__main__":
    main()