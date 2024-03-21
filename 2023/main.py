import random

from dataclass import Point
from dataparser import parse_data

def flush_path(points):
    for p in points:
        snakes_map[p.row][p.column] = 0

def greedy(s):
    path = []
    start_p = Point(s.start_row, s.start_column, 0, 0)
    path.append(start_p)
    snakes_map[s.start_row][s.start_column] = 1
    neighbours = get_highest_neighbour(s.start_row, s.start_column, [start_p])
    res = []
    greedy_rec(neighbours, 0, s.len, res, [])
    for po in res:
        snakes_map[po.row][po.column] = 1
        s.commands.append(po.direction)
        s.commands.reverse()
    print(len(res))
    # for i in range(s.len):
    #     direct = get_highest_neighbour(s)
    #     path.append(Point(s.row, s.column))
    #     snakes_map[s.row][s.column] = 1
    #     if direct == 'F':
    #         s.flush()
    #         flush_path(path)
    #         return False
    #     s.commands.append(direct)
    return True

def greedy_rec(neighb, lvl, slen, res, visited):
    if lvl == slen and len(neighb) > 0:
        res.append(neighb[0])
        return
    for n in neighb:
        snakes_map[n.row][n.column] = 1
        neighbours = get_highest_neighbour(n.row, n.column, visited)
        greedy_rec(neighbours, lvl+1, slen, res, visited)
        if len(res) > 0:
            res.append(n)
            return
        else:
            snakes_map[n.row][n.column] = 0

def choose_warm_hole():
    pass

def get_highest_neighbour(x, y, visited):
    left = y-1 if y-1 >= 0 else columns-1
    right = y+1 if y+1 < columns else 0
    down = x+1 if x+1 < rows else 0
    up = x-1 if x-1 >= 0 else rows-1

    val_left = game_map[x][left]
    val_right = game_map[x][right]
    val_down = game_map[down][y]
    val_up = game_map[up][y]

    left_free = snakes_map[x][left]
    right_free = snakes_map[x][right]
    down_free = snakes_map[down][y]
    up_free = snakes_map[up][y]

    free_vals = [left_free, right_free, down_free, up_free]
    vals = [val_left, val_right, val_down, val_up]
    point_arr = []
    for i in range(len(vals)):
        if free_vals[i] == 1:
            continue
        if vals[i] == '*':
            continue
        if i == 0:
            p = Point(x, left, val_left, 'L')
            if p not in visited:
                point_arr.append(p)
        elif i == 1:
            p = Point(x, right, val_right, 'R')
            if p not in visited:
                point_arr.append(p)
            point_arr.append(p)
        elif i == 2:
            p = Point(down, y, val_down, 'D')
            if p not in visited:
                point_arr.append(p)
            point_arr.append(p)
        else:
            p = Point(up, y, val_up, 'U')
            if p not in visited:
                point_arr.append(p)
            point_arr.append(p)
    point_arr.sort(key=lambda v: v.value, reverse=True)
    return point_arr

def output():
    with open(f'out_{current_file}.txt', mode='w') as file:
        for snak in snakes:
            snak.commands.pop()
            to_write = f'{snak.start_column} {snak.start_row}'
            for c in snak.commands:
                to_write += f' {c}'
            file.write(to_write + '\n')


random.seed(69420911)
file_0 = "00-example.txt"
file_1 = "01-chilling-cat.txt"
file_2 = "02-swarming-ant.txt"
file_3 = "03-input-anti-greedy.txt"
file_4 = "04-input-low-points.txt"
file_5 = "05-input-opposite-points-holes.txt"

current_file = file_4

first_line, snakes, game_map, longest_snake = parse_data(current_file)
columns = int(first_line[0])
rows = int(first_line[1])
snakes_num = int(first_line[2])
# game_map[row][col]
worm_holes = []
snakes_map = [[0 for x in range(columns)] for y in range(rows)]
for i in range(rows):
    for j in range(columns):
        if game_map[i][j] == '*':
            worm_holes.append(Point(i, j, 0, 0))

start_position = False
snake_assigned = False
for snake in snakes:
    while not snake_assigned:
        while not start_position:
            ran_col = random.randint(0, columns-1)
            ran_row = random.randint(0, rows-1)
            if snakes_map[ran_row][ran_col] == 0 and game_map[ran_row][ran_col] != '*':
                start_position = True

        snake.row = ran_row
        snake.column = ran_col
        snake.start_row = ran_row
        snake.start_column = ran_col
        SUCC = greedy(snake)
        if SUCC:
            snake_assigned = True
        start_position = False
    snake_assigned = False

output()


