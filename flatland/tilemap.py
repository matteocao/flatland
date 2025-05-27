class TileMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [["grass" for _ in range(width)] for _ in range(height)]

    def get_tile(self, x, y):
        return self.grid[y % self.height][x % self.width]

    def set_tile(self, x, y, tile_type):
        self.grid[y % self.height][x % self.width] = tile_type

    def is_walkable(self, x, y):
        return self.get_tile(x, y) in ["grass"]