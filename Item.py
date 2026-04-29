import pygame
import random
import sprites

TILE_SIZE = 32

POTION_NAMES = ["Red potion", "Blue potion", "Green potion", "Bubbly potion", "Smoky potion"]
SCROLL_NAMES = ["Scroll of KAUNAN", "Scroll of SOWILO", "Scroll of TIWAZ", "Scroll of BERKANAN"]

random.shuffle(POTION_NAMES)
random.shuffle(SCROLL_NAMES)

# True identity mapped to shuffled name
POTION_ID = {
    "healing":    POTION_NAMES[0],
    "strength":   POTION_NAMES[1],
    "poison":     POTION_NAMES[2],
}

# Icon mapping per item subtype
ITEM_ICON = {
    # potions
    "healing":  "potion_normal1",
    "strength": "potion_upgraded1",
    "poison":   "potion_rare1",
    # weapons
    "Short sword": "gladius",
    "Dagger":      "dagger",
    "Hand axe":    "war_axe",
    # armor
    "Leather armor": "leather_armour",
    "Mail armor":    "iron_armour",
}

class Item:
    def __init__(self, tx, ty, kind, subtype, value):
        self.tx = tx
        self.ty = ty
        self.kind = kind        # "potion", "weapon", "armor"
        self.subtype = subtype  # "healing", "strength", "poison", "sword", etc
        self.value = value      # hp restore, attack bonus, defense bonus
        self.identified = False

    @property
    def name(self):
        if self.kind == "potion":
            if self.identified:
                return f"Potion of {self.subtype} (+{self.value})"
            return POTION_ID.get(self.subtype, "Unknown potion")
        if self.kind == "weapon":
            return f"{self.subtype} (atk +{self.value})"
        if self.kind == "armor":
            return f"{self.subtype} (def +{self.value})"
        return self.subtype

    def draw(self, surface, camera_x, camera_y):
        px = self.tx * TILE_SIZE - camera_x
        py = self.ty * TILE_SIZE - camera_y
        icon_name = ITEM_ICON.get(self.subtype)
        icon = sprites.get(icon_name) if icon_name else None
        if icon:
            surface.blit(icon, (px, py))
        else:
            pygame.draw.rect(surface, (100, 180, 255), (px + 8, py + 8, TILE_SIZE - 16, TILE_SIZE - 16))


def spawn_items(dungeon):
    items = []
    for room in dungeon.rooms[1:]:
        if random.random() < 0.7:
            tx, ty = _random_floor_tile(room, dungeon)
            items.append(_random_item(tx, ty))
    return items

def _random_floor_tile(room, dungeon):
    for _ in range(20):
        tx = random.randint(room.x + 1, room.x + room.width - 2)
        ty = random.randint(room.y + 1, room.y + room.height - 2)
        if dungeon.tiles[ty][tx] == "floor":
            return tx, ty
    return room.center()

def _random_item(tx, ty):
    roll = random.random()
    if roll < 0.5:
        subtype = random.choice(list(POTION_ID.keys()))
        value = {"healing": 10, "strength": 2, "poison": -8}[subtype]
        return Item(tx, ty, "potion", subtype, value)
    elif roll < 0.75:
        subtype = random.choice(["Short sword", "Dagger", "Hand axe"])
        value = random.randint(1, 4)
        return Item(tx, ty, "weapon", subtype, value)
    else:
        subtype = random.choice(["Leather armor", "Mail armor"])
        value = random.randint(1, 3)
        return Item(tx, ty, "armor", subtype, value)
