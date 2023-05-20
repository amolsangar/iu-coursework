#!/usr/local/bin/python3
#
# arrange_pichus.py : arrange agents on a grid, avoiding conflicts
#
# Submitted by : Amol Dattatray Sangar (asangar)
#
# Based on skeleton code in CSCI B551, Fall 2021.

import sys
import copy

# Parse the map from a given filename
def parse_map(filename):
	with open(filename, "r") as f:
		return [[char for char in line] for line in f.read().rstrip("\n").split("\n")][3:]

# Count total # of pichus on house_map
def count_pichus(house_map):
    return sum([ row.count('p') for row in house_map ] )

# Return a string with the house_map rendered in a human-pichuly format
def printable_house_map(house_map):
    return "\n".join(["".join(row) for row in house_map])

# Add a pichu to the house_map at the given position, and return a new house_map (doesn't change original)
def add_pichu(house_map, row, col):
    return house_map[0:row] + [house_map[row][0:col] + ['p',] + house_map[row][col+1:]] + house_map[row+1:]

# Get list of successors of given house_map state
def successors(house_map, attack):
    return [ add_pichu(house_map, r, c) for r in range(0, len(house_map)) for c in range(0,len(house_map[0])) if house_map[r][c] == '.' and house_map[r][c] not in attack ]

# check if house_map is a goal state
def is_goal(house_map, k):
    return count_pichus(house_map) == k 

# Generates a list of positions visible from one node 
# Visible nodes are represented by 'attack' array
def generate_attack_array(house_map, p_loc):
    attack = []
    max_row = len(house_map)
    max_col = len(house_map[0])
    
    (start_row, start_col) = (p_loc)

    # Check Upper Row
    start_row = p_loc[0] - 1
    while (start_row >= 0 and start_row < max_row and house_map[start_row][p_loc[1]] != 'X' and house_map[start_row][p_loc[1]] != '@' ):
        if((p_loc[0],start_col) not in attack):
            attack.append((start_row,p_loc[1]))
        
        start_row += -1

    # Check Lower Row
    start_row = p_loc[0] + 1
    while (start_row >= 0 and start_row < max_row and house_map[start_row][p_loc[1]] != 'X' and house_map[start_row][p_loc[1]] != '@' ):
        if((p_loc[0],start_col) not in attack):
            attack.append((start_row,p_loc[1]))
        
        start_row += 1

    # Check Right Column
    start_col = p_loc[1] + 1
    while (start_col >= 0 and start_col < max_col and house_map[p_loc[0]][start_col] != 'X' and house_map[p_loc[0]][start_col] != '@' ):
        if((p_loc[0],start_col) not in attack):
            attack.append((p_loc[0],start_col))
        
        start_col += 1

    # Check Left Column
    start_col = p_loc[1] - 1
    while (start_col >= 0 and start_col < max_col and house_map[p_loc[0]][start_col] != 'X' and house_map[p_loc[0]][start_col] != '@' ):
        if((p_loc[0],start_col) not in attack):
            attack.append((p_loc[0],start_col))
        
        start_col += -1

    # Check Upper Left Diagonal
    start_row = p_loc[0] - 1
    start_col = p_loc[1] - 1
    while (start_row >= 0 and start_row < max_row and start_col >= 0 and start_col < max_col and house_map[start_row][start_col] != 'X' and house_map[start_row][start_col] != '@' ):
        if((start_row,start_col) not in attack):
            attack.append((start_row,start_col))
        
        start_row += -1
        start_col += -1

    # Check Lower Left Diagonal
    start_row = p_loc[0] + 1
    start_col = p_loc[1] + 1
    while (start_row >= 0 and start_row < max_row and start_col >= 0 and start_col < max_col and house_map[start_row][start_col] != 'X' and house_map[start_row][start_col] != '@' ):
        if((start_row,start_col) not in attack):
            attack.append((start_row,start_col))
        
        start_row += 1
        start_col += 1

    # Check Upper Right Diagonal
    start_row = p_loc[0] - 1
    start_col = p_loc[1] + 1
    while (start_row >= 0 and start_row < max_row and start_col >= 0 and start_col < max_col and house_map[start_row][start_col] != 'X' and house_map[start_row][start_col] != '@' ):
        if((start_row,start_col) not in attack):
            attack.append((start_row,start_col))
        
        start_row += -1
        start_col += 1

    # Check Lower Right Diagonal
    start_row = p_loc[0] + 1
    start_col = p_loc[1] - 1
    while (start_row >= 0 and start_row < max_row and start_col >= 0 and start_col < max_col and house_map[start_row][start_col] != 'X' and house_map[start_row][start_col] != '@' ):
        if((start_row,start_col) not in attack):
            attack.append((start_row,start_col))
        
        start_row += 1
        start_col += -1
    
    return attack

# Arrange agents on the map
# This function MUST take two parameters as input -- the house map and the value k --
# and return a tuple of the form (new_house_map, success), where:
# - new_house_map is a new version of the map with k agents,
# - success is True if a solution was found, and False otherwise.
res_arr = []
def place_recursively(house_map, col, att, k):
    answer = []
    max_row = len(house_map)
    max_col = len(house_map[0])
    attack = att

    if is_goal(house_map,k):
        return (house_map, True, attack)
    
    if col >= max_col:
        return (house_map, False, attack)

    for i in range(max_row):
        flatten_attack = [x for arr in attack for x in arr]
        if (i,col) not in flatten_attack and house_map[i][col] != 'X' and house_map[i][col] != 'p' and house_map[i][col] != '@':
            house_map[i][col] = 'p'
            attack.append(generate_attack_array(house_map, (i,col)))
            
            if place_recursively(house_map, col , attack, k)[1] == True:
                # Capturing copies of the generated solutions as values are passed by reference in Python
                answer = copy.deepcopy(house_map)
                res_arr.append(answer)
                return (answer, True, attack)

            attack.pop()
            house_map[i][col] = '.'    # Backtracking

    # Move to the next column if pichu cannot be placed on the current column
    place_recursively(house_map, col + 1, attack, k)

    return (house_map, False, attack)

# Check if the final map satisfies all conditions or not
def is_result_non_attacking(res_map):
    pichu_locs=[(row_i,col_i) for col_i in range(len(res_map[0])) for row_i in range(len(res_map)) if res_map[row_i][col_i]=="p"]
    for pichu_loc in pichu_locs:
        temp = generate_attack_array(res_map, pichu_loc)
        check =  any(item in temp for item in pichu_locs)
        if(check == True):
            return False    
    return True

def solve(house_map,k):
    if k == 1:
        return (house_map, True)

    pichu_loc=[(row_i,col_i) for col_i in range(len(house_map[0])) for row_i in range(len(house_map)) if house_map[row_i][col_i]=="p"][0]
    agent_loc = [(row_i,col_i) for col_i in range(len(house_map[0])) for row_i in range(len(house_map)) if house_map[row_i][col_i]=="@"][0]

    attack = generate_attack_array(house_map, pichu_loc)
    place_recursively(house_map, 0, [attack], k)

    for res in res_arr:
        if(is_result_non_attacking(res)):
            if is_goal(res,k):
                return (res,True)
    
    return (house_map, False)

# Main Function
if __name__ == "__main__":
    house_map=parse_map(sys.argv[1])
    # This is k, the number of agents
    k = int(sys.argv[2])
    print ("Starting from initial house map:\n" + printable_house_map(house_map) + "\n\nLooking for solution...\n")
    solution = solve(house_map,k)
    print ("Here's what we found:")
    print (printable_house_map(solution[0]) if solution[1] else "False")
