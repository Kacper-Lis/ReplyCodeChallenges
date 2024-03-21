import copy, random
import numpy as np


class QueenProblem:
    
    def __init__(self, n, fixed_x, fixed_y):
        self.board = []
        self.queens = []
        self.blocked = []
        self.n = n #board size
        self.fixed_x = fixed_x
        self.fixed_y = fixed_y
        self.max = 100 #points blocked by fixed queen
        self.solutions = []
        
    #Create a matrix with blocked tiles that holds the score for each tile
    def define_blocked_paths(self, step=0):
        matrix = np.zeros((self.n,self.n))
        self.block_paths(self.fixed_x, self.fixed_y, matrix, fixed=True)
        for i in range(step+1):
            if self.queens[i].fixed:
                continue
            self.block_paths(self.queens[i].x, self.queens[i].y, matrix)
        #Offest queen position due to blocking on the board 4 times
        for i in range(step+1):
            matrix[self.queens[i].x][self.queens[i].y] -= 4
            
        self.blocked = matrix
    
    #Given queen position, increase the score for each tile it is blocking
    def block_paths(self, x, y, matrix, fixed=False):
        point = self.max if fixed else 1
        #Block column and rows
        for i in range(self.n):
            matrix[x][i] += point
            matrix[:,y][i] += point
        #Block diagonals 
        rows, cols = np.indices((self.n,self.n))
        diag1 = y - x
        diag2 = 7 - (y+x)
        row_vals = np.diag(rows, k=diag1)
        col_vals = np.diag(cols, k=diag1)
        matrix[row_vals,col_vals] += point
        row_vals = np.diag(np.fliplr(rows), k=diag2)
        col_vals = np.diag(np.fliplr(cols), k=diag2)
        matrix[row_vals,col_vals] += point
    
    def solve(self):
        self.create_board()
        step = 0
        #root starts at the first row unless fixed queen is on first row
        if self.fixed_x == 0:
            step = 1
            root = self.create_queue(step, True)
        else:
            root = self.create_queue(step, True)
        
        #Check every possible move for starting row
        while root:
            self.move_queen(self.queens[step], root.pop(0))
            self.define_blocked_paths(step)
            self.find_solution(step+1)
        
    def find_solution(self, step):
        if step == self.fixed_x:
            #if row with fixed queen is last row it means we have a solution 
            #otherwise skip this row
            if self.fixed_x == (self.n-1):
                self.solutions.append(copy.deepcopy(self.board))
                return
            else:
                self.find_solution(step+1)
        
        que = self.create_queue(step=step)
        #If there is any legal move in last row it means we have a solution
        if step == (self.n-1):
            if que:
                #for j in range(8):
                    #print(self.board[j])
                #print('======')
                self.move_queen(self.queens[step], que.pop(0))
                self.solutions.append(copy.deepcopy(self.board))
            return
        
        while que:
            self.move_queen(self.queens[step], que.pop(0))
            self.define_blocked_paths(step)
            self.find_solution(step+1)
    
    def move_queen(self, queen, goal):
        x, start_y = queen.x, queen.y
        queen.y = goal
        self.board[x][start_y], self.board[x][goal] = '0', self.board[x][start_y]
    
    def create_queue(self, step, root=False):
        q = []
        for i in range(self.n):
            #Ignore any tiles blocked by fixed queen
            if self.max <= self.blocked[step][i]:
                continue
            #Pick only legal moves unless root then take all
            if root:
                q.append(i)
            elif self.blocked[step][i] <= 0:
                q.append(i)
        return q

    #Create board with fixed queen and fill it randomly with the rest
    def create_board(self):
        self.board = [['0']*self.n for i in range(self.n)]
        self.queens = []
        self.board[self.fixed_x][self.fixed_y] = Queen(self.fixed_x, self.fixed_y, True)
        for i in range(self.n):
            if i == start_x:
                self.queens.append(self.board[self.fixed_x][self.fixed_y])
                continue
            rand = random.randint(0,self.n-1)
            self.board[i][rand] = Queen(i, rand)
            self.queens.append(self.board[i][rand])
        self.define_blocked_paths()
    
#Class used to store the Queen object
class Queen:
    
    def __init__(self, x, y, fixed=False):
        self.x = x
        self.y = y
        self.fixed = fixed
        self.prev = 0
        
    def __str__(self):
        if self.fixed:
            return 'F'
        return 'Q'
    
    def __repr__(self):
        if self.fixed:
            return 'F'
        return 'Q'


#Student Number 1911309
#Given that chessboard counts from 1-8 and 2d array 0-7 I ommit the '+1' from coordinates
start_x = (9 % 8) 
start_y = (0 % 8)
board_size = 8
q = QueenProblem(board_size, start_x, start_y)
q.solve()
results = f'Starting x: {start_x}, y: {start_y} | Solutions: {len(q.solutions)} | F stands for fixed Queen\n'
results += '======================================\n'
for i in range(len(q.solutions)):
    for j in range(8):
        results += str(q.solutions[i][j]) + '\n'
    results += '======================================\n'
print(results)
with open('output.txt', 'w') as f:
    f.write(results)

