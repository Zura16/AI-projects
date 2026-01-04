'''
CECS 451: Artifical Intelligence
Assignment 2: Genetic Algorithm to solve the n-queens problem
Name: Aalind Kale
Student ID: 030892041
Due Date: 09/24/2025
'''

# imports
import time
import random
from board import Board

# Gonna be using whst we studied in class to implement the logic for this algorithm. 
# Also, we'll use the random crossover points and random rows, cols to murate

class geneticAlgo:
    def __init__(self, n_queens = 5, popu_s = 8, muta_r = 0.1):
        self.n_queens = n_queens
        self.popu_s = popu_s
        self.muta_r = muta_r
        self.popu = []

    def fit(self, board):
        return board.get_fitness()
    
    def population(self):
        self. popu = []
        for i in range (self.popu_s):
            board = Board(self.n_queens)
            self.popu.append(board)

    def selection(self):
        par = []
        for j in range(2):
            tourn = random.sample(self.popu, 3)
            top = min(tourn, key=self.fit)
            par.append(top)

        return par
    
    def cross(self, par1, par2) :
        c1 = par1.encode()
        c2 = par2.encode()
        cross_point = random.randint(1, self.n_queens - 1)

        chc1 = c1[:cross_point] + c2[cross_point:]
        chc2 = c2[:cross_point] + c1[cross_point:]

        ch1 = Board(self.n_queens)
        ch1. decode(chc1)
        ch2 = Board(self.n_queens)
        ch2.decode(chc2)

        return  ch1,  ch2
    
    # Here's where the change in position of the queen will maorly occur.
    def mutation(self, board):
        if random.random() < self.muta_r:
            r = random.randint(0, self.n_queens- 1)
            curr_c = None
            for c in range(self.n_queens):
                if board.get_map()[r][c] == 1:
                    curr_c = c
                    break

            max_c = [c for c in range(self.n_queens) if c != curr_c]
            newc = random.choice(max_c)

            board.flip(r, curr_c)
            board.flip(r, newc)

        return board

    def top_indi(self):
        return min (self.popu, key=self.fit)
    # we'll make the rest of the population and then evolve and oin the end, reduce it. 
    def evolve(self, total_generate = 1000 ):
        for grn in range(total_generate):
            a = self.top_indi()
            if self.fit(a) == 0:
                return a, grn
            
            newPop = []
            newPop.append(a)

            while len(newPop) < self.popu_s :
                par1, par2 = self.selection()
                ch1, ch2 = self.cross(par1, par2)

                ch1 = self .mutation(ch1)
                ch2 = self.mutation(ch2)
                newPop.extend([ch1, ch2])

            self.popu = newPop[:self.popu_s]
        return self.top_indi(), total_generate
    
#Just the main function to get things going.
def main():
    begin = time.time()
    gene_algo = geneticAlgo(n_queens=5, popu_s=8, muta_r=0.15)            
    gene_algo.population()

    sol, generation = gene_algo.evolve(total_generate=1000)
    ending = time.time()
    running  = int((ending- begin)* 1000)

    print(f"Running time: {running}ms")

    if sol.get_fitness() == 0:
        print("Soution found:")
    else:
        print("Best Solution: ")

    sol.print_map()
    print(f"{sol.encode()}")

if __name__ == "__main__":
    main()