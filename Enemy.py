import pygame
import random

TILE_SIZE = 32

# All available monster types by filename (Icon42 missing from assets)
ENEMY_TYPES = [
    # name,      sprite,    hp, attack, aggro
    ("Icon0",  "Icon0.png",  10,  3,  6),
    ("Icon1",  "Icon1.png",  12,  3,  6),
    ("Icon2",  "Icon2.png",  14,  4,  6),
    ("Icon3",  "Icon3.png",  14,  4,  7),
    ("Icon4",  "Icon4.png",  16,  4,  7),
    ("Icon5",  "Icon5.png",  16,  5,  7),
    ("Icon6",  "Icon6.png",  18,  5,  7),
    ("Icon7",  "Icon7.png",  18,  5,  8),
    ("Icon8",  "Icon8.png",  20,  5,  8),
    ("Icon9",  "Icon9.png",  20,  6,  8),
    ("Icon10", "Icon10.png", 22,  6,  8),
    ("Icon11", "Icon11.png", 22,  6,  8),
    ("Icon12", "Icon12.png", 24,  6,  8),
    ("Icon13", "Icon13.png", 24,  7,  8),
    ("Icon14", "Icon14.png", 26,  7,  8),
    ("Icon15", "Icon15.png", 26,  7,  9),
    ("Icon16", "Icon16.png", 28,  7,  9),
    ("Icon17", "Icon17.png", 28,  8,  9),
    ("Icon18", "Icon18.png", 30,  8,  9),
    ("Icon19", "Icon19.png", 30,  8,  9),
    ("Icon20", "Icon20.png", 32,  8,  9),
    ("Icon21", "Icon21.png", 32,  9,  9),
    ("Icon22", "Icon22.png", 34,  9,  9),
    ("Icon23", "Icon23.png", 34,  9,  9),
    ("Icon24", "Icon24.png", 36,  9, 10),
    ("Icon25", "Icon25.png", 36, 10, 10),
    ("Icon26", "Icon26.png", 38, 10, 10),
    ("Icon27", "Icon27.png", 38, 10, 10),
    ("Icon28", "Icon28.png", 40, 10, 10),
    ("Icon29", "Icon29.png", 40, 11, 10),
    ("Icon30", "Icon30.png", 42, 11, 10),
    ("Icon31", "Icon31.png", 42, 11, 10),
    ("Icon32", "Icon32.png", 44, 11, 10),
    ("Icon33", "Icon33.png", 44, 12, 10),
    ("Icon34", "Icon34.png", 46, 12, 10),
    ("Icon35", "Icon35.png", 46, 12, 10),
    ("Icon36", "Icon36.png", 48, 12, 10),
    ("Icon37", "Icon37.png", 48, 13, 10),
    ("Icon38", "Icon38.png", 50, 13, 10),
    ("Icon39", "Icon39.png", 50, 13, 10),
    ("Icon40", "Icon40.png", 55, 14, 10),
    ("Icon41", "Icon41.png", 55, 14, 10),
    ("Icon43", "Icon43.png", 60, 14, 10),
    ("Icon44", "Icon44.png", 60, 15, 10),
    ("Icon45", "Icon45.png", 65, 15, 10),
    ("Icon46", "Icon46.png", 65, 15, 10),
    ("Icon47", "Icon47.png", 70, 16, 10),
    ("Icon48", "Icon48.png", 70, 16, 10),
]

_sprite_cache = {}

def _load_sprite(filename):
    if filename not in _sprite_cache:
        img = pygame.image.load(f"assets/{filename}").convert_alpha()
        _sprite_cache[filename] = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    return _sprite_cache[filename]

def random_enemy_for_floor(tx, ty, floor):
    # Higher floors unlock stronger enemy types
    max_idx = min(len(ENEMY_TYPES) - 1, (floor - 1) * 5 + random.randint(0, 4))
    min_idx = max(0, max_idx - 6)
    entry = ENEMY_TYPES[random.randint(min_idx, max_idx)]
    return Enemy(tx, ty, name=entry[0], sprite_file=entry[1],
                 hp=entry[2], attack=entry[3], aggro=entry[4])


class Enemy:
    def __init__(self, tx, ty, name="Icon0", sprite_file="Icon0.png", hp=10, attack=3, aggro=6):
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
