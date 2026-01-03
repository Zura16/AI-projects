'''
CECS 451: Artifical Intelligence
Assignment 1: A* Algorithm
Name: Aalind Kale
Student ID: 030892041
Due Date: 09/17/2025
'''



import sys
import math
import heapq


# I'm gonna make a path class to deal with finding the best route using thr A* here
class Path:
    def __init__(self):
        self.coordinates = {}
        self.map = {}

# Opening both the coordinates.txt and map.txt file from the main folder and adding that info to this class.
    def add_info(self):
        with open('coordinates.txt', 'r') as file:
            for i in file:
                if ':' in i:
                    a, b = i.strip().split(':')
                    latitudes, longitutes = map(float, b.strip('()').split(','))
                    self.coordinates[a] = (latitudes, longitutes)
        with open('map.txt', 'r') as file:
            for i in file:
                if '-' in i:
                    a, c = i.strip().split('-')
                    self.map[a] = []
                    for j in c.split(','):
                        neigh = j.split('(')[0]
                        dist = float(j.split('(')[1].strip(')'))
                        self.map[a].append((neigh, dist))

# Using A* and in this case, the priority quese beacause I think it will work better considering the situation
    def A_Star(self, start, end):
        queue = [(0, 0, start, [start])]
        m = set()

        while queue:
            f, g, curr, path = heapq.heappop(queue)

            if curr in m:
                continue
            if curr == end:
                return path, g
            m.add(curr)

            if curr in self.map:
                for neigh, dist in self.map[curr]:
                    if neigh not in  m:
                        g2 = g + float(dist)
                        heuristic_val = self.heuristic_func(neigh, end)
                        f2 = g2 + heuristic_val
                        path2 = path + [neigh]
                        heapq.heappush(queue, (f2, g2, neigh, path2))

        return None,float('inf')


# As per the given function in the canvas, this should more or less work. It was a bit complicated to get it started.
    def heuristic_func(self, starting_city, ending_city):
        lati1, longi1 = self.coordinates[starting_city]
        lati2, longi2 = self.coordinates[ending_city]

        lati1, longi1, lati2, longi2 = map(math.radians, [lati1, longi1, lati2, longi2])

        distance_lati = lati2 - lati1
        distance_longi =longi2 - longi1

        l = math.sin(distance_lati / 2) ** 2 + math.cos(lati1) * math.cos(lati2) * math.sin(distance_longi / 2) **2
        return 3958.8 * 2 *  math.asin(math.sqrt(l))
    
# Just printing the output that's needed
    def show_path(self, start, end):
        path, dist = self.A_Star(start, end)

        print(f"From city: {start}\nTo city: {end}")
        if path:
            print(f"Best Route: {' - '.join(path)}\nTotal distance: {dist:.2f} mi")
        else:
            print("No route found")


# Just the main function to end up and get things running
def main():
    if len(sys.argv) != 3:
        print("Usage: python a-star.py <start_city> <end_city>")
        sys.exit(1)

    start_city = sys.argv[1]
    end_city = sys.argv[2]

    path_finder = Path()
    path_finder.add_info()
    path_finder.show_path(start_city, end_city)

if __name__ == "__main__" :
    main()


