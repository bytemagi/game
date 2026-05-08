import pygame
import os

_BASE = os.path.dirname(os.path.abspath(__file__))
SHEET_PATH  = os.path.join(_BASE, "assets", "#1 - Transparent Icons.png")
ICON_SIZE   = 32
COLS        = 16
_sheet      = None
_cache      = {}

# Icon index map (row * COLS + col), based on pack order:
# Row 0:  status effects (11)
# Row 1:  body icons (5) + buffs/debuffs (7) + 4 special moves
# Row 2:  special moves continued (12) + non-combat (4)
# Row 3:  non-combat continued (5) + weapons (11)
# Row 4:  weapons continued (16)
# Row 5:  weapons continued (1) + clothing/armour (15)
# Row 6:  clothing/armour continued (11) + healing (5)
# Row 7:  healing continued (11) + general items (5)
# Row 8-11: general items (64 total)
# Row 12-13: food (31)
# Row 14-15: fishing (15) + resources (11) + orbs (6)

ICONS = {
    # Status effects (row 0)
    "skull":        0,
    "poison":       1,
    "sleeping_eye": 2,
    "silenced":     3,
    "cursed":       4,
    "dizzy":        5,
    "charmed":      6,
    "sleeping":     7,
    "paralysis":    8,
    "burned":       9,
    "sweat":        10,

    # Body icons (row 0 col 11 - row 1)
    "heart":        11,
    "lungs":        12,
    "stomach":      13,
    "brain":        14,
    "strong_arm":   15,

    # Buffs & debuffs (row 1)
    "buff1":        16,
    "buff2":        17,
    "buff3":        18,
    "debuff1":      19,
    "debuff2":      20,
    "debuff3":      21,
    "repeat":       22,

    # Special moves
    "dripping_blade":   23,
    "saber_slash":      24,
    "lightning_attack": 25,
    "headshot":         26,
    "raining_arrows":   27,
    "healing_move":     28,
    "heal_injury":      29,
    "battle_gear":      30,
    "guard":            31,
    "ring_of_fire":     32,
    "disintegrate":     33,
    "fist_hit":         34,
    "gust":             35,
    "tremor":           36,
    "psychic_waves":    37,
    "sunrays":          38,

    # Non-combat actions
    "speech_square":    39,
    "speech_round":     40,
    "campfire":         41,
    "tent":             42,
    "blacksmith":       43,
    "mining":           44,
    "woodcutting":      45,
    "spellbook":        46,
    "steal":            47,

    # Weapons
    "wooden_waster":    48,
    "longsword":        49,
    "enchanted_sword":  50,
    "katana":           51,
    "gladius":          52,
    "saber":            53,
    "dagger":           54,
    "broad_dagger":     55,
    "sai":              56,
    "dual_swords":      57,
    "war_axe":          58,
    "battle_axe":       59,
    "flail":            60,
    "spiked_club":      61,
    "whip":             62,
    "fist":             63,
    "buckler":          64,
    "wooden_shield":    65,
    "checkered_shield": 66,
    "bow":              67,
    "crossbow":         68,
    "slingshot":        69,
    "boomerang":        70,
    "wizard_staff":     71,
    "gem_staff1":       72,
    "gem_staff2":       73,
    "gem_staff3":       74,
    "gem_staff4":       75,

    # Clothing & armour
    "robin_hood_hat":   76,
    "barbute_helm":     77,
    "leather_helm":     78,
    "cross_helm":       79,
    "iron_armour":      80,
    "steel_armour":     81,
    "leather_armour":   82,
    "plate_armour":     83,
    "blue_tunic":       84,
    "green_tunic":      85,
    "trousers":         86,
    "shorts":           87,
    "heart_boxers":     88,
    "dress":            89,
    "cloak":            90,
    "belt":             91,
    "leather_gauntlet": 92,
    "metal_gauntlet":   93,
    "leather_boots":    94,
    "steeltoe_boots":   95,
    "ring":             96,
    "diamond_ring":     97,
    "gold_necklace":    98,
    "prayer_beads":     99,
    "tribal_necklace":  100,
    "leather_pouch":    101,

    # Healing items
    "potion_normal1":   102,
    "potion_normal2":   103,
    "potion_normal3":   104,
    "potion_normal4":   105,
    "potion_upgraded1": 106,
    "potion_upgraded2": 107,
    "potion_upgraded3": 108,
    "potion_upgraded4": 109,
    "potion_rare1":     110,
    "potion_rare2":     111,
    "potion_rare3":     112,
    "potion_rare4":     113,
    "brew1":            114,
    "brew2":            115,
    "brew3":            116,
    "bandage":          117,

    # General items
    "knapsack":         118,
    "axe":              119,
    "pickaxe":          120,
    "shovel":           121,
    "hammer":           122,
    "grappling_hook":   123,
    "hookshot":         124,
    "telescope":        125,
    "magnifying_glass": 126,
    "lantern":          127,
    "torch":            128,
    "candle":           129,
    "bomb":             130,
    "rope":             131,
    "bear_trap":        132,
    "hourglass":        133,
    "runestone":        134,
    "mirror":           135,
    "shackles":         136,
    "lyre":             137,
    "violin":           138,
    "ocarina":          139,
    "flute":            140,
    "panpipes":         141,
    "horn":             142,
    "brass_key":        143,
    "silver_keyring":   144,
    "treasure_chest":   145,
    "mortar_pestle":    146,
    "herb1":            147,
    "herb2":            148,
    "herb3":            149,
    "mushrooms":        150,
    "flower_bulb":      151,
    "root_tip":         152,
    "seedling":         153,
    "plant_growing":    154,
    "plant_grown":      155,
    "money_purse":      156,
    "crown_coin":       157,
    "bronze_coins":     158,
    "silver_coins":     159,
    "gold_coins":       160,
    "large_gold_coins": 161,
    "receive_money":    162,
    "pay_money":        163,
    "gems":             164,
    "rupee":            165,
    "book1":            166,
    "book2":            167,
    "book3":            168,
    "book4":            169,
    "book5":            170,
    "book6":            171,
    "book7":            172,
    "book8":            173,
    "open_book":        174,
    "letter":           175,
    "tied_scroll":      176,
    "open_scroll":      177,
    "old_map":          178,
    "dice":             179,
    "card":             180,
    "wine":             181,

    # Food
    "apple":            182,
    "banana":           183,
    "pear":             184,
    "lemon":            185,
    "strawberry":       186,
    "grapes":           187,
    "carrot":           188,
    "sweetcorn":        189,
    "garlic":           190,
    "tomato":           191,
    "eggplant":         192,
    "chili":            193,
    "mushroom":         194,
    "bread":            195,
    "baguette":         196,
    "whole_chicken":    197,
    "chicken_leg":      198,
    "steak":            199,
    "ham":              200,
    "morsel":           201,
    "cooked_fish":      202,
    "eggs":             203,
    "big_egg":          204,
    "cheese":           205,
    "milk":             206,
    "honey":            207,
    "salt":             208,
    "spices":           209,
    "candy":            210,
    "cake":             211,
    "drink":            212,

    # Fishing
    "fishing_rod":      213,
    "fishing_hook":     214,
    "worm_bait":        215,
    "lake_trout":       216,
    "brown_trout":      217,
    "eel":              218,
    "tropical_fish":    219,
    "clownfish":        220,
    "jellyfish":        221,
    "octopus":          222,
    "turtle":           223,
    "fish_bone":        224,
    "old_boot":         225,
    "fossil":           226,
    "sunken_chest":     227,

    # Resources
    "wood":             228,
    "stone":            229,
    "ore":              230,
    "gold_resource":    231,
    "gems_resource":    232,
    "cotton":           233,
    "yarn":             234,
    "cloth":            235,
    "pelts":            236,
    "monster_claw":     237,
    "feathers":         238,

    # Orbs
    "orb1":             239,
    "orb2":             240,
    "orb3":             241,
    "orb4":             242,
    "orb5":             243,
    "orb6":             244,
}

def _load_sheet():
    global _sheet
    if _sheet is None:
        _sheet = pygame.image.load(SHEET_PATH).convert_alpha()

def get(name, size=ICON_SIZE):
    key = (name, size)
    if key in _cache:
        return _cache[key]
    _load_sheet()
    idx = ICONS.get(name)
    if idx is None:
        return None
    col = idx % COLS
    row = idx // COLS
    surf = pygame.Surface((ICON_SIZE, ICON_SIZE), pygame.SRCALPHA)
    surf.blit(_sheet, (0, 0), (col * ICON_SIZE, row * ICON_SIZE, ICON_SIZE, ICON_SIZE))
    if size != ICON_SIZE:
        surf = pygame.transform.scale(surf, (size, size))
    _cache[key] = surf
    return surf
