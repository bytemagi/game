import pygame
from dungeon import Dungeon
from Enemy import Enemy, random_enemy_for_floor
from Item import spawn_items
from fov import compute_fov
import sprites
import tileset

SCREEN_WIDTH  = 1280
SCREEN_HEIGHT = 720
TILE_SIZE     = 32
FPS           = 60
FOV_RADIUS    = 8

PLAYER_MAX_HP = 30
PLAYER_ATTACK = 5
PLAYER_DEFENSE = 2

LOG_MAX      = 5

MINIMAP_TILE = 3
MINIMAP_X = SCREEN_WIDTH - 160
MINIMAP_Y = 10


def make_level(floor=1):
    dungeon = Dungeon(50, 40)
    tileset.set_theme(tileset.theme_for_floor(floor))
    enemies = []
    for room in dungeon.rooms[1:]:
        cx, cy = room.center()
        e = random_enemy_for_floor(cx, cy, floor)
        e.load_sprite()
        enemies.append(e)
    items = spawn_items(dungeon)
    return dungeon, enemies, items


def draw_hud(surface, player_hp, max_hp, atk, def_, floor, log, inventory, font):
    # Heart icon + HP bar
    heart = sprites.get("heart", 14)
    if heart:
        surface.blit(heart, (10, 10))
    pygame.draw.rect(surface, (80, 0, 0),  (28, 10, 132, 14))
    pygame.draw.rect(surface, (220, 0, 0), (28, 10, int(132 * player_hp / max_hp), 14))
    surface.blit(font.render(f"HP {player_hp}/{max_hp}", True, (255, 255, 255)), (30, 11))
    surface.blit(font.render(f"ATK {atk}  DEF {def_}  Floor {floor}", True, (200, 200, 200)), (10, 28))

    # Inventory — icon + name
    surface.blit(font.render("Inventory (1-5 to use):", True, (220, 220, 180)), (10, 46))
    for i, item in enumerate(inventory[:5]):
        from Item import ITEM_ICON
        icon_name = ITEM_ICON.get(item.subtype)
        icon = sprites.get(icon_name, 12) if icon_name else None
        iy = 58 + i * 16
        if icon:
            surface.blit(icon, (10, iy))
        surface.blit(font.render(f"{i+1}. {item.name}", True, (180, 180, 140)), (26, iy + 1))

    # Message log
    for i, msg in enumerate(log[-LOG_MAX:]):
        surface.blit(font.render(msg, True, (220, 220, 180)),
                     (10, SCREEN_HEIGHT - 16 * (LOG_MAX - i)))


