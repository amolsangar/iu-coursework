# a0

# Part 1: Navigation

**Initial State:** Location of p on the house map

**Goal State:** Location of @ on the house map

**Valid States:** Places showing . on the map

**Successor function:** Given a state, the set of possible states where 'p' can move i.e places with . 

**Cost Function:** Cost of each step is 1

**Why does the program often fail to find a solution?  Implement a fix to make the code work better,and explain what you did in the report.**
- The code already given didn't work as expected because it was not keeping track of the visited cells which resulted in recursion. The successor function would generate the already visited nodes again and thus the same nodes were getting selected repeatedly.
- I solved the problem by making use of the A* algorithm and using Manhattan distance as the heuristic since the only possible movements available were up, down, left or right. Instead of using a list, I used priority queue to select the next node with the least cost to reach the goal node. Finally, when the goal node is found, I backtracked the steps to find the optimal path and converted it to directions.


# Part 2: Hide-and-seek

**Initial State:** Map with one p and one @ present

**Goal State:** k number of agents placed on the map and they cannot see each other

**Valid States:** Places showing . on the map

**Successor function:** Given a state, the set of possible states where the agent can move i.e places with . and cannot be seen from previous placed agents

The state space that is generated from the code involves only selecting those nodes for expansion from a single column where previous placed agents cannot see. This drastically reduced the search space and improved the execution time. 

The approach I have used involves placing maximum agents on one column without seeing each other. If no more agents can be placed on the column, then we move to the next column and repeat the process. If the solution is not found then it backtracks the tree and continues. 
The use of global variable helps in capturing all the leaf nodes which are possible solutions. I found that generally the first solution among the leaf nodes is the best one.
It is also **capable of placing agents more than the maximum no of columns** in the house map.

I faced a lot of challenges completing this assignment which involved trying different methods and finally getting it to work with the backtracking solution.
In backtracking too I faced issues such as not able to place agents more than the maximum columns available in the grid.

Since this solution uses recursion to achieve the functionality, I fear that at one point error may occur due to stackoverflow.
