class Snake:
    def __init__(self, length):
        self.len = length
        self.start_row = None
        self.start_column = None
        self.row = None
        self.column = None
        self.worm_hole_row = None
        self.worm_hole_column = None
        self.commands = []
        self.step_entered_worm_hole = None


    def flush(self):
        self.commands = []

    def __str__(self):
        return f'{self.len}'

    def __repr__(self):
        return f'{self.len}'


class Point:

    def __init__(self, row, column, value, direction):
        self.row = row
        self.column = column
        self.value = value
        self.direction = direction

    def __eq__(self, other):
        return self.row == other.row and self.column == other.column

    def __str__(self):
        return f'{self.row} | {self.column}'

    def __repr__(self):
        return f'{self.row} | {self.column}'
