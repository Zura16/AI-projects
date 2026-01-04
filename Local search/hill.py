'''
CECS 451: Artifical Intelligence
Assignment 2: Hill Climbing Algorithm to solve the n-queens problem
Name: Aalind Kale
Student ID: 030892041
Due Date: 09/24/2025
'''


# imports

import time 
import random
from board import Board

# making the hill climbing algorithm using random restart as recommended in the module.
# Also, I will create another random board 

def hillClimbAlgo(n_queens, total_restart = 500):
    begin = time .time()
    restart = 0

    while restart <total_restart:
        board = Board(n_queens)
        curr_fitness = board.get_fitness()

        if curr_fitness == 0:
            ending = time.time()
            running = int((ending - begin) * 1000)
            
            return board, running
        
        # we'll be moving the queen in it's row into different columns to look for the most suitable one
        # we'll settle for a better one until we find the one which will in turn be the best.
        new_curr = True
        while new_curr:
            new_curr = False
            top = curr_fitness
            top_move  = None

            for i in range(n_queens):
                curr_col = None
                for j in range(n_queens):
                    if board.get_map()[i][j] == 1:
                        curr_col = j
                        break

            for k in range(n_queens):
                if k != curr_col:
                    board.flip (i, curr_col)
                    board.flip(i, k)

                    fir = board.get_fitness ()
                    if fir < top:
                        top = fir
                        top_move = ( i, curr_col, k)

                    board.flip(i, k)
                    board.flip (i, curr_col)

        # this is whwre the top meaning the most optimal move will be made.
        if top_move:
            i, m, k = top_move
            board. flip(i, m)
            board.flip(i, k)
            curr_fitness = top
            new_curr = True

            if curr_fitness == 0:
                ending = time.time()
                running = int((ending - begin) * 1000)
                
                return board, running
            
        restart += 1
    ending = time.time()
    running = int((ending - begin) * 1000)
    
    return None, running

#Just the main function to get things going.

def main():
    sol, running = hillClimbAlgo(5)

    if sol :
        print(f"Running time: {running}ms")
        sol.print_map()
        print(f"{sol.encode()}")
    else:
        print(f"Solution can't be found. We ran out of restarts after {running}ms")

if __name__ == "__main__":
    main()