def game_over_screen(screen, font_big, font):
    screen.fill((0, 0, 0))
    screen.blit(font_big.render("YOU DIED", True, (200, 0, 0)),
                (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 40))
    screen.blit(font.render("Press R to restart or Q to quit", True, (200, 200, 200)),
                (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 10))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                if event.key == pygame.K_q:
                    return False


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pixel Dungeon Clone")
    clock = pygame.time.Clock()
    font     = pygame.font.SysFont(None, 16)
    font_big = pygame.font.SysFont(None, 64)

    player_sprite = pygame.image.load("assets/player.png")
    player_sprite = pygame.transform.scale(player_sprite, (TILE_SIZE, TILE_SIZE))

    while True:  # restart loop
        floor  = 1
        dungeon, enemies, items = make_level(floor)
        px, py = dungeon.rooms[0].center()
        player_hp  = PLAYER_MAX_HP
        player_atk = PLAYER_ATTACK
        player_def = PLAYER_DEFENSE
        inventory  = []
        explored   = set()
        log        = [f"Welcome to floor {floor}!"]

        running = True
        while running:
            clock.tick(FPS)

            visible = compute_fov(dungeon.tiles, px, py, FOV_RADIUS,
                                  dungeon.map_width, dungeon.map_height)
            explored |= visible

            camera_x = px * TILE_SIZE - SCREEN_WIDTH  // 2
            camera_y = py * TILE_SIZE - SCREEN_HEIGHT // 2

            # --- Input ---
            player_acted = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                if event.type == pygame.KEYDOWN:
                    dx, dy = 0, 0
                    if event.key == pygame.K_LEFT:   dx = -1
                    if event.key == pygame.K_RIGHT:  dx =  1
                    if event.key == pygame.K_UP:     dy = -1
                    if event.key == pygame.K_DOWN:   dy =  1
                    if event.key == pygame.K_PERIOD:
                        player_acted = True

                    # Use inventory item
                    for i, key in enumerate([pygame.K_1, pygame.K_2, pygame.K_3,
                                             pygame.K_4, pygame.K_5]):
                        if event.key == key and i < len(inventory):
                            item = inventory.pop(i)
                            item.identified = True
                            if item.kind == "potion":
                                if item.value > 0:
                                    player_hp = min(PLAYER_MAX_HP, player_hp + item.value)
                                    log.append(f"Used {item.name}. HP restored.")
                                else:
                                    player_hp += item.value
                                    log.append(f"Used {item.name}. You feel sick!")
                                if item.subtype == "strength":
                                    player_atk += item.value
                                    log.append("You feel stronger!")
                            elif item.kind == "weapon":
                                player_atk += item.value
                                log.append(f"Equipped {item.name}.")
                            elif item.kind == "armor":
                                player_def += item.value
                                log.append(f"Equipped {item.name}.")
                            player_acted = True

                    if dx != 0 or dy != 0:
                        nx, ny = px + dx, py + dy
                        target = next((e for e in enemies if e.tx == nx and e.ty == ny), None)
                        if target:
                            dmg = max(1, player_atk)
                            target.hp -= dmg
                            log.append(f"You hit for {dmg} dmg. ({target.hp}/{target.max_hp})")
                            if target.hp <= 0:
                                enemies.remove(target)
                                log.append("Enemy defeated!")
                            player_acted = True
                        elif dungeon.tiles[ny][nx] in ("floor", "stairs"):
                            px, py = nx, ny
                            player_acted = True

                            # Pick up item
                            for item in items[:]:
                                if item.tx == px and item.ty == py:
                                    if len(inventory) < 5:
                                        inventory.append(item)
                                        items.remove(item)
                                        log.append(f"Picked up {item.name}.")
                                    else:
                                        log.append("Inventory full!")

                            # Stairs
                            if dungeon.tiles[py][px] == "stairs":
                                floor += 1
                                dungeon, enemies, items = make_level(floor)
                                px, py = dungeon.rooms[0].center()
                                explored = set()
                                log.append(f"You descend to floor {floor}.")

            # --- Enemy turns ---
            if player_acted:
                for enemy in enemies[:]:
                    result = enemy.take_turn(px, py, dungeon.tiles, enemies)
                    if result and result[0] == "attack":
                        dmg = max(1, result[1] - player_def)
                        player_hp -= dmg
                        log.append(f"Enemy hits you for {dmg} dmg.")

                if player_hp <= 0:
                    restart = game_over_screen(screen, font_big, font)
                    if restart:
                        break
                    else:
                        pygame.quit()
                        return

            # --- Draw ---
            screen.fill((0, 0, 0))
            for row in range(dungeon.map_height):
                for col in range(dungeon.map_width):
                    tile = dungeon.tiles[row][col]
                    sx = col * TILE_SIZE - camera_x
                    sy = row * TILE_SIZE - camera_y
                    in_fov = (col, row) in visible
                    in_exp = (col, row) in explored

                    if in_fov:
                        if tile == "wall":
                            screen.blit(tileset.get_wall(col, row), (sx, sy))
                        elif tile == "stairs":
                            screen.blit(tileset.get_stair(), (sx, sy))
                        elif tile == "floor":
                            screen.blit(tileset.get_floor(col, row), (sx, sy))
                    elif in_exp:
                        screen.blit(tileset.get_dimmed(col, row, tile), (sx, sy))

            # Items only visible in FOV
            for item in items:
                if (item.tx, item.ty) in visible:
                    item.draw(screen, camera_x, camera_y)

            # Enemies only visible in FOV
            for enemy in enemies:
                if (enemy.tx, enemy.ty) in visible:
                    enemy.draw(screen, camera_x, camera_y)

            for row in range(dungeon.map_height):
                for col in range(dungeon.map_width):
                    if (col, row) not in explored:
                        continue
                    tile = dungeon.tiles[row][col]
                    if tile == "wall":
                        color = (60, 60, 60)
                    elif tile == "stairs":
                        color = (200, 180, 50)
                    else:
                        color = (120, 120, 120)
                    pygame.draw.rect(screen, color, (MINIMAP_X + col * MINIMAP_TILE, MINIMAP_Y + row * MINIMAP_TILE, MINIMAP_TILE, MINIMAP_TILE))


            screen.blit(player_sprite, (px * TILE_SIZE - camera_x, py * TILE_SIZE - camera_y))
            draw_hud(screen, player_hp, PLAYER_MAX_HP, player_atk, player_def, floor, log, inventory, font)
            pygame.display.flip()


if __name__ == "__main__":
    main()
