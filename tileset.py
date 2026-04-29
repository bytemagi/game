import pygame
import random

# --- Tile assignments ---
# Change these numbers once you know what each tile looks like.
# Tip: run python3 -c "import tileset; tileset.preview()" to see all tiles printed to /tmp/tile_preview.png

FLOOR_TILES  = [0, 1, 2, 3, 4, 5]       # tiles used for floor (picked randomly per-cell for variety)
WALL_TILES   = [20, 21, 22, 23, 24, 25]  # tiles used for walls
STAIR_TILE   = 10                         # tile used for stairs
EXPLORED_DIM = 0.4                        # brightness multiplier for explored-but-not-visible tiles

_cache = {}

def _load(index):
    if index not in _cache:
        path = f"assets/tile_{index:03d}.png"
        img = pygame.image.load(path).convert_alpha()
        _cache[index] = img
    return _cache[index]

def get_floor(col, row):
    # Deterministic random variety per cell so it doesn't flicker
    idx = FLOOR_TILES[(col * 7 + row * 13) % len(FLOOR_TILES)]
    return _load(idx)

def get_wall(col, row):
    idx = WALL_TILES[(col * 11 + row * 17) % len(WALL_TILES)]
    return _load(idx)

def get_stair():
    return _load(STAIR_TILE)

def get_dimmed(col, row, tile_type):
    """Return a darkened version of a tile for explored-but-not-visible areas."""
    if tile_type == "wall":
        surf = get_wall(col, row).copy()
    elif tile_type == "stairs":
        surf = get_stair().copy()
    else:
        surf = get_floor(col, row).copy()
    dark = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
    alpha = int(255 * EXPLORED_DIM)
    dark.fill((0, 0, 0, 255 - alpha))
    surf.blit(dark, (0, 0))
    return surf

def preview():
    """Save a preview image of all tiles to /tmp/tile_preview.png"""
    from PIL import Image, ImageDraw, ImageFont
    import os
    cols = 16
    rows = 115 // cols + 1
    size = 32
    out = Image.new("RGBA", (cols * size, rows * size), (30, 30, 30, 255))
    for i in range(115):
        img = Image.open(f"assets/tile_{i:03d}.png")
        c = i % cols
        r = i // cols
        out.paste(img, (c * size, r * size), img)
    out.save("/tmp/tile_preview.png")
    print("Saved to /tmp/tile_preview.png")
