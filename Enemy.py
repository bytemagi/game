import pygame
import random

TILE_SIZE = 32

# name, sprite file, hp, attack, aggro
ENEMY_TYPES = [
    ("Fat Mushroom",      "fat_mushroom_enemy3.png",      10,  3, 5),
    ("Mushdino",          "mushdino_enemy4.png",           12,  3, 5),
    ("Topeye Shroom",     "topeye_shroom_enemy5.png",      12,  4, 6),
    ("Sad Shroom",        "sadshroom_enemy6.png",          14,  4, 6),
    ("Savage Shroom",     "savageshroom_enemy7.png",       14,  4, 6),
    ("Rose Monster",      "rose_monster_enemy8.png",       16,  5, 6),
    ("Scorpio Shroom",    "scorpioshroom_enemy9.png",      16,  5, 6),
    ("Crab Shroom",       "crabshroom_enemy10.png",        18,  5, 7),
    ("Maroloboro",        "maroloboro_enemy11.png",        18,  5, 7),
    ("Vine Whip",         "vinewhip_enemy12.png",          20,  6, 7),
    ("Bluestar Plant",    "bluestar_plant_enemy13.png",    20,  6, 7),
    ("Lava Crab",         "lavacrab_enemy14.png",          22,  6, 7),
    ("Mad Onion",         "madonion_enemy15.png",          22,  7, 7),
    ("Pump Spike",        "pumpspike_enemy16.png",         24,  7, 7),
    ("Gay Bulb",          "gaybulb_enemy17.png",           24,  7, 8),
    ("Mane Flower",       "maneflower_enemy18.png",        26,  7, 8),
    ("Hyabusabiskis",     "hyabusabiskis_enemy19.png",     26,  8, 8),
    ("Crack Plant",       "crackplant_enemy20.png",        28,  8, 8),
    ("Shy Slime",         "shyslime_enemy21.png",          28,  8, 8),
    ("Savage Slime",      "savageslime_enemy22.png",       30,  8, 8),
    ("Gay Blobs",         "gayblobs_enemy23.png",          30,  9, 8),
    ("Hungry Slime",      "hungryslime_enemy24.png",       32,  9, 8),
    ("Spood Beast",       "spood_beast_enemy25.png",       32,  9, 9),
    ("Taytos",            "taytos_enemy26.png",            34,  9, 9),
    ("Melty",             "melty_enemy27.png",             34, 10, 9),
    ("Sad Sac",           "sadsac_enemy28.png",            36, 10, 9),
    ("Gay Plant",         "gayplant_enemy29.png",          36, 10, 9),
    ("Cactus",            "cactus_enemy30.png",            38, 10, 9),
    ("Plant Shelder",     "plantshelder_enemy31.png",      38, 11, 9),
    ("Spike Beast",       "spikebeast_enemy32.png",        40, 11, 9),
    ("Jackalope",         "jackalope_enemy33.png",         40, 11, 9),
    ("Garga Pup",         "gargapup_enemy34.png",          42, 11, 9),
    ("Centisting",        "centisting_enemy35.png",        42, 12, 9),
    ("Tick",              "tick_enemy36.png",              44, 12, 9),
    ("Shit Fly",          "shitfly_enemy37.png",           44, 12, 9),
    ("Batatata",          "batatata_enemy38.png",          46, 12, 9),
    ("Toadapest",         "toadapest_enemy38.png",         46, 13, 9),
    ("Mantadantatitis",   "mantadantatitis_enemy39.png",   48, 13, 10),
    ("Eye Cupoo",         "eyecupoo_enemy40.png",          48, 13, 10),
    ("Obese Avian",       "obeseavian_enemy41.png",        50, 13, 10),
    ("Voltarion",         "voltarion_enemy43.png",         55, 14, 10),
    ("Underpants Gnome",  "underpants_gnome_enemy44.png",  55, 14, 10),
    ("Pumpkimatoe",       "pumpkimatoe_enemy45.png",       60, 15, 10),
    ("Obese Rodent",      "obese_rodent_enemy46.png",      60, 15, 10),
    ("Death Seagull",     "death_seagull_enemy47.png",     65, 16, 10),
]

_sprite_cache = {}

def _load_sprite(filename):
    if filename not in _sprite_cache:
        img = pygame.image.load(f"assets/{filename}").convert_alpha()
        _sprite_cache[filename] = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    return _sprite_cache[filename]

def random_enemy_for_floor(tx, ty, floor):
    max_idx = min(len(ENEMY_TYPES) - 1, (floor - 1) * 5 + random.randint(0, 4))
    min_idx = max(0, max_idx - 6)
    entry = ENEMY_TYPES[random.randint(min_idx, max_idx)]
    return Enemy(tx, ty, name=entry[0], sprite_file=entry[1],
                 hp=entry[2], attack=entry[3], aggro=entry[4])


class Enemy:
    def __init__(self, tx, ty, name="Fat Mushroom", sprite_file="fat_mushroom_enemy3.png",
                 hp=10, attack=3, aggro=5):
        self.tx = tx
        self.ty = ty
        self.name = name
        self.sprite_file = sprite_file
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.aggro_range = aggro
        self.sprite = None

    def load_sprite(self):
        self.sprite = _load_sprite(self.sprite_file)

    def take_turn(self, player_tx, player_ty, tiles, enemies):
        dx = player_tx - self.tx
        dy = player_ty - self.ty
        dist = abs(dx) + abs(dy)

        if dist > self.aggro_range:
            return None

        if dist == 1:
            return ("attack", self.attack)

        step_x, step_y = 0, 0
        if abs(dx) >= abs(dy):
            step_x = 1 if dx > 0 else -1
        else:
            step_y = 1 if dy > 0 else -1

        new_tx = self.tx + step_x
        new_ty = self.ty + step_y
        occupied = any(e.tx == new_tx and e.ty == new_ty for e in enemies if e is not self)
        if tiles[new_ty][new_tx] == "floor" and not occupied:
            self.tx = new_tx
            self.ty = new_ty

        return None

    def draw(self, surface, camera_x, camera_y):
        px = self.tx * TILE_SIZE - camera_x
        py = self.ty * TILE_SIZE - camera_y
        if self.sprite:
            surface.blit(self.sprite, (px, py))
        else:
            pygame.draw.rect(surface, (200, 50, 50), (px, py, TILE_SIZE, TILE_SIZE))

        hp_ratio = self.hp / self.max_hp
        pygame.draw.rect(surface, (100, 0, 0), (px, py - 6, TILE_SIZE, 4))
        pygame.draw.rect(surface, (220, 0, 0), (px, py - 6, int(TILE_SIZE * hp_ratio), 4))

        font = pygame.font.SysFont(None, 12)
        surface.blit(font.render(self.name, True, (255, 200, 200)), (px, py - 14))
