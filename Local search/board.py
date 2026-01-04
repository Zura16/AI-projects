import random
import numpy as np


class Board:
    def __init__(self, n):
        self.n_queen = n
        self.reset()
        for i in range(self.n_queen):
            j = random.randint(0, self.n_queen - 1)
            self.map[i][j] = 1

    def reset(self):
        self.map = [[0 for j in range(self.n_queen)] for i in range(self.n_queen)]

    def get_fitness(self):
        fit = 0
        for i in range(self.n_queen):
            for j in range(self.n_queen):
                if self.map[i][j] == 1:
                    for k in range(1, self.n_queen - i):
                        if self.map[i + k][j] == 1:
                            fit += 1
                        if j - k >= 0 and self.map[i + k][j - k] == 1:
                            fit += 1
                        if j + k < self.n_queen and self.map[i + k][j + k] == 1:
                            fit += 1
        return fit

    def get_map(self):
        return self.map

    def print_map(self):
        for i in range (self.n_queen):
              for j in range (self.n_queen):
                if self.map[i][j] == 1: 
                  print("x",end=" ")
                else:
                  print("-",end=" ")
              print()

    def flip(self, i, j):
        if self.map[i][j] == 0:
            self.map[i][j] = 1
        else:
            self.map[i][j] = 0

    def encode(self):
        code = ''.join([str(self.map[i].index(1)) for i in range(self.n_queen)])
        return code

    def decode(self, code):
        self.reset()
        for i in range (self.n_queen):
            self.map[i][int(code[i])] = 1


if __name__ == '__main__':
    test = Board(5)
    print(test.get_fitness())
    print(test.get_map())
    test.print_map()
    print(test.encode())
    test.decode('20314')
    print(test.get_fitness())
    test.print_map()
    print(test.encode())