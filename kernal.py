import numpy as py
import random

class game2048:
    def __init__(self, dimension=4, status=None):
        """
        attribuites: dimension, matrix, score
        """
        # if status is not None, then the game is initialized with the status
        if status:
            self.matrix = status[0]
            self.score = status[1]
            self.dimension = len(self.matrix)
            return
        # if status is None, then the game is initialized with the dimension
        self.dimension = dimension
        self.matrix = py.zeros((dimension, dimension))
        self.random_generate()
        self.score = 0

    def status(self):
        """return the status of 2048game"""
        return [self.matrix, self.score]

    def empty_cells(self):
        """return the empty cells in the matrix"""
        empty_cells = []
        for line in range(0, self.dimension):
            for column in range(0, self.dimension):
                if self.matrix[line][column] == 0:
                    empty_cells.append([line, column])
        return empty_cells

    def random_generate(self):
        """generate 2 or 4 in a random empty cell"""
        line, column = random.choice(self.empty_cells())
        self.matrix[line][column] = random.choice([2, 4])

    def merge(self, points):
        """merge the matrix according to the direction"""
        array = [self.matrix[point] for point in points if self.matrix[point] != 0]
        ap = 0
        while ap < len(array) - 1:
            if array[ap] == array[ap + 1]:
                array[ap] *= 2
                self.score += array[ap]
                array.pop(ap + 1)
            ap += 1
        for i in range(len(points)):
            if i < len(array):
                self.matrix[points[i]] = array[i]
            else:
                self.matrix[points[i]] = 0

    def get_points(self, direction):
        """return the points in the matrix according to the direction"""
        if direction == 'up':
            return [[(line, column) for line in range(0, self.dimension)] for column in range(0, self.dimension)]
        if direction == 'down':
            return [[(line, column) for line in range(self.dimension - 1, -1, -1)] for column in range(0, self.dimension)]
        if direction == 'left':
            return [[(line, column) for column in range(0, self.dimension)] for line in range(0, self.dimension)]
        if direction == 'right':
            return [[(line, column) for column in range(self.dimension - 1, -1, -1)] for line in range(0, self.dimension)]
    
    def update_without_generate(self,direction):
        """update the matrix according to the direction without generating a new number"""
        last_matrix = self.matrix.copy()
        points_list = self.get_points(direction)
        for points in points_list:
            self.merge(points)
        if (last_matrix == self.matrix).all():
            return False
        return True
    
    def update(self, direction):
        """update the matrix and the point according to player's action"""
        if self.update_without_generate(direction):
            self.random_generate()
    
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
        print("matrix:")        
        print()
        for line in range(0, self.dimension):
            for colume in range(0, self.dimension):
                print(int(self.matrix[line][colume]),end = '\t')
            print()
        print()

if __name__ == '__main__':
    game = game2048()
    game.print()
    while not game.gameover():
        direction = input("Enter the direction: ")
        game.update(direction)
        game.print()
    print("Game Over!")

