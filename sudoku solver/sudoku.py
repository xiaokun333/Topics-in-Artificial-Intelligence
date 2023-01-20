#!/usr/bin/env python
#coding:utf-8

"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""

import sys
import copy
import numpy as np
import time

ROW = "ABCDEFGHI"
COL = "123456789"

class CSP:
    def __init__(self, current_board):
        """
        available is all the numbers available for a cell
        available['A1'] = [1, 3, 9]
        """
        
        self.avail_domain = dict()
        for r in ROW:
            for c in COL: 
                # if not filled, set available to all possible numbers
                #print(current_board[r+c])
                if current_board[r+c] == 0:
                    self.avail_domain[r+c] = "123456789"
                #no available
                else: 
                    #same type as avail_domain
                    self.avail_domain[r+c] = str(current_board[r+c])
       # print(self.avail_domain)
        #print(1)
    
def get_all_grid():
    """
    Input: 
    Output: dict key in order
    A1, A2, A3...
    """
    
    ordered_key = []
    for i in ROW:
      for j in COL:
        ordered_key.append(i + j)
    return ordered_key
    
def find_neighbor(var):
    """
    Input: a key in current board, type = string
    Output: the row/col/grid containing that key
    
    - used to check if row/col/grid constraints are violated
    """
    
    # Use a set to remove duplicate
    neighbors = set()
    # keys is a list of strings
    keys = get_all_grid()
    idx = keys.index(var)
    
    idx_row = idx // 9
    idx_col = idx % 9
    
    # get row:
    for j in COL:
        arr_row = []
        arr_row.append(ROW[idx_row] + j)
        if var != arr_row[0]:
            neighbors.update(arr_row)
        else:
            continue
    
    # get col:
    for i in ROW: 
        arr_col = []
        arr_col.append(i + COL[idx_col])
        if var != arr_col[0]:
            neighbors.update(arr_col)
        else:
            continue
        
    # get grid
    #grid_set = set()
    for i in range(idx_row // 3 * 3, idx_row // 3 * 3 + 3):
        for j in range(idx_col //3  * 3, idx_col // 3 * 3 + 3):
            arr = [] 
            arr.append(ROW[i] + COL[j])
            if var != arr[0]:
                neighbors.update(arr)
                
    return neighbors
    
            
def is_complete(assignment):
    #used in backtrack
    """
    Input: assignment
    Output: True if the assignment is complete
    """
    if len(assignment) == 81:
        return True
    else: return False
        
def valid_board(var, value, assignment):
    # this is checking constriants, consistency
    """
    Input: the variable returned by mrv, value is the value we try to assign to the variable, assignment is our current attempt
    Output: True if none of the neighbor is same as var
    else false
    """
    #csp = CSP(board)
    neighbors = find_neighbor(var)
    flag = False
    
    
    for n in neighbors:
        # neighbor hasnt been assigned
        if n not in assignment:
            continue
        # the value we try already exists in neighbors
        #print(assignment[n])
        if value == assignment[n]:
            return flag
    flag = True
    return flag
     

def mrv(csp, assignment):
    """
    Input: csp.avail_domain, current assignment
    Output: var with smallest available domain, string
    
    It if multiple smallest length, go to the last one
    """
    available = csp.avail_domain
    min_len = 10
    var = None
    for r in ROW:
        for c in COL:
            current_key = r + c
            var_len = len(available[current_key])
            # don't select the assigned key twice
            if current_key in assignment:
                continue
            # select var with least availble domain
            if var_len > min_len:
                continue
            # update minimum len for comparison in next iteration
            min_len = var_len
            # update var for comparison in next iteration
            var = current_key
    #print("mrv var: " + str(var))
    return var

def backtrack(assignment, csp):
    """
    Input: current assignment and their available domain
    Output: result(solution) or None(failure)
    """
    if is_complete(assignment) == True:
        return assignment
    
    var = mrv(csp, assignment)
    result = None
    # pick next var, val by mrv
    for val in csp.avail_domain[var]:
        # if value we picked is consistent with assignment/satisfies constraints
        if valid_board(var, val, assignment):
            # add value to assignment
            assignment[var] = val
            # update current available domain
            new_csp = copy.deepcopy(csp)
            new_csp.avail_domain[var] = val

            # forward checking: delete assignment from neighbor's domain (update) 
            is_forward_checking_consistent = True
            assigned_neighbors = find_neighbor(var)
            for neighbor in assigned_neighbors:
                # skip if neighbor is assigned
                if neighbor in assignment:
                    continue
                new_csp.avail_domain[neighbor] = new_csp.avail_domain[neighbor].replace(val, '')
                
              
                # check if any var has no legal values, if so terminates
                if new_csp.avail_domain[neighbor] == "": 
                    is_forward_checking_consistent = False
            
            if is_forward_checking_consistent == False:
                continue
            
            result = backtrack(assignment, new_csp)
            
            if result != None:
                return result
    del assignment[var]            
    return None


def backtracking(board):
    """Takes a board and returns solved board."""
    # TODO: implement this
    csp = CSP(board)
    # assignment is initialized here
    assignment = dict()
    return backtrack(assignment, csp)

def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)


def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)




