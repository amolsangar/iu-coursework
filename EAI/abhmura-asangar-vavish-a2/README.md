# Assignment 2: Games and Bayesian Classifiers

### **Part 1 (Raichu-Vaibhav Vishwanath)** ###
The game of Raichu is a 2 player game which comprises of 3 pieces each : a pichu, a pikachu and raichu. The pichu can move only diagonally or above another opponent piece thus eliminating it. Similarly, the Pikachu can move only vertically and horizontally and can capture opposition pichu and pikachu, A Raichu can move in any direction and can move any number of moves.
For this problem, I have used minimax algorithm with alpha beta pruning . The successors for a current board involves searching all possible moves for the pieces we have remaining. SInce i am searching till depth 4, it will look at all successors at depth 4. 
I have defined the rules for all pieces possible. 
The minimax function has been adapted from the youtube video <a href='https://www.youtube.com/watch?v=l-hh51ncgDI'></a>.
The summary of my code is as follows:
<ul>
	<li> First call the minimax  algorithm with the successors of the initial board state.</li>
	<li> Then, the recursive implementation will look at all possible successors after choosing the first move</li>
	<li> The evaluation or utility function involves subtracting the number of white pichus and black pichus, white pikachus and black pikachus and white raichus and black raichus when the white player is playing. The inverse is done when the player is black. </li>
</ul>
This assignment helped me understand minimax algorithm and how it is used in 2 player games.  

Attached is the output of the my code playing on Tank against Prof. David's AI.
<img src='https://github.iu.edu/cs-b551-fa2021/abhmura-asangar-vavish-a2/blob/master/part1/Tank_op.png' alt='Output Image'>
  

### **Part 2 (The Game of Quintris-Abhijeet Sridhar M)** ###
- The problem here to design an AI that can play the game of quintris. To solve this, we would first need to get all possible locations at which a current piece can be placed, then pick the best solution, and perform the move. 
- By manually playing the game of quintris, I came up with a few good heuristics to measure on how good the board is. 
- We first generate all possible places in which the current piece can go:
  - We split this into 2 parts, checking all locations on the left, then all places on the right.
  - For each column in which the piece can go, we compute all rotations and flips for the piece, execute the down command, and store the result.
  - While going through each location, we keep storing temporary paths to append them to the final path.
- On each of the possible board generated, we calcuate the heuristic, which is a weighted average of:
  - Landing height - row number of the top left part of the current piece after putting it down
  - number of lines completed after putting the piece.
  - Transitions - Number of time in a row/column where the value changes from 'x' to ' ' - that is filled to empty or vice versa.
  - Holes - Number of empty locations on the board on top which there is a filled location.
  - Bad holes - Number of consecutive empty locations which have a top location filled and left and right of the top filled. (Empty location is blocked from above and side)
- Implementing lookahead:
  - After calculating the score of each of the possible locations of the piece, we pick the best 5 boards out of them.
  - We again generate all possible locations on each of these top 5 boards, and calculate the scores.
  - Finally, we execute the path that can produce the least score after considering the next piece as well.
- There are 2 different ways in which the implementation is handled-
  - In function minmax(), we make copies of the quintris and execute the moves left, right etc to generate future boards. In turn all further calculation and implementation is based on using a quintris object.
  - In function get_best_path(), we just use the board and the piece and numerically compute all possible locations without executing the movement functions on the quintris, rather use given methdos in QuintrisGame.py to manipulate piece locations.
  - On following this method, the AI was able to get a high score of 231.
  - ![image](https://media.github.iu.edu/user/18478/files/3473b100-4019-11ec-88a9-96dd50b04f1d)
   
### **Part 3 (Truth be Told - Amol Sangar)** ###
- The problem is to classify multiple hotel reviews in two categories – Deceptive and Truthful. To solve this problem, the use of naïve bayes makes perfect sense as we can select the category based on the probability of each word in the corpus and multiplying them. 
- The first step to perform is to clean the data into a list or dictionary of words excluding special characters and numbers and then converting to lowercase characters. Then, the task is to remove words which are quite common and doesn’t contribute much to the prediction of the classes. Examples of such stop words are if, an, the, that etc.
- After data cleaning and splitting into words, the program calculates prior probability and likelihood terms. Prior probability is calculated by dividing numbers of reviews in one class by number of reviews in every other class. Example – P(Deceptive) = P(Deceptive) / P(Deceptive) + P(Truthful)

- Next is to calculate likelihood term for each term i.e.,

  - P(Word | Deceptive) = Number of times Word occurs in review + alpha / Total number of words in Deceptive + alpha * Total number of words in the vocabulary

  Here, alpha is called as Laplace smoothing parameter and is used to handle the problem of zero probability.

- The last step is to calculate posterior probability which is simply multiplying likelihood and prior probability. Using log, we can do the same multiplication as - log(A*B) = logA + logB.

- Finally, the program cleans the input test reviews the same way as the training data and predicts the class output.
