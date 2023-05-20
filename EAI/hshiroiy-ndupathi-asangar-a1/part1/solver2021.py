#!/usr/local/bin/python3
# solver2021.py : 2021 Sliding tile puzzle solver
#
# Code by: Amol Dattatray Sangar (asangar)
#
# Based on skeleton code by D. Crandall & B551 Staff, September 2021
#

from os import close
import sys
import copy
from queue import Empty, PriorityQueue
from typing import Match

ROWS=5
COLS=5

def printable_board(board):
    return [ ('%3d ')*COLS  % board[j:(j+COLS)] for j in range(0, ROWS*COLS, COLS) ]

def move_outer_ring(state, direction):
    board = copy.deepcopy(state)
    board_size = len(board)

    temp1 = board[1][0]
    temp2 = board[1][board_size-1]

    if(direction == "clockwise"):
        board_1 = move_right(copy.deepcopy(board), 0)
        board_2 = move_downward(copy.deepcopy(board), board_size-1)
        board_3 = move_left(copy.deepcopy(board), board_size-1)
        board_4 = move_upward(copy.deepcopy(board), 0)
    elif(direction == "anticlockwise"):
        board_1 = move_left(copy.deepcopy(board), 0)
        board_2 = move_downward(copy.deepcopy(board), 0)
        board_3 = move_right(copy.deepcopy(board), board_size-1)
        board_4 = move_upward(copy.deepcopy(board), board_size-1)
    else:
        return []

    for i in range(len(board)):
        for j in range(len(board[0])):
            # Copy data
            if(i == 0 and direction == "clockwise"):
                board[i][j] = board_1[i][j]
            elif(j==board_size-1 and direction == "clockwise"):
                board[i][j] = board_2[i][j]
            elif(i==board_size-1 and direction == "clockwise"):
                board[i][j] = board_3[i][j]
            elif(j==0 and direction == "clockwise"):
                board[i][j] = board_4[i][j]
            elif(i == 0 and direction == "anticlockwise"):
                board[i][j] = board_1[i][j]
            elif(j==0 and direction == "anticlockwise"):
                board[i][j] = board_2[i][j]
            elif(i==board_size-1 and direction == "anticlockwise"):
                board[i][j] = board_3[i][j]
            elif(j==board_size-1 and direction == "anticlockwise"):
                board[i][j] = board_4[i][j]

    if(direction == "clockwise"):
        board[0][0] = temp1
    elif(direction == "anticlockwise"):
        board[0][board_size-1] = temp2
    return board

def move_inner_ring(state, direction):
    board = copy.deepcopy(state)
    board_size = len(board)

    inner_ring = [sub_matrix[1:board_size-1] for sub_matrix in board[1:board_size-1] ]
    inner_ring = move_outer_ring(inner_ring, direction)

    if(not inner_ring):
        return []

    for i in range(1,len(board)-1):
        for j in range(1,len(board[0])-1):
            board[i][j] = inner_ring[i-1][j-1]    
    
    return board

def move_upward(state, col):
    board = copy.deepcopy(state)
    temp = board[0][col]
    board_size = len(board)
    for i in range(board_size-1):
        board[i][col] = board[i+1][col]

    board[board_size-1][col] = temp
    return board

def move_downward(state, col):
    board = copy.deepcopy(state)
    board_size = len(board)
    temp = board[board_size-1][col]
    for i in range(board_size-1, 0, -1):
        board[i][col] = board[i-1][col]

    board[0][col] = temp
    return board

def move_left(state, row):
    board = copy.deepcopy(state)
    board[row].append(board[row].pop(0))
    return board

def move_right(state, row):
    board = copy.deepcopy(state)
    board[row].insert(0, board[row].pop())
    return board

# return a list of possible successor states
def successors(state):
    board_size = len(state)

    succ_states = {}

    for i in range(0,board_size):
        board = move_upward(state,i)
        board_state_hash = hash(' '.join(map(str, conv_2D_to_1D(board))))
        succ_states[board_state_hash] = {
            "move": "U"+str(i+1),
            "state": board,
            "hash": board_state_hash
        }
        board = move_downward(state,i)
        board_state_hash = hash(' '.join(map(str, conv_2D_to_1D(board))))
        succ_states[board_state_hash] = {
            "move": "D"+str(i+1),
            "state": board,
            "hash": board_state_hash
        }
        board = move_left(state,i)
        board_state_hash = hash(' '.join(map(str, conv_2D_to_1D(board))))
        succ_states[board_state_hash] = {
            "move": "L"+str(i+1),
            "state": board,
            "hash": board_state_hash
        }
        board = move_right(state,i)
        board_state_hash = hash(' '.join(map(str, conv_2D_to_1D(board))))
        succ_states[board_state_hash] = {
            "move": "R"+str(i+1),
            "state": board,
            "hash": board_state_hash
        }
    
    board = move_outer_ring(state,"clockwise")
    board_state_hash = hash(' '.join(map(str, conv_2D_to_1D(board))))
    succ_states[board_state_hash] = {
        "move": "Oc",
        "state": board,
        "hash": board_state_hash
    }
    board = move_outer_ring(state,"anticlockwise")
    board_state_hash = hash(' '.join(map(str, conv_2D_to_1D(board))))
    succ_states[board_state_hash] = {
        "move": "Occ",
        "state": board,
        "hash": board_state_hash
    }
    board = move_inner_ring(state,"clockwise")
    board_state_hash = hash(' '.join(map(str, conv_2D_to_1D(board))))
    succ_states[board_state_hash] = {
        "move": "Ic",
        "state": board,
        "hash": board_state_hash
    }
    board = move_inner_ring(state,"anticlockwise")
    board_state_hash = hash(' '.join(map(str, conv_2D_to_1D(board))))
    succ_states[board_state_hash] = {
        "move": "Icc",
        "state": board,
        "hash": board_state_hash
    }
    
    return succ_states

