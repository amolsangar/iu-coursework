#!/usr/local/bin/python3
# route.py : Find routes through maps
#
# Code by: Lalith Dupathi(ndupathi), Amol Sangar(asangar), Harshit Shiroiya(hshiroiy)
#
# Based on skeleton code by V. Mathur and D. Crandall, January 2021
#
# !/usr/bin/env python3
import sys
import numpy as np
from math import radians, cos, sin, asin, sqrt
from queue import PriorityQueue
def get_route(start, end, cost):
 
    '''
    The general sense of using files to read data into data structures has been taken from
    https://www.kite.com/python/answers/how-to-convert-a-file-into-a-dictionary-in-python
    '''

    #Loads the gps data into a dictionary where the key in the city name and the values are the latitude and longitude
    def loading_gps_data(filename):
        gps={}
        with open(filename,"r") as f:
            for line in f:
                data= line.split()
                gps[data[0]] = (float(data[1]), float(data[2]))
        return gps
    '''
    end of copied code to read files
    '''
    #Creates a dictionary of dictionary wherein a city has all posible routes we can vist directly by storing 
    #its distance,speed and highway to be taken
    def load_road_segments(filename):
        cities=[]
        with open(filename, 'r') as f:
            for line in f.readlines():
                segments = line.split()
                cities.append(segments[0])
                cities.append(segments[1])
                
        unique_cities=[]
        for x in cities:
            if x not in unique_cities:
                unique_cities.append(x)
                
        unique_cities_dict= {}
        for i in unique_cities:
            unique_cities_dict[i]= {}
        
        
        
        with open(filename, 'r') as f:
            for line in f.readlines():
                segments = line.split()
                city_a = segments[0]
                city_b = segments[1]
                unique_cities_dict[city_a][city_b] = (float(segments[2]), float(segments[3]), segments[4])
                unique_cities_dict[city_b][city_a] = (float(segments[2]), float(segments[3]), segments[4])
        
        return unique_cities_dict

    gps_data=loading_gps_data('city-gps.txt')
    temp=load_road_segments('road-segments.txt')
    '''
    The following excerpt of code to calculate haversian distance has been taken from 
    https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
    '''
    #Calculates the haversine distance between two geo points
    def city_distance(city1, city2):
        
        R = 3956.0
        s_lat,s_lng= gps_data[city1]
        e_lat,e_lng= gps_data[city2]
        s_lat = s_lat*np.pi/180.0                      
        s_lng = np.deg2rad(s_lng)     
        e_lat = np.deg2rad(e_lat)                       
        e_lng = np.deg2rad(e_lng)  
        d = np.sin((e_lat - s_lat)/2)**2 + np.cos(s_lat)*np.cos(e_lat) * np.sin((e_lng - s_lng)/2)**2
        
        return 2 * R * np.arcsin(np.sqrt(d))

    '''
    end of copied code of haversian distance
    '''

    #This is the successor function that gives the possible next cities we can go from a current city
    def next_city(current_city):
        return temp[current_city].keys()

    #This is to check the goal state if current city in the queue is the actual goal
    def is_goal(city1,city2): 
        if city1 == city2:   
            return True
        else:
            return False

    '''
    1) A* high level logic building, understanding and basic implementation was derived from the following links
    #https://www.youtube.com/watch?v=ob4faIum4kQ
    #https://www.teachyourselfpython.com/challenges.php?a=01_Solve_and_Learn&t=7-Sorting_Searching_Algorithms&s=02d_A__Algorithm

    2) Priority Queue implementation was done by refering below link
    #https://careerkarma.com/blog/python-priority-queue/

    3)Started code by Proff Crandall was used from A0 on how to implement fringe methodology
    #https://github.iu.edu/cs-b551-fa2021/ndupathi-a0
    '''


    #This segment is executed when the cost function to be optimised is 'distance'
    if cost=='distance':
        
        #This is the cost function that defines the priority in the A* implementation i.e f(s)=g(s)+h(s)
        #g(s)= the total miles covered from start city to current city from the segments file
        #h(s)= haversine distance that defines the distance from current city to end node as a heuristic
        def distance_priority(end, route_covered,miles_covered):
            if route_covered[-1][0] not in gps_data:
                distance_to_cover=0
            else:
                distance_to_cover = city_distance(route_covered[-1][0], end)
            return miles_covered + distance_to_cover

        #Here the A* search is implemented where we first start of with an empty fringe with all required variables as 0
        #and keep on exploring the succesors from a current city and append to the fringe with their priority to pop out
        #the one with highest priority(lowest value) to finally get the most efficient path to minimize distance from start
        #to end
        visited=[]
        fringe=PriorityQueue() #defining the fringe data structure as a priority queue
        route_covered=[(start,'0')]
        miles_covered=0
        time=0
        delivery=0
        fringe.put((distance_priority(end,route_covered,miles_covered),route_covered, miles_covered,time,delivery)) #Initialise fringe
        while not fringe.empty(): #Keep checking route till fringe empty
            (priority,route_so_far,miles_covered,time,delivery)= fringe.get(0) #popping the highest priority set
            city_now=route_so_far[-1][0] #extracting the current city of the route travelled
            visited.append(city_now)
            if is_goal(city_now,end): #to check goal state
                return {"total-segments" : len(route_so_far)-1, "total-miles" : miles_covered, "total-hours" : time, "total-delivery-hours" : delivery, "route-taken" : route_so_far[1:]}
            else:
                for city in next_city(city_now): #to check all successor cities
                    if city not in visited:
                        #Calcutes new parameters from previous city to current city
                        milestonewcity= temp[city_now][city][0]
                        speedtonewcity= temp[city_now][city][1]
                        highwaytaken=temp[city_now][city][2]
                        timetonewcity=milestonewcity/speedtonewcity
                        #Inputs into fringe the distance,time,route,time and delivery to calculate next best state according to the priority function
                        if speedtonewcity >=50:
                            fringe.put((distance_priority(end,route_so_far + [(city,str(highwaytaken) + ' for ' + str(milestonewcity) + ' miles')],miles_covered+milestonewcity),route_so_far + [(city,highwaytaken + ' for ' + str(milestonewcity) + ' miles')], miles_covered+milestonewcity,time+timetonewcity,2*(delivery+ timetonewcity)*np.tanh((milestonewcity/1000))+timetonewcity +delivery))
                        else:
                            fringe.put((distance_priority(end,route_so_far + [(city,str(highwaytaken) + ' for ' + str(milestonewcity) + ' miles')],miles_covered+milestonewcity),route_so_far + [(city,highwaytaken + ' for ' + str(milestonewcity) + ' miles')], miles_covered+milestonewcity,time+timetonewcity,delivery+ timetonewcity))
                    else:
                        continue
        return "-1"
    
    #This segment is executed when the cost function to be optimised is 'time'
    elif cost=='time':
        def max_speed(file):
            speeds=[]
            with open(file, 'r') as f:
                for line in f.readlines():
                    line1 = line.split()
                    speeds.append(line1[3])
            return max(speeds)
        
        max1=max_speed('road-segments.txt')
        
        #This is the cost function that defines the priority in the A* implementation i.e f(s)=g(s)+h(s)
        #g(s)= the total time taken from start city to current city from the segments file
        #h(s)= haversine distance divided by max speed that defines the time from current city to end node as a heuristic
        def time_priority(end, route_covered,time_taken):
            if route_covered[-1][0] not in gps_data:
                time_to_cover=0
            else:
                distance_to_cover = city_distance(route_covered[-1][0], end)
                time_to_cover= float(distance_to_cover)/float(max1)
            return time_taken + time_to_cover
        
        #Here the A* search is implemented where we first start of with an empty fringe with all required variables as 0
        #and keep on exploring the succesors from a current city and append to the fringe with their priority to pop out
        #the one with highest priority(lowest value) to finally get the most efficient path to minimize time from start
        #to end
        visited=[]
        fringe=PriorityQueue() #defining the fringe data structure as a priority queue
        route_covered=[(start,'0')]
        miles_covered=0
        time=0
        delivery=0
        fringe.put((time_priority(end,route_covered,time),route_covered, miles_covered,time,delivery)) #Initialise fringe
        while not fringe.empty(): #Keep checking route till fringe empty
            (priority,route_so_far,miles_covered,time,delivery)= fringe.get()
            city_now=route_so_far[-1][0]#extracting the current city of the route travelled
            visited.append(city_now)
            if is_goal(city_now,end): #to check goal state
                return {"total-segments" : len(route_so_far)-1, "total-miles" : miles_covered, "total-hours" : time, "total-delivery-hours" : delivery, "route-taken" : route_so_far[1:]}
            else:
                for city in next_city(city_now):#to check all successor cities
                    if city not in visited:
                        #Calcutes new parameters from previous city to current city
                        milestonewcity= temp[city_now][city][0]
                        speedtonewcity= temp[city_now][city][1]
                        highwaytaken=temp[city_now][city][2]
                        timetonewcity=milestonewcity/speedtonewcity
                        #Inputs into fringe the distance,time,route,time and delivery to calculate next best state according to the priority function
                        if speedtonewcity >=50:
                            fringe.put((time_priority(end,route_so_far + [(city,str(highwaytaken) + ' for ' + str(milestonewcity) + ' miles')],time+timetonewcity),route_so_far + [(city,str(highwaytaken) + ' for ' + str(milestonewcity) + ' miles')], miles_covered+milestonewcity,time+timetonewcity,2*(delivery+ timetonewcity)*np.tanh((milestonewcity/1000))+timetonewcity +delivery))
                        else:
                            fringe.put((time_priority(end,route_so_far + [(city,str(highwaytaken) + ' for ' + str(milestonewcity) + ' miles')],time+timetonewcity),route_so_far + [(city,str(highwaytaken) + ' for ' + str(milestonewcity) + ' miles')], miles_covered+milestonewcity,time+timetonewcity,delivery+ timetonewcity))
                    else:
                        continue
        return "-1"

    #This segment is executed when the cost function to be optimised is 'delivery'
    elif cost=='delivery':

        #This is the cost function that defines the priority in the A* implementation i.e f(s)=g(s)+h(s)
        #g(s)= the total time taken from start city to current city from the segments file
        #h(s)= haversine distance divided by max speed that defines the time from current city to end node as a heuristic
        def delivery_priority(end, route_covered,time_taken):
            if route_covered[-1][0] not in gps_data:
                time_to_cover=0
            else:
                distance_to_cover = city_distance(route_covered[-1][0], end)
                time_to_cover= float(distance_to_cover)/float(max1)
            return time_taken + time_to_cover 

        def max_speed(file):
            speeds=[]
            with open(file, 'r') as f:
                for line in f.readlines():
                    line1 = line.split()
                    speeds.append(line1[2])
            return max(speeds)
        max1=max_speed('road-segments.txt')


        #Here the A* search is implemented where we first start of with an empty fringe with all required variables as 0
        #and keep on exploring the succesors from a current city and append to the fringe with their priority to pop out
        #the one with highest priority(lowest value) to finally get the most efficient path to minimize delivery time from start
        #to end
        visited=[]
        fringe=PriorityQueue() #defining the fringe data structure as a priority queue
        route_covered=[(start,'0')]
        miles_covered=0
        time=0
        delivery=0
        fringe.put((delivery_priority(end,route_covered,delivery),route_covered, miles_covered,time,delivery))
        while not fringe.empty(): #Keep checking route till fringe empty
            (priority,route_so_far,miles_covered,time,delivery)= fringe.get()
            city_now=route_so_far[-1][0]#extracting the current city of the route travelled
            visited.append(city_now)
            if is_goal(city_now,end):#to check goal state
                return {"total-segments" : len(route_so_far)-1, "total-miles" : miles_covered, "total-hours" : time, "total-delivery-hours" : delivery, "route-taken" : route_so_far[1:]}
            else:
                for city in next_city(city_now): #to check all successor cities
                    if city not in visited:
                        #Calcutes new parameters from previous city to current city
                        milestonewcity= temp[city_now][city][0]
                        speedtonewcity= temp[city_now][city][1]
                        highwaytaken= temp[city_now][city][2]
                        timetonewcity=milestonewcity/speedtonewcity
                        #Inputs into fringe the distance,time,route,time and delivery to calculate next best state according to the priority function
                        if speedtonewcity >=50:
                            fringe.put((delivery_priority(end,route_so_far + [(city,str(highwaytaken) + ' for ' + str(milestonewcity) + ' miles')],2*(delivery+ timetonewcity)*np.tanh((milestonewcity/1000))+timetonewcity +delivery),route_so_far + [(city,str(highwaytaken) + ' for ' + str(milestonewcity) + ' miles')], miles_covered+milestonewcity,time+timetonewcity,2*(delivery+ timetonewcity)*np.tanh((milestonewcity/1000))+timetonewcity +delivery))
                        else:
                            fringe.put((delivery_priority(end,route_so_far + [(city,str(highwaytaken) + ' for ' + str(milestonewcity) + ' miles')],time+timetonewcity),route_so_far + [(city,str(highwaytaken) + ' for ' + str(milestonewcity) + ' miles')], miles_covered+milestonewcity,time+timetonewcity,delivery+ timetonewcity))
                    else:
                        continue
        return "-1"

    #This segment is executed when the cost function to be optimised is 'segments'
    elif cost=='segments':

        #This is the cost function that defines the priority in the A* implementation i.e f(s)=g(s)+h(s)
        #g(s)= the segments from start city to current city
        #h(s)= haversine distance divided by max length of total segments that defines the approx segments from current city to end node as a heuristic
        def segments_priority(end, route_covered,segments):
            if route_covered[-1][0] not in gps_data:
                distance_to_cover=0
            else:
                distance_to_cover = city_distance(route_covered[-1][0], end)
            return segments + float(distance_to_cover)/float(max_segments)
        
        def max_segment(file):
            s=[]
            with open(file, 'r') as f:
                for line in f.readlines():
                    line1 = line.split()
                    s.append(line1[2])
            return len(s)
        max_segments=max_segment('road-segments.txt')


        #Here the A* search is implemented where we first start of with an empty fringe with all required variables as 0
        #and keep on exploring the succesors from a current city and append to the fringe with their priority to pop out
        #the one with highest priority(lowest value) to finally get the most efficient path to minimize segments from start
        #to end
        visited=[]
        fringe=PriorityQueue() #defining the fringe data structure as a priority queue
        route_covered=[(start,'0')]
        miles_covered=0
        time=0
        delivery=0
        segments=0
        fringe.put((segments_priority(end,route_covered,segments),segments,route_covered, miles_covered,time,delivery))
        while not fringe.empty(): #Keep checking route till fringe empty
            (priority,segments,route_so_far,miles_covered,time,delivery)= fringe.get()
            city_now=route_so_far[-1][0] #extracting the current city of the route travelled
            visited.append(city_now)
            if is_goal(city_now,end): #to check goal state
                return {"total-segments" : segments, "total-miles" : miles_covered, "total-hours" : time, "total-delivery-hours" : delivery, "route-taken" : route_so_far[1:]}
            else:
                for city in next_city(city_now): #to check all successor cities
                    if city not in visited:
                        #Calcutes new parameters from previous city to current city
                        milestonewcity= temp[city_now][city][0]
                        speedtonewcity= temp[city_now][city][1]
                        highwaytaken= temp[city_now][city][2]
                        timetonewcity=milestonewcity/speedtonewcity
                        #Inputs into fringe the distance,time,route,time and delivery to calculate next best state according to the priority function
                        if speedtonewcity >=50:
                            fringe.put((segments_priority(end,route_so_far + [(city,str(highwaytaken) + ' for ' + str(milestonewcity) + ' miles')],segments+1),segments+1,route_so_far + [(city,str(highwaytaken) + ' for ' + str(milestonewcity) + ' miles')], miles_covered+milestonewcity,time+timetonewcity,2*(delivery+ timetonewcity)*np.tanh((milestonewcity/1000))+timetonewcity +delivery))
                        else:
                            fringe.put((segments_priority(end,route_so_far + [(city,str(highwaytaken) + ' for ' + str(milestonewcity) + ' miles')],segments+1),segments+1,route_so_far + [(city,str(highwaytaken) + ' for ' + str(milestonewcity) + ' miles')], miles_covered+milestonewcity,time+timetonewcity,delivery+ timetonewcity))
                    else:
                        continue
        return "-1"
    
    

# Please don't modify anything below this line
#
if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise(Exception("Error: expected 3 arguments"))

    (_, start_city, end_city, cost_function) = sys.argv
    if cost_function not in ("segments", "distance", "time", "delivery"):
        raise(Exception("Error: invalid cost function"))

    result = get_route(start_city, end_city, cost_function)

    # Pretty print the route
    print("Start in %s" % start_city)
    for step in result["route-taken"]:
        print("   Then go to %s via %s" % step)

    print("\n          Total segments: %4d" % result["total-segments"])
    print("             Total miles: %8.3f" % result["total-miles"])
    print("             Total hours: %8.3f" % result["total-hours"])
    print("Total hours for delivery: %8.3f" % result["total-delivery-hours"])
