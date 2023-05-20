# Simple quintris program! v0.2
# D. Crandall, Sept 2021

from AnimatedQuintris import *
from SimpleQuintris import *
from kbinput import *
import time, sys
from copy import deepcopy
import math

class HumanPlayer:
    def get_moves(self, quintris):
        print("Type a sequence of moves using: \n  b for move left \n  m for move right \n  n for rotation\n  h for horizontal flip\nThen press enter. E.g.: bbbnn\n")
        moves = input()
        return moves

    def control_game(self, quintris):
        while 1:
            c = get_char_keyboard()
            commands =  { "b": quintris.left, "h": quintris.hflip, "n": quintris.rotate, "m": quintris.right, " ": quintris.down }
            commands[c]()

#####
# This is the part you'll want to modify!
# Replace our super simple algorithm with something better
#
class ComputerPlayer:
    # This function should generate a series of commands to move the piece into the "optimal"
    # position. The commands are a string of letters, where b and m represent left and right, respectively,
    # and n rotates. quintris is an object that lets you inspect the board, e.g.:
    #   - quintris.col, quintris.row have the current column and row of the upper-left corner of the 
    #     falling piece
    #   - quintris.get_piece() is the current piece, quintris.get_next_piece() is the next piece after that
    #   - quintris.left(), quintris.right(), quintris.down(), and quintris.rotate() can be called to actually
    #     issue game commands
    #   - quintris.get_board() returns the current state of the board, as a list of strings.
    #
    def get_moves(self, quintris):
        # super simple current algorithm: just randomly move left, right, and rotate a few times
        return random.choice("mnbh") * random.randint(1, 3)
       
    # This is the version that's used by the animted version. This is really similar to get_moves,
    # except that it runs as a separate thread and you should access various methods and data in
    # the "quintris" object to control the movement. In particular:
    #   - quintris.col, quintris.row have the current column and row of the upper-left corner of the 
    #     falling piece
    #   - quintris.get_piece() is the current piece, quintris.get_next_piece() is the next piece after that
    #   - quintris.left(), quintris.right(), quintris.down(), and quintris.rotate() can be called to actually
    #     issue game commands
    #   - quintris.get_board() returns the current state of the board, as a list of strings.
    #
    def control_game(self, quintris):


        #print((quintris.get_piece()[0]))
        #print(self.get_piece_dim(quintris.get_piece()[0]))
        #print((quintris.get_piece()[0]))
        #print(self.get_best_path(quintris))
        #print((max(quintris.get_piece()[0], key=len)))
        #temp_q1 = deepcopy(quintris)
        '''
        level1results = []
        for (next_path, next_quintris, a_height) in (self.get_all_boards(deepcopy(quintris))):
            level1results.append((next_path, next_quintris, self.get_quintris_score(next_quintris, a_height)))
        
        #level1results.sort(key=lambda x:x[2], reverse = True)
        print("THIS THE ONE", self.get_piece_dim(quintris.get_piece()[0]), quintris.row, quintris.col)
        for l in level1results:
            print(l[0] , l[2])
        '''
        #cc = 25 - self.col_height(quintris.get_board(), quintris.col, self.get_piece_dim(quintris.get_piece()[0])[0])
        #cc = 24 - self.get_col_height(quintris.get_board(), quintris.col) + self.get_piece_dim(quintris.get_piece()[0])[0] - 1
        #x = QuintrisGame.place_piece(quintris.get_board(), quintris.get_score(), quintris.get_piece()[0], cc ,0)
        #x = QuintrisGame.place_piece(x[0], x[1], quintris.get_next_piece(), 0,0)
        #print("POIPOIPOIPOI")
        #cc = self.get_all_boards(deepcopy(quintris.get_board()), quintris.get_score(), deepcopy(quintris.get_piece()[0]), quintris.col)
        #for rr in cc:
        #    print(rr[0], self.get_quintris_score(rr[0],rr[2]))
        #print("POIPOIPOIPOI2")
        #for i in self.get_all_piece_orientations(quintris.get_piece()[0]):
        #    x = QuintrisGame.place_piece(quintris.get_board(), quintris.get_score(), i[0], 0 ,"")
        #    x = self.place_piece(deepcopy(quintris.get_board()), quintris.get_score(), i[0], 0, [])
        #    x = self.place_piece(deepcopy(x[1]), quintris.get_score(), i[0], 0, [])
        #    for rr in x[1]:
        #        print("..[", rr, "]..")
        #    print("YYYYYY")
        #cc=self.get_all_piece_orientations(quintris.get_piece()[0])
        #print(quintris.get_piece()[0])
        #place_piece(self, board, score, piece, col, path):
        #if cc[0][0] == quintris.get_piece()[0]:
         #   print("THEY ARE SAME")
        #print((cc[1][0]))
        #print(QuintrisGame.rotate_piece(quintris.get_piece()[0], 90))
        
                
            
        #print(self.get_col_height(quintris.get_board() , 0), " IS THE COL HEIGHT")
        
        #print(cc)
        #for i in cc:
        #    print(i[0],i[2])
        print("POIPOIPOIPOI2")
        #for rr in x[0]:
        #    print("..[", rr, "]..")

        #print("POIPOIPOIPOI")
        while 1:
            time.sleep(0.1)

          

            
            (moves,score) = self.minimax(quintris)
            #moves2 = self.search_best_path(quintris)
            #print("The path is \n\n\n\n")
            #print(moves)
            #print("\n\n\n\n")
            #run = False
            # moves = self.get_best_row(quintris)
            #if moves1[1] > moves2[1]:
            #    moves = moves1[0]
            #else:
            #    moves = moves2[0]
            for move in moves:
                if move == 'm':
                    quintris.right()
                elif move == 'b':
                    quintris.left()
                elif move == 'n':
                    quintris.rotate() 
                elif move == 'h':
                    quintris.hflip() 
                elif move == 'v':
                    quintris.vflip() 
                elif move == 'd':
                    quintris.down()   
                    print(moves, score)

                    #print(self.get_max_height(quintris.get_board()))
               
            
    
    # Defs
    def get_max_height(self, board):
        
        r = 0
        for i in range(24, -1, -1):
            found = False
            for j in range(15):
                #print(i, " , ", j , " value " , board[i][j])
                if board[i][j] == "x":
                    found = True
                    #break
            if not found:
                #print("r is : " + str(r))
                break
            r += 1
        #print('\nBOARD FOR R'.join(map(''.join, board)))

        return r
     
    def get_piece_dim(self, piece):
        width = 0
        height = 0
        for row in piece:
            row_len = len(row)
            if row_len > width:
                width = row_len
            height += 1
        return (height,width)

    def a_height(self, board):
        
        diff = 0
        bump_values = []
        bump = 0
        for column in zip(*board): 
            for i in range(len(column)):
                if column[i] == 'x':
                    size = (len(column) - i)
                    diff += size
                    bump_values.append(size)
                    break
        
        diff_bump = [t - s for s, t in zip(bump_values, bump_values[1:])]
        for val in diff_bump:
            bump += abs(val)
        #print(diff_bump, bump)
        return (diff,bump)

    def get_bad_holes(self, board):
        
        holes = 0
        streak = 0
        

        # for column in zip(*board): 
        for idx, column in enumerate(zip(*board)):
            found = False
            for i in range(1, len(column)):
                if not found:
                    if column[i] == 'x':
                        found = True
                else:
                    if column[i] == ' ':
                        if streak > 0:
                            holes += ((streak * (streak-1))/2)
                            break
                        if idx == 0:
                            if board[i-1][idx+1] == 'x':
                                holes += 1
                        elif idx == 14:
                            if board[i-1][idx-1] == 'x':
                                holes += 1
                        else:
                            if board[i-1][idx-1] == 'x' and board[i-1][idx+1] == 'x':
                                holes += 1
                        
                        streak += 1
                    else:
                        streak = 0
                        

        return holes

    def get_holes(self, board):
        
        holes = 0

        for column in zip(*board): 
            found = False
            for i in range(1, len(column)):
                if not found:
                    if column[i] == 'x':
                        found = True
                else:
                    if column[i] == ' ':
                        holes += 1
                        
        return holes

    def get_transitions(self, board):
        
        row_result = 0
        col_result = 0

        for column in zip(*board):   
            for i in range(0, len(column) - 1):
                if column[i] != column[i+1]:
                    col_result += 1

        for row in board: 
            for i in range(0, len(row) - 1):
                if row[i] != row[i+1]:
                    row_result += 1
        return (row_result,col_result)  

    def get_complete_lines(self, board):
        c = 0
        for row in board:
            flag = False
            for elem in row:
                if elem == ' ':
                    flag = True
                    break
            if not flag:
                c += 1
        return c

   

    def get_path(self, quintris):
        combos = self.get_best_path(quintris)
        #self.a_height(quintris)
        min_eval = math.inf

        evals = []
        '''
         x
        x x        
        a = -0.510066
        b = 0.760666
        c = -0.35663
        d = -0.184483
        e = 0.5
        '''
        a=1
        b=1
        c=1
        d=1
        e=1


        best_path = []
        # print("YAHA PAR HAI")
        for combo in combos:
            #combo_eval = a*combo[1] + d*combo[2] + c*combo[3] - b* combo[4] + e*combo[5]
            combo_eval = self.get_evaluation(combo[1], combo[2], combo[3], combo[4], combo[5], combo[6])

            evals.append(combo_eval)


        max_eval = max(evals)
        max_eval_index = evals.index(max_eval)
        #print("COMBO")
        #print(combos[max_eval_index], self.get_evaluation(combos[max_eval_index][1], combos[max_eval_index][2], combos[max_eval_index][3], combos[max_eval_index][4], combos[max_eval_index][5], combos[max_eval_index][5]))
        return combos[max_eval_index][0]
    

    def get_evaluation(self, l_height, score,r_trans, c_trans, holes, bad_holes, bump):
        a = -4.500158825082766 # l height
        b = 3.4181268101392694 # score
        c = -3.2178882868487753 # r trans
        d = -9.348695305445199 # c trans 
        e = -7.899265427351652 # holes
        f = -3.3855972247263626 # bad holes
        
        

        return a*l_height + b*score + c*r_trans + d*c_trans + e*holes + f*bad_holes + g*bump


    def get_eval(self, a_height, bump, holes, score, height):
        a = -3.3855972247263626
        b = -3.3855972247263626
        c = -7.899265427351652
        d = 3.4181268101392694
        e = -4.500158825082766 

        a=1
        b=1
        c=1
        d=-100
        e=10

        a = -0.510066
        b = 0.760666
        c = -0.35663
        d = -0.184483
      
        return a*a_height + b*score + c*holes + d*bump #+ e*height

    def get_quintris_score(self, board, l_height): 

    # Explicit values of these parameters taken from line 121-127 in https://github.com/ielashi/eltetris/blob/master/src/eltetris.js
        a = -4.500158825082766 # l height
        b = 19.4181268101392694 # score
        c = -3.2178882868487753 # r trans
        d = -9.348695305445199 # c trans 
        e = -7.899265427351652 # holes
        f = -3.3855972247263626 # bad holes
        g = -5.3178882868487753 # bump

        #a_height = self.get_max_height(quintris.get_board())
        score = self.get_complete_lines(board)

        tr_evals = self.get_transitions(board)
        r_tr = tr_evals[0]
        c_tr = tr_evals[1]

        holes = self.get_holes(board)
        bad_holes = self.get_bad_holes(board)

        (_,bump) = self.a_height(board)

        #print(l_height, score, r_tr, c_tr, holes, bad_holes)

        return a*l_height + b*score + c*r_tr + d*c_tr + e*holes + f*bad_holes  + g*bump




    def get_row_results(self, quintris, path, all_combos):
        _quintris = deepcopy(quintris)
        for i in range(4):
            if i != 0:
                _quintris.rotate()
                path.append('n')

            temp_q1 = deepcopy(_quintris)
            t_path = deepcopy(path)
            
            temp_q1.hflip()
            temp_q1.down()
            t_path.append('h')

            #combos = self.get_best_path(quintris)
            t_evals = self.a_height(temp_q1.get_board())
            tr_evals = self.get_transitions(temp_q1.get_board())
            all_combos.append((temp_q1, t_path+['d'], self.get_max_height(temp_q1.get_board()), temp_q1.get_score(), tr_evals[0], tr_evals[1], self.get_holes(temp_q1.get_board()), self.get_bad_holes(temp_q1.get_board()) ))



            temp_q1 = deepcopy(_quintris)
            t_path = deepcopy(path)
            
            temp_q1.vflip()
            temp_q1.down()
            t_path.append('v')
            t_evals = self.a_height(temp_q1.get_board())
            tr_evals = self.get_transitions(temp_q1.get_board())
            all_combos.append((temp_q1, t_path+['d'], self.get_max_height(temp_q1.get_board()), temp_q1.get_score(), tr_evals[0], tr_evals[1], self.get_holes(temp_q1.get_board()), self.get_bad_holes(temp_q1.get_board()) ))


            temp_q1 = deepcopy(_quintris)

            temp_q1.down()
            evals = self.a_height(temp_q1.get_board())
            t_evals = self.a_height(temp_q1.get_board())
            tr_evals = self.get_transitions(temp_q1.get_board())
            all_combos.append((temp_q1, t_path+['d'], self.get_max_height(temp_q1.get_board()), temp_q1.get_score(), tr_evals[0], tr_evals[1], self.get_holes(temp_q1.get_board()), self.get_bad_holes(temp_q1.get_board()) ))
            #print("ROW RESULT")
            #print(path+['d'])
        return all_combos

    def get_best_path(self,quintris):
        
        all_combos = []
        i = quintris.col
        #i = 0
        temp_q = deepcopy(quintris)
        path = []
        #print("part1 done")
        #print(i)
        while(i - self.get_piece_dim(quintris.get_piece()[0])[1] > -1):
        #while(i > 15):
            #print(i)
            temp_q.left()
            path.append('b')
            all_combos = (self.get_row_results(temp_q, deepcopy(path), all_combos))
            #i-=1
            i-=1
       
        #i = quintris.col
        i = 0
        temp_q = deepcopy(quintris)
        path = []

        while(i + self.get_piece_dim(quintris.get_piece()[0])[1] < 15):
        #while(i < 15):
            temp_q.right()
            path.append('m')
            
            all_combos = (self.get_row_results(temp_q, deepcopy(path), all_combos))

            i+=1


        #print(all_combos)
        return all_combos


    def minimax1(self, quintris):
        cur_max = math.inf
        cur_score = 0

        depth = 3
        path = []

        temp_q = deepcopy(quintris)

        for m in range (depth):
           
            best = self.get_best_quintris(temp_q)
            temp_q = best[0]
            if m == 0:
                path = best[1]
        return path

    def minimax(self, quintris):

        cur_best = -math.inf
        best_path = []

        level1results = []
        level2results = []
        
        
        q1 = deepcopy(quintris)
        for (next_path, next_quintris, a_height) in (self.get_all_boards1(q1)):
            level1results.append((next_path, next_quintris, self.get_quintris_score(next_quintris.get_board(), a_height)))


        level1results.sort(key=lambda x:x[2], reverse = True)

        for i in range(len(level1results)):
            if i > 4:
                break
            q1 = deepcopy(level1results[i][1])
            for (next_path, next_quintris, a_height) in (self.get_all_boards1(q1)):
                cur_score = self.get_quintris_score(next_quintris.get_board(), a_height)
                if cur_score > cur_best:
                    cur_best = cur_score
                    best_path = level1results[i][0]
        '''
        for i in range(5):
            
            q1 = deepcopy(level1results[i][1])
            for (next_path, next_quintris, a_height) in (self.get_all_boards(q1)):
                level2results.append((level1results[i][0], next_quintris, self.get_quintris_score(next_quintris, a_height)))
               

        level2results.sort(key=lambda x:x[2], reverse = True)
        '''
        '''
        for i in range(len(level2results) - 1, len(level2results) - 6, -1):
            
            q1 = deepcopy(level2results[i][1])
            for (next_path, next_quintris, a_height) in (self.get_all_boards(q1)):
                
                cur_score = self.get_quintris_score(next_quintris, a_height)
                if cur_score > cur_best:
                    cur_best = cur_score
                    best_path = level2results[i][0]
        '''

        #level2results = level2results[:5]
        #level1results = level1results[:5]

        #best_path = level1results[0][0]
        #cur_best = level1results[0][2]

        score = self.get_complete_lines(level1results[0][1].get_board())

        tr_evals = self.get_transitions(level1results[0][1].get_board())
        r_tr = tr_evals[0]
        c_tr = tr_evals[1]

        holes = self.get_holes(level1results[0][1].get_board())
        bad_holes = self.get_bad_holes(level1results[0][1].get_board())

        (_,bump) = self.a_height(level1results[0][1].get_board())

        #print("LH", l_height, "SCORE: ", score, "RTR: ", r_tr, "cTR:" , c_tr, "hOLES",  holes, "BHOLES:", bad_holes)
        print("PATHHHHH IS ",best_path, cur_best)
        

        return (best_path, cur_best)

    def search_best_path(self, quintris):

        cur_best = -math.inf
        best_path = []

        level1results = []
        level2results = []
        
        
        q1 = deepcopy(quintris)
        for (next_path, next_board, a_height) in (self.get_all_boards(q1.get_board(), q1.get_score(), q1.get_piece()[0], q1.col)):
            level1results.append((next_path, next_board, self.get_quintris_score(next_board, a_height)))

        #print("JHJGJGJGVJGG")
        #print(level1results)
        level1results.sort(key=lambda x:x[2], reverse = True)
        
        for i in range(len(level1results)):
            if i > 4:
                break
            q1 = deepcopy(level1results[i][1])
            for (next_path, next_board, a_height) in (self.get_all_boards(q1, level1results[i][2], quintris.get_next_piece(), 0)):
                cur_score = self.get_quintris_score(next_board, a_height)
                if cur_score > cur_best:
                    cur_best = cur_score
                    best_path = level1results[i][0]
                #level2results.append((level1results[i][0], next_board, self.get_quintris_score(next_board, a_height)))
               
        
        #level2results.sort(key=lambda x:x[2], reverse = True)
        '''
        
        for i in range(len(level2results)):
            
            q1 = deepcopy(level2results[i][1])
            #for (next_path, next_quintris, a_height) in (self.get_all_boards(q1)):
                
                cur_score = self.get_quintris_score(next_quintris, a_height)
                if cur_score > cur_best:
                    cur_best = cur_score
                    best_path = level2results[i][0]
        '''

        #level2results = level2results[:5]
        level1results = level1results[:5]
        #print("LEVEL1 result")
        #for re in level1results:
        #    print(re[0], re[2])

        #best_path = level1results[0][0]
        #   cur_best = level1results[0][2]
        
        score = self.get_complete_lines(level1results[0][1])

        tr_evals = self.get_transitions(level1results[0][1])
        r_tr = tr_evals[0]
        c_tr = tr_evals[1]

        holes = self.get_holes(level1results[0][1])
        bad_holes = self.get_bad_holes(level1results[0][1])

        (_,bump) = self.a_height(level1results[0][1])

        print("LH", 3, "SCORE: ", score, "RTR: ", r_tr, "cTR:" , c_tr, "hOLES",  holes, "BHOLES:", bad_holes, self.get_quintris_score(level1results[0][1] , 3))
       
        best_path = level1results[0][0]
        cur_best = level1results[0][2]
        #print("PATHHHHH IS ",best_path, cur_best)
        

        return (best_path,cur_best)

    def col_height(self, board, index, height):
        #print("asdfasd",height)
        for idx,column in enumerate(zip(*board)):
            if idx == index:
                #print("COL: " , column)
                for i in range(25):
                    if column[i] == 'x':
                        #print("DIFFFFF", len(column) - i)
                        return (len(column) - i - 1) + (height)
        return height
        
    def get_col_height(self, board, index):
        #print("asdfasd",height)
        for idx,column in enumerate(zip(*board)):
            if idx == index:
                #print("COL: " , column)
                for i in range(25):
                    if column[i] == 'x':
                        #print("DIFFFFF", len(column) - i)
                        return (len(column) - i)
        return 0


    def get_all_piece_orientations(self, piece):
        all_orientations = []
        pieces = []
        new_path = []
        rotations = [0,90,180,270]
        for rot in rotations:
            new_piece = QuintrisGame.rotate_piece(deepcopy(piece), rot)
            
            if new_piece not in pieces:
                all_orientations.append((new_piece, deepcopy(new_path)))
                pieces.append(new_piece)
            new_piece = QuintrisGame.hflip_piece(deepcopy(piece))
            if new_piece not in pieces:
                all_orientations.append((new_piece, deepcopy(new_path) + ['h']))
                pieces.append(new_piece)
            new_piece = QuintrisGame.vflip_piece(deepcopy(piece))
            if new_piece not in pieces:
                all_orientations.append((new_piece, deepcopy(new_path) + ['v']))
                pieces.append(new_piece)

            #print("YAHOOOOO1")
            #print(all_orientations)
            #print("YAHOOOOO2")
            #print(pieces)
            #print("YAHOOOOO3")
            new_path.append('n')
            
        return all_orientations

    def place_piece(self, board, score, piece, col, path):
        row_to_insert = 25 - self.get_col_height(board, col) - self.get_piece_dim(piece)[0] 

        #print(row_to_insert,self.get_col_height(board, col))
        #print()
        #for rr in board:
            #print("...[", rr, "]...")
        collision = QuintrisGame.check_collision(deepcopy(board), score, piece, row_to_insert, col)
        #print("PPIOIOII", collision, " at ", row_to_insert)
        if not collision:
                placed_board = QuintrisGame.place_piece(deepcopy(board), score, piece, row_to_insert , col)[0]
                a_height = self.get_col_height(placed_board, col)
                #print("YOHOO")
                #print(placed_board)
                #print("YOHOOO2")
                return (path + ['d'], placed_board, a_height)
        return None

    def get_piece_with_orientation(self, piece, path):
        new_piece = []
        for i in path:
            if i != 'b' and i != 'm':
                if i == 'n':
                    new_piece = QuintrisGame.rotate_piece(deepcopy(piece), 90)
                if i == 'h':
                    new_piece = QuintrisGame.hflip_piece(deepcopy(piece))
                if i == 'v':
                    new_piece = QuintrisGame.vflip_piece(deepcopy(piece))
        return new_piece

    def get_all_boards(self, cur_board, score, piece, col):
        
       
        path = []
        #q = deepcopy(quintris)
        #quin = deepcopy(quintris)
        #c = quin.col
        #a_height = self.col_height(quin.get_board(), c, self.get_piece_dim(quintris.get_piece()[0])[0])

        visited = []

        #print("DIFFFFF", a_height, c)
        #quin.down()
        board = deepcopy(cur_board)

        orientations = self.get_all_piece_orientations(piece)

        for (new_piece, new_path) in orientations:
            #new_piece = self.get_piece_with_orientation(piece, new_path)
            to_yield = self.place_piece(deepcopy(board), score, new_piece, col, deepcopy(new_path))
        #print("PPPPPP")
        #print(to_yield)
            if to_yield != None:
                if to_yield[1] not in visited:
                    visited.append(to_yield[1])
                    #print("PPPPPP")
                    #print(to_yield)
                    yield to_yield

        

        i = col
        while(i > 0):
            i -= 1
            #quin.left()
            path.append('b')
            #orientations = self.get_all_piece_orientations(piece)

            for (new_piece, new_path) in orientations:
                #new_piece = self.get_piece_with_orientation(piece, new_path)
                to_yield = self.place_piece(deepcopy(board), score, new_piece, i, deepcopy(path) + new_path)
                if to_yield != None:
                    if to_yield[1] not in visited:
                        visited.append(to_yield[1])
                        #print("PPPPPP1")
                         
                        #print(to_yield)
                        yield to_yield
            

        path = []
        i = col

        while(i + self.get_piece_dim(piece)[1] < 15):
                
            #quin.left()
            i += 1
            path.append('m')
                
            #orientations = self.get_all_piece_orientations(piece)

            for (new_piece, new_path) in orientations:
                #new_piece = self.get_piece_with_orientation(piece, new_path)
                to_yield = self.place_piece(deepcopy(board), score, new_piece, i, deepcopy(path) + new_path)
                if to_yield != None:
                    if to_yield[1] not in visited:
                        visited.append(to_yield[1])
                        #print("PPPPPP2")
                        #to_yield[0] = path + to_yield[0] 
                        #print(to_yield)
                        yield to_yield
            
                        


    def get_all_boards1(self, quintris):
        path = []
        #q = deepcopy(quintris)
        quin = deepcopy(quintris)
        c = quin.col
        a_height = self.col_height(quin.get_board(), c, self.get_piece_dim(quintris.get_piece()[0])[0])

        visited = []

        #print("DIFFFFF", a_height, c)
        quin.down()
        if quin.get_board() not in visited:
            visited.append(quin.get_board())
            yield (path + ['d'], quin, a_height)

        quin = deepcopy(quintris)

        i = quintris.col
        while(i > 0):
                
            quin.left()
            path.append('b')
                
            temp_path = deepcopy(path)
            for j in range(4):
                q1 = deepcopy(quin)
                c = q1.col
                q1.down()
                if q1.get_board() not in visited:
                    visited.append(q1.get_board())
                    a_height = self.col_height(q1.get_board(), c, self.get_piece_dim(quintris.get_piece()[0])[0])
                    yield (temp_path + ['d'], q1, a_height)
                q1 = deepcopy(quin)
                q1.hflip()
                c = q1.col
                a_height = self.col_height(q1.get_board(), c, self.get_piece_dim(quintris.get_piece()[0])[0])
                q1.down()
                if q1.get_board() not in visited:
                    visited.append(q1.get_board())
                    yield (temp_path + ['h'] +['d'], q1, a_height)
                q1 = deepcopy(quin)
                q1.vflip()
                c = q1.col
                a_height = self.col_height(q1.get_board(), c, self.get_piece_dim(quintris.get_piece()[0])[0])
                q1.down()
                if q1.get_board() not in visited:
                    visited.append(q1.get_board())
                    yield (temp_path + ['v']+['d'], q1, a_height)

                rot_quintris = quin.rotate()
                temp_path.append('n')
                    
            i -= 1


        i = quintris.col

        quin = deepcopy(quintris)
        path = []
        while(i + self.get_piece_dim(quintris.get_piece()[0])[1] < 15):
                
            quin.right()
            path.append('m')
                
            temp_path = deepcopy(path)
            for j in range(4):
                   
                q1 = deepcopy(quin)
                c = q1.col
                a_height = self.col_height(q1.get_board(), c, self.get_piece_dim(quintris.get_piece()[0])[0])
                q1.down()
                #print(type(q1), temp_path)
                yield (temp_path + ['d'], q1, a_height)
                q1 = deepcopy(quin)
                q1.hflip()
                c = q1.col
                a_height = self.col_height(q1.get_board(), c, self.get_piece_dim(quintris.get_piece()[0])[0])
                q1.down()
                yield (temp_path + ['h'] +['d'], q1, a_height)
                q1 = deepcopy(quin)
                q1.vflip()
                c = q1.col
                a_height = self.col_height(q1.get_board(), c, self.get_piece_dim(quintris.get_piece()[0])[0])
                q1.down()
                yield (temp_path + ['v']+['d'], q1, a_height)

                rot_quintris = quin.rotate()
                temp_path.append('n')
                    
            i += 1
                
                    

    def get_best_quintris(self, quintris):
        all_combos = []
        i = quintris.col
        #i = 0
        temp_q = deepcopy(quintris)
        path = []
        #print("part1 done")
        #print(i)
        while(i - self.get_piece_dim(quintris.get_piece()[0])[1] > -1):
        #while(i > 15):
            #print(i)
            temp_q.left()
            path.append('b')
            all_combos = (self.get_row_results(temp_q, deepcopy(path), all_combos))
            #i-=1
            i-=1
       
        #i = quintris.col
        i = 0
        temp_q = deepcopy(quintris)
        path = []

        while(i + self.get_piece_dim(quintris.get_piece()[0])[1] < 15):
        #while(i < 15):
            temp_q.right()
            path.append('m')
            
            all_combos = (self.get_row_results(temp_q, deepcopy(path), all_combos))

            i+=1
        
        max_eval = -math.inf
        index = 0
        best = []
        for combo in all_combos:
        #combo_eval = a*combo[1] + d*combo[2] + c*combo[3] - b* combo[4] + e*combo[5]
            combo_eval = self.get_evaluation(combo[2], combo[3], combo[4], combo[5], combo[6], combo[7])
            if combo_eval > max_eval:
                best = []
                for k in range(len(combo)):
                    best.append(combo[k])

            
        #print(all_combos)
        return best
                    
                
            
    
    '''
    def get_best_row(self, quintris):
        
        _quintris = deepcopy(quintris)

        right_quintris = deepcopy(_quintris)
        left_quintris = deepcopy(_quintris)
        best_height = 25
        board_width = 15
        best_moves = ''
        counter = 0
        #         for i in range(right_quintris.row + len(max(right_quintris.get_piece()[0], key=len)),board_width):

        for i in range(15):
            right_quintris.right()
            counter += 1
            test_quintris = deepcopy(right_quintris)
            test_quintris.down()
            cur_height = self.get_max_height(test_quintris.get_board())
            if cur_height < best_height:
                best_moves = ['m']*counter
                best_moves.append('d')
        # for i in range(left_quintris.row, len(max(left_quintris.get_piece()[0], key=len)) - 1,-1):
        for i in range(15,- 1,-1):
            left_quintris.left()
            counter += 1
            test_quintris = deepcopy(left_quintris)
            test_quintris.down()
            cur_height = self.get_max_height(test_quintris.get_board())
            if cur_height < best_height:
                best_moves = ['b']*counter
                best_moves.append('d')
        return best_moves


    
    
    def get_best_in_row(self, quintris):
        
        board_width = 15

        _quintris = deepcopy(quintris)
        right_quintris = deepcopy(quintris)

        best_score = 0
        best_height = 25
        best_moves = (0,0)
        for i in range(right_quintris.row + len(max(right_quintris.get_piece()[0], key=len)),board_width):
            t_quintris = deepcopy(right_quintris)
            
            for j in range(t_quintris.row, i):
                t_quintris.right()
            t_quintris.down()

            cur_score = t_quintris.get_score()
            #print("printed board : \n\n\n\n" + str(len(t_quintris.get_board())) + "andndn" + str(len(t_quintris.get_board()[0])) + "asdasd")
            #print('\n'.join(map(''.join, t_quintris.get_board())))
            
            cur_height = self.get_max_height(t_quintris.get_board())
            #print((cur_height) , " and " , (best_height))
            if cur_height < best_height:
                #best_moves = (1,1)
                best_moves = (i - len(max(right_quintris.get_piece())) , 1)

        left_quintris = deepcopy(quintris)

        for i in range(left_quintris.row, len(max(left_quintris.get_piece()[0], key=len)) - 1,-1):
            t_quintris = deepcopy(left_quintris)
            
            for j in range(i, t_quintris.row):
                t_quintris.left()
            t_quintris.down()

            cur_score = t_quintris.get_score()
            cur_height = self.get_max_height(t_quintris.get_board())
            if cur_height < best_height:
                best_height = cur_height
                best_moves = (t_quintris.row - i,0)

        for i in range(best_moves[0]):
            if best_moves[1] == 1:
                quintris.right()
            else:
                quintris.left()

    '''



###################
#### main program

(player_opt, interface_opt) = sys.argv[1:3]

try:
    if player_opt == "human":
        player = HumanPlayer()
    elif player_opt == "computer":
        player = ComputerPlayer()
    else:
        print("unknown player!")

    if interface_opt == "simple":
        quintris = SimpleQuintris() 
    elif interface_opt == "animated":
        quintris = AnimatedQuintris()
    else:
        print("unknown interface!")

    quintris.start_game(player)

except EndOfGame as s:
    print("\n\n\n", s)


