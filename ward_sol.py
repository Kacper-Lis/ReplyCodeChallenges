import heapq

class TILE_MAPPINGS:
    id_to_directions = {
        "3": "LR",
        "5": "DR",
        "6": "LD",
        "7": "LR LD DR",
        "9": "UR",
        "96": "LD UR",
        "A": "LU",
        "A5": "LU DR",
        "B": "LR LU UR",
        "C": "UD",
        "C3": "LR UD",
        "D": "UD UR DR",
        "E": "LU LD UD",
        "F": "LR LD LU UD DR UR",
    }
    direction_to_ids = {
        # "LR": ["3", "7", "B", "C3", "F"],
        # "UD": ["C", "C3", "D", "E", "F"],
        # "LU": ["A", "A5", "B", "E", "F"],
        # "LD": ["6", "7", "96", "E", "F"],
        # "UR": ["9", "96", "B", "D", "F"],
        # "DR": ["5", "7", "A5", "D", "F"],
        # #Same but opposite
        # "RL": ["3", "7", "B", "C3", "F"],
        # "DU": ["C", "C3", "D", "E", "F"],
        # "UL": ["A", "A5", "B", "E", "F"],
        # "DL": ["6", "7", "96", "E", "F"],
        # "RU": ["9", "96", "B", "D", "F"],
        # "RD": ["5", "7", "A5", "D", "F"],
        "LR": {"3", "7", "B", "F"},
        "UD": {"C", "D", "E", "F"},
        "LU": {"A", "B", "E", "F"},
        "LD": {"6", "7", "E", "F"},
        "UR": {"9", "B", "D", "F"},
        "DR": {"5", "7", "D", "F"},
        #Same but opposite
        "RL": {"3", "7", "B", "F"},
        "DU": {"C", "D", "E", "F"},
        "UL": {"A", "B", "E", "F"},
        "DL": {"6", "7", "E", "F"},
        "RU": {"9", "B", "D", "F"},
        "RD": {"5", "7", "D", "F"},
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

        return self.get_tile(tile_id)

    def get_tile(self, tile_id):
        '''Returns tile and keeps track of it'''

        if tile_id in self.tile_avaliability_dict:
            self.tile_avaliability_dict[tile_id] -= 1
            return self.tile_dictionary[tile_id].id
        elif tile_id.id in self.tile_avaliability_dict:
            self.tile_avaliability_dict[tile_id.id] -= 1
            return tile_id.id
        else:
            raise Exception("NO TILE TYPE DETECTED")

    def get_cheapest_tile_with_directions(self, directions):
        direction_tiles = self.get_tile_based_on_direction_list(directions)

        cheapest_tile_cost = 999999999999999999999999
        cheapest_tile = direction_tiles[0]

        for tile in direction_tiles:
            if self.check_if_tile_is_avaliable(tile):
                if self.tile_dictionary[tile].cost < cheapest_tile_cost:
                    cheapest_tile_cost = self.tile_dictionary[tile].cost
                    cheapest_tile = self.tile_dictionary[tile]

        return cheapest_tile


class PathFinder():
    '''Gets a selected golden point and finds the path to the nearest silver or golden point'''

    def __init__(self, golden_point_list, silver_point_list, golden_point, tilemanager, width, height):
        self.golden_point_list = golden_point_list
        self.silver_point_list = silver_point_list
        self.golden_point = golden_point

        self.tile_manager = tilemanager
        self.tilemap = TileMap(width, height)

        self.create_golden_paths()

    def create_golden_paths(self):
        tolerance = 20 # Get the points within this amount

        silver_point_list = []
        closest_golden_points = []
        closest_golden_point_distance = 999999999999
        second_closest_golden_point_distance = 9999999999999

        for silver_point in self.silver_point_list:
            x_diff = abs(silver_point.x - self.golden_point.x)
            y_diff = abs(silver_point.y - self.golden_point.y)
            if x_diff < tolerance and y_diff < tolerance:
                silver_point_list.append(silver_point)

        for golden_point in self.golden_point_list:
            x_diff = abs(golden_point.x - self.golden_point.x)
            y_diff = abs(golden_point.y - self.golden_point.y)
            distance = x_diff + y_diff
            if distance < closest_golden_point_distance:
                closest_golden_points.append(golden_point)
                closest_golden_point_distance = distance
            elif distance < second_closest_golden_point_distance:
                closest_golden_points.append(golden_point)

        # Got the Silver points within list and Golden points
        for silver_point in silver_point_list:
            self.create_path(self.golden_point, silver_point)

        for golden_point in self.golden_point_list:
            self.create_path(self.golden_point, golden_point)

        return self.tilemap.compile_solution()

    def create_path(self, golden_point, silver_point):
        diff_x = silver_point.x - golden_point.x
        diff_y = silver_point.y - golden_point.y

        # Select cheapest option
        # Get the amount of R's or L's
        # Diff x - if negative: L, if positive: R
        # Diff y - if negative: U, if positive: D

        current_pos_x = golden_point.x
        current_pos_y = golden_point.y

        # Start path creation
        path = []
        current_path_cost = 0

        while diff_x != 0:
            if diff_x < 0:
                path.append("LR")
                cheapest_tile = self.tile_manager.get_cheapest_tile_with_directions(path)
                # current_path_cost += self.tile_manager.tile_dictionary[cheapest_tile].cost
                self.tilemap.add_tile(current_pos_x, current_pos_y, cheapest_tile)
                self.tile_manager.get_tile(cheapest_tile.id)

                current_pos_x -= 1
                path = []

            elif diff_x > 0:
                path.append("RL")
                cheapest_tile = self.tile_manager.get_cheapest_tile_with_directions(path)
                # current_path_cost += self.tile_manager.tile_dictionary[cheapest_tile].cost
                self.tilemap.add_tile(current_pos_x, current_pos_y, cheapest_tile)
                self.tile_manager.get_tile(cheapest_tile)

                current_pos_x += 1
                path = []

        path = ["RL"]

        while diff_y != 0:
            if diff_y < 0:
                path.append("UD")
                cheapest_tile = self.tile_manager.get_cheapest_tile_with_directions(path)
                # current_path_cost += self.tile_manager.tile_dictionary[cheapest_tile].cost
                self.tilemap.add_tile(current_pos_x, current_pos_y, cheapest_tile)
                self.tile_manager.get_tile(cheapest_tile.id)

                current_pos_y += 1
                path = []

            elif diff_y > 0:
                path.append("DU")
                cheapest_tile = self.tile_manager.get_cheapest_tile_with_directions(path)
                # current_path_cost += self.tile_manager.tile_dictionary[cheapest_tile].cost
                self.tilemap.add_tile(current_pos_x, current_pos_y, cheapest_tile)
                self.tile_manager.get_tile(cheapest_tile.id)

                current_pos_y -= 1
                path = []

class TileMap():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[None for i in range(width)] for j in range(height)]

    def add_tile(self, x, y, tile):
        print(len(self.grid[:][y]))
        self.grid[x][y] = tile

    def compile_solution(self):
        output = []
        for x in range(len(self.width)):
            for y in range(len(self.height)):
                if self.grid[x][y] is not None:
                    output.append([self.grid[x][y], x, y])
        return output

