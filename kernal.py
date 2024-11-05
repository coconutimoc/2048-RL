import numpy as np
import random

class game2048:
    def __init__(self,dimension):
        self.dimension = dimension    
        self.time = 0  
        self.score = 0
        self.last_score = 0                            
        self.matrix = np.zeros((dimension,dimension))
        self.random_generate()
        self.last_matrix = self.matrix.copy()
        self.cm = np.zeros((dimension,dimension))

    def reset(self):
        self.score = 0
        self.last_score = 0
        for line in range(self.dimension):
            for col in range(self.dimension):
                self.matrix[line][col] = 0
        self.random_generate()
        for line in range(self.dimension):
            for col in range(self.dimension):
                self.last_matrix[line][col] = self.matrix[line][col]
        self.time = 0

    def random_generate(self):
        while True:
            x = random.randint(0,self.dimension-1)
            y = random.randint(0,self.dimension-1)
            if self.matrix[x][y] == 0:
                self.matrix[x][y] = random.choice([2,4])
                break
    
    def move_up(self):
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

    def move_down(self):
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

    def move_left(self):
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
    
    def move_right(self):
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

    def move(self,direction):
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
    
    def update(self,direction):
        last_score = self.score
        changed = self.move(direction)
        if changed:
            self.last_score = last_score
            self.time += 1
            self.random_generate()
        return changed

    def gameover(self):
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
    while not game.gameover():
        direction = input("Enter the direction: ")
        _ = game.update(direction)
        game.print()
    print("Game Over!")

    
