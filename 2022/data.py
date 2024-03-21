serial_ID = 0


class Demon:
    def __init__(self, S, T, Sr, No, Na):
        self.T = T
        self.S = S
        self.Sr = Sr
        self.No = No
        self.Na = Na
        self.ID = serial_ID
        self.max_point = sum([int(x) for x in Na])
        self.points_to_get = self.max_point

        self.fought_turn = None
        self.recovered = False

    def fight(self, current_turn):
        self.fought_turn = current_turn

    def tick(self, current_turn):
        if self.recovered:
            return 0
        if self.fought_turn is not None:
            if self.T - (current_turn - self.fought_turn) <= 0:
                self.recovered = True
                return self.Sr
            else:
                return 0
        else:
            return 0

    def __str__(self):
        return f'{self.S} {self.T} {self.Sr} {self.No} {self.Na}'

    def calcualte_points(self, turns_left):
        if turns_left < self.No:
            self.points_to_get = sum([int(x) for x in self.Na[:turns_left]])
        else:
            self.points_to_get = sum([int(x) for x in self.Na])
