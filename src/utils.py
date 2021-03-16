import os
import arcade
import json
import string
import random

def get_file_path(sub_dir: str, file_name: str, file_ext: str) -> str:
        return os.path.join(os.path.dirname(__file__), "..", sub_dir, file_name+"."+file_ext)

def load_images(img: str, sprite_w: int, sprite_h: int) -> list:
    # load image from file, divide into 32x32 tiles
    # assign to character facing, DOWN, LEFT, RIGHT or UP
    filename = get_file_path("assets",img,"png")
    images = {}
    for h in range(4):
        tmp = []
        for w in range(3):
            x, y = sprite_w*w, sprite_h*h
            tmp.append(arcade.load_texture(filename,
                                           x, y, 32, 32, False))
        images[["DOWN", "LEFT", "RIGHT", "UP"][h]] = tmp
    return images

def load_savegame() -> dict:
    ''' return game progress '''
    savegame = {}
    with open(get_file_path("data", "save", "json"), "r") as f:
        savegame = json.load(f)
    return savegame

# LEVEL BASIC UTILS

def load_levels() -> tuple[dict, int]:
    ''' return a dict containg the list of worlds and max world # '''
    levels = {}
    with open(get_file_path("data", "levels", "json"), "r") as f:
        levels = json.load(f)
    return (levels, max_world(levels))

def max_world(levels: list) -> int:
    ''' retrieve max world # '''
    return len(levels)-1

def max_level(levels: list, world: int) -> int:
    ''' retrieve max level for the selected world '''
    return len(levels[world]["Levels"])-1

def max_wave(waves: list) -> int:
    ''' retrieve max wave for the selected stage '''
    return len(waves)-1

def random_name() -> str:
    chars = string.digits + string.ascii_letters
    return "".join(random.choice(chars) for _ in range(12))

def random_stage_id(name: str = "dummy") -> str:
    name = random_name()
    file = get_file_path("data/levels", name, "json")
    if os.path.isfile(file):
        return random_stage_id(name)
    else:
        with open(file, "w") as f:
            with open(get_file_path("data/levels", "dummy", "json"),"r") as source_file:
                data = json.load(source_file)
                json.dump(data, f, indent=2)
        return name

# LOAD LEVELS DATA

# WORLD RELATED

def add_world(n: int, levels: list) -> tuple[list, int]:
    name = random_stage_id()
    levels.append({"Title": "Default", "Levels":[name]})
    return (levels, max_world(levels))

def del_world(n: int, levels: list) -> tuple[list, int]:
    current_world = levels[n]
    for stage in current_world["Levels"]:
        delete_stage(stage)
    del levels[n]
    write_world(levels) 
    return (levels, max_world(levels))

def edit_world_name(params) -> list:
    levels, world, input_box = params
    levels[world]["Title"]=input_box.text
    write_world(levels)
    return levels

def write_world(data: list) -> None:
    with open(get_file_path("data", "levels", "json"), "w") as f:
        json.dump(data, f, indent=2)

# STAGE RELATED

def load_stage(stage:str) -> list:
    ''' return the stage data '''
    current_stage = []
    with open(get_file_path("data/levels", stage, "json"), "r") as f:
        current_stage = json.load(f)
    return current_stage

def delete_stage_from_world(levels: list ,stage: int) -> list:
    name = levels[stage]
    delete_stage(name)
    del levels[stage]
    return levels
    
def delete_stage(stage: str) -> None:
    file = get_file_path("data/levels", stage, "json")
    if os.path.isfile(file):
        os.remove(file)

def add_stage(levels: list) -> list:
    name = random_stage_id()
    levels.append(name)
    return levels

# WAVES RELATED

def add_wave(stage: list, wave: list=[]) -> list:
    stage.append(wave)
    with open(get_file_path("data/levels", stage, "json"), "w") as f:
        
        json.dump(stage, f, indent=2)
    return stage

def load_waves(stage: str) -> list:
    data = []
    filename = get_file_path("data/levels", stage, "json")
    if os.path.isfile(filename):
        with open(filename, "r") as f:
            data = json.load(f)
    return data

def del_wave(waves: list, index: int) -> list:
    del waves[index]
    return waves

def write_waves(stage: str, waves: list) -> None:
    with open(get_file_path("data/levels", stage, "json"), "w") as f:
        json.dump(waves, f)
