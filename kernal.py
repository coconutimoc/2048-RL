"""
The game2048 class is the neural data structure of this project, and serves as
the kernak of gui. It records and updated the game state(time, score, matrix).

It also provides APIs to operate the status of game:

    - clone(game: game2048)->None: clone the state of another game

    - reset()->None: reset the game (time,score,matrix)

    - move(direction:str)->bool: move the matrix and uodate score(without
             generating a new number) and return if the matrix has changed

    - update(direction:str)->bool: update time, score and matrix(random generate)
            and return if the matrix has changed

    - gameover()->bool: return if the game is over
"""


import numpy as np
import random

class game2048:
    def __init__(self,dimension:int) -> None:
        """initialize the game
        Args:
            dimension: the dimension of the game matrix
        parameters:
            time: the number of steps
            score: the score player gained
            dimension: the dimension of the game matrix
            matrix: the game matrix
            cm: the copy of the game matrix(used to check if the matrix has changed)
        """
        #constant
        self.dimension = dimension
        #state of game
        self.time = 0
        self.score = 0
        self.matrix = np.zeros((dimension,dimension))
        self.random_generate()
        self.last_matrix = self.matrix.copy()
        #tools
        self.cm = np.zeros((dimension,dimension))

    def clone(self,game)->None:
        """clone the state of another game"""
        self.time = game.time
        self.score = game.score
        self.dimension = game.dimension
        self.matrix = game.matrix.copy()

    def reset(self) -> None:
        """reset the game (time,score,matrix)"""
        self.score = 0
        self.time = 0
        for line in range(self.dimension):
            for col in range(self.dimension):
                self.matrix[line][col] = 0
        self.random_generate()

    def random_generate(self) -> None:
        """randomly generate a 2 or 4 in an empty cell"""
        while True:
            line = random.randint(0,self.dimension-1)
            col = random.randint(0,self.dimension-1)
            if self.matrix[line][col] == 0:
                self.matrix[line][col] = random.choice([2,4])
                break
    
    def move_up(self)->None:
        """move the matrix up and update the score if needed"""
        for col in range(self.dimension):
            for line in range(1,self.dimension):
                while line > 0 and self.matrix[line][col] != 0 and self.matrix[line-1][col] == 0:
                    self.matrix[line-1][col] = self.matrix[line][col]
                    self.matrix[line][col] = 0
                    line -= 1
            for line in range(1,self.dimension):
                if self.matrix[line][col] != 0 and self.matrix[line][col] == self.matrix[line-1][col]:
                    self.matrix[line-1][col] *= 2
                    self.score += self.matrix[line-1][col]
                    self.matrix[line][col] = 0
                    line -= 1
            for line in range(1,self.dimension):
                while line > 0 and self.matrix[line][col] != 0 and self.matrix[line-1][col] == 0:
                    self.matrix[line-1][col] = self.matrix[line][col]
                    self.matrix[line][col] = 0
                    line -= 1

    def move_down(self)->None:
        """move the matrix down and update the score if needed"""
        for col in range(self.dimension):
            for line in range(self.dimension-2,-1,-1):
                while line < self.dimension-1 and self.matrix[line][col] != 0 and self.matrix[line+1][col] == 0:
                    self.matrix[line+1][col] = self.matrix[line][col]
                    self.matrix[line][col] = 0
                    line += 1
            for line in range(self.dimension-2,-1,-1):
                if self.matrix[line][col] != 0 and self.matrix[line][col] == self.matrix[line+1][col]:
                    self.matrix[line+1][col] *= 2
                    self.score += self.matrix[line+1][col]
                    self.matrix[line][col] = 0
                    line += 1
            for line in range(self.dimension-2,-1,-1):
                while line < self.dimension-1 and self.matrix[line][col] != 0 and self.matrix[line+1][col] == 0:
                    self.matrix[line+1][col] = self.matrix[line][col]
                    self.matrix[line][col] = 0
                    line += 1

    def move_left(self)->None:
        """move the matrix left and update the score if needed"""
        for line in range(self.dimension):
            for col in range(1,self.dimension):
                while col > 0 and self.matrix[line][col] != 0 and self.matrix[line][col-1] == 0:
                    self.matrix[line][col-1] = self.matrix[line][col]
                    self.matrix[line][col] = 0
                    col -= 1
            for col in range(1,self.dimension):
                if self.matrix[line][col] != 0 and self.matrix[line][col] == self.matrix[line][col-1]:
                    self.matrix[line][col-1] *= 2
                    self.score += self.matrix[line][col-1]
                    self.matrix[line][col] = 0
                    col -= 1
            for col in range(1,self.dimension):
                while col > 0 and self.matrix[line][col] != 0 and self.matrix[line][col-1] == 0:
                    self.matrix[line][col-1] = self.matrix[line][col]
                    self.matrix[line][col] = 0
                    col -= 1
    
    def move_right(self)->None:
        """move the matrix right and update the score if needed"""
        for line in range(self.dimension):
            for col in range(self.dimension-2,-1,-1):
                while col < self.dimension-1 and self.matrix[line][col] != 0 and self.matrix[line][col+1] == 0:
                    self.matrix[line][col+1] = self.matrix[line][col]
                    self.matrix[line][col] = 0
                    col += 1
            for col in range(self.dimension-2,-1,-1):
                if self.matrix[line][col] != 0 and self.matrix[line][col] == self.matrix[line][col+1]:
                    self.matrix[line][col+1] *= 2
                    self.score += self.matrix[line][col+1]
                    self.matrix[line][col] = 0
                    col += 1
            for col in range(self.dimension-2,-1,-1):
                while col < self.dimension-1 and self.matrix[line][col] != 0 and self.matrix[line][col+1] == 0:
                    self.matrix[line][col+1] = self.matrix[line][col]
                    self.matrix[line][col] = 0
                    col += 1

    def move(self,direction)->bool:
        """move the matrix in the given direction and return if the matrix has changed
        used to update the matrix without generating a new number
        """
        for col in range(self.dimension):
            for line in range(self.dimension):
                self.cm[line][col] = self.matrix[line][col]
        if direction == 'up':
            self.move_up()
        elif direction == 'down':
            self.move_down()
        elif direction == 'left':
            self.move_left()
        elif direction == 'right':
            self.move_right()
        changed = False
        for col in range(self.dimension):
            for line in range(self.dimension):
                if self.cm[line][col] != self.matrix[line][col]:
                    changed = True
                    break
        return changed
    
    def update(self,direction)->bool:
        """update the time, random generate and return if the matrix has changed"""
        changed = self.move(direction)
        if changed:
            self.time += 1
            self.random_generate()
        return changed

    def gameover(self)->bool:
        """return if the game is over"""
        for line in range(self.dimension):
            for col in range(self.dimension):
                if self.matrix[line][col] == 0:
                    return False
        for line in range(self.dimension):
            for col in range(self.dimension-1):
                if self.matrix[line][col] == self.matrix[line][col+1]:
                    return False
        for col in range(self.dimension):
            for line in range(self.dimension-1):
                if self.matrix[line][col] == self.matrix[line+1][col]:
                    return False
        return True

    def print(self):
        """print the matrix and score(point)"""
        print('Time:', self.time)
        print('Score:', self.score)
        print("matrix:")        
        print()
        for line in range(0, self.dimension):
            for colume in range(0, self.dimension):
                print(int(self.matrix[line][colume]),end = '\t')
            print()
        print()

if __name__ == '__main__':
    game = game2048(4)
    game.print()
    game.move('up')
    game.print()
    game.move('down')
    game.print()
    game.move('left')
    game.print()
    game.move('right')
    game.print()
    game.update('up')
    game.print()
    game.update('down')
    game.print()
    game.update('left')
    game.print()
    game.update('right')
    game.print()
    print(game.gameover())
    game.reset()
    game.print()