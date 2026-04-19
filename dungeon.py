import random

class Room:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def center(self):
        return(self.x + self.width // 2, self.y + self.height // 2)

    def overlaps(self, other):
        return (self.x <= other.x + other.width and self.x + self.width >= other.x and self.y <= other.y + other.height and self.y+ self.height >= other.y)

class Dungeon:
    def __init__(self, map_width, map_height):
        self.map_width = map_width
        self.map_height = map_height
        self.tiles = [["wall" for x in range(map_width)] for y in range(map_height)]
        self.rooms = []
        self.generate()

    def generate(self):
        for _ in range(10):
            w = random.randint(6, 12)
            h = random.randint(6, 12)
            x = random.randint(1, self.map_width - w - 1)
            y = random.randint(1, self.map_height -h - 1)
            new_room = Room(x, y , w, h)
            if not any(new_room.overlaps(r) for r in self.rooms):
                for row in range(y, y + h):
                    for col in range(x, x + w):
                        self.tiles[row][col] = "floor"
                self.rooms.append(new_room)
                if len(self.rooms) > 1:
                    prev_center = self.rooms[-2].center()
                    new_center = self.rooms[-1].center()
                    self.carve_corridor(prev_center, new_center)

    def carve_corridor(self, start, end):
        x1, y1 = start
        x2, y2 = end
        #carve horizontal, then verticle
        for col in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[y1][col] = "floor"
        for row in range(min (y1, y2), max(y1, y2) + 1):
            self.tiles[row][x2] = "floor"