if __name__ == '__main__':
    if len(sys.argv) > 1:
        
        # Running sudoku solver with one board $python3 sudoku.py <input_string>.
        print(sys.argv[1])
        # Parse boards to dict representation, scanning board L to R, Up to Down
        board = { ROW[r] + COL[c]: int(sys.argv[1][9*r+c]) for r in range(9) for c in range(9)}       
        csp = CSP(board)
        solved_board = backtracking(board)
        print_board(solved_board)
        # Write board to file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")
        outfile.write(board_to_string(solved_board))
        outfile.write('\n')
        outfile.close()

    else:
        # Running sudoku solver for boards in sudokus_start.txt $python3 sudoku.py
        str_time = time.time()
        #  Read boards from source.
        src_filename = 'sudokus_start.txt'
        try:
            srcfile = open(src_filename, "r")
            sudoku_list = srcfile.read()
        except:
            print("Error reading the sudoku file %s" % src_filename)
            exit()

        # Setup output file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")
        time_statistics = np.zeros((1, 400))
        # Solve each board using backtracking
        index = 0
        for line in sudoku_list.split("\n"):
            line_sudoku_str_time = time.time()
            if len(line) < 9:
                continue
            
            # Parse boards to dict representation, scanning board L to R, Up to Down
            board = { ROW[r] + COL[c]: int(line[9*r+c])
                      for r in range(9) for c in range(9)}
                
            # Print starting board. TODO: Comment this out when timing runs.
            print_board(board)

            # Solve with backtracking
            solved_board = backtracking(board)

            # Print solved board. TODO: Comment this out when timing runs.
            print_board(solved_board)

            # Write board to file
            outfile.write(board_to_string(solved_board))
            outfile.write('\n')
            
            line_sudoku_end_time = time.time()
            time_statistics[0][index] = line_sudoku_end_time - line_sudoku_str_time
            index += 1    
        outfile.close()
        end_time = time.time()
        
        number_of_board_solved = len(np.where(time_statistics > 0)[0])
        README_out_filename = 'README.txt'
        README_outfile = open(README_out_filename, "w")
        README_outfile.write("Number of Board Solved: " + str(number_of_board_solved))
        README_outfile.write('\n')
        README_outfile.write("Total Time: " + str(end_time - str_time))
        README_outfile.write('\n')
        README_outfile.write("Mean Time: " + str(np.mean(time_statistics)))
        README_outfile.write('\n')
        README_outfile.write("Max Time: :" + str(np.max(time_statistics)))
        README_outfile.write('\n')
        README_outfile.write("Min Time: :" + str( np.min(time_statistics)))
        README_outfile.write('\n')
        README_outfile.write("STD Time: " + str(np.std(time_statistics)))
        README_outfile.write('\n')
        README_outfile.close()
        print("Finishing all boards in file.")