import pygame
from dungeon import Dungeon
from Enemy import Enemy

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 32
FPS = 60
PLAYER_SPEED = 3
PLAYER_HP = 100

dungeon = Dungeon(80, 50)

def get_spawn(rooms):
    cx, cy = rooms[0].center()
    return cx * TILE_SIZE, cy * TILE_SIZE

def collides_with_wall(rect, tiles, map_width, map_height):
    corners = [
        (rect.left, rect.top),
        (rect.right - 1, rect.top),
        (rect.left, rect.bottom - 1),
        (rect.right - 1, rect.bottom - 1),
    ]
    for cx, cy in corners:
        col = cx // TILE_SIZE
        row = cy // TILE_SIZE
        if 0 <= row < map_height and 0 <= col < map_width:
            if tiles[row][col] == "wall":
                return True
        else:
            return True
    return False

def draw_player_hp(surface, hp, max_hp):
    bar_x, bar_y, bar_w, bar_h = 10, 10, 150, 14
    pygame.draw.rect(surface, (80, 0, 0), (bar_x, bar_y, bar_w, bar_h))
    pygame.draw.rect(surface, (220, 0, 0), (bar_x, bar_y, int(bar_w * hp / max_hp), bar_h))
    font = pygame.font.SysFont(None, 16)
    surface.blit(font.render(f"HP {hp}/{max_hp}", True, (255, 255, 255)), (bar_x + 2, bar_y + 1))

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Untitled Game")
    clock = pygame.time.Clock()

    player_sprite = pygame.image.load("assets/player.png")
    player_sprite = pygame.transform.scale(player_sprite, (TILE_SIZE - 4, TILE_SIZE - 4))

    spawn_x, spawn_y = get_spawn(dungeon.rooms)
    player = pygame.Rect(spawn_x, spawn_y, TILE_SIZE - 4, TILE_SIZE - 4)
    player_hp = PLAYER_HP

    enemies = []
    for room in dungeon.rooms[1:]:
        cx, cy = room.center()
        enemies.append(Enemy(cx * TILE_SIZE, cy * TILE_SIZE))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    attack_rect = player.inflate(20, 20)
                    for enemy in enemies[:]:
                        if attack_rect.colliderect(enemy.rect):
                            enemy.hp -= 10
                            if enemy.hp <= 0:
                                enemies.remove(enemy)

        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[pygame.K_LEFT]:  dx = -PLAYER_SPEED
        if keys[pygame.K_RIGHT]: dx =  PLAYER_SPEED
        if keys[pygame.K_UP]:    dy = -PLAYER_SPEED
        if keys[pygame.K_DOWN]:  dy =  PLAYER_SPEED
        player.x += dx
        if collides_with_wall(player, dungeon.tiles, dungeon.map_width, dungeon.map_height):
            player.x -= dx

        player.y += dy
        if collides_with_wall(player, dungeon.tiles, dungeon.map_width, dungeon.map_height):
            player.y -= dy

        # Camera centers on player
        camera_x = player.centerx - SCREEN_WIDTH // 2
        camera_y = player.centery - SCREEN_HEIGHT // 2

        for enemy in enemies:
            enemy.update(player, dungeon.tiles, dungeon.map_width, dungeon.map_height, enemies)

        # Draw
        screen.fill((0, 0, 0))
        for row in range(dungeon.map_height):
            for col in range(dungeon.map_width):
                if dungeon.tiles[row][col] == "floor":
                    pygame.draw.rect(screen, (100, 100, 100),
                        (col * TILE_SIZE - camera_x, row * TILE_SIZE - camera_y, TILE_SIZE, TILE_SIZE))

        for enemy in enemies:
            enemy.draw(screen, camera_x, camera_y)

        screen.blit(player_sprite, (player.x - camera_x, player.y - camera_y))


        draw_player_hp(screen, player_hp, PLAYER_HP)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
