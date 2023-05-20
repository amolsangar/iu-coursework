# Assignment 1- Searching

### **Part 1 (The 2021 Puzzle-Amol Sangar)** ###

* **Initial State**: Board with tiles not in correct place
* **Goal State**: All tiles arranged sequentially on board
* **Valid States**: Tiles having values from 1 to 25 will constitute as a valid state for 5x5 board
* **Successor Function**: Set of states after performing valid operations like R1-R5, L1-L5, U1-U5, D1-D5, Occ, Oc, Icc and Ic.
* **Cost Function**: Cost of each step is 1
* **Heuristic Function:** 
   * Starting with Manhattan distance as the heuristic function, it was observed that the goal state was unreachable due to its inadmissibility in the first place. Since it was overestimating the number of steps it required to reach the goal node, I ended up calculating the minimum number of steps for each tile. 
   * I also implemented a lot of other heuristics without success. One was to subtract the sum of number of tiles not in correct row from the sum of number of tiles not in correct column. Another one was based upon pattern heuristic which computed a couple of heuristics functions and returned the maximum value amongst both. This would serve as the upper bound for the algorithm but this too didn’t work well.
   * The implemented heuristic is the sum of minimum number of steps for each tile to reach its correct position. Above this, the function also checks if there are any good row or column movement present and if its available it subtracts 4 from the sum in order to consider it as a single move and thus prioritizes this movement over others. 

* **Optimization:** 
It was observed that most of the solutions were found in the starting branches of the tree. In order to improve the efficiency, no more than 2000 nodes were considered for expansion at each step. This definitely works well for solving the board which have reasonable smallest steps to find. In case of complex boards like board1, I fear the use of 2000 nodes limit destroys the working of the algorithm.

* **In this problem, what is the branching factor of the search tree?**
   * The branching factor is 24 since there are 24 operations available for each state which are R1-R5, L1-L5, U1-U5, D1-D5, Occ, Oc, Icc and Ic.

* **If the solution can be reached in 7 moves, about how many states would we need to explore before we found it if we used BFS instead of A\* search?  A rough answer is fine**
   * In BFS every node is traversed level-by-level and thus for 7 moves the goal node would be present on the depth level 7. So, in worst case with branching factor 24, we would need to explore **24^7** states before we find a solution.


### **Part 2 (Road Trip-Lalith Dupathi)** ###

* <u>**Search Problem**</u>- In this case, given two cities one start and the other destination- the search problem is basically to find the optimum route between the two cities based on various parameters and cost function. So the main goal here is envisioned to find the shortest driving route through mapping using A* search algorithm
* <u>**Set of Valid States**</u>- This represents all the nodes i.e. all the cities in the raw input file through which a person can travel to reach a particular destination from the start point
* <u>**Successor Function**</u>- The next_city function acts as the succesor function over here wherein it reutrns a list of cities that can be travelled direclty from a particular "current_city"
* <u>**Goal State**</u>- It is basically reached when start==end after traversing a particular path.The state which gives the path from current city to end city by optimising the cost function provided i.e distance,time,deliery or segments. 
* <u>**Cost Functions**</u>- 
    * <u>**Distance Optimisation**</u>
        * Multiple heuristics were tried initially, first setting **h(s)** to 0 to see runtime of the algorithm, but for longer city distances it was failing and was executing in 1-2hrs essentially showing that though heuristic being admissable it wouldnt be A* implementation and the whole graph would've been searched
        * I then tried implementing Manhattan and Euclidean distance as well, manhattan again was not admissable as it calculates the distance in x-y space/direction only which wouldn't make sense as the cities not necessarily would be in the same horizontal or vertical line.
        Eulidean would also be inadmissable as calculating the distance through latitudes and longitudes wouldn't make sense and would provide incorrect units to the h(s) function
        * The final f(s) used for calculating the distance metric is taking **g(s)** as the distance that is covered from the start city to the current city till now in the search problem which is extracted from the road-segments.txt file and the **h(s)** used is the haversine distance between the current city reached and the end goal which approximately gives an estimation of how many more miles there are left to travel. Haversine out of all the 3 would be best as it is meant to calculate distances given the latitutdes and longitudes and also takes into account the spherical nature of the globe to give an approximation
    
    * <u>**Time Optimisation**</u>
        * The final f(s) used for calculating the time metric is taking **g(s)** as the distance/speed that is covered from the start city to the current city till now in the search problem which is extracted from the road-segments.txt file and the **h(s)** used is the time that is calculated haversine distance/max_speed between the current city reached and the end goal which approximately gives an estimation of how much more time is left to travel. 
        * Apart from the max_speed...I tried using the min_speed and average speed from the road-segments file, but upon further analysis they would be inadmissable as taking the min speed of the txt file on faster routes would overestimate the expected time same would be the case with average speed as well eg- if on a road speed limit is 100 and the average is 50 it would overestimate, hence max_speed was the best choice to keep h(s) admissable

    * <u>**Delivery Optimisation**</u>
        * The final f(s) used to calculate the delivery metric is same as the time above, but in this case the cost function was modified to take into account the chance of an accident on a segment with speed more than 50mph i.e if the threshold is exceeded on a particular highway given that the speed on the highway is >50 then the driver would return to the start city to collect the package again which inturn would increase the time as round trips are made

    * <u>**Segments Optimisation**</u>
        * Initially to evaluate the **h(s)** segment, the idea was to create a dictionary of a range from 0 to max distance from a city to another with intervals of 50-100miles where I could approximate the average segments in each case and according to the haversine distance left to cover I could lookup the average segment left to cover, but the approach turned out to be convoluted in terms of implementation and runtime 
        * The next approach was discussed in office hours by Proff Crandall was to go inline with the logic implemented in the time optimisation, in this case I first tried dividing haversine distance left to cover by min and average length of segments from the road-segments txt file to get an approximate number of segments but they would be inadmissable as in cases where the segment length is greater than the min or average it would overestimate segments left to cover
        * Another approach used was to divide haversine distance left from current city to end city by the maximum length of road segment which is an admissable heuristic as it would never overestimate i.e. even when the distance is the maximum it would divide the segments according to max segment length
        * The final f(s) used for calculating the segments metric is taking **g(s)** as the segments covered from the start city to the current city till now in the search problem which is just +1 of every step taken to a new city and the **h(s)** used is the segments that is calculated by haversine distance/allnumberofsegments which was derived through trial and error methodology which will always be admissable given the maximum denominator taken.

