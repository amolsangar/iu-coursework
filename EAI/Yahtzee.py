import copy
import pprint

def expected_value(sum,prob):
    return sum*prob

def avg_expected_value(D, pos, prob):
    exp_sum = []
    for i in range(1,7):
        roll_sum = 0
        D[pos] = i
        if(D[0] == D[1] == D[2]):
            roll_sum += 25
        else:
            roll_sum += sum(D)
        
        #print("->",D,roll_sum)
        exp_sum.append(expected_value(roll_sum, prob))
    return round(sum(exp_sum),2)

def avg_expected_value_two_roll(D, pos1, pos2 , prob):
    exp_sum = []
    for i in range(1,7):
        D[pos1] = i
        exp_sum.append(avg_expected_value(D, pos2, prob))
    return round(sum(exp_sum),2)

def avg_expected_value_three_roll(D, pos1, pos2, pos3, prob):
    exp_sum = []
    for i in range(1,7):
        D[pos1] = i
        exp_sum.append(avg_expected_value_two_roll(D, pos2, pos3, prob))
    return round(sum(exp_sum),2)

def yahtzee_lite(dice):
    D = [int(c) for c in dice]
    print("Die #0:", D[0])
    print("Die #1:", D[1])
    print("Die #2:", D[2])
    score = {}

    # No roll
    if(D[0] == D[1] == D[2]):
        score["no_roll"] = 25
    else:
        score["no_roll"] = sum(D)

    # One roll
    for i in range(0,3):
        temp = avg_expected_value(copy.deepcopy(D),i,1/6)
        score["roll_"+str(i)] = temp

    # Two roll
    score["roll_0_1"] = avg_expected_value_two_roll(copy.deepcopy(D),0,1,1/36)
    score["roll_1_2"] = avg_expected_value_two_roll(copy.deepcopy(D),1,2,1/36)
    score["roll_0_2"] = avg_expected_value_two_roll(copy.deepcopy(D),0,2,1/36)

    # Three roll
    score["roll_0_1_2"] = avg_expected_value_three_roll(copy.deepcopy(D),0,1,2,1/216)

    print("\nScore:")
    pprint.pprint(score)

    max = 0
    roll = ""
    for k in score.keys():
        if(score[k] > max):
            max = score[k]
            roll = k
        
    print("\nMax Score:", max)
    print("Roll:",roll)
    result = roll.split("_")
    if(roll != "no_roll"):
        s = ""
        for r in result[1:]:
            s += r+" "
        print( f"\nPlease reroll dice number :", s)
    else:
        print("No reroll needed!")

dice_roll = input("Enter dice roll values: ")
yahtzee_lite(dice_roll)


# OUTPUT
"""
C:\Users\AMOL\IUB - Code\EAI
λ python Yahtzee.py
Enter dice roll values: 123
Die #0: 1
Die #1: 2
Die #2: 3

Score:
{'no_roll': 6,
 'roll_0': 8.5,
 'roll_0_1': 10.45,
 'roll_0_1_2': 10.91,
 'roll_0_2': 9.53,
 'roll_1': 7.5,
 'roll_1_2': 8.61,
 'roll_2': 6.5}

Max Score: 10.91
Roll: roll_0_1_2

Please reroll dice number : 0 1 2

==================================
C:\Users\AMOL\IUB - Code\EAI
λ python Yahtzee.py
Enter dice roll values: 356
Die #0: 3
Die #1: 5
Die #2: 6

Score:
{'no_roll': 14,
 'roll_0': 14.5,
 'roll_0_1': 13.2,
 'roll_0_1_2': 10.91,
 'roll_0_2': 12.28,
 'roll_1': 12.5,
 'roll_1_2': 10.45,
 'roll_2': 11.5}

Max Score: 14.5
Roll: roll_0

Please reroll dice number : 0
"""