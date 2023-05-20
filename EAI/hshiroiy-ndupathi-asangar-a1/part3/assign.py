#!/usr/bin/env python
# coding: utf-8

# assign.py : finds the cost of assigning of team members as per preferences of students
#
# Code by: Harshit Shiroiya(hshiroiy), Lalith Dupathi(ndupathi), Amol Sangar(asangar)
#
# Based on skeleton code by B. Aravind  and D. Crandall, January 2021
#
# !/usr/bin/env python3



import sys
import copy




def student_choice(file_name):
    
    file = open(file_name, "r")
    Studentlist = []
    group_choice = {}
    for line in file:
        count = 1
        for word in line.split():
            if(count == 1):
                temp = word
                Studentlist.append(word)
            elif(count == 2):
                selected_partners = word.split('-')
                preferred_partners=[]
                total_partners = 0
                for x in selected_partners:
                    total_partners += 1
                    if x == ("xxx"):
                        continue
                    elif x == ("zzz"):
                        continue
                    else:
                        preferred_partners.append(x)
            else:
                not_preferred_partners = word.split(',')
            count += 1
        group_choice[temp] = {}

        group_choice[temp]['total_partners'] = total_partners
        group_choice[temp]['preferred_partners'] = preferred_partners
        group_choice[temp]['not_preferred_partners'] = not_preferred_partners
    file.close()
    return (Studentlist,group_choice)


# In[3]:


def calculate_cost(a,group_pref):
    
    grade_group_time = 5 
    wrong_group_size_time = 2  # taking 1 min of instructor's time as was assigned to a different group size
    wrong_group_time = 3 # not assigned to someone requested
    not_requested_time = 10 # student assigned to someone they requested not to work with
    
# Case 1:  Per team Assesment (5m)
    length = len(a)
    grade_group_cost = grade_group_time * length
    
    
    incorrect_group = 0
    person_requested = 0
    person_not_requested = 0
    total_cost = 0

    for group in a:
        for members in group:
            
            number_of_partners = group_pref[members]['total_partners']
            number_of_partners = int(number_of_partners)
            if((number_of_partners != len(group)) and (number_of_partners != 0) ):
                incorrect_group += 1
            for person in group_pref[members]['not_preferred_partners']:
                if person in group:
                    person_not_requested += 1
                        
            for person in group_pref[members]['preferred_partners']:
                if (person == '_'):
                    break
                if person not in group:
                    person_requested += 1
            
             
           
    
            
    total_cost = grade_group_cost + incorrect_group * wrong_group_size_time + person_requested * wrong_group_time  + person_not_requested * not_requested_time

    return total_cost


# In[4]:


def create_group(a,Studentlist):    
    listOfGroups = [y.copy() for y in a]
    for members in Studentlist:
        existing_student = False
        for groups in listOfGroups:
            if members in groups:
                existing_student = True
                break # not considering the student if already in a group
        if existing_student:
            continue
        else:
            listOfGroups.append([members])
            break
    return listOfGroups



def is_goal(a,Studentlist):
    x = 0
    for i in range(len(a)):
        x += len(a[i])
    return len(Studentlist) == x





def possible_team_members(groupList,Studentlist):
    
    possible_team = groupList[len(groupList)-1]
    final_groups = []
    for group in groupList:
        for student in group:
            final_groups.append(student)

    two_members= []
    for student in Studentlist:
        if student not in final_groups:
            team = [possible_team[0], student]
            if(sorted(team) not in two_members):
                two_members.append(sorted(team))

    three_members = []
    for groups in two_members:
        for student in Studentlist:
            if student not in final_groups and student not in groups:
                team = [groups[0],groups[1], student]
                if(sorted(team) not in three_members):
                    three_members.append(sorted(team))

    for groups in two_members:
        groupList.append(groups)

    for groups in three_members:
        groupList.append(groups)

    return groupList


# In[7]:


def successors(a,Studentlist):
    succ_list = []
    grouplist = create_group(a,Studentlist)
    possible_groups = possible_team_members(grouplist,Studentlist)
    for finalgroup in possible_groups:
        tempGroup = [i.copy() for i in a]
        if finalgroup not in a:
            tempGroup.append(finalgroup)
            succ_list.append(tempGroup)
    return succ_list





def solver(input_file):
    """
    1. This function should take the name of a .txt input file in the format indicated in the assignment.
    2. It should return a dictionary with the following keys:
        - "assigned-groups" : a list of groups assigned by the program, each consisting of usernames separated by hyphens
        - "total-cost" : total cost (time spent by instructors in minutes) in the group assignment
    3. Do not add any extra parameters to the solver() function, or it will break our grading and testing code.
    4. Please do not use any global variables, as it may cause the testing code to fail.
    5. To handle the fact that some problems may take longer than others, and you don't know ahead of time how
       much time it will take to find the best solution, you can compute a series of solutions and then
       call "yield" to return that preliminary solution. Your program can continue yielding multiple times;
       our test program will take the last answer you 'yielded' once time expired.
    """
    
    (Studentlist,group_pref) = student_choice(input_file)

    
    result_dictionary = {'assigned-groups':[], 'total-cost':0}
    
    initial_group = []
    

    fringe = [initial_group]
    probable_goal = []
    probable_goal_time = sys.maxsize 
    while len(fringe) > 0:
        for a in successors(fringe.pop(),Studentlist):
            if is_goal(a,Studentlist):
                a_time = calculate_cost(a,group_pref)
                if((probable_goal_time > a_time)):
                    result = copy.deepcopy(result_dictionary)
                    probable_goal = a
                    probable_goal_time = a_time
                    for group in probable_goal:
                        str_grp = '-'.join(group)
                        result["assigned-groups"].append(str_grp)
                    result["total-cost"]=probable_goal_time
                    yield(result)
            fringe.append(a)




if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected an input filename"))

    for result in solver(sys.argv[1]):
        print("----- Latest solution:\n" + "\n".join(result["assigned-groups"]))
        print("\nAssignment cost: %d \n" % result["total-cost"])





