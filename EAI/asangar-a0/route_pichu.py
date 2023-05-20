#!/usr/local/bin/python3
#
# route_pichu.py : a maze solver
#
# Submitted by : Amol Dattatray Sangar (asangar)
#
# Based on skeleton code provided in CSCI B551, Fall 2021.

import sys
from queue import Empty, PriorityQueue
import copy

# Parse the map from a given filename
def parse_map(filename):
        with open(filename, "r") as f:
                return [[char for char in line] for line in f.read().rstrip("\n").split("\n")][3:]
                
# Check if a row,col index pair is on the map
def valid_index(pos, n, m):
        return 0 <= pos[0] < n  and 0 <= pos[1] < m

# Find the possible moves from position (row, col)
def moves(map, row, col):
        moves={"D":{"move":(row+1,col),"path":[]}, "U":{"move":(row-1,col),"path":[]}, "L":{"move":(row,col-1),"path":[]}, "R":{"move":(row,col+1),"path":[]}}

        # Return only moves that are within the house_map and legal (i.e. go through open space ".")
        return [ {op:move} for op,move in moves.items() if valid_index(move["move"], len(map), len(map[0])) and (map[move["move"][0]][move["move"][1]] in ".@" ) ]

# Calculates Manhattan Distance between two points
def manhattan(point1x, point1y, point2x, point2y):
        return abs(point2x-point1x) + abs(point2y - point1y)

# Calculates the optimal path by backtracking from the goal node till the start node
# Returns list in reverse order i.e. from start position to end position
def generate_optimal_path(result, goal_loc, start_loc):
        op_path = []
        node = goal_loc;

        while node is not Empty:
                if(node in result):
                        op_path.append(node)
                        node = result[node]['parent']
                        if(node == start_loc):
                                return op_path[::-1]

# Takes the optimal path and returns the directions taken to reach that step
# Returns a single string of directions
def convert_to_direction(path, start_loc):
        previous_step = start_loc
        str = ""
        for step in path:
                if(previous_step[0] - step[0] > 0):
                        str += 'U'
                elif(previous_step[0] - step[0] < 0):
                        str += 'D'
                elif(previous_step[1] - step[1] > 0):
                        str += 'L'
                elif(previous_step[1] - step[1] < 0):
                        str += 'R'
                previous_step = step
        return str

        
# Perform search on the map
# This function MUST take a single parameter as input -- the house map --
# and return a tuple of the form (move_count, move_string), where:
# - move_count is the number of moves required to navigate from start to finish, or -1
#    if no such route exists
# - move_string is a string indicating the path, consisting of U, L, R, and D characters
#    (for up, left, right, and down)

def search(house_map):
        # Find pichu start position
        pichu_loc=[(row_i,col_i) for col_i in range(len(house_map[0])) for row_i in range(len(house_map)) if house_map[row_i][col_i]=="p"][0]
        goal_loc = [(row_i,col_i) for col_i in range(len(house_map[0])) for row_i in range(len(house_map)) if house_map[row_i][col_i]=="@"]

        if not goal_loc:
                return (-1,"")

        dict_mov = {
                "move": pichu_loc,
                "path": []
        }
        q = PriorityQueue()
        q.put((0,dict_mov))
        
        result = {}
        closed = set()
        cost_fn = 0
        while not q.empty():
                (curr_dist, dict_mov_2)=q.get()
                dict_mov_2 = dict(dict_mov_2)
                key = list(dict_mov_2)[0]
                curr_move = dict_mov_2["move"]
                curr_path_cost = dict_mov_2["path"]
                closed.add(curr_move)

                if house_map[curr_move[0]][curr_move[1]]=="@":
                        return (len(''.join(curr_path_cost)), ''.join(curr_path_cost))
                
                cost_fn += 1
                for move in moves(house_map, *curr_move):
                        op = list(move)[0]
                        mv = move[op]["move"]
                        if(mv not in closed):
                                temp = copy.deepcopy(curr_path_cost)
                                temp.append(op)
                                move[op]["path"] = temp
                                my_list = [(k, v) for k, v in move[op].items()]
                                q.put((cost_fn + manhattan(mv[0], mv[1],*goal_loc[0]), my_list))    # 1st parameter -> g(s) + h(s)
        
        return (-1,"")
        
# Main Function
if __name__ == "__main__":
        house_map=parse_map(sys.argv[1])
        print("Shhhh... quiet while I navigate!")
        solution = search(house_map)
        print("Here's the solution I found:")
        print(str(solution[0]) + " " + solution[1])
