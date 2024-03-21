class GoldenPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Tile:
    def __init__(self, id, cost, num_of_tiles):
        self.id = id
        self.cost = cost
        self.num_of_tiles = num_of_tiles


class SilverPoint:
    def __init__(self, x, y, score):
        self.x = x
        self.y = y
        self.score = score


class MapPoint:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.directions = [direction]


def tile_direction(direction):
    tile_id_to_dir = {
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
    dir_to_tile_ids = {
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

    return dir_to_tile_ids[direction]


def parse_data(file_name):
    W = 0
    H = 0
    Gn = 0
    Sm = 0
    Tl = 0
    golden_points = []
    silver_points = []
    tiles = {}
    first_line = None
    golden_points_counter = 0
    silver_points_counter = 0
    tile_types_counter = 0
    with open(file_name, 'r', encoding='utf-8-sig') as file:
        for line in file:
            if first_line is None:
                first_line = line.split()
                W = int(first_line[0])
                H = int(first_line[1])
                Gn = int(first_line[2])
                Sm = int(first_line[3])
                Tl = int(first_line[4])
                golden_points_counter = Gn
                silver_points_counter = Sm
                tile_types_counter = Tl
            elif golden_points_counter > 0:
                golden_points_counter -= 1
                first_line = line.split()
                golden_points.append(GoldenPoint(int(first_line[0]), int(first_line[1])))
            elif silver_points_counter > 0:
                silver_points_counter -= 1
                first_line = line.split()
                silver_points.append(SilverPoint(int(first_line[0]), int(first_line[1]), int(first_line[2])))
            elif tile_types_counter > 0:
                tile_types_counter -= 1
                first_line = line.split()
                tiles[first_line[0]] = Tile(first_line[0], int(first_line[1]), int(first_line[2]))

    return W, H, Gn, Sm, Tl, golden_points, silver_points, tiles


def output_results(file_name):
     with open(f'out_{file_name}.txt', mode='w') as file:
        for row in data_solution:
            file.write(f"{row.directions[0]} {row.x} {row.y}\n")


def find_common_elements(sets):
    common_elements = sets[0]  # Start with the first set

    for s in sets[1:]:
        common_elements = common_elements.intersection(s)

    return common_elements


def calculate_middle_point():
    # Calculate the total sum of x-coordinates and y-coordinates
    total_x = sum(point.x for point in golden_points)
    total_y = sum(point.y for point in golden_points)

    # Calculate the average (mean) of x-coordinates and y-coordinates
    middle_x = total_x / len(golden_points)
    middle_y = total_y / len(golden_points)

    return int(middle_x), int(middle_y)


def add_to_grid(grid, x, y, direction):
    if grid[x][y] is None:
        grid[x][y] = MapPoint(x, y, direction)
        map_tiles.append(grid[x][y])
    else:
        grid[x][y].directions.append(direction)

def solution():
    middle_x, middle_y = calculate_middle_point()
    grid = [[None for _ in range(H)] for _ in range(W)]
    print(f"Middle Point: x:{middle_x}|y:{middle_y}")
    for golden_point in golden_points:
        x_diff = golden_point.x - middle_x
        y_diff = golden_point.y - middle_y
        current_x = golden_point.x
        current_y = golden_point.y
        while x_diff != 0:
            if x_diff < 0:
                # From left to right
                x_diff += 1
                current_x += 1
                if current_x == 0:
                    if y_diff > 0:
                        add_to_grid(grid, current_x, current_y, "DL")
                    else:
                        add_to_grid(grid, current_x, current_y, "UL")
                else:
                    add_to_grid(grid, current_x, current_y, "LR")
            else:
                # From right to left
                x_diff -= 1
                current_x -= 1
                if current_x == 0:
                    if y_diff > 0:
                        add_to_grid(grid, current_x, current_y, "DR")
                    else:
                        add_to_grid(grid, current_x, current_y, "UR")
                else:
                    add_to_grid(grid, current_x, current_y, "LR")
        while y_diff != 0:
            if y_diff > 0:
                # From down to up
                y_diff -= 1
                current_y -= 1
                add_to_grid(grid, current_x, current_y, "UD")
            else:
                # From up to down
                y_diff += 1
                current_y += 1
                add_to_grid(grid, current_x, current_y, "UD")

    tile_placement = []
    for tile in map_tiles:
        if len(tile.directions) == 1:
            common_tile_ids = tile_direction(tile.directions[0])
            for tile_id_c in common_tile_ids:
                if tiles[tile_id_c].num_of_tiles > 0:
                    tile_placement.append(MapPoint(tile.x, tile.y, tile_id_c))
                    tiles[tile_id_c].num_of_tiles -= 1
                    break
        else:
            list_of_dirs = []
            for direction in tile.directions:
                list_of_dirs.append(tile_direction(direction))
            common_tile_ids = find_common_elements(list_of_dirs)
            for tile_id_c in common_tile_ids:
                if tiles[tile_id_c].num_of_tiles > 0:
                    tile_placement.append(MapPoint(tile.x, tile.y, tile_id_c))
                    tiles[tile_id_c].num_of_tiles -= 1
                    break

    return tile_placement


if __name__ == "__main__":
    file_0 = "00-trailer.txt"
    file_1 = "01-comedy.txt"
    file_2 = "02-sentimental.txt"
    file_3 = "03-adventure.txt"
    file_4 = "04-drama.txt"
    file_5 = "05-horror.txt"

    current_file = file_5

    W, H, Gn, Sm, Tl, golden_points, silver_points, tiles = parse_data(current_file)

    print(f"Width: {W}, Height: {H}, Golden Points: {Gn}, Silver Points: {Sm}, Tiles Types: {Tl}")
    for golden_point in golden_points:
        print(f"Golden Point x:{golden_point.x}|y:{golden_point.y}")
    for silver_point in silver_points:
        print(f"Silver Point x:{silver_point.x}|y:{silver_point.y}|score:{silver_point.score}")
    for tile_key, tile in tiles.items():
        print(f"Tile id:{tile_key}|cost:{tile.cost}|num:{tile.num_of_tiles}")

    map_tiles = []

    data_solution = solution()

    output_results(current_file)
