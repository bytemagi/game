import pygame
import random

TILE_SIZE = 32

class Enemy:
    def __init__(self, x, y, hp=50):
        self.rect = pygame.Rect(x, y, TILE_SIZE - 4, TILE_SIZE - 4)
        self.sprite = pygame.image.load("assets/enemy.png")
        self.sprite = pygame.transform.scale(self.sprite, (TILE_SIZE - 4, TILE_SIZE - 4))
        self.hp = hp
        self.max_hp = hp
        self.speed = 1
        self.aggro_range = TILE_SIZE * 5
        self.move_timer = 0
        self.move_interval = 60  # frames between random moves
        self.dx = 0
        self.dy = 0

    def update(self, player_rect, tiles, map_width, map_height, enemies):
        px, py = player_rect.centerx, player_rect.centery
        ex, ey = self.rect.centerx, self.rect.centery
        dist = ((px - ex) ** 2 + (py - ey) ** 2) ** 0.5

        if dist < self.aggro_range:
            step = self.speed
            self.dx = step if px > ex else -step if px < ex else 0
            self.dy = step if py > ey else -step if py < ey else 0
        else:
            self.move_timer += 1
            if self.move_timer >= self.move_interval:
                self.move_timer = 0
                self.dx = random.choice([-self.speed, 0, self.speed])
                self.dy = random.choice([-self.speed, 0, self.speed])

        self._move(self.dx, 0, tiles, map_width, map_height)
        self._move(0, self.dy, tiles, map_width, map_height)
        self._separate(enemies)

    def _separate(self, enemies):
        for other in enemies:
            if other is self:
                continue
            if self.rect.colliderect(other.rect):
                ox = self.rect.centerx - other.rect.centerx
                oy = self.rect.centery - other.rect.centery
                if ox == 0 and oy == 0:
                    ox, oy = 1, 0
                length = (ox ** 2 + oy ** 2) ** 0.5
                self.rect.x += int(ox / length * 2)
                self.rect.y += int(oy / length * 2)

    def _move(self, dx, dy, tiles, map_width, map_height):
        self.rect.x += dx
        if self._collides_with_wall(tiles, map_width, map_height):
            self.rect.x -= dx

        self.rect.y += dy
        if self._collides_with_wall(tiles, map_width, map_height):
            self.rect.y -= dy

    def _collides_with_wall(self, tiles, map_width, map_height):
        corners = [
            (self.rect.left, self.rect.top),
            (self.rect.right - 1, self.rect.top),
            (self.rect.left, self.rect.bottom - 1),
            (self.rect.right - 1, self.rect.bottom - 1),
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

    def draw(self, surface, camera_x, camera_y):
        draw_x = self.rect.x - camera_x
        draw_y = self.rect.y - camera_y

        surface.blit(self.sprite, (draw_x, draw_y))

        # HP bar
        bar_w = self.rect.width
        hp_ratio = self.hp / self.max_hp
        pygame.draw.rect(surface, (100, 0, 0), (draw_x, draw_y - 6, bar_w, 4))
        pygame.draw.rect(surface, (220, 0, 0), (draw_x, draw_y - 6, int(bar_w * hp_ratio), 4))