* <u>**Algorithm Working**</u>
    * The get_route function first takes the start, stop and cost function, a visited list is firstly initialied, all other parameters miles,time,delivery,segments are initiliased to 0 and the fringe is defined as the priority queue and initialised by putting in the firt segment i.e the start city. The algorithm then continues to the while loop to pop out the fringe with highest priority to get its corresponding miles,time,delivery and route so far to check if we have reached the goal state.
    * The next step is to check for all the successors in the for loop which is all the cities that one can visit from the current city we are on, all parameters are then incremented by the amount from the road-segments txt file which acts as the current cost(g(s)) in the priority function  and priority is calculated according to the cost function passed, the path with highest priority is then popped- this process continues till end city is reached
    
* <u>**Assumptions**</u>
    * Dealing with missing latitudes and longitudes for an entry was a major obstacle in the overall case as there were multiple zero division errors and huge runtimes when the algorithm reached a particular highway section or city. To start off I tried to implement a method to estimate the direction in which the highway was panning and then looked at the successors and predecessor of that particular junction to check which cities are directly connected and then averaged out the latitudes and longitudes of 2-3 nearest ones- inline with KNN logic but it still proved to be overestimating the haversine distance in some cases.
    * Upon further testing it was found that in some of the longest paths i.e Tampa,_Florida to Seattle,_Washington only 10-12% segments were highway intersections so a design decision to take h(s) as 0 in those cases was implemented knowing that it is always admissable and it was estimating the distance to cover accurately with reasonable runtimes

### **Part 3 (Choosing Team-Harshit Shiroiya)** ###
•	Set of Valid States- There are a set of states, in the initial state there are no students assigned to any team. The input is taken where the students are asked for their group preferences and the list of members, they do not want to work with. The valid states are assigning the students in the groups in all possible ways i.e. group of one, two or three as per their preference.
•	Successor Function- The successor function here is to assign the groups to all the students with consideration of their choices in the input.
•	Goal State- The goal is achieved when all the students are assigned to team and such that the time spent by the AI’s is the least.

•	Cost Functions-
1.	Total Grading Time:
	The time taken to grade all the groups by the AI’s. It is 5 mins per group. So total will be Total no. of teams * 5.
2.	Different Group Size:
	The students who mentioned a group size in their preference and they get assigned a group size of not their choice. This will take 2 mins per student.
3.	Members in Different Group but share their code.
	There is a probability of 5% that the students with different team share code which will lead to a cost of 60 mins. Therefore, 60*0.05.
4.	Student assigned a team member who they selected not to work with:
	If a student is assigned a team member who they opted not to work with then this will cost 10 mins.

•	Algorithm Working
o	The search algorithm used here is Depth first Search as we firstly create random possibility of group formation. Later we, compute the cost for all the possibility and we yield the best cost that is the least cost calculated and display the same.
o	The student_choice function first takes the given preferences of each student and returns the list of students along with their preferences in the form of dictionary.
o	Then we initiate create_group function and possible_team_members wherein we create all permutations (one, two or three members) of the groups that can be formed in the preference form.
o	Then, The successor group creates a list where in it checks with all the previously assigned groups and looks if all the groups are full or not.
o	Then we compute the cost of all the permutation of assigned teams and yield the better solution.

•	Result
o	We noticed that the first testcase which has six students had the minimum cost of 24 mins.
o	In the second testcase, we found the cost to be 43 mins and this test case had thirteen students
o	While in the third testcase there were twenty students and the cost turned out to be 66 mins which took a longer time to find this solution as this had many permutation of groups and students.


