from ward_sol import *

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


def tile_direction():
    {
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
    {
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
            file.write(row + '\n')
        pass


def solution():
    results = []
    for i in range(W):
        for j in range(H):
            pass
    return results


if __name__ == "__main__":
    file_0 = "00-trailer.txt"
    file_1 = "01-comedy.txt"
    file_2 = "02-sentimental.txt"
    file_3 = "03-adventure.txt"
    file_4 = "04-drama.txt"
    file_5 = "05-horror.txt"

    current_file = file_0

    W, H, Gn, Sm, Tl, golden_points, silver_points, tiles = parse_data(current_file)

    print(f"Width: {W}, Height: {H}, Golden Points: {Gn}, Silver Points: {Sm}, Tiles Types: {Tl}")
    for golden_point in golden_points:
        print(f"Golden Point x:{golden_point.x}|y:{golden_point.y}")
    for silver_point in silver_points:
        print(f"Silver Point x:{silver_point.x}|y:{silver_point.y}|score:{silver_point.score}")
    for tile_key, tile in tiles.items():
        print(f"Tile id:{tile_key}|cost:{tile.cost}|num:{tile.num_of_tiles}")

    # Create Tile Manager
    tile_manager = TileManager(tiles)


    data_solution = solution()

    output_results(current_file)
