import arcade
import characters
import party
import enemy_waves
from settings import *

class MyGame(arcade.View):
    """ Our custom Window Class"""
    
    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__()
        #self.ui_manager = ui_manager
        
        self.last_level = LAST_LEVEL
        self.world = 0
        self.level = 0

        # Sprite lists
        self.player_list = None
        self.coin_list = None
        self.pause = PauseView(self)
        self.level_view = ""

        # Set up the player
        self.score = 0
        self.gold = 0

        self.party = party.Party()
        #self.setup()

    def setup(self) -> None:
        """ Set up the game and initialize the variables. """

        self.player_list = arcade.SpriteList()
        self.enemies_list = arcade.SpriteList()
        self.enemy_projectiles_list = arcade.SpriteList()
        self.player_projectiles_list = arcade.SpriteList()
        
        # Load party formation

        self.party.add_unit(characters.Heroes("Warrior"), 0, 1)
        self.party.add_unit(characters.Heroes("Monk"), 1, 0)
        self.party.add_unit(characters.Heroes("Healer"), 1, 2)
        
        self.player_list.extend(self.party.list_units)
        
        # Load enemies formation
        wave_map = utils.load_stage(self.window.levels[self.world]["Levels"][self.level])
        current_wave = enemy_waves.EnemyWave(wave_map[0])
        self.enemies_list.extend(current_wave.enemies_list)

        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self) -> None:
        # This command has to happen before we start drawing
        arcade.set_background_color(arcade.color.AMAZON)
        arcade.start_render()

        # Draw all the sprites.
        for hero in self.player_list:
            hero.hp_bar()
        for enemy in self.enemies_list:
            enemy.hp_bar()
        self.player_list.draw()
        self.enemies_list.draw()
        self.enemy_projectiles_list.draw()
        self.player_projectiles_list.draw()

        # Put the text on the screen.
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)
        
        output = f"Gold: {self.gold}"
        arcade.draw_text(output, 10, 50, arcade.color.WHITE, 14)

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
        elif key == arcade.key.P:
            self.window.show_view(self.pause)
        elif key == arcade.key.ESCAPE:
            self.window.show_view(self.level_view)

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

    def _check_projectiles_position(self, proj_list:list) -> arcade.SpriteList:
        '''
        Control if projectiles are still on screen
        '''
        for projectile in proj_list:
            pos = projectile.move()
            if 0 >= pos[0] <= SCREEN_HEIGHT or 0 >= pos[1] <= SCREEN_WIDTH:
                proj_list.remove(projectile)
                del projectile
        return proj_list

    def _check_projectiles_collisions(self, proj_list: list, targets: list) -> list:
        '''
        Control projectiles collision
        '''
        for projectile in proj_list:
            characters = arcade.check_for_collision_with_list(projectile, targets)
            if len(characters) > 0:
                for character in characters:
                    if character.active == False:
                        continue
                    character.take_damage(projectile)
                    if character.current_hp <= 0:
                        character.killed()
                        if character.type == "Enemy":
                            self.enemies_list.remove(character)
                            self.score += character.xp
                            self.gold += character.gold
                            del character
                        elif character.type == "Hero":
                            self.party.size -= 1
                proj_list.remove(projectile)
                del projectile
        return proj_list

    def on_update(self, delta_time) -> None:
        """ Movement and game logic """

        if self.party.size == 0:
            print("GAME OVER")
            return

        # Move the player
        self.player_list.update()
        for hero in self.player_list:
            fire = hero.fire()
            if fire:
                self.player_projectiles_list.append(fire)

        # Check Enemies Postion, hp and fire
        for enemy in self.enemies_list:
            enemy.update_position()
            fire = enemy.fire()
            if fire:
                self.enemy_projectiles_list.append(fire)
            if enemy.bottom < 0 or enemy.current_hp <= 0:
                self.enemies_list.remove(enemy)
                if enemy.hp <= 0:
                    # give player money and XP not sure if this is the right place to do that
                    print("DEAD")
                del enemy
        
        # Check Projectiles
        
        self.enemy_projectiles_list = self._check_projectiles_position(self.enemy_projectiles_list)
        self.enemy_projectiles_list = self._check_projectiles_collisions(self.enemy_projectiles_list,self.player_list)
        self.enemy_projectiles_list.update()
        
        self.player_projectiles_list = self._check_projectiles_position(self.player_projectiles_list)
        self.player_projectiles_list = self._check_projectiles_collisions(self.player_projectiles_list,self.enemies_list)
        self.player_projectiles_list.update()

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

class PauseView(arcade.View):

    def __init__(self, game):
        super().__init__()
        self.game = game

    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("PAUSE MENU", SCREEN_WIDTH/2, SCREEN_HEIGHT/2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("Click to advance", SCREEN_WIDTH/2, SCREEN_HEIGHT/2-75,
                         arcade.color.GRAY, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        self.window.show_view(self.game)    