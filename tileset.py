import pygame
import os

_BASE = os.path.dirname(os.path.abspath(__file__))

EXPLORED_DIM = 0.4

# Floor tiles grouped by theme — swap group used per dungeon floor in main.py
THEMES = {
    "dirt": [
        "brown_dirt_floor0.png", "brown_dirt_floor1.png", "brown_dirt_floor2.png",
        "brown_dirt_Floor3.png", "brown_dirt_floor4.png", "brown_dirt_floor5.png",
        "brown_dirt_floor6.png", "brown_dirt_floor7.png", "brown_dirt_floor8.png",
        "brown_dirt_floor9.png", "brown_dirt_floor10.png",
    ],
    "cracked_dirt": [
        "Brown_crack_floor11.png", "brown_crack_floor12.png", "brown_crack_floor13.png",
        "cracked_dirt_floor17.png", "cracked_dirt_floor18.png",
    ],
    "wood": [
        "brown_wood_floor14.png", "broken_wood_floor15.png", "broken_wood_Floor16.png",
        "2_brown_logs_floor49.png", "brown_log_wgrass_floor50.png",
        "brown_log_wplant_floor51.png", "hollow_grass_log_Floor52.png",
    ],
    "grass": [
        "green_grass_floor22.png", "green_grass_floor23.png", "green_grass_floor24.png",
        "green_grass_floor40.png", "cracked_grass_floor25.png", "cracked_grass_floor26.png",
        "grass_row_floor27.png", "grass_row_floor28.png",
        "green_plant_grass_floor29.png", "green_plant_grass_floor30.png",
        "dirt_plants_floor19.png", "dirt_plants_Floor20.png",
    ],
    "stone": [
        "grey_stone_floor61.png", "cracked_stone_floor62.png", "smooth_stone_Floor63.png",
        "stone_Floor69.png", "brown_hard_clay_floor21.png",
    ],
    "dark_stone": [
        "cracked_dark_floor91.png", "flat_dark_floor92.png",
        "cobblestone_dark_floor93.png", "black_stone_floor94.png",
        "cobble_Stone_Floor100.png", "black_stone_floor101.png",
        "cobblestone_Floor102.png", "checker_floor103.png",
    ],
    "ice": [
        "ice_floor87.png", "ice_floor88.png", "ice_stone_floor89.png",
        "frozen_floor104.png", "frozen_floor105.png", "frozen_floor106.png",
        "frozen_floor107.png", "frozen_floor108.png", "frozen_floor109.png",
        "frozen_floor110.png", "frozen_floor111.png", "frozen_floor112.png",
        "stepping_stone_floor90.png",
    ],
    "water": [
        "boulder_in_water_floor72.png", "gboulder_in_water_floor73.png",
        "gboulder_in_water_floor74.png", "boulder_in_water_floor76.png",
        "3stones_movingwater_floor77.png", "2boulders_in_water_floor78.png",
        "2boulders_in_water_floor79.png", "boulder_in_water_floor80.png",
        "transparent_stones_floor82.png", "transparent_stones_floor83.png",
        "transparent_stones_floor84.png", "transparent_stones_floor85.png",
        "puddles_floor95.png", "puddle_floor96.png", "puddle_floor97.png",
    ],
}

# Wall tiles per theme (reuse darker/boulder tiles as walls)
WALL_TILES = {
    "dirt":        ["brown_boulder_floor53.png", "brown_boulder_floor54.png",
                    "brown_boulder_floor55.png", "brown_boulder_floor56.png"],
    "cracked_dirt":["brown_boulder_floor57.png", "brown_boulder_floor58.png"],
    "wood":        ["brown_boulder_floor59.png", "brown_boulder_floor60.png"],
    "grass":       ["grey_boulder_floor64.png", "grey_boulder_floor65.png",
                    "cracked_gboulder_floor66.png", "cracked_gboulder_floor67.png"],
    "stone":       ["grey_boulder_floor64.png", "grey_boulder_floor65.png"],
    "dark_stone":  ["black_stone_floor94.png", "black_stone_floor101.png"],
    "ice":         ["ice_block_floor113.png", "ice_stone_floor89.png"],
    "water":       ["transparent_stones_floor82.png", "transparent_stones_floor85.png"],
}

STAIR_TILE = "stepping_stone_floor90.png"

# Which theme to use — set this from main.py based on floor number
current_theme = "dirt"

_cache = {}

def set_theme(theme):
    global current_theme
    if theme in THEMES:
        current_theme = theme

def theme_for_floor(floor):
    order = ["dirt", "cracked_dirt", "grass", "wood", "stone", "water", "dark_stone", "ice"]
    return order[(floor - 1) % len(order)]

def _load(filename):
    if filename not in _cache:
        path = os.path.join(_BASE, "assets", filename)
        img = pygame.image.load(path).convert_alpha()
        _cache[filename] = img
    return _cache[filename]

def get_floor(col, row):
    tiles = THEMES.get(current_theme, THEMES["dirt"])
    filename = tiles[(col * 7 + row * 13) % len(tiles)]
    return _load(filename)

def get_wall(col, row):
    walls = WALL_TILES.get(current_theme, WALL_TILES["dirt"])
    filename = walls[(col * 11 + row * 17) % len(walls)]
    return _load(filename)

def get_stair():
    return _load(STAIR_TILE)

def get_dimmed(col, row, tile_type):
    if tile_type == "wall":
        surf = get_wall(col, row).copy()
    elif tile_type == "stairs":
        surf = get_stair().copy()
    else:
        surf = get_floor(col, row).copy()
    dark = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
    dark.fill((0, 0, 0, int(255 * (1 - EXPLORED_DIM))))
    surf.blit(dark, (0, 0))
    return surf
