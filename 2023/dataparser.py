from dataclass import Snake


def parse_data(file_name):
    game_map = []
    first_line = None
    snakes = None
    longest_snake = 0
    with open(file_name) as file:
        for line in file:
            if first_line is None:
                first_line = line.split()
            elif snakes is None:
                second_line = line.split()
                snakes = []
                for i in second_line:
                    snakes.append(Snake(int(i)))
                    if int(i) > longest_snake:
                        longest_snake = int(i)
            else:
                arr = line.split()
                game_map.append([int(i) if i != '*' else i for i in arr])
    return first_line, snakes, game_map, longest_snake
