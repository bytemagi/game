import pygame
from dungeon import Dungeon

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 32
FPS = 60
dungeon = Dungeon(80, 50)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    pygame.display.set_caption("Untitled Game")
    clock = pygame.time.Clock()

    running = True
    while running: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        for row in range(dungeon.map_height):
            for col in range(dungeon.map_width):
                if dungeon.tiles[row][col] == "floor":
                    pygame.draw.rect(screen, (100, 100, 100), (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()

