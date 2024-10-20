import numpy as py
import random

class matrix:
    def __init__(self, dimension, matrix=None, score=0):
        """
        attribuites: dimension, matrix, score
        """
        # case where the object is created with a copied matrix
        if matrix is not None:
            assert len(matrix) == dimension, 'the length of the matrix should be equal to the dimension'
            self.matrix = matrix
        # case where the matrix is initialized at the start of the game
        else:
            self.matrix = py.zeros((dimension, dimension))
            self.matrix[random.randint(0, dimension-1)][random.randint(0, dimension-1)] = 2* random.randint(1, 2)
        self.dimension = dimension
        self.score = score

    @property
    def maxnum(self):
        """return the maximum number in the matrix"""
        return max([max(int(_) for _ in self.matrix[i]) for i in range(self.dimension)])
    

    def drop(self,direction):
        changed = False
        if direction == 'up':
            for column in range(0, self.dimension):
                for line in range(1, self.dimension):
                    while(line > 0 and self.matrix[line][column]!=0 and self.matrix[line-1][column]==0):
                        self.matrix[line-1][column] = self.matrix[line][column]
                        self.matrix[line][column] = 0
                        line -= 1
                        changed = True
        elif direction == 'down':
            for column in range(0, self.dimension):
                for line in range(self.dimension-2, -1, -1):
                    while(line < self.dimension-1 and self.matrix[line][column]!=0 and self.matrix[line+1][column]==0):
                        self.matrix[line+1][column] = self.matrix[line][column]
                        self.matrix[line][column] = 0
                        line += 1
                        changed = True
        elif direction == 'left':
            for line in range(0, self.dimension):
                for column in range(1, self.dimension):
                    while(column > 0 and self.matrix[line][column]!=0 and self.matrix[line][column-1]==0):
                        self.matrix[line][column-1] = self.matrix[line][column]
                        self.matrix[line][column] = 0
                        column -= 1
                        changed = True
        elif direction == 'right':
            for line in range(0, self.dimension):
                for column in range(self.dimension-2, -1, -1):
                    while(column < self.dimension-1 and self.matrix[line][column]!=0 and self.matrix[line][column+1]==0):
                        self.matrix[line][column+1] = self.matrix[line][column]
                        self.matrix[line][column] = 0
                        column += 1
                        changed = True                       
        return changed
    
    def merge(self,direction):
        changed = False
        if direction == 'up':
            for column in range(0, self.dimension):
                for line in range(0, self.dimension-1):
                    if self.matrix[line][column] !=0 and self.matrix[line][column] == self.matrix[line+1][column]:
                        self.matrix[line][column] = 2*self.matrix[line][column]
                        self.matrix[line+1][column] = 0
                        self.score += self.matrix[line][column]
                        changed = True
        elif direction == 'down':
            for column in range(0, self.dimension):
                for line in range(self.dimension-1, 0, -1):
                    if self.matrix[line][column] !=0 and self.matrix[line][column] == self.matrix[line-1][column]:
                        self.matrix[line][column] = 2*self.matrix[line][column]
                        self.matrix[line-1][column] = 0
                        self.score += self.matrix[line][column]
                        changed = True
        elif direction == 'left':
            for line in range(0, self.dimension):
                for column in range(0, self.dimension-1):
                    if self.matrix[line][column] !=0 and self.matrix[line][column] == self.matrix[line][column+1]:
                        self.matrix[line][column] = 2*self.matrix[line][column]
                        self.matrix[line][column+1] = 0
                        self.score += self.matrix[line][column]
                        changed = True
        elif direction == 'right':
            for line in range(0, self.dimension):
                for column in range(self.dimension-1, 0, -1):
                    if self.matrix[line][column] !=0 and self.matrix[line][column] == self.matrix[line][column-1]:
                        self.matrix[line][column] = 2*self.matrix[line][column]
                        self.matrix[line][column-1] = 0
                        self.score += self.matrix[line][column]
                        changed = True
        return changed
        

    def update_without_generate(self,direction):
        changed = False
        changed = self.drop(direction) or changed
        changed = self.merge(direction) or changed
        changed = self.drop(direction) or changed            
        return changed
    

    def update(self, direction):
        """update the matrix and the point according to player's action"""
        if self.update_without_generate(direction):
            line, column = random.choice(self.empty_cells())
            self.matrix[line][column] = 2* random.randint(1, 2)
    
    def gameover(self):
        """return True if the game is over, False otherwise"""
        for line in range(0, self.dimension):
            for column in range(0, self.dimension):
                if self.matrix[line][column] == 0:
                    return False
                if line < self.dimension - 1 and self.matrix[line][column] == self.matrix[line+1][column]:
                    return False
                if column < self.dimension - 1 and self.matrix[line][column] == self.matrix[line][column+1]:
                    return False
        return True
    
    def print(self):
        """print the matrix and score(point)"""
        print('Score:', self.score)
        print()
        for line in range(0, self.dimension):
            for colume in range(0, self.dimension):
                print(int(self.matrix[line][colume]),end = '\t')
            print()
        print()

    def empty_cells(self):
        """return the empty cells in the matrix"""
        empty_cells = []
        for line in range(0, self.dimension):
            for column in range(0, self.dimension):
                if self.matrix[line][column] == 0:
                    empty_cells.append([line, column])
        return empty_cells


if __name__ == '__main__':
    print('test matrix')
    mat = matrix(4)
    mat.print()
    mat.update('up')
    mat.print()
    mat.update('down')
    mat.print()
    mat.update('left')
    mat.print()
    mat.update('right')
    mat.print()
    mat.update_without_generate('up')
    mat.print()
    mat.update_without_generate('down')
    mat.print()
    mat.update_without_generate('left')
    mat.print()
    mat.update_without_generate('right')
    mat.print()
    print(mat.gameover())
    print(mat.empty_cells())
    print(mat.maxnum)
    print(mat.score)
    print(mat.matrix)
    print(mat.dimension)
