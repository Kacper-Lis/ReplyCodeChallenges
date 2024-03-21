

class TILE_MAPPINGS:
    id_to_directions = {
        "3": ["LR"],
        "5": ["DR"],
        "6": ["LD"],
        "7": ["LR", "LD", "DR"],
        "9": ["UR"],
        "96": ["LD", "UR"],
        "A": ["LU"],
        "A5": ["LU", "DR"],
        "B": ["LR", "LU", "UR"],
        "C": ["UD"],
        "C3": ["LR", "UD"],
        "D": ["UD", "UR", "DR"],
        "E": ["LU", "LD", "UD"],
        "F": ["LR", "LD", "LU", "UD", "DR", "UR"],
    }
    direction_to_ids = {
        "LR": ["3", "7", "B", "C3", "F"],
        "UD": ["C", "C3", "D", "E", "F"],
        "LU": ["A", "A5", "B", "E", "F"],
        "LD": ["6", "7", "96", "E", "F"],
        "UR": ["9", "96", "B", "D", "F"],
        "DR": ["5", "7", "A5", "D", "F"],
        #Same but opposite
        "RL": ["3", "7", "B", "C3", "F"],
        "DU": ["C", "C3", "D", "E", "F"],
        "UL": ["A", "A5", "B", "E", "F"],
        "DL": ["6", "7", "96", "E", "F"],
        "RU": ["9", "96", "B", "D", "F"],
        "RD": ["5", "7", "A5", "D", "F"],
    }

class TileManager():
    def __init__(self, tiles):
        self.main_tile_list = tiles
        self.create_tile_dictionary()

    def create_tile_dictionary(self):
        self.tile_dictionary = {}
        self.tile_avaliability_dict = {}
        for tile in self.main_tile_list:
            self.tile_dictionary[tile.id] = tile
            self.tile_avaliability_dict[tile.id] = tile.num_of_tiles

    def check_if_tile_is_avaliable(self, tile_id):
        if (self.tile_avaliability_dict[tile_id] > 0):
            return True
        else:
            return False

    def get_tile_based_on_direction_list(self, directions):
        # Initialize the set of matching tile IDs with the tile IDs that match the first direction
        matching_tile_ids = set(TILE_MAPPINGS.direction_to_ids[directions[0]])

        # For each subsequent direction, intersect the current set of matching tile IDs with the tile IDs that match the current direction
        for direction in directions[1:]:
            matching_tile_ids &= set(TILE_MAPPINGS.direction_to_ids[direction])

        # Get the first matching tile ID, Returns None if no tile ID matches all directions
        tile_id = next(iter(matching_tile_ids), None)

        return self.tile_dictionary[tile_id]
        

    def get_tile(self, tile_id):
        if tile_id in self.tile_avaliability_dict:
            self.tile_avaliability_dict[tile_id] -= 1
            return self.tile_dictionary[tile_id].id
        else:
            raise Exception("NO TILE TYPE DETECTED")