# https://stackoverflow.com/questions/5775352/python-return-2-ints-for-index-in-2d-lists-given-item
def index_2d(myList, v):
    for i, x in enumerate(myList):
        if v in x:
            return (i, x.index(v))

def heuristic(board):
    cost_calc = [
        [4,3,2,3,4],
        [3,2,1,2,3],
        [2,1,0,1,2],
        [3,2,1,2,3],
        [4,3,2,3,4]
    ]
    result_mat = [
        [1,2,3,4,5],
        [6,7,8,9,10],
        [11,12,13,14,15],
        [16,17,18,19,20],
        [21,22,23,24,25]
    ]

    res_mat = [
        [0,0,0,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0]
    ]
    cost = 0
    for i in range(len(board)):
        for j in range(len(board[0])):
            (pos_x, pos_y) = index_2d(result_mat, board[i][j])

            # Subtract current matrix position with result matrix position
            pos_x = i - pos_x
            pos_y = j - pos_y

            # Subtract from center of cost_calc matrix
            pos_x = (2 - pos_x)%5
            pos_y = (2 - pos_y)%5
            
            temp_cost = cost_calc[pos_x][pos_y]
            cost += temp_cost

            res_mat[i][j] += cost_calc[pos_x][pos_y]

    # No of good moves that can be performed
    nRows = 0
    nCols = 0
    for i in range(len(board)):
            flag_row = True
            flag_col = True
            for j in range(len(board[0])):
                if(res_mat[i][j] == 0):
                    flag_row = False
                if(res_mat[j][i] == 0):
                    flag_col = False

            if(flag_row):
                nRows+=1
            elif(flag_col):
                nCols+=1
    
    cost = cost - nRows*4 - nCols*4

    return cost

# check if we've reached the goal
def is_goal(state):
    state = conv_2D_to_1D(state)
    for i in range(1,len(state)):
        if(state[i-1] > state[i]):
            return False
    return True

def conv_to_2D(state):
    new_state = []
    for i in range(0,25,5):
        new_state.append([state[j] for j in range(i,i+5)])
    return new_state

def conv_2D_to_1D(state):
    flatten_board = [int(x) for arr in state for x in arr]
    return flatten_board

def solve(initial_board):
    """
    1. This function should return the solution as instructed in assignment, consisting of a list of moves like ["R2","D2","U1"].
    2. Do not add any extra parameters to the solve() function, or it will break our grading and testing code.
       For testing we will call this function with single argument(initial_board) and it should return 
       the solution.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """

    board_2D = conv_to_2D(initial_board)
    initial_board_obj = {
        "move": "",
        "state": board_2D,
        "hash": hash(' '.join(map(str, conv_2D_to_1D(board_2D)))),
        "path": []
    }

    q = PriorityQueue()
    q.put((0,initial_board_obj))

    closed = set()
    cost = 0
    while not q.empty():

        (curr_dist, curr_board_state) = q.get()
        curr_board_state = dict(curr_board_state)
        closed.add(curr_board_state["hash"])

        if(is_goal(curr_board_state["state"])):
            return curr_board_state["path"]

        succ_states = successors(curr_board_state["state"])
        cost += 1
        for key in succ_states:
            h_x = heuristic(succ_states[key]["state"])

            if(key not in closed):
                temp = copy.deepcopy(curr_board_state["path"])
                temp.append(succ_states[key]["move"])
                succ_states[key]["path"] = temp
                
                # conversion to tuple
                my_list = [(k, v) for k, v in succ_states[key].items()]
                q.put((cost + h_x, my_list))   # 1st parameter -> g(s) + h(s)

        # Selecting the best 2000 nodes for efficiency
        prune_len = 2000
        new_q = PriorityQueue()
        for i in range(0,prune_len):
            if not q.empty():
                new_q.put(q.get())

        q = new_q
    
    return []

# Please don't modify anything below this line
#
if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected a board filename"))

    start_state = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            start_state += [ int(i) for i in line.split() ]

    if len(start_state) != ROWS*COLS:
        raise(Exception("Error: couldn't parse start state file"))

    print("Start state: \n" +"\n".join(printable_board(tuple(start_state))))

    print("Solving...")
    route = solve(tuple(start_state))

    print("Solution found in " + str(len(route)) + " moves:" + "\n" + " ".join(route))
