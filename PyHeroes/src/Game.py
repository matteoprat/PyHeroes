'''
Created on 24 feb 2021

@author: Matteo Pratellesi
'''

# map tileset Stealthix
# char sprites Pipoya

import arcade
import characters
import party
import enemy_waves
from settings import *


class MyGame(arcade.Window):
    """ Our custom Window Class"""

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Sprite lists
        self.player_list = None
        self.coin_list = None

        # Set up the player
        self.score = 0

        self.party = party.Party()

    def setup(self) -> None:
        """ Set up the game and initialize the variables. """

        self.player_list = arcade.SpriteList()
        self.enemies_list = arcade.SpriteList()
        # Set up the player
        self.score = 0

        self.party.add_unit(characters.Heroes("Warrior"), 0, 1)
        self.party.add_unit(characters.Heroes("Monk"), 1, 0)
        self.party.add_unit(characters.Heroes("Healer"), 1, 2)

        self.player_list.extend(self.party.list_units)
        wave_map = [["Bride", "", "Bride", "", ""], ["", "Bride", "", "Bride", ""], [
            "Ghost", "", "Naga", "", "Knight"], ["Bride", "", "Bride", "", ""], ["", "Bride", "", "Bride", ""]]
        current_wave = enemy_waves.EnemyWave(wave_map)
        self.enemies_list.extend(current_wave.enemies_list)

        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self) -> None:
        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw all the sprites.
        for hero in self.player_list:
            hero.hp_bar()
        for enemy in self.enemies_list:
            enemy.hp_bar()
        self.player_list.draw()
        self.enemies_list.draw()

        # Put the text on the screen.
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

    def on_key_press(self, key, modifiers) -> None:
        """
        Called whenever a key is pressed.
        """
        if key == arcade.key.UP:
            for unit in self.player_list:
                unit.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            for unit in self.player_list:
                unit.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            for unit in self.player_list:
                unit.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            for unit in self.player_list:
                unit.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers) -> None:
        """
        Called when the user releases a key.
        """
        if key == arcade.key.UP or key == arcade.key.DOWN:
            for unit in self.player_list:
                unit.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            for unit in self.player_list:
                unit.change_x = 0

    def on_update(self, delta_time) -> None:
        """ Movement and game logic """

        # Move the player
        self.player_list.update()

        # Check Enemies Postion and hp
        for enemy in self.enemies_list:
            enemy.update_position()
            if enemy.bottom < 0 or enemy.current_hp <= 0:
                self.enemies_list.remove(enemy)
                if enemy.hp <= 0:
                    # give player money and XP not sure if this is the right place to do that
                    print("DEAD")
                del enemy

        self.enemies_list.update()

        # Get the party boundaries and check if the party is out of screen
        # if it is out add or subtract the movement speed before drawing
        self.party.get_party_boundaries(self.player_list)
        if self.party.left < 0:
            for unit in self.player_list:
                unit.left += MOVEMENT_SPEED
        if self.party.right > SCREEN_WIDTH:
            for unit in self.player_list:
                unit.right -= MOVEMENT_SPEED
        if self.party.top > SCREEN_HEIGHT:
            for unit in self.player_list:
                unit.top -= MOVEMENT_SPEED
        if self.party.bottom < 0:
            for unit in self.player_list:
                unit.bottom += MOVEMENT_SPEED

        # Update sprite
        # Update the players animation
        self.player_list.update_animation()


def main() -> None:
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()